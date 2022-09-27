import matplotlib
import matplotlib.pyplot as plt
import spatial_data as sd
import streamlit as st
import xarray as xr

params = {"legend.fontsize": 5, "legend.handlelength": 2, "legend.markerscale": 0.4}
plt.rcParams.update(params)


@st.cache(
    hash_funcs={xr.core.dataset.Dataset: id, matplotlib.figure.Figure: lambda _: None},
    allow_output_mutation=True,
)
def overview_map(ds, xmin, xmax, ymin, ymax):
    fig, ax = plt.subplots()
    ds.pl.scatter(ax=ax).pl.add_box([xmin, xmax], [ymin, ymax], color="black")
    ax.axis("off")
    return fig


@st.cache(hash_funcs={xr.core.dataset.Dataset: id}, allow_output_mutation=True)
def plain_img_box(ds, xmin, xmax, ymin, ymax):
    fig, ax = plt.subplots()
    # _ = (
    #     ds.im['Hoechst']
    #     .im.colorize(colors=["C2", "C0", "C3", "C1", "C4", "C5", "C6", "C7"])
    #     .pl.add_box([xmin, xmax], [ymin, ymax], color="white")
    #     .pl.imshow(ax=ax)
    # )
    ax.vlines(xmin, ymin, ymax)
    ax.vlines(xmax, ymin, ymax)
    ax.hlines(ymin, xmin, xmax)
    ax.hlines(ymax, xmin, xmax)
    ax.set_xlim([0, ds.dims["x"]])
    ax.set_ylim([0, ds.dims["y"]])
    ax.axis("off")
    return fig


@st.cache(hash_funcs={xr.core.dataset.Dataset: id}, allow_output_mutation=True)
def plain_img(ds, channels, xmin, xmax, ymin, ymax):
    fig, ax = plt.subplots()
    _ = (
        ds.im[channels, xmin:xmax, ymin:ymax]
        .im.colorize(colors=["C2", "C0", "C3", "C1", "C4", "C5", "C6", "C7"])
        .pl.imshow(ax=ax, legend_background=True)
    )
    ax.axis("off")
    return fig
