import streamlit as st  # type: ignore
import hashlib
from cryptography.fernet import Fernet  # type: ignore
import time

# Set page config at the top
st.set_page_config(
    page_title="Secure Vault",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Home"  # Default selection

# Instead of generating a new key every time, store a fixed key or generate one and use it for both encryption and decryption.
if 'key' not in st.session_state:
    # You can either store this key securely or generate one and use it for both encryption and decryption.
    st.session_state.key = Fernet.generate_key()

cipher = Fernet(st.session_state.key)

# Hash function
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt
def encrypt_data(text, passkey):
    return cipher.encrypt(text.encode()).decode()

# Decrypt
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    for key, value in st.session_state.stored_data.items():
        if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            # Use the stored key for decryption
            cipher = Fernet(value["key"])  # This assumes you store the key with the encrypted data
            try:
                return cipher.decrypt(encrypted_text.encode()).decode()
            except Exception as e:
                st.error(f"Decryption failed. Error: {str(e)}")
                return None
    st.session_state.failed_attempts += 1
    return None

# Main app logic
def main():
    with st.sidebar:
        st.title("Secure Vault")

        # Dynamically set text color based on selected menu
        sidebar_text_color = "black" if st.session_state.get("selected_menu") == "Store Data" else "white"
        
        st.markdown(f"""
            <div style='background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;'>
                <p style='color: {sidebar_text_color};'>Store and retrieve your sensitive data securely using encryption.</p>
            </div>
        """, unsafe_allow_html=True)

        menu = ["Home", "Store Data", "Retrieve Data", "Login"]
        choice = st.radio("Navigation", menu, index=0 if not st.session_state.failed_attempts >= 3 else 3)
        st.session_state.selected_menu = choice

    if choice == "Home":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Secure Data Encryption System")
            st.markdown("""
                <div style='background-color: rgba(30, 136, 229, 0.2); padding: 20px; border-radius: 10px;'>
                    <h3 style='color: #1e88e5;'>Your Personal Digital Safe</h3>
                    <p>Store sensitive information with encryption and retrieve it using your secret passkey.</p>
                    <p style='color: #ff9800;'>No data is stored on disk — full privacy.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("### Features:")
            st.markdown("""
                - Store Data: Encrypt your information with a passkey.
                - Retrieve Data: Decrypt only with the correct passkey.
                - Security: After 3 failed attempts, system locks down.
            """)
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/295/295128.png", width=200)
        st.markdown("---")
        st.info("This app uses Fernet symmetric encryption for data protection.")

    elif choice == "Store Data":
        st.title("Store Data Securely")
        col1, col2 = st.columns([3, 1])
        with col1:
            user_data = st.text_area("Enter Data", height=150, placeholder="Paste your sensitive information here...")
            passkey = st.text_input("Create Passkey", type="password", help="You’ll need this passkey to retrieve your data.")
            if st.button("Encrypt & Store", key="store_btn"):
                if user_data and passkey:
                    with st.spinner("Encrypting..."):
                        time.sleep(1)
                        hashed = hash_passkey(passkey)
                        encrypted = encrypt_data(user_data, passkey)
                        st.session_state.stored_data[encrypted] = {"encrypted_text": encrypted, "passkey": hashed, "key": st.session_state.key}
                        st.success("Data encrypted and stored successfully.")
                        st.code(encrypted, language="text")
                        st.warning("Copy and save this encrypted text and passkey. You'll need both.")
                else:
                    st.error("Both fields are required.")

    elif choice == "Retrieve Data" and not st.session_state.failed_attempts >= 3:
        st.title("Retrieve Data")
        encrypted_input = st.text_area("Encrypted Data", height=100, placeholder="Paste encrypted text...")
        passkey_input = st.text_input("Passkey", type="password", help="Enter the same passkey used earlier.")
        if st.button("Decrypt", key="retrieve_btn"):
            if encrypted_input and passkey_input:
                with st.spinner("Decrypting..."):
                    time.sleep(1)
                    decrypted = decrypt_data(encrypted_input, passkey_input)
                    if decrypted:
                        st.success("Decryption successful.")
                        st.text_area("Decrypted Data", value=decrypted, height=150)
                    else:
                        st.error(f"Incorrect passkey. Attempts remaining: {3 - st.session_state.failed_attempts}")
                        if st.session_state.failed_attempts >= 3:
                            st.warning("Too many failed attempts. Access restricted.")
                            st.session_state.authenticated = False
                            time.sleep(2)
                            st.experimental_rerun()
            else:
                st.error("Both fields are required.")

    elif choice == "Login" or st.session_state.failed_attempts >= 3:
        st.title("Authentication Required")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=200)
        with col2:
            st.warning("You have exceeded the maximum allowed attempts.")
            admin_pass = st.text_input("Enter Admin Password", type="password")
            if st.button("Authenticate", key="auth_btn"):
                if admin_pass == "secureVault123":  # In production, manage securely
                    st.session_state.failed_attempts = 0
                    st.session_state.authenticated = True
                    st.success("Authenticated successfully.")
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.error("Incorrect admin password.")

    # Footer with glowing LinkedIn logo and "Made by Bilal Waseem"
    st.markdown("""
    <style>
    .footer {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        background-color: #333;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .linkedin-logo {
        margin-left: 10px;
        width: 30px;
        height: 30px;
        transition: transform 0.3s ease;
    }
    .linkedin-logo:hover {
        transform: scale(1.2);
        filter: drop-shadow(0 0 10px rgba(0, 0, 255, 0.7));
    }
    </style>
    <div class="footer">
        <span>Made by Bilal Waseem</span>
        <a href="https://www.linkedin.com/in/bilal-waseem-b44006338" target="_blank">
            <img class="linkedin-logo" src="https://upload.wikimedia.org/wikipedia/commons/0/01/LinkedIn_Logo_2023.png" alt="LinkedIn Logo"/>
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
