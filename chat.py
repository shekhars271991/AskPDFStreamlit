import streamlit as st
import requests

def chat_page():
    """Display the chat page for interacting with documents."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Chat with Documents</h2>", unsafe_allow_html=True)

    # Chat with Documents Section
    st.subheader("Interaction Settings")

    # Checkboxes to select document types
    col1, col2 = st.columns(2)
    with col1:
        shared_docs_checkbox = st.checkbox("Include Shared Documents", value=True)
    with col2:
        private_docs_checkbox = st.checkbox("Include Private Documents", value=True)
    
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
                "query": user_input
            }

            # Set skip_cache in the query parameters based on the checkbox state
            skip_cache = "yes" if skip_cache_checkbox else "no"
            api_url = f"http://127.0.0.1:5000/api/ask?skip_cache={skip_cache}"

            # Make the API request
            try:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                response_data = response.json()

                # Display related documents if any
                related_docs = response_data.get('relatedDocs', [])
                if related_docs:
                    st.subheader("Related Documents")
                    for doc_id, roles in related_docs:
                        doc_name, doc_summary = get_document_details(doc_id)
                        if doc_name:
                            display_document_in_chat(doc_name, doc_summary)
                        else:
                            st.write(f"- Unknown Document (Roles: {', '.join(roles)})")

                # Display the response
                st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
                st.subheader("Response")
                st.write(response_data.get('answer', 'No response from API.'))

                
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a message or query.")


def get_document_details(doc_id):
    """Helper function to get document name and summary based on doc_id."""
    for doc in st.session_state.get('documents', []):
        if doc["id"] == f"file_{doc_id}_metadata":
            return doc["doc_name"], doc["summary"]
    return None, None


def display_document_in_chat(doc_name, doc_summary):
    """Helper function to display a document with clickable summary in chat."""
    with st.expander(doc_name):
        st.write(f"**Summary for {doc_name}:**")
        st.write(doc_summary)


if __name__ == "__main__":
    chat_page()
