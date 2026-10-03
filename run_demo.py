import os

from src.infrai_client import send_sms
from src.nonprofit_sms import SuppressionBook, campaign_report, deliver, receipt, volunteer_reminder


def main() -> None:
    phone = os.environ.get("DEMO_SMS_TO")
    if not phone:
        raise SystemExit("Set DEMO_SMS_TO to run the live example")
    book = SuppressionBook()
    print(deliver(receipt(phone, "Amina", "R-104", "$40"), book, send_sms))
    book.opt_out(phone)
    print(deliver(volunteer_reminder(phone, "V-7", "Saturday 09:00"), book, send_sms))
    print(deliver(campaign_report(phone, "Spring drive", 128), book, send_sms))


if __name__ == "__main__":
    main()
