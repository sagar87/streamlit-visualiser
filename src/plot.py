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
def plain_img_box(thumbnail, xmin, xmax, ymin, ymax, xdim, ydim):
    fig, ax = plt.subplots()
    # _ = (
    #     ds.im['Hoechst']
    #     .im.colorize(colors=["C2", "C0", "C3", "C1", "C4", "C5", "C6", "C7"])
    #     .pl.add_box([xmin, xmax], [ymin, ymax], color="white")
    #     .pl.imshow(ax=ax)
    # )
    ax.imshow(thumbnail, extent=[0, xdim, 0, ydim])
    ax.vlines(xmin, ymin, ymax, color="k")
    ax.vlines(xmax, ymin, ymax, color="k")
    ax.hlines(ymin, xmin, xmax, color="k")
    ax.hlines(ymax, xmin, xmax, color="k")

    ax.axhline(ymax, color="k", linestyle="--")
    ax.axhline(ymin, color="k", linestyle="--")
    ax.axvline(xmax, color="k", linestyle="--")
    ax.axvline(xmin, color="k", linestyle="--")
    ax.text(
        xmin - 100,
        ydim / 100 * 5,
        s=f"{xmin}",
        fontsize=16,
        color="k",
        va="bottom",
        ha="right",
    )
    ax.text(
        xmax + 100,
        ydim - (ydim / 100 * 5),
        s=f"{xmax}",
        fontsize=16,
        color="k",
        va="top",
        ha="left",
    )
    ax.text(
        xdim / 100 * 5,
        ymax + 100,
        s=f"{ymax}",
        fontsize=16,
        color="k",
        va="bottom",
        ha="left",
    )
    ax.text(
        xdim - (xmax / 100 * 5),
        ymin - 200,
        s=f"{ymin}",
        fontsize=16,
        color="k",
        va="top",
        ha="right",
    )

    # ax.set_xlim([0, ds.dims["x"]])
    # ax.set_ylim([0, ds.dims["y"]])
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


st.cache(hash_funcs={xr.core.dataset.Dataset: id}, allow_output_mutation=True)


def annot_img(ds, channels, show, cells, xmin, xmax, ymin, ymax, override, alpha):
    if show:
        fig, ax = plt.subplots()
        _ = (
            ds.im[channels, xmin:xmax, ymin:ymax]
            .la[cells]
            .im.colorize(colors=["C2", "C0", "C3", "C1", "C4", "C5", "C6", "C7"])
            .la.render_label(alpha=alpha, override_color="w" if override else None)
            .pl.imshow(ax=ax, legend_background=True, legend_label=True)
        )
        ax.axis("off")
    else:
        fig, ax = plt.subplots()
        _ = (
            ds.im[channels, xmin:xmax, ymin:ymax]
            .im.colorize(colors=["C2", "C0", "C3", "C1", "C4", "C5", "C6", "C7"])
            .pl.imshow(ax=ax, legend_background=True)
        )
        ax.axis("off")

    return fig
