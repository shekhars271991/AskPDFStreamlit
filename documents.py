import streamlit as st
import requests

def documents_page():
    """Display the documents page with a list of shared and private document icons and upload functionality."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Documents</h2>", unsafe_allow_html=True)

    # Ensure the user is logged in before accessing the page
    if not st.session_state.get('logged_in', False):
        st.warning("You need to be logged in to view this page.")
        st.button("Go to Login Page", on_click=lambda: st.rerun())
        return

    # Initialize session state if not already
    st.session_state.setdefault('selected_summary', None)
    st.session_state.setdefault('selected_doc', None)
    st.session_state.setdefault('upload_in_progress', False)

    # API details
    api_url = "http://127.0.0.1:5000/api/documents"
    upload_url = "http://127.0.0.1:5000/api/upload"
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    # Fetch documents from API
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        documents = response.json().get("documents", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch documents: {e}")
        documents = []

    # Separate documents into shared and private
    shared_docs = [doc for doc in documents if st.session_state.user_name not in doc["roles"]]
    private_docs = [doc for doc in documents if st.session_state.user_name in doc["roles"]]

    # Layout for displaying documents side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Shared Documents")
        for doc in shared_docs:
            display_document(doc, key_prefix="shared")

    with col2:
        st.subheader("Private Documents")
        for doc in private_docs:
            display_document(doc, key_prefix="private")

    # Display the selected summary section above the upload section
    st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
    st.subheader("Document Summary")
    if st.session_state.selected_summary:
        st.write(f"**{st.session_state.selected_doc}**")
        st.write(st.session_state.selected_summary)
    else:
        st.info("Select a document to see the summary.")

    # Horizontal separator
    st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)

    # Upload Section
    st.subheader("Upload a Document")
    upload_document_section(upload_url, headers)


def display_document(doc, key_prefix):
    """Helper function to display a document with an icon and clickable summary."""
    doc_name = doc["doc_name"]
    doc_summary = doc["summary"]
    doc_id = doc.get("id", "unknown")

    # Create two columns for icon and text
    icon_col, text_col = st.columns([1, 4])
    with icon_col:
        st.image("pdf_icon.png", width=30)
    with text_col:
        # Clickable text for showing summary
        if st.button(f"{doc_name}", key=f"{key_prefix}_show_summary_{doc_id}"):
            st.session_state.selected_doc = doc_name
            st.session_state.selected_summary = doc_summary


def upload_document_section(upload_url, headers):
    """Helper function to handle document upload with roles selection."""
    # File uploader (only PDF supported)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    # Select roles (example roles)
    roles = ["admin", "partner", "user", "staff", "private"]
    if "admin" in st.session_state.user_roles:
        selected_roles = st.multiselect("Assign Roles", roles)
        if "private" in selected_roles:
            selected_roles = [st.session_state.user_name]
    else:
        selected_roles = [st.session_state.user_name]

    # Submit and Cancel buttons
    if st.button("Submit", disabled=st.session_state.upload_in_progress):
        if uploaded_file and selected_roles:
            st.session_state.upload_in_progress = True

            # Prepare file and roles for API request
            files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
            data = {'roles': ','.join(selected_roles)}

            try:
                response = requests.post(upload_url, headers=headers, files=files, data=data)
                response.raise_for_status()
                st.success(f"File '{uploaded_file.name}' queued for upload with  roles: {', '.join(selected_roles)}")
                # Reset the form
                st.session_state.upload_in_progress = False
                st.session_state.selected_roles = []
                st.session_state.uploaded_file = None
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to upload file: {e}")
                st.session_state.upload_in_progress = False
        else:
            st.error("Please select a file and assign at least one role.")


if __name__ == "__main__":
    documents_page()
