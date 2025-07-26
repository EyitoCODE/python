import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import json
import base64
import os
import random
import string

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import bcrypt

# --- Configuration ---
# File to store encrypted user data. This file will hold all user accounts.
USER_DATA_FILE = "user_data.encrypted"

# Salt for PBKDF2 key derivation.
# This salt is NOT a secret. It's used to make the key derivation process more robust
# against pre-computation attacks (like rainbow tables). It should be unique and
# fixed for your application. Changing this salt will make previously encrypted
# data unreadable with the same master passphrase.
PBKDF2_SALT = b'a_strong_random_fixed_salt_for_pbkdf2_derivation_for_your_app_12345'

class UserAccountManager:
    """
    Manages user accounts, including creation, login, and data encryption/decryption.
    Also provides a secure password generator.
    """
    def __init__(self):
        # Initialize internal state variables
        self.master_key = None # The derived Fernet key, set when data is unlocked
        self.fernet = None     # Fernet instance for encryption/decryption, tied to master_key
        # Stores decrypted user data: {username: {password_hash: ..., profile: {...}}}
        # This dictionary holds the user data in memory once unlocked.
        self.users = {}
        # Flag to track if the application's data is currently unlocked in memory.
        # This is crucial for controlling access to account management features.
        self.is_data_unlocked = False

        # --- Tkinter GUI Setup ---
        self.root = tk.Tk()
        self.root.title("User Account Manager & Password Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False) # Prevent window resizing for consistent layout
        self.root.configure(bg="#2c3e50") # Dark blue-grey background for modern look

        # Define modern fonts for consistent UI styling
        self.font_large = ("Inter", 16, "bold")
        self.font_medium = ("Inter", 12)
        self.font_small = ("Inter", 10)

        # Attempt to prompt for master passphrase at startup if data file exists.
        # This is the first interaction the user has, trying to unlock existing data.
        self._prompt_for_startup_unlock()

        # Initialize the main menu GUI after attempting to unlock data.
        self.create_main_menu()

    def derive_key(self, passphrase: str) -> bytes:
        """
        Derives a Fernet key (32 bytes) from a given passphrase using PBKDF2HMAC.
        This process stretches the passphrase, making it computationally harder
        to brute-force, even if the salt is known.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), # Hashing algorithm to use
            length=32,                 # Desired length of the derived key in bytes (Fernet requires 32)
            salt=PBKDF2_SALT,          # Application-specific salt for key derivation
            iterations=480000,         # High iteration count for strong key stretching (industry recommendation)
            backend=default_backend()  # Cryptographic backend
        )
        # Derive the key and base64 URL-safe encode it, as Fernet requires this format.
        key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode('utf-8')))
        return key

    def _load_data_from_file(self, passphrase: str):
        """
        Internal helper to load and decrypt data from the file using a given passphrase.
        This method attempts to decrypt the data. If successful, it returns the
        decrypted user data dictionary and the Fernet instance used.
        If decryption fails (e.g., wrong passphrase or corrupted data), it returns (None, None).
        This method does NOT modify self.users or self.is_data_unlocked directly;
        it's a utility for other methods to use for temporary or permanent unlocks.
        """
        try:
            temp_master_key = self.derive_key(passphrase) # Derive key from the provided passphrase
            temp_fernet = Fernet(temp_master_key)         # Create a Fernet instance with this key

            # Check if the data file exists and contains content.
            # If it's a fresh start, the file might not exist or be empty.
            if not os.path.exists(USER_DATA_FILE) or os.path.getsize(USER_DATA_FILE) == 0:
                # If no data file or empty, it's a first-time setup or file was cleared.
                # In this case, return an empty dictionary of users and the newly created Fernet instance.
                # This signifies that the passphrase is valid for creating *new* data.
                return {}, temp_fernet
            
            # If the file exists and has content, attempt to read and decrypt it.
            with open(USER_DATA_FILE, "rb") as f:
                encrypted_data = f.read()

            # Attempt decryption. If the passphrase is wrong, InvalidToken will be raised.
            decrypted_data = temp_fernet.decrypt(encrypted_data).decode('utf-8')
            # Parse the JSON string into a Python dictionary.
            return json.loads(decrypted_data), temp_fernet
        
        except InvalidToken:
            # This specific exception means the passphrase was incorrect or data is corrupted.
            messagebox.showerror("Decryption Error", "Invalid master passphrase or corrupted data.")
            return None, None # Indicate failure
        except Exception as e:
            # Catch other potential errors during file operations or JSON parsing.
            messagebox.showerror("Error", f"An error occurred while loading data: {e}")
            return None, None # Indicate failure

    def _save_data_to_file(self, users_data: dict, fernet_instance: Fernet) -> bool:
        """
        Internal helper to encrypt and save the user data to the file.
        This method takes the dictionary of user data and a Fernet instance to encrypt it.
        It returns True on successful save, False otherwise.
        """
        if not fernet_instance:
            # Ensure an encryption key is available before attempting to save.
            messagebox.showerror("Error", "Encryption key not available for saving. Data not saved.")
            return False

        try:
            # Convert the Python dictionary to a JSON string, formatted for readability.
            json_data = json.dumps(users_data, indent=4)
            # Encrypt the JSON string using the provided Fernet instance.
            encrypted_data = fernet_instance.encrypt(json_data.encode('utf-8'))
            # Write the encrypted bytes to the file in binary write mode.
            with open(USER_DATA_FILE, "wb") as f:
                f.write(encrypted_data)
            return True # Indicate success
        except Exception as e:
            # Catch any errors during encryption or file writing.
            messagebox.showerror("Error", f"Failed to save user data: {e}")
            return False # Indicate failure

    def _prompt_for_startup_unlock(self):
        """
        Prompts the user for the master passphrase at application startup.
        This determines if existing data can be loaded and if account management features
        requiring unlocked data can be used. It sets `self.users`, `self.fernet`,
        and `self.is_data_unlocked` for the duration of the session.
        """
        # Check if the data file exists and has content (i.e., not a brand new file).
        file_exists_and_not_empty = os.path.exists(USER_DATA_FILE) and os.path.getsize(USER_DATA_FILE) > 0

        if file_exists_and_not_empty:
            # If data exists, prompt for the master passphrase to unlock it.
            messagebox.showinfo("Unlock Data", "Please enter your master passphrase to unlock user data for this session.")
            passphrase = simpledialog.askstring("Unlock Data", "Enter your master passphrase:", show='*')
            if not passphrase:
                messagebox.showwarning("Cancelled", "Data remains locked. Some features (Create, Login, Manage) may be unavailable.")
                return # User cancelled, data stays locked

            # Attempt to load and decrypt data with the entered passphrase.
            temp_users, temp_fernet = self._load_data_from_file(passphrase)
            if temp_users is not None:
                # If decryption was successful, update the application's persistent state.
                self.users = temp_users
                self.fernet = temp_fernet
                self.is_data_unlocked = True
                messagebox.showinfo("Success", "Data unlocked for this session!")
            else:
                # _load_data_from_file already showed an error message if decryption failed.
                # Data remains locked, self.is_data_unlocked remains False.
                pass
        else:
            # If the file doesn't exist or is empty, it's the very first run.
            # Inform the user they need to set a master passphrase.
            messagebox.showinfo("First-time Setup", "Welcome! It looks like this is your first time using the application or your data file is empty.\n\nPlease set a master passphrase to secure your future account data. You can do this via 'Set/Change Master Passphrase' in the main menu.")
            # For a truly empty state, ensure `self.users` is an empty dictionary
            # so that `create_account_gui` can proceed without immediately failing
            # on `self.users` being None, although `is_data_unlocked` will still be False.
            self.users = {}
            self.is_data_unlocked = False # Data is not unlocked until a passphrase is set/verified.

    def create_main_menu(self):
        """
        Creates and displays the main menu GUI elements.
        It clears any existing widgets before creating new ones.
        """
        # Clear all widgets from the root window to prepare for the new menu.
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a central frame for the main menu buttons.
        main_frame = tk.Frame(self.root, bg="#34495e", bd=5, relief="raised")
        main_frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        # Configure grid to make buttons expand proportionally
        main_frame.grid_rowconfigure(0, weight=1) # Title row
        for i in range(1, 6): # Button rows
            main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title label for the main menu.
        tk.Label(main_frame, text="Welcome to Account Manager", font=("Inter", 24, "bold"), fg="#ecf0f1", bg="#34495e").grid(row=0, column=0, pady=20)

        # Buttons for various functionalities, styled for a modern look.
        # Commands are linked to respective GUI methods.
        tk.Button(main_frame, text="Create New Account", command=self.create_account_gui,
                    font=self.font_large, bg="#27ae60", fg="white", activebackground="#2ecc71",
                    relief="raised", bd=3, width=25, height=2).grid(row=1, column=0, pady=10)

        tk.Button(main_frame, text="Login to Account", command=self.login_gui,
                    font=self.font_large, bg="#3498db", fg="white", activebackground="#2980b9",
                    relief="raised", bd=3, width=25, height=2).grid(row=2, column=0, pady=10)
            
        tk.Button(main_frame, text="View/Manage All Accounts", command=self.view_all_accounts_gui,
                    font=self.font_large, bg="#f39c12", fg="white", activebackground="#e67e22",
                    relief="raised", bd=3, width=25, height=2).grid(row=3, column=0, pady=10)

        # Button to open the Password Generator in a new window.
        tk.Button(main_frame, text="Generate Secure Password", command=self.password_generator_gui,
                    font=self.font_large, bg="#8e44ad", fg="white", activebackground="#9b59b6",
                    relief="raised", bd=3, width=25, height=2).grid(row=4, column=0, pady=10)

        # Button for setting or changing the master passphrase.
        tk.Button(main_frame, text="Set/Change Master Passphrase", command=self.set_change_master_passphrase_prompt,
                    font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                    relief="raised", bd=2, width=25, height=2).grid(row=5, column=0, pady=10)

    def view_all_accounts_gui(self):
        """
        Prompts for the master passphrase to view all accounts.
        This ensures that even if data wasn't unlocked at startup,
        a user can temporarily unlock it to view accounts.
        """
        passphrase = simpledialog.askstring("Master Passphrase", "Enter your master passphrase to view all accounts:", show='*')
        if not passphrase:
            messagebox.showwarning("Cancelled", "Master passphrase not entered. Cannot view accounts.")
            return
            
        # Attempt to load data for display. This creates a temporary decryption context.
        temp_users, temp_fernet = self._load_data_from_file(passphrase)
        if temp_users is None: # _load_data_from_file already showed an error message if decryption failed.
            return # Do not proceed if data could not be decrypted.

        # Now display the accounts using the temporarily decrypted data.
        self._display_accounts_list_gui(temp_users)

    def _display_accounts_list_gui(self, users_data_to_display: dict):
        """
        Displays a list of all accounts from the provided `users_data_to_display` dictionary.
        This allows showing accounts either from the persistently unlocked data or
        from a temporary decryption (e.g., for 'View All Accounts').
        """
        # Clear current widgets.
        for widget in self.root.winfo_children():
            widget.destroy()

        accounts_list_frame = tk.Frame(self.root, bg="#34495e", bd=5, relief="raised")
        accounts_list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(accounts_list_frame, text="All Registered Accounts", font=("Inter", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=10)

        if not users_data_to_display:
            tk.Label(accounts_list_frame, text="No accounts registered yet.", font=self.font_medium, fg="#ecf0f1", bg="#34495e").pack(pady=10)
        else:
            # Create a frame for the listbox and scrollbar.
            listbox_frame = tk.Frame(accounts_list_frame, bg="#34495e")
            listbox_frame.pack(pady=10, fill="both", expand=True)

            scrollbar = tk.Scrollbar(listbox_frame)
            scrollbar.pack(side="right", fill="y")

            # Listbox to show usernames.
            self.account_listbox = tk.Listbox(listbox_frame, font=self.font_medium,
                                                bg="#2c3e50", fg="#ecf0f1", bd=2, relief="sunken",
                                                yscrollcommand=scrollbar.set)
            self.account_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=self.account_listbox.yview)

            # Populate the listbox with usernames.
            for username in users_data_to_display.keys():
                self.account_listbox.insert(tk.END, username)
                
            # Button to view the profile of the selected account.
            tk.Button(accounts_list_frame, text="View Selected Account", 
                        command=lambda: self._view_selected_account_from_list(users_data_to_display),
                        font=self.font_medium, bg="#3498db", fg="white", activebackground="#2980b9",
                        relief="raised", bd=3, width=25).pack(pady=10)

        # Back button, whose action depends on how this view was accessed.
        tk.Button(accounts_list_frame, text="Back to Main Menu", command=self.create_main_menu,
                    font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                    relief="raised", bd=2, width=20).pack(pady=20)

    def _view_selected_account_from_list(self, users_data_to_display: dict):
        """
        Callback function to view an individual account's profile after selection
        from the listbox.
        """
        selected_indices = self.account_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select an account from the list.")
            return
            
        selected_username = self.account_listbox.get(selected_indices[0])
        # Display the profile using the same data source that populated the list.
        self._show_individual_user_profile_gui(selected_username, users_data_to_display)

    def _show_individual_user_profile_gui(self, username: str, users_data_source: dict):
        """
        Displays the profile details of a single user.
        Takes `users_data_source` as an argument to be flexible (e.g., display from
        persistent `self.users` after login, or from temporary data after "View All Accounts").
        """
        if username not in users_data_source:
            messagebox.showerror("Error", "User not found in data source.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        profile_frame = tk.Frame(self.root, bg="#34495e", bd=5, relief="raised")
        profile_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(profile_frame, text=f"Profile for {username}", font=("Inter", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=10)

        profile_data = users_data_source[username]["profile"]
        # Iterate through profile data and display each key-value pair.
        for key, value in profile_data.items():
            display_key = key.replace("_", " ").title() # Format key for better display (e.g., "first_name" -> "First Name")
            tk.Label(profile_frame, text=f"{display_key}: {value if value is not None else 'N/A'}",
                            font=self.font_medium, fg="#ecf0f1", bg="#34495e", anchor="w").pack(fill="x", padx=20, pady=2)

        # Back button logic: if showing from `self.users` (persistent), go to main menu.
        # If showing from a temporary `users_data_source`, go back to the all accounts list.
        if users_data_source is self.users:
            tk.Button(profile_frame, text="Back to Main Menu", command=self.create_main_menu,
                        font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                        relief="raised", bd=2, width=20).pack(pady=20)
        else:
            tk.Button(profile_frame, text="Back to All Accounts", command=lambda: self._display_accounts_list_gui(users_data_source),
                        font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                        relief="raised", bd=2, width=20).pack(pady=20)

    def set_change_master_passphrase_prompt(self):
        """
        Handles the logic for setting the master passphrase for the first time
        or changing an existing one. This is a critical security function.
        """
        file_exists_and_not_empty = os.path.exists(USER_DATA_FILE) and os.path.getsize(USER_DATA_FILE) > 0

        if file_exists_and_not_empty:
            # Scenario 1: Master passphrase has been set before; user wants to change it.
            messagebox.showinfo("Unlock Required", "To change your master passphrase, you must first unlock your data with the CURRENT passphrase.")
            current_passphrase = simpledialog.askstring("Current Master Passphrase", "Enter your CURRENT master passphrase:", show='*')
            if not current_passphrase:
                messagebox.showwarning("Cancelled", "Operation cancelled.")
                return
                
            # Verify current passphrase by attempting to load data with it.
            # This is a temporary load, just for verification.
            temp_users_check, temp_fernet_check = self._load_data_from_file(current_passphrase)
            if temp_users_check is None:
                # _load_data_from_file already showed an error if the passphrase was wrong.
                return # Stop if current passphrase is incorrect.
                
            # If current passphrase is correct, we now have the decrypted data in temp_users_check.
            # Crucially, we update the main `self.users` and `self.fernet` to reflect this
            # *unlocked state* for the session, which is needed to re-encrypt the data later.
            self.users = temp_users_check
            self.fernet = temp_fernet_check
            self.is_data_unlocked = True # Data is now unlocked with the OLD passphrase.

            # Warn the user about the irreversible nature of forgetting the new passphrase.
            if not messagebox.askyesno("Warning", "WARNING: Changing the master passphrase will re-encrypt all your data. If you forget the NEW passphrase, your data will be PERMANENTLY LOST. Do you wish to proceed?"):
                return

            new_passphrase = simpledialog.askstring("New Master Passphrase", "Enter your NEW master passphrase:", show='*')
            if not new_passphrase:
                messagebox.showwarning("Cancelled", "New master passphrase not entered.")
                return
                
            confirm_new_passphrase = simpledialog.askstring("Confirm New Passphrase", "Confirm your NEW master passphrase:", show='*')
            if new_passphrase != confirm_new_passphrase:
                messagebox.showerror("Error", "New passphrases do not match.")
                return

            # Re-derive the master key and Fernet instance using the NEW passphrase.
            try:
                self.master_key = self.derive_key(new_passphrase)
                self.fernet = Fernet(self.master_key)
                
                # Save the *current* `self.users` data (which is the decrypted data)
                # using the *new* `self.fernet` instance (derived from the new passphrase).
                if self._save_data_to_file(self.users, self.fernet):
                    messagebox.showinfo("Success", "Master passphrase successfully changed and data re-encrypted!")
                    # The `self.is_data_unlocked` remains True, now with the new passphrase.
                else:
                    # If save fails, inform the user about potential data corruption.
                    messagebox.showerror("Error", "Failed to save data with new passphrase. Your data might be corrupted. Please restart and use your OLD passphrase if possible.")
                    # Revert to a locked state or try to load with old key to prevent data loss impression
                    self.is_data_unlocked = False 
                    self.fernet = None
                    self.users = {} # Clear potentially compromised data in memory
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change master passphrase: {e}")
                self.is_data_unlocked = False
                self.fernet = None
                self.users = {}

        else:
            # Scenario 2: Master passphrase has NOT been set yet (first time setup).
            if not messagebox.askyesno("Warning", "WARNING: You are about to set a master passphrase for your data. If you forget this passphrase, your data will be PERMANENTLY LOST. Do you wish to proceed?"):
                return

            new_passphrase = simpledialog.askstring("Set Master Passphrase", "Enter your master passphrase:", show='*')
            if not new_passphrase:
                messagebox.showwarning("Cancelled", "Master passphrase not set.")
                return
                
            confirm_new_passphrase = simpledialog.askstring("Confirm Master Passphrase", "Confirm your master passphrase:", show='*')
            if new_passphrase != confirm_new_passphrase:
                messagebox.showerror("Error", "Passphrases do not match.")
                return

            # Derive the key and initialize Fernet with the new passphrase.
            # This is for the first time setup.
            try:
                self.master_key = self.derive_key(new_passphrase)
                self.fernet = Fernet(self.master_key)
                self.users = {} # Initialize users as empty dictionary since no data exists yet.
                self.is_data_unlocked = True # Data is now "unlocked" with this new passphrase.

                # Save an empty JSON to the file to initialize it with the new master passphrase.
                # This creates the `user_data.encrypted` file.
                if self._save_data_to_file(self.users, self.fernet):
                    messagebox.showinfo("Success", "Master passphrase set successfully! Data is now unlocked for this session.")
                else:
                    messagebox.showerror("Error", "Failed to initialize data file with new passphrase. Please try again.")
                    self.is_data_unlocked = False
                    self.fernet = None
                    self.users = {}
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set master passphrase: {e}")
                self.is_data_unlocked = False
                self.fernet = None
                self.users = {}


    def create_account_gui(self):
        """
        GUI for creating a new user account.
        Requires that the master data be unlocked.
        """
        # Critical check: Ensure the master data is unlocked for persistent account creation.
        if not self.is_data_unlocked:
            messagebox.showwarning("Data Not Unlocked", "Please unlock your data first by entering the master passphrase at startup, or by using 'Set/Change Master Passphrase' to set/unlock it.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        account_frame = tk.Frame(self.root, bg="#34495e", bd=5, relief="raised")
        account_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(account_frame, text="Create New Account", font=("Inter", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=10)

        # --- Account Creation Form ---
        form_frame = tk.Frame(account_frame, bg="#34495e")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Username:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.username_entry = tk.Entry(form_frame, font=self.font_medium, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Password:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.password_entry = tk.Entry(form_frame, font=self.font_medium, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Confirm Password:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.confirm_password_entry = tk.Entry(form_frame, font=self.font_medium, show="*", width=30)
        self.confirm_password_entry.grid(row=2, column=1, pady=5, padx=5)

        # Dynamic creation of profile fields.
        profile_fields = ["Age:", "Gender:", "Weight (kg):", "Height (cm):", "Occupation:"]
        self.profile_entries = {} # Store references to profile entry widgets.
        for i, field in enumerate(profile_fields):
            tk.Label(form_frame, text=field, font=self.font_medium, fg="#ecf0f1", bg="#34495e").grid(row=i+3, column=0, sticky="w", pady=5, padx=5)
            entry = tk.Entry(form_frame, font=self.font_medium, width=30)
            entry.grid(row=i+3, column=1, pady=5, padx=5)
            # Store entry widgets by a simplified key (e.g., "age", "gender").
            self.profile_entries[field.replace(" (kg):", "").replace(" (cm):", "").replace(":", "").strip().lower()] = entry

        tk.Button(account_frame, text="Register Account", command=self.register_account,
                    font=self.font_large, bg="#27ae60", fg="white", activebackground="#2ecc71",
                    relief="raised", bd=3, width=20).pack(pady=15)

        tk.Button(account_frame, text="Back to Main Menu", command=self.create_main_menu,
                    font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                    relief="raised", bd=2, width=15).pack(pady=10)

    def register_account(self):
        """
        Handles the registration logic for a new user account.
        Performs validation checks and saves the new account data if valid.
        """
        # Ensure data is unlocked before attempting to save a new account.
        if not self.is_data_unlocked:
            messagebox.showerror("Error", "Data is not unlocked. Cannot register account. Please unlock data at startup or via 'Set/Change Master Passphrase'.")
            return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Input validation for basic fields.
        if not username or not password or not confirm_password:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Input Error", "Passwords do not match.")
            return

        if username in self.users:
            messagebox.showerror("Registration Error", "Username already exists. Please choose a different one.")
            return

        # Validate password against the defined policy.
        if not self.validate_password_policy(password):
            return # Policy validation function shows its own error messages.

        # Hash the password using bcrypt for secure storage.
        # bcrypt.gensalt() generates a random salt for each hash, making rainbow table attacks ineffective.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        profile_data = {}
        # Collect and validate profile data.
        for key, entry_widget in self.profile_entries.items():
            value = entry_widget.get().strip()
            if key in ["age", "weight", "height"]:
                try:
                    # Attempt to convert to integer; store None if empty.
                    profile_data[key] = int(value) if value else None
                except ValueError:
                    messagebox.showerror("Input Error", f"Please enter a valid number for {key}.")
                    return # Stop registration if numeric input is invalid.
            else:
                profile_data[key] = value if value else None # Store string value or None if empty.

        # Add the new user to the in-memory users dictionary.
        self.users[username] = {
            "password_hash": hashed_password,
            "profile": profile_data
        }
            
        # Save the updated `self.users` data using the persistently available `self.fernet` instance.
        if self._save_data_to_file(self.users, self.fernet):
            messagebox.showinfo("Success", f"Account for '{username}' created successfully!")
            self.create_main_menu() # Return to main menu on success.
        else:
            # If saving fails, remove the user from the in-memory dictionary to maintain consistency.
            del self.users[username]
            messagebox.showerror("Error", "Account could not be saved due to an encryption or file issue. Please try again.")

    def validate_password_policy(self, password: str) -> bool:
        """
        Checks if the provided password meets the required security policy:
        - Minimum length of 8 characters.
        - At least one uppercase letter.
        - At least one lowercase letter.
        - At least one number.
        - At least one special character (from string.punctuation).
        Returns True if policy is met, False otherwise and shows an error message.
        """
        if len(password) < 8:
            messagebox.showerror("Password Policy", "Password must be at least 8 characters long.")
            return False
        if not any(char.isupper() for char in password):
            messagebox.showerror("Password Policy", "Password must contain at least one uppercase letter.")
            return False
        if not any(char.islower() for char in password):
            messagebox.showerror("Password Policy", "Password must contain at least one lowercase letter.")
            return False
        if not any(char.isdigit() for char in password):
            messagebox.showerror("Password Policy", "Password must contain at least one number.")
            return False
        if not any(char in string.punctuation for char in password):
            messagebox.showerror("Password Policy", "Password must contain at least one special character.")
            return False
        return True

    def login_gui(self):
        """
        GUI for logging into a single user account.
        Requires that the master data be unlocked.
        """
        # Critical check: Ensure the master data is unlocked to access user hashes.
        if not self.is_data_unlocked:
            messagebox.showwarning("Data Not Unlocked", "Please unlock your data first by entering the master passphrase at startup, or by using 'Set/Change Master Passphrase' to set/unlock it.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root, bg="#34495e", bd=5, relief="raised")
        login_frame.pack(pady=50, padx=50, fill="both", expand=True)

        tk.Label(login_frame, text="Login to Your Account", font=("Inter", 20, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=20)

        tk.Label(login_frame, text="Username:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.login_username_entry = tk.Entry(login_frame, font=self.font_medium, width=30)
        self.login_username_entry.pack(pady=5)

        tk.Label(login_frame, text="Password:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.login_password_entry = tk.Entry(login_frame, font=self.font_medium, show="*", width=30)
        self.login_password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", command=self.perform_login,
                    font=self.font_large, bg="#3498db", fg="white", activebackground="#2980b9",
                    relief="raised", bd=3, width=15).pack(pady=15)

        tk.Button(login_frame, text="Back to Main Menu", command=self.create_main_menu,
                    font=self.font_medium, bg="#7f8c8d", fg="white", activebackground="#95a5a6",
                    relief="raised", bd=2, width=15).pack(pady=5)

    def perform_login(self):
        """
        Performs the user login authentication by checking username and password.
        Uses bcrypt to safely verify the password against the stored hash.
        """
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        if username not in self.users:
            messagebox.showerror("Login Error", "User not found.")
            return

        # Retrieve the stored password hash for the given username.
        stored_hash = self.users[username]["password_hash"].encode('utf-8')
        # Use bcrypt.checkpw to securely compare the entered password with the stored hash.
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            # Upon successful login, display the user's profile using the persistently loaded data.
            self._show_individual_user_profile_gui(username, self.users)
        else:
            messagebox.showerror("Login Error", "Incorrect password.")

    def password_generator_gui(self):
        """
        Creates a new Toplevel window dedicated to the secure password generator.
        This isolates the generator from the main application flow.
        """
        pw_gen_window = Toplevel(self.root) # Create a new top-level window.
        pw_gen_window.title("Generate Secure Password")
        pw_gen_window.geometry("500x450")
        pw_gen_window.resizable(False, False)
        pw_gen_window.configure(bg="#2c3e50")

        pw_gen_frame = tk.Frame(pw_gen_window, bg="#34495e", bd=5, relief="raised")
        pw_gen_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(pw_gen_frame, text="Secure Password Generator", font=("Inter", 18, "bold"), fg="#ecf0f1", bg="#34495e").pack(pady=10)

        # Password length selection using a Scale widget.
        tk.Label(pw_gen_frame, text="Password Length:", font=self.font_medium, fg="#ecf0f1", bg="#34495e").pack(pady=5)
        self.length_scale_gen = tk.Scale(pw_gen_frame, from_=8, to=32, orient="horizontal", length=300,
                                        font=self.font_medium, bg="#34495e", fg="#ecf0f1", troughcolor="#2c3e50",
                                        highlightbackground="#34495e", sliderrelief="flat", sliderlength=20)
        self.length_scale_gen.set(12) # Default password length.
        self.length_scale_gen.pack(pady=5)

        # Checkboxes for including different character types.
        # BooleanVars are explicitly created with `master=pw_gen_window` to associate them with this Toplevel.
        self.include_lowercase_gen = tk.BooleanVar(master=pw_gen_window, value=True) # Always include lowercase
        self.include_caps_gen = tk.BooleanVar(master=pw_gen_window, value=True)
        self.include_numbers_gen = tk.BooleanVar(master=pw_gen_window, value=True)
        self.include_special_gen = tk.BooleanVar(master=pw_gen_window, value=True)

        tk.Checkbutton(pw_gen_frame, text="Include Lowercase Letters", variable=self.include_lowercase_gen,
                        font=self.font_medium, bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                        activebackground="#34495e", activeforeground="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Checkbutton(pw_gen_frame, text="Include Uppercase Letters", variable=self.include_caps_gen,
                        font=self.font_medium, bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                        activebackground="#34495e", activeforeground="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Checkbutton(pw_gen_frame, text="Include Numbers", variable=self.include_numbers_gen,
                        font=self.font_medium, bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                        activebackground="#34495e", activeforeground="#ecf0f1").pack(anchor="w", padx=20, pady=2)
        tk.Checkbutton(pw_gen_frame, text="Include Special Characters", variable=self.include_special_gen,
                        font=self.font_medium, bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50",
                        activebackground="#34495e", activeforeground="#ecf0f1").pack(anchor="w", padx=20, pady=2)

        # Label to display the generated password.
        self.generated_password_var_gen = tk.StringVar(master=pw_gen_window)
        self.generated_password_label_gen = tk.Label(pw_gen_frame, textvariable=self.generated_password_var_gen,
                                                        font=("Inter", 14, "bold"), fg="#2ecc71", bg="#2c3e50",
                                                        relief="sunken", bd=2, width=40, height=2, wraplength=350) # Added wraplength
        self.generated_password_label_gen.pack(pady=15)

        # Buttons for generating and copying the password.
        button_frame = tk.Frame(pw_gen_frame, bg="#34495e")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Generate Password", command=self._generate_password_in_new_window,
                    font=self.font_medium, bg="#f39c12", fg="white", activebackground="#e67e22",
                    relief="raised", bd=3, width=20).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Copy to Clipboard", command=self._copy_to_clipboard_from_new_window,
                    font=self.font_medium, bg="#3498db", fg="white", activebackground="#2980b9",
                    relief="raised", bd=3, width=20).grid(row=0, column=1, padx=10)

    def _generate_password_in_new_window(self):
        """
        Generates a secure random password based on user selections and ensures
        it meets common password policy rules (at least one of each selected type).
        """
        length = self.length_scale_gen.get()
        
        # Define character sets.
        lowercase_chars = string.ascii_lowercase
        uppercase_chars = string.ascii_uppercase
        digit_chars = string.digits
        special_chars = string.punctuation

        # Initialize password components and character pool.
        password_chars = []
        all_possible_chars = ""

        # Ensure at least one character from each selected category is included.
        if self.include_lowercase_gen.get():
            password_chars.append(random.choice(lowercase_chars))
            all_possible_chars += lowercase_chars
        
        if self.include_caps_gen.get():
            password_chars.append(random.choice(uppercase_chars))
            all_possible_chars += uppercase_chars
        
        if self.include_numbers_gen.get():
            password_chars.append(random.choice(digit_chars))
            all_possible_chars += digit_chars
        
        if self.include_special_gen.get():
            password_chars.append(random.choice(special_chars))
            all_possible_chars += special_chars

        # Handle case where no character types are selected.
        if not all_possible_chars:
            messagebox.showerror("Selection Error", "Please select at least one character type (e.g., lowercase letters).")
            self.generated_password_var_gen.set("")
            return

        # Fill the remaining length of the password with random characters from the combined pool.
        # Subtract the number of characters already added to guarantee inclusion.
        remaining_length = length - len(password_chars)
        if remaining_length < 0: # This can happen if length is too short and many types are selected
            # Forcing a minimum length for each category might exceed total length if it's too small
            # This logic prioritizes minimum type inclusion over exact length for very small lengths.
            # A more robust approach might be to enforce minimum length for each chosen category and increase total length if needed.
            # For simplicity, we'll just use the currently accumulated password_chars if length is too small.
            pass
        else:
            password_chars.extend(random.choice(all_possible_chars) for _ in range(remaining_length))

        # Shuffle the list of characters to ensure randomness and prevent predictable patterns.
        random.shuffle(password_chars)
        generated_password = ''.join(password_chars)
        
        self.generated_password_var_gen.set(generated_password)

    def _copy_to_clipboard_from_new_window(self):
        """
        Copies the currently displayed generated password to the system clipboard.
        """
        password = self.generated_password_var_gen.get()
        if password:
            self.root.clipboard_clear() # Clear any previous clipboard content.
            self.root.clipboard_append(password) # Append the new password.
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy. Generate one first!")

    def run(self):
        """Starts the Tkinter event loop, launching the application GUI."""
        self.root.mainloop()

# Entry point of the application.
if __name__ == "__main__":
    app = UserAccountManager() # Create an instance of the account manager.
    app.run() # Run the application.