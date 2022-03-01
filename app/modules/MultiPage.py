import itertools
import os

import streamlit as st
from modules.helper import sha


class MultiPage:
    """Framework for combining multiple streamlit applications."""

    def __init__(self):
        self.pages = list()

        # Each widget must have its own id.
        # To make sure each widget is unique, we request the next one
        # from the below generator
        st.session_state['widget_id'] = itertools.count()

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
        st.sidebar.header(os.getenv('APP_NAME', 'Set APP_NAME'))
        st.sidebar.markdown(body=sha())

        page = st.sidebar.radio(
            'Go to',
            self.pages,
            format_func=lambda pages: pages['title']
        )

        st.sidebar.markdown('---')

        st.session_state['historical'] = st.sidebar.checkbox('Historical')
        st.session_state['show_download'] = st.sidebar.checkbox('Show Download')
      
        # run the app function 
        page['function']()
