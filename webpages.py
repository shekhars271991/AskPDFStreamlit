import streamlit as st
import requests

# Constants
ITEMS_PER_PAGE = 10

def url_indexing_page():
    """Display the URL Indexing page with input for URL, depth selection, and result sections."""
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>URL Indexing</h2>", unsafe_allow_html=True)

    # Ensure the user is logged in before accessing the page
    if not st.session_state.get('logged_in', False):
        st.warning("You need to be logged in to view this page.")
        st.button("Go to Login Page", on_click=lambda: st.rerun())
        return

    # Initialize session state if not already
    st.session_state.setdefault('urls_enqueued', [])
    st.session_state.setdefault('urls_unreachable', [])
    st.session_state.setdefault('indexing_in_progress', False)
    st.session_state.setdefault('indexed_urls', [])
    st.session_state.setdefault('current_page', 1)
    st.session_state.setdefault('show_results', False)  # Control visibility of results

    # API details
    enqueue_url = "http://127.0.0.1:5000/api/index_webpage"
    webpages_url = "http://127.0.0.1:5000/api/webpages"
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    # URL Input Section
    st.subheader("Provide URL for Indexing")
    input_url = st.text_input("Enter the URL to index:")
    depth = st.selectbox("Select Depth (0, 1, or 2):", options=[0, 1, 2])
    max_urls = st.number_input("Max URLs to Import", min_value=1, step=1, value=10)

    # Submit button
    if st.button("Submit", disabled=st.session_state.indexing_in_progress):
        if input_url:
            st.session_state.indexing_in_progress = True
            st.session_state.show_results = True  # Show results when the user submits
            st.session_state.current_page = 1  # Reset to the first page on new submission

            # Prepare data for API request
            data = {
                'url': input_url,
                'level': depth,
                'maxcount': max_urls,
                'allowed_domains': [],  # Assuming you might have some domain restriction logic
            }

            try:
                response = requests.post(enqueue_url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                
                st.session_state.urls_enqueued = result.get("enqued_for_indexing", [])
                st.session_state.urls_unreachable = result.get("unreachable_urls", [])

                st.success("URL processing completed. Check the results below.")
                st.session_state.indexing_in_progress = False
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to enqueue URL: {e}")
                st.session_state.indexing_in_progress = False
        else:
            st.error("Please enter a valid URL.")

    # Display the enqueued and unreachable URLs only if results are available
    if st.session_state.show_results and (st.session_state.urls_enqueued or st.session_state.urls_unreachable):
        st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
        st.subheader("URL Indexing Results")
        
        with st.expander("Enqueued URLs"):
            if st.session_state.urls_enqueued:
                for url in st.session_state.urls_enqueued:
                    st.write(url)
            else:
                st.info("No URLs were enqueued.")

        with st.expander("Unreachable URLs"):
            if st.session_state.urls_unreachable:
                for url in st.session_state.urls_unreachable:
                    st.write(url)
            else:
                st.info("No URLs were unreachable.")

    # Fetch and display indexed URLs with pagination
    if not st.session_state.indexed_urls:
        try:
            response = requests.get(webpages_url, headers=headers)
            response.raise_for_status()
            st.session_state.indexed_urls = response.json().get('indexed_webpages', [])
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch indexed webpages: {e}")

    # Always show Indexed URLs section
    if st.session_state.indexed_urls:
        st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)
        st.subheader("Indexed URLs")
        
        # Pagination variables
        total_pages = (len(st.session_state.indexed_urls) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        current_page = st.session_state.current_page

        # Display current page of indexed URLs
        start_index = (current_page - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        paginated_urls = st.session_state.indexed_urls[start_index:end_index]

        for webpage in paginated_urls:
            with st.expander(f"{webpage['webpage_title']} ({webpage['unique_title']})"):
                st.write(webpage['summary'])

        # Pagination controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_page > 1:
                if st.button("Previous"):
                    st.session_state.current_page -= 1
                    st.rerun()
        with col2:
            st.write(f"Page {current_page} of {total_pages}")
        with col3:
            if current_page < total_pages:
                if st.button("Next"):
                    st.session_state.current_page += 1
                    st.rerun()

    # Reset the results section if the user navigates away or reloads the page
    if not input_url:
        st.session_state.show_results = False

if __name__ == "__main__":
    url_indexing_page()
