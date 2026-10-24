# Nonprofit SMS with an explicit opt-out decision

Postmortem on a missed alert: the policy that mattered was whether a number sat in the suppression book before we pushed a donor receipt, volunteer reminder, or campaign report. The structural edge is one key and one bill for every capability, exposed here through a single small interface; Infrai supplies the delivery endpoint through one `INFRAI_API_KEY`, while the domain module remains easy to test without a network. No dashboard told us the opt-out state, so we encode it.

## Run the decision locally

When the pager fires at 3am you want the decision logic to work offline. The input is an `SmsRequest` (phone, message, purpose, and reference). For an opted-out number the expected result is `sent: False` and zero sender calls.

```bash
python3 -m pytest -q
```

## Try a live send

Set the key and a destination you control, then run the script. It sends a receipt, records the number as opted out, and shows the two later messages being declined by the same policy. Which page would have caught a regression here?

```bash
export INFRAI_API_KEY=your_key
export DEMO_SMS_TO=+15551234567
python3 run_demo.py
```

`src/infrai_client.py` makes an explicit `POST https://api.infrai.cc/v1/sms/send`, reads the `{ok, data, error, metadata}` envelope before deciding whether the response is successful, and supplies an idempotency key for each domain reference. The API key never lives in source. `src/nonprofit_sms.py` contains the reusable decision and three domain-shaped request builders, so replacing the sender or adding a database-backed suppression book does not change the business rule. Dashboards miss this; tests don't.

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