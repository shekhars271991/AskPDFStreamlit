import streamlit as st
from documents import documents_page
from chat import chat_page
from login import login_page
from webpages import url_indexing_page

# Define the pages of the app
PAGES = {
    "Documents": documents_page,
    "Webpages": url_indexing_page,
    "Chat": chat_page,

    # Add other pages here
}

def main():
    """Main function to run the Streamlit app."""
    
    # Ensure the user is logged in before accessing any page
    if not st.session_state.get('logged_in', False):
        login_page()
        return

    # Sidebar navigation and user information display
    with st.sidebar:
        st.title("Navigation")
        st.write(f"**Logged in as:** {st.session_state.get('user_name', 'Guest')}")
        st.write(f"**Roles:** {', '.join(st.session_state.get('user_roles', []))}")
        
        # Logout button
        if st.button("Logout"):
            # Clear session state for logout
            st.session_state.clear()
            st.rerun()  # Redirect to login page after logout

        # Navigation options
        selection = st.radio("Go to", list(PAGES.keys()))

    # Display the selected page's content
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
