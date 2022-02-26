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

## Works, but we may not need it in favor of the singleton cache
# class S3Bucket(object):
#     _instance = None
#     _s3       = None
#     _bucket   = None
#     def __new__(cls):
#         if cls._instance is None:
#             print('Creating the object')
#             cls._instance = super(S3Bucket, cls).__new__(cls)
#             # Put any initialization here.
#             bucket_name = os.getenv("BUCKET_NAME")
#             cls._s3 = boto3.resource('s3')
#             cls._bucket = cls._s3.Bucket("demotlanalytics23526")

#         return cls._instance

#     def get_bucket(cls):
#         return cls._bucket
