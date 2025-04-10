import streamlit as st
import hashlib
import time

# Set page config
st.set_page_config(page_title="Secure Data Storage App", layout="centered")

# Styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# In-memory Databases
if "users" not in st.session_state:
    st.session_state.users = {}  # username: hashed_password

if "data" not in st.session_state:
    st.session_state.data = {}   # username: [{"encrypted": "xyz", "key": "abc"}, ...]

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "decrypt_attempts" not in st.session_state:
    st.session_state.decrypt_attempts = 0


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def caesar_encrypt(text, key):
    result = ""
    key = int(key) % 26
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result


def caesar_decrypt(text, key):
    return caesar_encrypt(text, -int(key))


# Login Page
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hash_text(password)
        if username in st.session_state.users and st.session_state.users[username] == hashed:
            # Successful login
            st.session_state.current_user = username
            st.session_state.login_attempts = 0
            st.session_state.logged_in = True  # Set the logged-in state
            st.success("Login Successful!")
             # This will automatically rerun the app to show the dashboard

        else:
            # Failed login attempt
            st.session_state.login_attempts += 1
            st.error(f"Invalid Credentials. Attempts: {st.session_state.login_attempts}/3")

        if st.session_state.login_attempts >= 3:
            st.warning("Too many failed attempts. Please try again later.")
            time.sleep(2)  # Delay for UX before stopping
            st.session_state.login_attempts = 0  # Reset attempts after 3 failed logins


    st.markdown("Don't have an account? [Register here](#register)")


# Register Page
def register():
    st.title("📝 Register")

    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")

    if st.button("Register"):
        if username in st.session_state.users:
            st.warning("Username already exists!")
        else:
            st.session_state.users[username] = hash_text(password)
            st.success("Registered Successfully! Please Login.")


# Encrypt Page
def encrypt_page():
    st.title("🔒 Encrypt Data")

    text = st.text_area("Enter your text")
    key = st.text_input("Enter Numeric Key")

    if st.button("Encrypt"):
        if not key.isdigit():
            st.error("Key must be numeric!")
        else:
            encrypted = caesar_encrypt(text, key)
            data = {"encrypted": encrypted, "key": key}
            st.session_state.data.setdefault(st.session_state.current_user, []).append(data)
            st.success(f"Encrypted Text: {encrypted}")


# Decrypt Page
def decrypt_page():
    st.title("🔓 Decrypt Data")

    cipher_text = st.text_area("Enter Cipher Text")
    key = st.text_input("Enter Key")

    if st.button("Decrypt"):
        found = False
        for data in st.session_state.data.get(st.session_state.current_user, []):
            if data["encrypted"] == cipher_text and data["key"] == key:
                plain_text = caesar_decrypt(cipher_text, key)
                st.success(f"Decrypted Text: {plain_text}")
                st.session_state.decrypt_attempts = 0
                found = True
                break
        if not found:
            st.session_state.decrypt_attempts += 1
            st.error(f"Invalid Key. Attempts: {st.session_state.decrypt_attempts}/3")

        if st.session_state.decrypt_attempts >= 3:
            st.warning("Too many wrong attempts. Redirecting to login...")
            time.sleep(2)
            st.session_state.decrypt_attempts = 0
            st.session_state.current_user = None
            # No rerun here, just clear session state for user logout


# View Stored Data Page
def view_data():
    st.title("📂 Stored Encrypted Data")

    user_data = st.session_state.data.get(st.session_state.current_user, [])

    if not user_data:
        st.info("No data found.")
        return

    for idx, item in enumerate(user_data):
        with st.expander(f"Record {idx+1}"):
            st.write(f"Encrypted Text: `{item['encrypted']}`")
            show_key = st.checkbox("Show Key", key=f"show_{idx}")
            if show_key:
                st.code(item["key"])
                st.button("Copy Key", key=f"copy_{idx}")
            else:
                st.write("Key is Hidden")


# Main App Logic
if st.session_state.current_user:
    st.sidebar.title(f"Welcome, {st.session_state.current_user}")
    page = st.sidebar.selectbox("Navigate", ["Encrypt", "Decrypt", "Stored Data", "Logout"])

    if page == "Encrypt":
        encrypt_page()
    elif page == "Decrypt":
        decrypt_page()
    elif page == "Stored Data":
        view_data()
    elif page == "Logout":
        st.session_state.current_user = None  # Clear current user
        # No need for rerun here, Streamlit will handle the logout automatically
        st.success("Logged out successfully!")

else:
    page = st.sidebar.selectbox("Choose", ["Login", "Register"])

    if page == "Login":
        login()
    else:
        register()
