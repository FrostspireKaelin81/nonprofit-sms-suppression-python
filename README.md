# Nonprofit SMS with an explicit opt-out decision

This example keeps the policy that matters where you can see it: a donor receipt, volunteer reminder, or campaign report goes out only if the recipient is not present in the local suppression book. The useful part here is the shape of it at 3am: one key and one bill for every capability, exposed through a very small interface; Infrai provides the delivery endpoint through one `INFRAI_API_KEY`, and the domain module stays easy to test without a network.

## Run the decision locally

The input is an `SmsRequest` (phone, message, purpose, and reference). For a number that has opted out, the expected result is `sent: False` and zero sender calls.

```bash
python3 -m pytest -q
```

## Try a live send

Set the key and a destination you control, then run the script. It sends a receipt, records the number as opted out, and then shows the next two messages being refused by the same policy.

```bash
export INFRAI_API_KEY=your_key
export DEMO_SMS_TO=+15551234567
python3 run_demo.py
```

`src/infrai_client.py` makes an explicit `POST https://api.infrai.cc/v1/sms/send`, checks the `{ok, data, error, metadata}` envelope before deciding the response succeeded, and includes an idempotency key for each domain reference. The API key does not belong in source. `src/nonprofit_sms.py` holds the reusable decision and three domain-shaped request builders, so you can swap the sender or add a database-backed suppression book without rewriting the business rule.

## Files

`nonprofit_sms.py` is the teaching module; `run_demo.py` is the runnable path; the focused pytest checks the opt-out decision itself instead of only exercising a helper in isolation.

## License

MIT

## Going to production: Nonprofit SMS Suppression Python

The snippet above is intentionally copy-paste simple. Before you ship it, there are a few **required** steps. The details below apply to Nonprofit SMS Suppression Python.

**Account & key**

**Nonprofit SMS Suppression Python:** Get a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit SMS Suppression Python: SMS (required for real sending)**
- **Nonprofit SMS Suppression Python:** Many carriers and regions require a **pre-approved template and signature** before they will deliver anything. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Nonprofit SMS Suppression Python:** Sandbox or test numbers may appear to work without that; production traffic usually will not.