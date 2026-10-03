from src.nonprofit_sms import SuppressionBook, deliver, receipt


def test_opted_out_donor_receipt_is_not_sent():
    book = SuppressionBook()
    book.opt_out("+15550001")
    calls = []
    result = deliver(receipt("+15550001", "Amina", "R-1", "$20"), book, calls.append)
    assert result == {"sent": False, "reason": "opted_out", "phone": "+15550001"}
    assert calls == []
