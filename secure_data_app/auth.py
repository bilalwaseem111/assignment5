import streamlit as st # type: ignore
from streamlit_extras.let_it_rain import rain # type: ignore


CREDENTIALS = {
    "bilalwaseem": "bilalbilal",
    "hello": "world",
    "bilalwaseemahmed": "bilal111"
}

def login():
    st.markdown("""
    <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        .login-container {
            animation: float 6s ease-in-out infinite;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.subheader(" Secure Login")
        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")

        if st.button("Login", type="primary"):
            if username in CREDENTIALS and CREDENTIALS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["failed_attempts"] = 0
                rain(
                    emoji="✨",
                    font_size=30,
                    falling_speed=5,
                    animation_length=1,
                )
                st.success("Login successful!")
                st.rerun()
            else:
                st.session_state["authenticated"] = False
                st.session_state["failed_attempts"] = st.session_state.get("failed_attempts", 0) + 1
                st.error("Invalid credentials")
                st.markdown("</div>", unsafe_allow_html=True)

def logout():
    st.session_state["authenticated"] = False
    st.rerun()

def is_logged_in():
    return st.session_state.get("authenticated", False)