import os

import s3fs
import streamlit as st
import xarray as xr
from dotenv import load_dotenv

load_dotenv(".env")

AWS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_KEY_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_URL = os.getenv("AWS_URL")
AWS_PATH = os.getenv("AWS_PATH")

fs = s3fs.S3FileSystem(anon=False, client_kwargs={"endpoint_url": AWS_URL})


@st.experimental_memo(ttl=3600)
def read_file(filename):
    print("loading file")
    store = s3fs.S3Map(root=filename, s3=fs, check=False)
    print("loading file")
    return xr.open_zarr(store=store, consolidated=True)


@st.experimental_memo(ttl=3600)
def get_file_list():
    return fs.ls(AWS_PATH)
