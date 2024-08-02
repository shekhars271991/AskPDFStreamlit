import streamlit as st

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
            st.success("Logged out successfully!")
            st.experimental_rerun()  # Redirect to login page
    else:
        # Login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Dummy authentication logic
            if username == "user" and password == "password":
                # Save login state
                st.session_state.logged_in = True
                st.session_state.user_name = username
                st.session_state.user_roles = ["Admin"]  # Example roles
                st.success("Login successful!")
                st.rerun()  # Redirect to main app
            else:
                st.error("Invalid username or password.")

# Example to display the login page
if __name__ == "__main__":
    login_page()
