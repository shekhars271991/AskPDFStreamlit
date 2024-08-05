import streamlit as st
import requests

def chat_page():
    """Display the chat page for interacting with documents."""
    st.title("Chat with Documents")

    # Chat with Documents Section
    st.subheader("Chat with Documents")

    # Checkboxes to select document types
    shared_docs_checkbox = st.checkbox("Include Shared Documents", value=True)
    private_docs_checkbox = st.checkbox("Include Private Documents", value=True)
    skip_cache_checkbox = st.checkbox("Skip Cache", value=False)  # Checkbox to skip cache

    # Text area for user input
    user_input = st.text_area("Enter your message or query here:", "")
    
    # Display selected options
    st.write(f"Selected Options: {'Shared Documents' if shared_docs_checkbox else ''} {'Private Documents' if private_docs_checkbox else ''}")
    st.write(f"Cache Skipping: {'Enabled' if skip_cache_checkbox else 'Disabled'}")

    if st.button("Send"):
        if user_input:

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
                response_data = response.json()

                # Display the response
                # if response_data.get('relatedDocs'):
                #     st.write(f"Related documents: {response_data.get('relatedDocs')}")
                st.write(f"Response: {response_data.get('answer', 'No response from API.')}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a message or query.")
