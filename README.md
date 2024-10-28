AskPDFStreamlit
===============

AskPDFStreamlit is a Streamlit application designed to help users interact with and query PDF documents using natural language processing and AI capabilities. The app allows users to upload PDF files, ask questions about the content, and receive accurate responses based on the document's contents. It leverages various AI tools and integrations to provide an interactive document management experience.

Backend
--------

Backend of this app can be found at: https://github.com/shekhars271991/AskPDFApp

Features
--------

-   **PDF Upload**: Easily upload PDF files for querying.
-   **Natural Language Querying**: Ask questions in natural language and get responses based on document content.
-   **Document Management**: View, download, and manage uploaded documents within the app.
-   **Role-Based Access**: Use JWT-based roles to control access and visibility of specific UI elements.
-   **Session State Storage**: Save API responses and document data within sessions for easy access across pages.

Getting Started
---------------

### Prerequisites

To run this project, you'll need:

-   **Python** 3.8+

-   **Streamlit** library

-   **Redis** (optional, if you want to enable backend caching or user management)

-   **Requirements**: Install all dependencies with the following command:

    bash

    Copy code

    `pip install -r requirements.txt`

### Installation

1.  Clone the repository:

    bash

    Copy code

    `git clone https://github.com/shekhars271991/AskPDFStreamlit.git
    cd AskPDFStreamlit`

2.  Install dependencies:

    bash

    Copy code

    `pip install -r requirements.txt`

3.  Start the Streamlit app:

    bash

    Copy code

    `streamlit run app.py`

### Configuration

To configure JWT and Redis (if applicable), update the `config.py` file with your credentials and settings.

Usage
-----

1.  **Upload PDFs**: Navigate to the upload page and select your PDF files.
2.  **Ask Questions**: On the main page, type questions related to the PDF content and view responses.
3.  **View and Manage Documents**: Access uploaded documents, view contents, or download files.

Project Structure
-----------------

-   `app.py`: The main Streamlit app.
-   `config.py`: Configurations for JWT, Redis, and app settings.
-   `services/`: Contains helper services for PDF processing, Redis interaction, and authentication.
-   `pages/`: Individual Streamlit pages for different parts of the app.

License
-------

This project is licensed under the MIT License. See LICENSE for more information.

Contributing
------------

1.  Fork the repository.
2.  Create a new branch.
3.  Make your changes and submit a pull request.

* * * * *

This README should provide a solid introduction and guide users on installation and usage. Let me know if you'd like to customize any sections further.
