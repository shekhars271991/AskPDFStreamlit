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
    user_input = st.text_area("", placeholder="Type your query here...")

    # Display selected options (optional, can be removed if not needed)
    st.write(f"**Selected Options:** {'Shared Documents' if shared_docs_checkbox else ''} {'Private Documents' if private_docs_checkbox else ''}")
    st.write(f"**Cache Skipping:** {'Enabled' if skip_cache_checkbox else 'Disabled'}")

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
                response.raise_for_status()  # Raise an error for bad responses
                response_data = response.json()

                # Display the response
                st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
                st.subheader("Response")
                st.write(response_data.get('answer', 'No response from API.'))
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a message or query.")

if __name__ == "__main__":
    chat_page()
