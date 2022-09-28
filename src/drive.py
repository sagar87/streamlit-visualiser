import os
from io import BytesIO

import numpy as np
import s3fs
import streamlit as st
import xarray as xr
from dotenv import load_dotenv
from PIL import Image

load_dotenv(".env")

AWS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_KEY_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_URL = os.getenv("AWS_URL")
AWS_PATH = os.getenv("AWS_PATH")

fs = s3fs.S3FileSystem(anon=False, client_kwargs={"endpoint_url": AWS_URL})


@st.experimental_memo(ttl=3600)
def read_zarr(filename):
    store = s3fs.S3Map(root=filename, s3=fs, check=False)
    return xr.open_zarr(store=store, consolidated=True)


@st.experimental_memo(ttl=3600)
def read_file(filename):
    with fs.open(filename, "rb") as f:
        return np.array(Image.open(BytesIO(f.read())))  # Image.open(f)
    # return Image.open(fs.open(filename,"rb"))


@st.experimental_memo(ttl=3600)
def get_zarr_dict():
    file_dict = {
        f.split("/")[-1].split(".")[0]: f
        for f in fs.ls(AWS_PATH)
        if f.endswith(".zarr")
    }
    return file_dict


@st.experimental_memo(ttl=3600)
def get_thumnails_dict():
    file_dict = {
        f.split("/")[-1].split(".")[0]: f
        for f in fs.ls(os.path.join(AWS_PATH, "thumbnails"))
        if f.endswith(".png")
    }
    return file_dict
