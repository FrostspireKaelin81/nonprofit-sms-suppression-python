from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class SmsRequest:
    phone: str
    message: str
    purpose: str
    reference: str


@dataclass
class SuppressionBook:
    numbers: set[str] = field(default_factory=set)

    def opt_out(self, phone: str) -> None:
        self.numbers.add(phone)

    def allowed(self, phone: str) -> bool:
        return phone not in self.numbers


def deliver(request: SmsRequest, suppressions: SuppressionBook, sender: Callable[..., dict]) -> dict:
    if not suppressions.allowed(request.phone):
        return {"sent": False, "reason": "opted_out", "phone": request.phone}
    result = sender(
        {"to": request.phone, "body": request.message},
        idempotency_key=f"nonprofit-{request.purpose}-{request.reference}",
    )
    return {"sent": True, "phone": request.phone, "message_id": result.get("message_id")}


def receipt(phone: str, donor: str, receipt_id: str, amount: str) -> SmsRequest:
    return SmsRequest(phone, f"Thank you {donor}; receipt {receipt_id} recorded for {amount}.", "receipt", receipt_id)


def volunteer_reminder(phone: str, shift_id: str, when: str) -> SmsRequest:
    return SmsRequest(phone, f"Reminder: volunteer shift {shift_id} starts {when}.", "volunteer", shift_id)


def campaign_report(phone: str, campaign: str, total: int) -> SmsRequest:
    return SmsRequest(phone, f"{campaign} update: {total} community members reached.", "campaign", campaign)
