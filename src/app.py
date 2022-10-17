import streamlit as st

st.set_page_config(page_title="CODEX Viewer", page_icon=":bar_chart:", layout="wide")

# from auth import authenticator
from constants import CELL2NUM, CELL_PANELS, CHANNEL_PANELS, NUM2CELL, filter_panel, META
from drive import get_thumnails_dict, get_zarr_dict, read_file, read_zarr
from plot import annot_img, plain_img_box

## SESSION STATE config
zarr_dict = get_zarr_dict()
thumbnails_dict = get_thumnails_dict()

# session state
if "xrange" not in st.session_state:
    st.session_state["xrange"] = [2000, 2500]
if "yrange" not in st.session_state:
    st.session_state["yrange"] = [2000, 2500]
if "file_list" not in st.session_state:
    st.session_state["file_list"] = list(zarr_dict.keys())

# load first file by default
if "file" not in st.session_state:
    st.session_state["file"] = st.session_state["file_list"][0]

file = st.session_state["file"]
ds = read_zarr(zarr_dict[file])
channels = ds.coords["channels"].values.tolist()
cells = ds["_labels"].values[:, 1].tolist()
thumb = read_file(thumbnails_dict[file])

if "panel" not in st.session_state:
    st.session_state["panel"] = "Hoechst"

panels = filter_panel(CHANNEL_PANELS, channels)

if "channel_selection" not in st.session_state:
    st.session_state["channel_selection"] = panels[st.session_state["panel"]]

channel_selection = st.session_state["channel_selection"]

if "cell" not in st.session_state:
    st.session_state["cell"] = "CD4+ T cells"

if "cell_selection" not in st.session_state:
    st.session_state["cell_selection"] = CELL_PANELS[st.session_state["cell"]]

if "override" not in st.session_state:
    st.session_state["override"] = False

if "alpha" not in st.session_state:
    st.session_state["alpha"] = 0.3

if "show" not in st.session_state:
    st.session_state["show"] = True

## INPUT VALIDATION
def validate_input():
    xmin_new, xmax_new = st.session_state["xrange"]
    if xmax_new - xmin_new > 2000:
        st.session_state["xrange"] = [xmin, xmax]
        st.warning("Please choose x-ranges < 2000 px. Falling back previous xrange.")

    ymin_new, ymax_new = st.session_state["yrange"]
    if ymax_new - ymin_new > 2000:
        st.session_state["yrange"] = [ymin, ymax]
        st.warning("Please choose x-ranges < 2000 px. Falling back previous xrange.")

    channel_selection = st.session_state["channel_selection"]
    if len(channel_selection) == 0:
        st.warning("Please select at least one channel.")
        st.session_state["channel_selection"] = ["Hoechst"]

    if len(channel_selection) >= 6:
        st.warning("More than 6 channels are currently not supported.")
        st.session_state["channel_selection"] = st.session_state["channel_selection"][
            :6
        ]
        
    # st.session_state['cell_selection'] = st.session_state['cell']


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

        st.write("You are viewing ", ymax - ymin, "pixels along the y-axis.")

        st.selectbox("Select a pannel.", CHANNEL_PANELS.keys(), key="panel")

        st.multiselect(
            "Select the channels:",
            options=channels,
            default=panels[st.session_state["panel"]],
            key="channel_selection",
        )
        
        "---"

        st.selectbox(
            "Select a cell panel:",
            options=list(CELL_PANELS.keys()),
            # default=st.session_state["cell"],
            key="cell",
        )

        st.multiselect(
            "Select cells:",
            options=cells,
            default=CELL_PANELS[st.session_state["cell"]],
            key="cell_selection",
        )
        
        st.slider(
            "Alpha",
            step=0.01,
            min_value=0.,
            max_value=1.,
            key="alpha",
        )
        
        left, right = st.columns(2)

        left.checkbox("Show cells", key="show")
        right.checkbox("Override color", key="override")
        # st.checkbox("Negative", key="negative")

        submitted = st.form_submit_button("Submit", on_click=validate_input)


channel_selection = st.session_state["channel_selection"]
cell_selection = st.session_state["cell_selection"]
show = st.session_state["show"]
override = st.session_state["override"]
alpha = st.session_state['alpha']
xmin, xmax = st.session_state["xrange"]
ymin, ymax = st.session_state["yrange"]


st.header("CODEX Viewer")

lcol, rcol = st.columns([8, 2])

with lcol:
    fig = annot_img(
        ds,
        channel_selection,
        show,
        [CELL2NUM[i] for i in cell_selection],
        xmin,
        xmax,
        ymin,
        ymax,
        override,
        alpha
    )
    st.pyplot(fig)

with rcol:
    st.write('## Instructions')
    st.write("""
             Select the region of interest using the sliders on the sidebar and the cells to visualise from the respective panel. 
             """)
    
    with st.expander("Samples"):
        
        
        st.dataframe(META) 