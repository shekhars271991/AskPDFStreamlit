import streamlit as st
import requests

def login_page():
    """Display the login page."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Login</h2>", unsafe_allow_html=True)

    # Check if the user is already logged in
    if st.session_state.get('logged_in', False):
        st.info(f"Already logged in as **{st.session_state.get('user_name', 'User')}**.")
        
        # Logout button with a confirmation dialog
        if st.button("Logout", key="logout_button", type="primary"):
            st.session_state.clear()  # Clear session state on logout
            st.success("Logged out successfully!")
            st.experimental_rerun()
    else:
        # Login form container
        with st.form(key='login_form'):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_button = st.form_submit_button("Login", type="primary")

        # Perform login if the login button is clicked
        if login_button:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                # API login request
                login_url = "http://127.0.0.1:5000/auth/login"
                payload = {"username": username, "password": password}
                try:
                    response = requests.post(login_url, json=payload)
                    response.raise_for_status()  # Raise an error for bad responses
                    data = response.json()
                    access_token = data.get("access_token")
                    roles = data.get("roles", [])

                    if access_token:
                        # Save login state
                        st.session_state.logged_in = True
                        st.session_state.user_name = username
                        st.session_state.user_roles = roles 
                        st.session_state.access_token = access_token
                        st.success("Login successful!")
                        st.experimental_rerun()  # Redirect to the main app
                    else:
                        st.error("Login failed. No access token received.")
                except requests.RequestException as e:
                    st.error(f"Login failed: {e}")

if __name__ == "__main__":
    login_page()
