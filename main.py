import boto3
import logging
import os

from modules import MultiPage
from pages import summary, flowusage
import streamlit as st

####
# TL AWS Analytics with Streamlit
# This is a Single Page App.
# Every view is a page, under pages/
# A page will have reports on it, which is taken from modules.report_functions
# Reports use a pandas DataFrame, which is requested from module.model.get_dataframe
####

loglevel = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=loglevel)

def main():
  app = MultiPage.MultiPage()
  config()

  pages = [
    ("Summary", summary.app),
    ("Flow and Menu Usage", flowusage.app),
  ]

  for page in pages:
    app.add_page(page[0], page[1])

  app.run()

def config():
  st.set_page_config(
    page_title            = "TL Analytics",
    initial_sidebar_state = "collapsed",
  )

if __name__ == '__main__':
  main()
