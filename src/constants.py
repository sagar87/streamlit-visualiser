import pandas as pd
import os
import pathlib



META = pd.read_csv(os.path.join(pathlib.Path(__file__).parent.resolve(), 'sample.csv'), index_col=0)

def filter_panel(panels, channels):
    panel = {}
    for k, v in panels.items():
        valid_panel = True
        for c in v:
            if c not in channels:
                valid_panel = False
                break

        if valid_panel:
            panel[k] = v

    return panel


CHANNELS = [
    "Hoechst",
    "BCL6",
    "CD103",
    "Myc",
    "CD39",
    "pSTAT3",
    "CD70",
    "GATA3",
    "CXCR5",
    "Tbet",
    "CD62L",
    "FOXP3",
    "CD163",
    "CD194",
    "Ki67",
    "TIM3",
    "PAX5",
    "CD134",
    "IL10",
    "CD5",
    "CD206",
    "CD25",
    "CD16",
    "CTLA4",
    "CD79a",
    "CD57",
    "CD34",
    "CXCL13",
    "CD21",
    "CD7",
    "PDPN",
    "PD1",
    "HLA-DR",
    "LAG3",
    "CD20",
    "CD56",
    "CD45RO",
    "ICOS",
    "CD90",
    "CD4",
    "CD11c",
    "CD3",
    "CD68",
    "CD69",
    "CD14",
    "CD8",
    "kappa",
    "CD45RA",
    "CD11b",
    "GRZB",
    "CD31",
    "CD45",
    "CD38",
    "CD44",
    "CD15",
    "lambda",
    "MCT",
    "DRAQ5",
]

CHANNEL_PANELS = {
    "Hoechst": ["Hoechst"],
    "CD4, CD8, PAX5": ["CD4", "CD8", "PAX5"],
    "CD45RA, CD45RO, PAX5": ["CD45RA", "CD45RO", "PAX5"],
    "T-REG (CD45RA, CD45RO, FOXP3)": ["CD45RA", "CD45RO", "FOXP3"],
    "T-FH (CD45RO, PD1)": ["CD45RO", "PD1"],
    "B/FDC (CD79a, CD21, PAX5)": ["CD79a", "CD21", "PAX5"],
    "TPR (Paper)": ["CD4", "CD8", "Ki67"],
    "T Naive (Paper)": ["CD4", "CD45RA"],
    "TH CM1 (Paper)": ["CD4", "CD45RO", "CD62L"],
    "TH CM2 (Paper)": ["CD4", "CD45RO", "CD69"],
    "TFH (Paper)": ["CD4", "PD1", "CXCR5"],
    "TREG CM1 (Paper)": ["CD25", "ICOS", "FOXP3"],
    "TREG CM2 (Paper)": ["CD25", "ICOS", "FOXP3"],
    "TREG EM1/2 (Paper)": ["CD69", "PD1", "FOXP3"],
    "TTOX Naive (Paper)": ["CD8", "CD45RA", "CD62L"],
    "TTOX EM1 (Paper)": [
        "CD31",
        "CD45RO",
    ],
    "TTOX EM2 (Paper)": ["CD31", "CD45RO", "PD1"],
    "TTOX EM3 (Paper)": ["CD31", "CD45RO", "TIM3"],
    "TDN (Paper)": ["CD31", "TIM3"],
}


CELL_PANELS = {
    "CD4+ T cells": ["T-CD4 Naive", "T-CD4", "T-FH", "T-REG"],
    "CD8+ T cells": ["T-TOX Naive", "T-TOX", "T-TOX Exhausted"],
    "B cells": ["B", "PC"],
    "All": [
        "T-CD4 Naive",
        "T-CD4",
        "T-REG",
        "T-FH",
        "T-TOX Naive",
        "T-TOX",
        "T-TOX Exhausted",
        "T-PR",
        "B",
        "PC",
        "Macro",
        "DC",
        "FDC",
        "NK",
        "NKT",
        "Granulo",
        "Stromal cells",
        "MC",
        "Unknown",
    ],
}


NUM2CELL = {
    1: "T-CD4 Naive",
    2: "T-CD4",
    3: "T-REG",
    4: "T-FH",
    5: "T-TOX Naive",
    6: "T-TOX",
    7: "T-TOX Exhausted",
    8: "T-PR",
    9: "B",
    10: "PC",
    11: "Macro",
    12: "DC",
    13: "FDC",
    14: "NK",
    15: "NKT",
    16: "Granulo",
    17: "Stromal cells",
    18: "MC",
    19: "Unknown",
}

CELL2NUM = {
    "T-CD4 Naive": 1,
    "T-CD4": 2,
    "T-REG": 3,
    "T-FH": 4,
    "T-TOX Naive": 5,
    "T-TOX": 6,
    "T-TOX Exhausted": 7,
    "T-PR": 8,
    "B": 9,
    "PC": 10,
    "Macro": 11,
    "DC": 12,
    "FDC": 13,
    "NK": 14,
    "NKT": 15,
    "Granulo": 16,
    "Stromal cells": 17,
    "MC": 18,
    "Unknown": 19,
}
