import streamlit as st

class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self):
        self.pages = list()
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project

        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append({
                "title": title, 
                "function": func,
            })

    def run(self):
        # Dropdown to select the page to run
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda pages: pages['title']
        )

        # run the app function 
        page['function']()