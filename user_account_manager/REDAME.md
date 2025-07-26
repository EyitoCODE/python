User Account Manager & Password Generator
This application provides a secure way to manage user accounts and generate strong, random passwords. It features a graphical user interface (GUI) built with Tkinter, robust password hashing with bcrypt, and secure data encryption with cryptography's Fernet symmetric encryption.

Features
Secure Master Passphrase: All user account data is encrypted and decrypted using a master passphrase. This passphrase is stretched using PBKDF2HMAC to resist brute-force attacks.

Account Creation: Create new user accounts with associated profile information.

Secure Password Storage: User passwords are not stored directly but are hashed using bcrypt, a strong, adaptive hashing algorithm, making them resistant to cracking.

User Login: Authenticate users against their stored password hashes.

View All Accounts: Decrypt and view a list of all registered usernames.

Individual Profile Viewing: See detailed profile information for any selected account.

Master Passphrase Management: Set a master passphrase for the first time or change an existing one, with all data securely re-encrypted.

Secure Password Generator: Generate strong, customizable random passwords that meet common security requirements (length, uppercase, lowercase, numbers, special characters).

Clipboard Integration: Easily copy generated passwords to your clipboard.

How to Use

1. Run the Application:

Navigate to the directory containing user_account_manager.py in your terminal and run:

Bash
python user_account_manager.py

2. First-Time Setup (Setting Your Master Passphrase):

On the very first run, the application will inform you that no master passphrase is set.
Click the "Set/Change Master Passphrase" button on the main menu.
Follow the prompts to enter and confirm your new master passphrase. Remember this passphrase! It is the ONLY key to your encrypted data. If you forget it, your account data cannot be recovered.

3. Unlocking Data at Startup:

After the first setup, whenever you launch the application and a user_data.encrypted file exists, you will be prompted to enter your master passphrase.
Entering the correct passphrase will unlock your data for the session, allowing you to create new accounts, log in, and view existing ones. If you cancel or enter an incorrect passphrase, these features will remain locked.

4. Creating a New Account:

Ensure your data is unlocked (see step 3).
Click "Create New Account".
Enter a username, password, confirm the password, and fill in optional profile details.
Passwords must meet the specified policy (minimum 8 characters, at least one uppercase, lowercase, number, and special character).

5. Logging In:

Ensure your data is unlocked.
Click "Login to Account".
Enter your username and password to log in and view that account's profile.

6. Viewing All Accounts:

Click "View/Manage All Accounts".
You will be prompted to re-enter your master passphrase (even if already unlocked). This is an added security measure for viewing all sensitive data.
If successful, a list of all registered usernames will appear. Select a username and click "View Selected Account" to see its profile.

7. Generating Secure Passwords:

Click "Generate Secure Password".
A new window will appear where you can adjust the password length and choose which character types to include (lowercase, uppercase, numbers, special characters).
Click "Generate Password" to create a new one, then "Copy to Clipboard" to easily use it elsewhere.

8. Changing Your Master Passphrase:

Click "Set/Change Master Passphrase".
You will first be asked for your current master passphrase to prove your identity and decrypt the existing data.
Then, you'll be prompted to enter and confirm your new master passphrase. All your existing account data will be re-encrypted with the new key.


Technical Details
Encryption: cryptography.fernet is used for symmetric encryption of the entire user_data.encrypted file.

Key Derivation: cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC stretches the user's master passphrase into a robust encryption key.

Password Hashing: bcrypt is used to securely hash individual user account passwords, preventing plain-text storage and protecting against common attack vectors.

GUI: Built with Python's standard tkinter library.


Issues Faced During Development
Master Passphrase Persistence: A significant challenge was ensuring the self.fernet instance and self.users dictionary (which holds the decrypted data) were correctly initialized and persisted throughout the application session after the master passphrase was entered.

Initially, the _prompt_for_startup_unlock method was designed to load data, but it didn't fully integrate the state (i.e., setting self.fernet and self.users permanently) if the user_data.encrypted file didn't exist or was empty. This led to the "Please unlock your data first" error even after seemingly providing the passphrase, as the application's internal state wasn't updated for persistent operations like account creation/login.

The fix involved explicitly setting self.users = {} and assigning the newly derived temp_fernet to self.fernet in _prompt_for_startup_unlock if the file was new/empty. This ensures the application is ready to create the first encrypted data entry. Similarly, the set_change_master_passphrase_prompt was refined to ensure self.users and self.fernet are correctly updated to reflect the unlocked state when setting the passphrase for the first time.

Random Password Generator Logic: The initial random password generator could sometimes produce passwords that didn't meet all the selected criteria (e.g., no uppercase letters, even if selected).

The issue was that it simply concatenated all selected character sets and then randomly picked from the combined pool. While random, this doesn't guarantee inclusion of each selected type.

The solution implemented explicitly picks at least one character from each selected category first, then fills the rest of the password length with random characters from the combined pool. Finally, the entire password string is shuffled to ensure true randomness and prevent predictable patterns.


Future Improvements
This application has a strong foundation, and here are some exciting features that could be added:

1. Delete Account Feature:

Contextual Deletion (When Logged In): Allow a user who is currently logged into their individual account to delete their own account. This would require confirming their password again for security.
Admin Deletion (From "View All Accounts"): Grant the ability to delete any account from the "View/Manage All Accounts" screen. This action would also require re-entering the master passphrase for confirmation, as it's a critical, system-level operation.

2. Edit Account Profile:

Allow logged-in users to update their profile information (age, gender, occupation, etc.).
Implement a separate GUI for profile editing.

3. Password Reset/Change for Individual Accounts:

Allow a logged-in user to change their own account password. This would require entering their old password and then a new one.

4. Export/Import Data:

Provide functionality to export encrypted user data to a backup file and import it back. This is crucial for disaster recovery or migrating data between systems.

5. User Interface Enhancements:

More dynamic and responsive layout (e.g., using grid more extensively with weights).
Visual feedback for successful operations (e.g., temporary "Password Copied!" message instead of a messagebox).
Theming options.

6. Advanced Password Generator Options:

Exclude ambiguous characters (e.g., l, 1, I, O, 0).
Generate pronounceable passwords.
Entropy meter/password strength indicator.

