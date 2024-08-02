import streamlit as st

def documents_page():
    """Display the documents page with a list of shared and private document icons and upload functionality."""
    st.title("Documents")

    # Example list of dummy documents with categories and summaries
    shared_docs = [
        {"name": "Shared Document 1", "icon": "pdf_icon.png", "summary": "Summary of Shared Document 1."},
        {"name": "Shared Document 2", "icon": "pdf_icon.png", "summary": "Summary of Shared Document 2."}
    ]

    private_docs = [
        {"name": "Private Document 1", "icon": "pdf_icon.png", "summary": "Summary of Private Document 1."},
        {"name": "Private Document 2", "icon": "pdf_icon.png", "summary": "Summary of Private Document 2."},
        {"name": "Private Document 3", "icon": "pdf_icon.png", "summary": "Summary of Private Document 3."}
    ]

    # Initialize session state if not already
    if 'selected_summary' not in st.session_state:
        st.session_state.selected_summary = None
        st.session_state.selected_doc = None

    # Layout for displaying documents side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shared Documents")
        for doc in shared_docs:
            doc_name = doc["name"]
            doc_icon = doc["icon"]
            doc_summary = doc["summary"]
            # Create two columns for icon and text
            icon_col, text_col = st.columns([1, 4])
            with icon_col:
                st.image(doc_icon, width=30)
            with text_col:
                # Clickable text for showing summary
                if st.button(f"{doc_name}", key=f"show_summary_shared_{doc_name}"):
                    st.session_state.selected_doc = doc_name
                    st.session_state.selected_summary = doc_summary

    with col2:
        st.subheader("Private Documents")
        for doc in private_docs:
            doc_name = doc["name"]
            doc_icon = doc["icon"]
            doc_summary = doc["summary"]
            # Create two columns for icon and text
            icon_col, text_col = st.columns([1, 4])
            with icon_col:
                st.image(doc_icon, width=30)
            with text_col:
                # Clickable text for showing summary
                if st.button(f"{doc_name}", key=f"show_summary_private_{doc_name}"):
                    st.session_state.selected_doc = doc_name
                    st.session_state.selected_summary = doc_summary

    # Display the selected summary section above the upload section
    st.subheader("Document Summary")
    if st.session_state.selected_summary:
        st.write(f"**{st.session_state.selected_doc}**")
        st.write(st.session_state.selected_summary)
    else:
        st.write("Select a document to see the summary.")

    # Horizontal separator
    st.markdown("---")

    # Upload Section
    st.subheader("Upload a Document")
        
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


# Example to display the documents page
if __name__ == "__main__":
    documents_page()
