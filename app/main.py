import logging
import os
import time

import streamlit as st

from modules import MultiPage
from pages import summary, usage, ctr


####
# TL AWS Analytics with Streamlit
# This is a Single Page App.
# Every view is a page, under pages/
# A page will have reports on it, which is taken from modules.report_functions
# Reports use a pandas DataFrame, which is requested from module.model.get_dataframe
####


def main():
    app = MultiPage.MultiPage()
    config()

    # Set app to timezone set in TZ
    time.tzset()

    pages = [
        ("Summary", summary.app),
        ("Contact Flow Usage", usage.app),
        ("CTR Debugging", ctr.app)
    ]

    for page in pages:
        app.add_page(page[0], page[1])

    app.run()


def config():
    st.set_page_config(
        page_title=os.getenv('APP_NAME', "Set APP_NAME"),
        page_icon="T"
        # initial_sidebar_state = "collapsed",
    )


if __name__ == '__main__':
    loglevel = os.environ.get('LOGLEVEL', 'WARNING').upper()
    level = logging.getLevelName(loglevel)

    logger = logging.getLogger()
    logger.setLevel(level)

    # logger.info(logging.getLevelName(logger.getEffectiveLevel()))
    main()
