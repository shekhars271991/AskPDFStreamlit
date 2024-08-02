import streamlit as st

def documents_page():
    """Display the documents page with a list of shared and private document icons."""
    st.title("Documents")

    # Example list of dummy documents with categories
    shared_docs = [
        {"name": "Shared Document 1", "icon": "📄"},
        {"name": "Shared Document 2", "icon": "📄"}
    ]

    private_docs = [
        {"name": "Private Document 1", "icon": "📄"},
        {"name": "Private Document 2", "icon": "📄"},
        {"name": "Private Document 3", "icon": "📄"}
    ]

    # Display Shared Documents
    st.subheader("Shared Documents")
    for doc in shared_docs:
        doc_name = doc["name"]
        doc_icon = doc["icon"]
        st.write(f"{doc_icon} {doc_name}")

    # Display Private Documents
    st.subheader("Private Documents")
    for doc in private_docs:
        doc_name = doc["name"]
        doc_icon = doc["icon"]
        st.write(f"{doc_icon} {doc_name}")
