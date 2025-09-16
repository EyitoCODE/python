import re

def validate_password(password: str):
    """
    Validates a password against complexity rules:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    :param password: Password string to validate
    :return: List of validation error messages, or None if valid
    """
    errors = []
    if not re.search(r'[A-Z]', password):
        errors.append("Missing uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Missing lowercase letter")
    if not re.search(r'[0-9]', password):
        errors.append("Missing number")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        errors.append("Missing special character")
    return errors if errors else None
