import boto3
import os

from modules import MultiPage
from pages import summary, flowusage
import streamlit as st

def main():
  # fs = s3fs.S3FileSystem(anon=False)
  # print(fs.ls("demotlanalytics23526"))
  # with fs.open("demotlanalytics23526/output(3).json") as f:
  #   print(f.read())

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
    page_title="TL Analytics",
    initial_sidebar_state="collapsed"
  )

if __name__ == '__main__':
  main()
