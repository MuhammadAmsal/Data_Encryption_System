Secure Data Storage App 🔐
A web application built using Streamlit that allows users to securely store and encrypt/decrypt their data. This app uses Caesar Cipher for encryption and decryption along with secure password hashing for user authentication.

Features ✨
User Authentication: Secure login and registration with password hashing (SHA-256).

Encryption & Decryption: Encrypt and decrypt data using the Caesar Cipher.

Data Storage: Store encrypted data and associated keys. View, copy, or hide the keys.

Security: Limit failed login and decryption attempts. After multiple failed attempts, the user is logged out and redirected to the login page.

User-Friendly UI: Intuitive interface using Streamlit with sidebar navigation and attractive design.

Usage 🛠️
Registration: Create a new user account by choosing a username and password.

Login: Log in using your credentials. After a successful login, you'll be redirected to the main dashboard.

Encryption: Encrypt text by entering the text and a numeric key.

Decryption: Decrypt previously encrypted data by providing the ciphertext and the key.

Stored Data: View previously stored encrypted data. You can show or hide the key and copy it for later use.

Security Features 🔒
Password Hashing: User passwords are securely hashed using SHA-256 before storage.

Login Attempts: Users are restricted to a maximum of 3 failed login attempts. After 3 failed attempts, the user will be locked out for a period of time.

Decryption Attempts: Users are restricted to 3 failed decryption attempts for each ciphertext. After 3 failed attempts, the app will log the user out and redirect to the login page.

Key Visibility: The encryption keys are hidden by default in the "Stored Data" section, but users can toggle to view the key or copy it for later use.

Future Enhancements 🚀
Add more encryption algorithms (e.g., AES) for stronger security.

Implement multi-factor authentication (MFA).

Allow users to download their encrypted data for offline storage.
