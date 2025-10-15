"""
Test đúng chuẩn pytest cho các service/helpers.

- Sử dụng import theo module thực tế: `app.*`
- Không dùng print, chỉ dùng assert.
"""

from app.services.user_service import UserService
from app.utils.helpers import validate_email, validate_password_strength


def test_email_validation():
    valid_emails = [
        "test@example.com",
        "user.name@domain.co.uk",
        "test123@test-domain.com",
    ]

    invalid_emails = [
        "invalid-email",
        "@domain.com",
        "test@",
        "test.com",
        "",
    ]

    for email in valid_emails:
        assert validate_email(email), f"Valid email failed: {email}"

    for email in invalid_emails:
        assert not validate_email(email), f"Invalid email passed: {email}"


def test_password_validation():
    weak_passwords = ["123", "abc", "12345"]
    strong_passwords = ["abc123", "test1234", "mypassword1"]

    for pwd in weak_passwords:
        errors = validate_password_strength(pwd)
        assert len(errors) > 0, f"Weak password should have errors: {pwd}"

    for pwd in strong_passwords:
        errors = validate_password_strength(pwd)
        assert errors == [], f"Strong password should have no errors: {pwd} -> {errors}"


def test_user_validation():
    # Valid data should return empty errors
    valid_errors = UserService.validate_user_data(
        "test@example.com", "testuser", "password123"
    )
    assert valid_errors == []

    # Invalid data should return at least one error
    invalid_errors = UserService.validate_user_data("invalid", "a", "123")
    assert len(invalid_errors) > 0
