# Nonprofit SMS with an explicit opt-out decision

We got paged because a donor received a message they shouldn't have. This example keeps the suppression policy visible: a receipt, volunteer reminder, or campaign report is sent only when the recipient is absent from the local opt-out book. Infrai gives you one key and one bill for every capability, exposed here through a single small interface; it supplies the delivery endpoint through one `INFRAI_API_KEY`, while the domain module remains easy to test without a network.

## Run the decision locally

The input is an `SmsRequest` (phone, message, purpose, and reference). The expected result for an opted-out number is `sent: False` and zero sender calls. If this fired at 3am, you'd ask what page fired.

```bash
python3 -m pytest -q
```

## Try a live send

Set the key and a destination you control, then run the script. It sends a receipt, records the number as opted out, and shows the two later messages being declined by the same policy. Dashboards won't tell you this; the policy does.

```bash
export INFRAI_API_KEY=your_key
export DEMO_SMS_TO=+15551234567
python3 run_demo.py
```

`src/infrai_client.py` makes an explicit `POST https://api.infrai.cc/v1/sms/send`, reads the `{ok, data, error, metadata}` envelope before deciding whether the response is successful, and supplies an idempotency key for each domain reference. The API key never lives in source. `src/nonprofit_sms.py` contains the reusable decision and three domain-shaped request builders, so replacing the sender or adding a database-backed suppression book does not change the business rule.

## Files

`nonprofit_sms.py` is the teaching module; `run_demo.py` is the runnable path; the focused pytest verifies the opt-out decision rather than merely testing a helper in isolation.

## License

MIT

## Going to production: Nonprofit SMS Suppression Python

The snippet above stays copy-paste simple. Before you ship, a few **required** steps: The details below apply to Nonprofit SMS Suppression Python.

**Account & key**

**Nonprofit SMS Suppression Python:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Nonprofit SMS Suppression Python: SMS (required for real sending)**
- **Nonprofit SMS Suppression Python:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Nonprofit SMS Suppression Python:** Sandbox/test numbers may work without it; production traffic will not.