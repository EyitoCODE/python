# Advanced Biometric & Account Management System ??

## Overview

This project implements a robust multi-factor biometric authentication and account management system designed to enhance security for personal applications or simulated building access. It combines **facial recognition** and **voice identification** with traditional **password-based authentication** and secure account creation protocols.

The system aims to provide a secure, user-friendly, and cross-platform compatible solution for verifying user identities using advanced biometric techniques.

## Features

* **Multi-Factor Biometric Authentication:** Authenticate users using a combination of:
    * **Facial Recognition:** Utilizes camera input to identify enrolled users.
    * **Voice Identification:** Uses microphone input to verify user's voice patterns.
* **Secure Account Creation:**
    * Guided user registration process.
    * Enforcement of strong password policies (uppercase, lowercase, numbers, special characters).
    * Password confirmation to prevent typos.
* **Cross-Platform Compatibility:** Designed to run on both **Windows** and **macOS** for seamless camera and microphone access.
* **Modular Architecture:** Code is organized into distinct modules for easy maintenance and scalability.
* **Graphical User Interface (GUI):** Intuitive interface for user registration, biometric enrollment, and login.

## Technologies Used

* **Python 3.x**
* **OpenCV:** For camera access and facial detection.
* **`face_recognition` / `dlib`:** For robust facial recognition (or custom TensorFlow/Keras model).
* **`librosa`:** For audio feature extraction (MFCCs).
* **`scikit-learn` / TensorFlow/Keras:** For training and utilizing voice identification models.
* **`pyaudio` / `sounddevice`:** For cross-platform microphone access.
* **`Tkinter` / `PyQt` / `Kivy`:** For building the graphical user interface.
* **`sqlite3` / `SQLAlchemy`:** For secure user data and biometric template storage.
* **`bcrypt` / `argon2-cffi`:** For secure password hashing.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/biometric_security_system.git](https://github.com/YourUsername/biometric_security_system.git)
    cd biometric_security_system
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (You will need to create a `requirements.txt` file listing all the libraries used, e.g., `opencv-python`, `face_recognition`, `librosa`, `scikit-learn`, `pyaudio`, `pyqt5`, `bcrypt`).

4.  **Hardware Requirements:**
    * Webcam (for facial recognition)
    * Microphone (for voice identification)

## Usage

1.  **Run the main application:**
    ```bash
    python main.py
    ```

2.  **Register a New Account:**
    * Follow the prompts to enter your name, sex, age, and email.
    * Create a strong password that meets the specified criteria.
    * The system will then guide you through the facial and voice enrollment process. Ensure good lighting for face capture and a quiet environment for voice recording.

3.  **Authenticate:**
    * Choose to log in using your username/password, or attempt biometric authentication (face, voice, or both).
    * The system will verify your identity using the enrolled biometric data.

## Project Structure
biometric_security_system/
??? main.py                     # Main application entry point
??? gui/
?   ??? __init__.py
?   ??? registration_window.py
?   ??? authentication_window.py
??? biometric_modules/
?   ??? __init__.py
?   ??? face_recognizer.py      # Handles face enrollment and recognition
?   ??? voice_identifier.py     # Handles voice enrollment and identification
??? account_manager/
?   ??? __init__.py
?   ??? user_db.py              # Database interactions
?   ??? password_utils.py       # Password hashing and policy enforcement
??? config.py                   # Configuration variables (e.g., database path)
??? models/                     # Directory for trained ML models (e.g., face, voice models)
??? data/                       # Directory for storing biometric templates/data
??? tests/
?   ??? test_security.py
??? README.md

## Future Enhancements

* **Liveness Detection:** Implement techniques to prevent spoofing for facial and voice biometrics.
* **Multi-User Management:** Admin panel to manage multiple users.
* **Cloud Integration:** Store biometric data and models securely in a cloud database.
* **Mobile Application:** Develop a complementary mobile app for seamless house/building entry.
* **Advanced UI/UX:** Improve the user interface for a more polished experience.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details