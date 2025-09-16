from user_account_setup import setup_account
from password_generator import generate_password
from morse_code_translator import english_to_morse

if __name__ == '__main__':
    print("1. Setup account")
    print("2. Generate password")
    print("3. Convert to Morse Code")
    choice = input("Choose an option: ")

    if choice == '1':
        # Start the account setup wizard
        setup_account()
    elif choice == '2':
        # Prompt user for password generation preferences
        length = int(input("Length: "))
        upper = input("Include uppercase? (y/n): ") == 'y'
        number = input("Include numbers? (y/n): ") == 'y'
        special = input("Include special characters? (y/n): ") == 'y'
        print("Generated Password:", generate_password(length, upper, number, special))
    elif choice == '3':
        # Translate a message to Morse code
        text = input("Enter text to convert: ")
        print("Morse Code:", english_to_morse(text))
    else:
        print("Invalid option")
