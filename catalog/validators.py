import re


def normalize_isbn(value):
    """Return a normalized ISBN-13 or raise ValueError with a user-safe message."""
    isbn = re.sub(r"[\s-]", "", value or "")
    if not re.fullmatch(r"\d{13}", isbn):
        raise ValueError("ISBN-13 숫자 13자리를 입력해 주세요.")
    if not isbn.startswith(("978", "979")):
        raise ValueError("책 ISBN 바코드가 아닙니다. ISBN-13 바코드를 스캔해 주세요.")
    if isbn.startswith("9790"):
        raise ValueError("9790으로 시작하는 악보용 번호는 ISBN이 아닙니다.")
    total = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(isbn))
    if total % 10:
        raise ValueError("ISBN 검사 숫자가 맞지 않습니다. 다시 스캔하거나 직접 확인해 주세요.")
    return isbn
