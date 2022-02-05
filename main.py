import s3fs
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
<<<<<<< HEAD
    # initial_sidebar_state="collapsed"
=======
    initial_sidebar_state="collapsed"
>>>>>>> 29d64693ca486691cdc17f4bc939bc5ccb68c5a5
  )

if __name__ == '__main__':
  main()
