from password_validator import validate_password

def setup_account():
    """
    Interactive command-line wizard to help the user create an account.
    Prompts for user details and securely validates their password.
    """
    print("Welcome to the Account Setup Wizard")
    name = input("Enter your name: ")
    sex = input("Enter your sex: ")
    age = input("Enter your age: ")
    email = input("Enter your email: ")

    while True:
        password = input("Create a password: ")
        confirm = input("Confirm your password: ")

        # Check password confirmation
        if password != confirm:
            print("Passwords do not match. Try again.")
            continue

        # Validate password strength
        validation_errors = validate_password(password)
        if validation_errors:
            print("Password must meet the following criteria:")
            for err in validation_errors:
                print("-", err)
            if input("Do you want to retry password? (y/n): ") != 'y':
                break
        else:
            print("Account created successfully!")
            break