# from datetime import date

# from data import tl_generation_wrapper as long_data
# import distinctipy
# import plotly.graph_objects as go
from dash import dcc, html

# from icecream import ic
# from plotly.graph_objects import scatter
# from plotly.subplots import make_subplots

from data import catalogue

# Hardcoded data source selection here
# long_data = catalogue.get_source("random_data")
long_data = catalogue.get_source("talklife-aggregated")



def create_user_id_dropdown():
    return dcc.Dropdown(
        id="user_id_dropdown",
        options=long_data.user_ids,
        value=long_data.user_ids[0],
        clearable=False,
    )


def create_cmoc_options_list():

    children = []

    # Switches for CMOC centreline and CMOC radius
    children.append(
        dcc.Checklist(
            id="cmoc_options_checklist",
            options={
                "cmoc_midpoint_visible": "Show CMOC midpoint",
                "cmoc_radius_visible": "Show CMOC radius",
            },
            value=["cmoc_midpoint_visible"],
        )
    )

    # slider for CMOC radius
    children.append(html.Div("CMOC Radius (Days)"))
    children.append(
        # dcc.Slider(min=1, max=21, step=1, value=7, id="cmoc_options_radius_width")
        dcc.Input(
            id="cmoc_options_radius_width",
            type="number",
            placeholder="Number of days",
            min=0,
            value=7,
        )
    )
    # slider for translucency
    children.append(html.Div("CMOC Radius Translucency"))
    children.append(
        dcc.Slider(
            min=0.0,
            max=1.0,
            marks=None,
            value=0.7,
            id="cmoc_options_radius_translucency",
            tooltip={"placement": "bottom", "always_visible": True},
        )
    )

    return children
