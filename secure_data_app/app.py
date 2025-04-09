import streamlit as st # type: ignore
from encryption import encrypt_data, decrypt_data
from auth import login, logout, is_logged_in
from utils import session_init
from streamlit_extras.stylable_container import stylable_container # type: ignore

st.set_page_config(
    page_title="Secure Data Encryption",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🔒"
)


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

session_init()

# Particle animation 
st.markdown("""
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
    "color": {"value": "#00bfff"},
    "shape": {"type": "circle", "stroke": {"width": 0, "color": "#000000"}},
    "opacity": {"value": 0.5, "random": false},
    "size": {"value": 3, "random": true},
    "line_linked": {"enable": true, "distance": 150, "color": "#00bfff", "opacity": 0.4, "width": 1},
    "move": {"enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out"}
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {"enable": true, "mode": "repulse"},
      "onclick": {"enable": true, "mode": "push"}
    }
  }
});
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="glow-header">Secure Data Encryption System</div>', unsafe_allow_html=True)

if not is_logged_in():
    login()
else:
    with stylable_container(
        key="main_container",
        css_styles="""
            {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                margin: 2rem 0;
                border: 1px solid rgba(0, 191, 255, 0.2);
                backdrop-filter: blur(10px);
                animation: fadeIn 0.5s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        """
    ):
        option = st.selectbox(
            "Choose an action",
            ["Store Data", "Retrieve Data", "Logout"],
            key="action_selector"
        )

        if option == "Store Data":
            st.subheader(" Encrypt & Store Data")
            with stylable_container(
                key="data_input",
                css_styles="""
                    textarea {
                        min-height: 150px !important;
                        transition: all 0.3s ease;
                    }
                    textarea:focus {
                        box-shadow: 0 0 0 2px #00bfff !important;
                    }
                """
            ):
                data = st.text_area("Enter your sensitive data here")
                passkey = st.text_input("Create a strong passkey", type="password", help="Remember this passkey - you'll need it to decrypt later")
                
                if st.button("Encrypt & Store", type="primary", use_container_width=True):
                    if data and passkey:
                        encrypted = encrypt_data(data, passkey)
                        st.session_state['secure_data'] = encrypted
                        st.balloons()
                        st.success("Data encrypted and stored securely! 🔐")
                    else:
                        st.warning("⚠️ Please fill both fields to proceed")

        elif option == "Retrieve Data":
            st.subheader("Retrieve & Decrypt Data")
            passkey = st.text_input("Enter your passkey", type="password", help="Enter the same passkey you used for encryption")
            
            if st.button("Decrypt & Show", type="primary", use_container_width=True):
                if st.session_state['failed_attempts'] >= 3:
                    st.error(" Too many failed attempts. Please login again.")
                    logout()
                    st.stop()
                
                encrypted = st.session_state.get('secure_data', None)
                if encrypted:
                    try:
                        decrypted = decrypt_data(encrypted, passkey)
                        with stylable_container(
                            key="decrypted_data",
                            css_styles="""
                                {
                                    background: #f0f9ff;
                                    border-radius: 10px;
                                    padding: 1rem;
                                    border-left: 4px solid #00bfff;
                                    font-family: monospace;
                                    white-space: pre-wrap;
                                    word-wrap: break-word;
                                }
                            """
                        ):
                            st.success(" Decryption successful!")
                            st.code(decrypted, language="text")
                        st.session_state['failed_attempts'] = 0
                    except:
                        st.session_state['failed_attempts'] += 1
                        st.error(" Incorrect passkey. Attempts: {}/3".format(st.session_state['failed_attempts']))
                else:
                    st.info("ℹ️ No encrypted data available to decrypt.")

        elif option == "Logout":
            st.warning("Are you sure you want to logout?")
            if st.button("Confirm Logout", type="primary"):
                logout()
                st.success(" Logged out successfully.")

st.markdown("""
<div class="footer">
    <p>Made by Bilal Waseem</p>
    <div class="social-links">
        <a href="#" class="social-icon">🌐</a>
        <a href="#" class="social-icon">💼</a>
        <a href="#" class="social-icon">🐱</a>
    </div>
</div>
""", unsafe_allow_html=True)