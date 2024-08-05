import streamlit as st
import requests

def login_page():
    """Display the login page."""
    st.title("Login")

    # Check if the user is already logged in
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.write(f"Already logged in as **{st.session_state.user_name}**.")
        if st.button("Logout"):
            # Clear session state
            st.session_state.logged_in = False
            st.session_state.user_name = None
            st.session_state.user_roles = None
            st.session_state.access_token = None
            st.success("Logged out successfully!")
            st.experimental_rerun()  # Redirect to login page
    else:
        # Login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
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
                    st.rerun()  # Redirect to main app
                else:
                    st.error("Login failed. No access token received.")
            except requests.RequestException as e:
                st.error(f"Login failed: {e}")

# Example to display the login page
if __name__ == "__main__":
    login_page()
