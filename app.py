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
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page
    page = PAGES[selection]
    page()

if __name__ == "__main__":
    main()
