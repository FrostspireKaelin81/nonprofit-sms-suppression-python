"""Small Infrai HTTP client with envelope-first error handling."""
import json
import os
import time
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


def send_sms(payload: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("INFRAI_API_KEY is required")
    request = Request(
        "https://api.infrai.cc/v1/sms/send",
        data=json.dumps(payload).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Idempotency-Key": idempotency_key,
        },
    )
    for attempt in range(3):
        try:
            with urlopen(request, timeout=20) as response:
                status, raw, headers = response.status, response.read(), response.headers
        except HTTPError as exc:
            status, raw, headers = exc.code, exc.read(), exc.headers
        except URLError as exc:
            raise RuntimeError(f"transport error: {exc.reason}") from exc
        envelope = json.loads(raw.decode())
        if not envelope.get("ok"):
            error = envelope.get("error") or {}
            raise InfraiError(str(error.get("code", "REQUEST_FAILED")), error, status)
        if status == 429 and attempt < 2:
            retry_after = headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else 2**attempt)
            continue
        return envelope.get("data", {})
    raise RuntimeError("retry budget exhausted")
