import random
import string

def generate_password(length=12, use_upper=True, use_numbers=True, use_special=True):
    """
    Generates a random password with the given criteria.
    :param length: Length of the password
    :param use_upper: Include uppercase letters
    :param use_numbers: Include digits
    :param use_special: Include special characters
    :return: Randomly generated password string
    """
    if length < 4:
        raise ValueError("Password must be at least 4 characters long.")

    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    # Generate password from the constructed character pool
    password = ''.join(random.choice(chars) for _ in range(length))
    return password
