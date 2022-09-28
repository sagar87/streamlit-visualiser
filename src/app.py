import streamlit as st

st.set_page_config(page_title="CODEX explorer", page_icon=":bar_chart:", layout="wide")

# from auth import authenticator
from constants import CHANNELS, PANELS
from drive import get_thumnails_dict, get_zarr_dict, read_file, read_zarr
from plot import plain_img, plain_img_box

zarr_dict = get_zarr_dict()
thumbnails_dict = get_thumnails_dict()

if "xrange" not in st.session_state:
    st.session_state["xrange"] = [500, 1000]
if "yrange" not in st.session_state:
    st.session_state["yrange"] = [500, 1000]
if "file_list" not in st.session_state:
    st.session_state["file_list"] = list(zarr_dict.keys())
if "file" not in st.session_state:
    st.session_state["file"] = st.session_state["file_list"][0]
if "panel" not in st.session_state:
    st.session_state["panel"] = "Hoechst"
if "selection" not in st.session_state:
    st.session_state["selection"] = PANELS[st.session_state["panel"]]


# authentication
# name, authentication_status, username = authenticator.login("Login")
# if authentication_status == False:
#     st.error("Username/Password is incorrect.")

# if authentication_status is None:
#     st.warning("Please enter your username and password.")

# if authentication_status:
file = st.session_state["file"]
selection = st.session_state["selection"]

ds = read_zarr(zarr_dict[file])
thumb = read_file(thumbnails_dict[file])

with st.sidebar:
    # authenticator.logout("Logout")
    xmin, xmax = st.session_state["xrange"]
    ymin, ymax = st.session_state["yrange"]

    fig = plain_img_box(thumb, xmin, xmax, ymin, ymax, ds.dims["x"], ds.dims["y"])
    st.sidebar.pyplot(fig)

    with st.form("image_view"):
        st.selectbox("Select sample.", st.session_state["file_list"], key="file")

        st.slider(
            "Select x-range:",
            value=[500, 1000],
            step=1,
            min_value=0,
            max_value=ds.dims["x"],
            key="xrange",
        )
        st.write("You are viewing ", xmax - xmin, "pixels along the x-axis.")

        st.slider(
            "Select y-range:",
            value=[500, 1000],
            step=1,
            min_value=0,
            max_value=ds.dims["y"],
            key="yrange",
        )

        st.write("You are viewing ", ymax - ymin, "pixels along the y axis.")

        st.selectbox("Select a pannel.", PANELS.keys(), key="panel")

        st.multiselect(
            "Select the channels:",
            options=CHANNELS,
            default=PANELS[st.session_state["panel"]],
            key="selection",
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            selection = st.session_state["selection"]
            xmin, xmax = st.session_state["xrange"]
            ymin, ymax = st.session_state["yrange"]


st.header("CODEX Viewer")
fig = plain_img(ds, selection, xmin, xmax, ymin, ymax)
st.pyplot(fig)
