import streamlit as st
from documents import documents_page
from chat import chat_page
from login import login_page

# Define the pages of the app
PAGES = {
    "Documents": documents_page,
    "Chat": chat_page
    # Add other pages here
}

def main():
    """Main function to run the Streamlit app."""
    
    # Check if the user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return

    # Display user info in the sidebar
    st.sidebar.title("Navigation")
    st.sidebar.write(f"**Logged in as:** {st.session_state.user_name}")
    st.sidebar.write(f"**Roles:** {', '.join(st.session_state.user_roles)}")
    
    # Add a logout option
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = None
        st.session_state.user_roles = None
        st.rerun()  # Redirect to login page

    # Navigation options
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
