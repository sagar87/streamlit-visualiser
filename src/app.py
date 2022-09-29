import streamlit as st

st.set_page_config(page_title="CODEX Viewer", page_icon=":bar_chart:", layout="wide")

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

file = st.session_state["file"]
selection = st.session_state["selection"]

ds = read_zarr(zarr_dict[file])
thumb = read_file(thumbnails_dict[file])


def validate_input():
    xmin_new, xmax_new = st.session_state["xrange"]
    if xmax_new - xmin_new > 2000:
        st.session_state["xrange"] = [xmin, xmax]
        st.warning("Please choose x-ranges < 2000 px. Falling back previous xrange.")

    ymin_new, ymax_new = st.session_state["yrange"]
    if ymax_new - ymin_new > 2000:
        st.session_state["yrange"] = [ymin, ymax]
        st.warning("Please choose x-ranges < 2000 px. Falling back previous xrange.")

    selection = st.session_state["selection"]
    if len(selection) == 0:
        st.warning("Please select at least one channel.")
        st.session_state["selection"] = ["Hoechst"]

    if len(selection) >= 6:
        st.warning("More than 6 channels are currently not supported.")
        st.session_state["selection"] = st.session_state["selection"][:6]


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
            step=1,
            min_value=0,
            max_value=ds.dims["x"],
            key="xrange",
        )
        st.write("You are viewing ", xmax - xmin, "pixels along the x-axis.")

        st.slider(
            "Select y-range:",
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

        submitted = st.form_submit_button("Submit", on_click=validate_input)


selection = st.session_state["selection"]
xmin, xmax = st.session_state["xrange"]
ymin, ymax = st.session_state["yrange"]

st.header("CODEX Viewer")
fig = plain_img(ds, selection, xmin, xmax, ymin, ymax)
st.pyplot(fig)
