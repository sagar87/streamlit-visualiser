import streamlit as st

st.set_page_config(page_title="CODEX explorer", page_icon=":bar_chart:", layout="wide")

from auth import authenticator
from constants import CHANNELS, PANELS
from drive import get_file_list, read_file
from plot import overview_map, plain_img, plain_img_box

if "file_list" not in st.session_state:
    st.session_state["file_list"] = get_file_list()
if "current_file" not in st.session_state:
    st.session_state["current_file"] = st.session_state["file_list"][0]
if "name" not in st.session_state:
    st.session_state["name"] = None
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None


# authentication
name, authentication_status, username = authenticator.login("Login")
if authentication_status == False:
    st.error("Username/Password is incorrect.")

if authentication_status is None:
    st.warning("Please enter your username and password.")

if authentication_status:
    ds = read_file(st.session_state["current_file"])

    with st.sidebar:
        authenticator.logout("Logout")
        with st.form("image_view"):
            xmin, xmax = st.slider(
                "Select x-range:",
                value=[500, 1000],
                key="xrange",
                step=1,
                min_value=0,
                max_value=ds.dims["x"],
            )
            st.write("You are viewing ", xmax - xmin, "pixels along the x-axis.")

            ymin, ymax = st.slider(
                "Select y-range:",
                value=[500, 1000],
                key="yrange",
                step=1,
                min_value=0,
                max_value=ds.dims["y"],
            )
            st.write("You are viewing ", ymax - ymin, "pixels along the y axis.")

            fig = plain_img_box(ds, xmin, xmax, ymin, ymax)

            st.sidebar.pyplot(fig)

            current_panel = st.selectbox(
                "Select a pannel.",
                PANELS.keys(),
            )

            current_channels = st.multiselect(
                "Select the channels:",
                options=CHANNELS,
                default=PANELS[current_panel],
            )

            submitted = st.form_submit_button("Submit")

    st.header("CODEX Viewer")
    fig = plain_img(ds, current_channels, xmin, xmax, ymin, ymax)
    st.pyplot(fig)
