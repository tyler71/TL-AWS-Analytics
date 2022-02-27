import logging
import os

import boto3
import streamlit as st

logger = logging.getLogger()


@st.experimental_singleton
def get_s3_bucket():
    logger.info("get_s3_bucket: singleton cached")
    bucket_name = os.getenv("BUCKET_NAME")

    logger.debug(f"get_s3_bucket: Loading s3 resource")
    s3 = get_s3_resource()

    logger.debug(f"get_s3_bucket: Loading bucket {bucket_name}")
    bucket = s3.Bucket(bucket_name)
    return bucket


@st.experimental_singleton
def get_s3_resource():
    logger.debug(f"get_s3_bucket: Loading s3 resource")
    s3 = boto3.resource('s3')
    return s3
