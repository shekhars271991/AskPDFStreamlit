import streamlit as st
from documents import documents_page
from chat import chat_page

# Define the pages of the app
PAGES = {
    "Documents": documents_page,
    "Chat": chat_page
    # Add other pages here
}

def main():
    """Main function to run the Streamlit app."""
    # Dummy user data
    user_name = "John Doe"
    user_roles = ["Admin", "Editor"]

    # Display the user info in the sidebar
    st.sidebar.title("Navigation")
    st.sidebar.write(f"**Logged in as:** {user_name}")
    st.sidebar.write(f"**Roles:** {', '.join(user_roles)}")

    # Navigation options
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
