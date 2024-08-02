import streamlit as st

def documents_page():
    """Display the documents page with a list of shared and private document icons and upload functionality."""
    # st.title("Documents")

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

    # Layout for displaying documents side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shared Documents")
        for doc in shared_docs:
            doc_name = doc["name"]
            doc_icon = doc["icon"]
            st.write(f"{doc_icon} {doc_name}")

    with col2:
        st.subheader("Private Documents")
        for doc in private_docs:
            doc_name = doc["name"]
            doc_icon = doc["icon"]
            st.write(f"{doc_icon} {doc_name}")

    # Horizontal separator
    st.markdown("---")

    # Upload Section
    st.subheader("Upload a Document")
    st.markdown("### Upload Document")
        
    # File uploader (only PDF supported)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
        
    # Select roles (example roles)
    roles = ["Admin", "Editor", "Viewer"]
    selected_roles = st.multiselect("Assign Roles", roles)
        
    # Submit and Cancel buttons
    if st.button("Submit"):
        if uploaded_file is not None and selected_roles:
            # Process the file and roles here
            st.success(f"File '{uploaded_file.name}' uploaded successfully with roles: {', '.join(selected_roles)}")
            # You can add logic to save the file and roles information
        else:
            st.error("Please select a file and assign at least one role.")
        
    if st.button("Cancel"):
        # Clear the file uploader and role selection (simulating form reset)
        st.caching.clear_cache()
        st.experimental_rerun()

# Example to display the documents page
if __name__ == "__main__":
    documents_page()
