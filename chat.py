import streamlit as st
import requests

def chat_page():
    """Display the chat page for interacting with documents and webpages."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Chat with Documents</h2>", unsafe_allow_html=True)

    # Load indexed webpages into session state if not already loaded
    if 'indexed_webpages' not in st.session_state:
        load_indexed_webpages()

    # Chat with Documents Section
    st.subheader("Interaction Settings")

    # Checkboxes to select document types
    doc_types = []
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Include Files", value=True):
            doc_types.append("files")
    with col2:
        if st.checkbox("Include Webpages", value=True):
            doc_types.append("webpages")
    
    skip_cache_checkbox = st.checkbox("Skip Cache", value=False)  # Checkbox to skip cache

    # Text area for user input
    st.markdown("<h4 style='margin-top: 30px;'>Enter your message or query:</h4>", unsafe_allow_html=True)
    user_input = st.text_area("Your query", placeholder="Type your query here...", label_visibility="hidden")

    # Send button with conditional input check
    if st.button("Send", type="primary"):
        if user_input.strip():
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {st.session_state.access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "query": user_input,
                "doc_types": doc_types  # Add selected document types to the payload
            }

            # Set skip_cache in the query parameters based on the checkbox state
            skip_cache = "yes" if skip_cache_checkbox else "no"
            api_url = f"http://127.0.0.1:5000/api/ask?skip_cache={skip_cache}"

            # Make the API request
            try:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                response_data = response.json()

            
                # st.json(response_data) # Uncomment this line if you need to see the full API response

                # Check if the response came from cache
                from_cache = response_data.get("fromCache", False)

                # Display a cache indicator if the response is from cache
                if from_cache:
                    st.info("This response is from cache. Check the Skip Cache checkbox to search deeper.")

                # Display the related documents, webpages, and response
                display_response(response_data)
                display_related_documents(response_data)
                display_related_webpages(response_data)
                

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a message or query.")

def load_indexed_webpages():
    """Load indexed webpages into session state."""
    try:
        # Assuming there's an API endpoint to fetch all indexed webpages
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}"
        }
        api_url = "http://127.0.0.1:5000/api/webpages"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        st.session_state['indexed_webpages'] = response.json().get('indexed_webpages', [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load indexed webpages: {e}")
        st.session_state['indexed_webpages'] = []


def display_related_documents(response_data):
    """Helper function to display related documents."""
    related_docs = response_data.get('relatedDocs', [])
    if related_docs:
        st.subheader("Related Documents")
        for doc in related_docs:
            doc_name = doc.get("filename", "Unknown Document")
            doc_roles = doc.get("roles", "")
            # Split the roles string into a list
            doc_roles_list = doc_roles.split(", ") if doc_roles else []
            display_document_in_chat(doc_name, doc_roles_list)

def display_related_webpages(response_data):
    """Helper function to display related webpages."""
    related_webpages = response_data.get('relatedWebpages', [])
    if related_webpages:
        st.subheader("Related Webpages")
        for webpage in related_webpages:
            webpage_title = webpage.get("title", "Unknown Webpage")
            webpage_roles = webpage.get("roles", "")
            # Split the roles string into a list
            webpage_roles_list = webpage_roles.split(", ") if webpage_roles else []
            display_webpage_in_chat(webpage_title, webpage_roles_list)

def display_document_in_chat(doc_name, doc_roles):
    """Helper function to display a document with roles in chat."""
    if "Unknown Document" in doc_name:  # If summary is missing, show as list
        st.write(f"- {doc_name} (Roles: {', '.join(doc_roles)})")
    else:
        with st.expander(doc_name):
            st.write(f"**Roles:** {', '.join(doc_roles)}")

def display_webpage_in_chat(webpage_title, webpage_roles):
    """Helper function to display a webpage with roles in chat."""
    if "Unknown Webpage" in webpage_title:  # If summary is missing, show as list
        st.write(f"- {webpage_title} (Roles: {', '.join(webpage_roles)})")
    else:
        with st.expander(webpage_title):
            st.write(f"**Roles:** {', '.join(webpage_roles)}")


def display_response(response_data):
    """Helper function to display the response from the chat API."""
    st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
    st.subheader("Response")
    with st.expander("AI Response", expanded=True):  # Small container that expands on click
        st.write(response_data.get('answer', 'No response from API.'))

if __name__ == "__main__":
    chat_page()
