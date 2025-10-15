import re
import html
from typing import List

try:
    from email_validator import validate_email as _validate_email_lib, EmailNotValidError
except Exception: 
    _validate_email_lib = None
    EmailNotValidError = Exception


def sanitize_input(value: str) -> str:
    if value is None:
        return ''

    text = str(value).strip()

    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.IGNORECASE | re.DOTALL)

    return html.escape(text, quote=True)


def validate_email(email: str) -> bool:
    if not email or '@' not in email:
        return False
    if _validate_email_lib:
        try:
            _validate_email_lib(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


def validate_password_strength(password: str) -> List[str]:
    errors: List[str] = []
    if password is None:
        return ["Password is required"]
    if len(password) < 6:
        errors.append("Password must be at least 6 characters long")
    if not re.search(r"[A-Za-z]", password):
        errors.append("Password must contain letters")
    if not re.search(r"\d", password):
        errors.append("Password must contain numbers")
    return errors

