from dash import Dash, Input, Output, dcc, html
from icecream import ic
from .timeline_fig import create_cmoc_options_list

styles = {
    "pre": {"border": "thin lightgrey solid", "overflowX": "scroll"},
    "legends": {
        "background-color": "#000000",
        "color": "#ffffff",
        "border-style": "solid",
        "padding": "3px 6px",
    },
    "fieldset": {
        "border-style": "solid",
        "border-color": "#000000",
        "border-width": "2px",
        "background-color": "#eeeeee",
    },
    "input": {"margin": ".4rem"},
}


header = html.Div(
    [
        html.Button("Home", id="home_btn", disabled=True),
        html.Button("Data Inventory", id="data_btn", disabled=True),
        html.Button("Timeline Selection", id="timeline_btn", disabled=True),
        html.Button("Annotation Preparation", id="annotate_prep_btn", disabled=True),
        html.Button("Advanced", id="advanced_btn", disabled=True),
        html.Button("Help", id="help_btn", disabled=True),
    ]
)

left_menu = html.Div(
    [
        html.H4("Timeline View"),
        html.Br(),
        html.A("List Users"),
        html.Br(),
        html.A("User's Timeline"),
        html.Br(),
        html.A("Raw Text"),
    ]
)

right_menu = html.Div(
    id="legend_top_container",
    children=[
        # Legend title
        html.H4("Legend"),
        # Sub heading - CMOC methods
        html.Br(),
        # html.A("Candidate Moments Of Change (CMOC)"),
        #   checklist for each CMOC
        html.Fieldset(
            id="legend_cmocs_fieldset",
            children=[
                html.Legend(
                    "Candidate Moments Of Change (CMOC)", style=ic(styles["legends"])
                ),
                # Place holder for checklist
                html.Div(id="legend_cmocs_container", children=[]),
            ],
            style=styles["fieldset"],
        ),
        html.Fieldset(
            id="legend_cmocs_options_fieldset",
            children=[
                html.Legend("Options for CMOCs", style=ic(styles["legends"])),
                # Place holder for checklist
                #   switches for CMOC centreline
                #   switches for CMOC radius
                #   slide for CMOC radius
                #   slide for translucency
                html.Div(
                    id="legend_cmocs_options", children=create_cmoc_options_list()
                ),
            ],
            style=styles["fieldset"],
        ),
        # Show callback data for debug purposes
        html.Pre(id="legend_cmocs_data", style=styles["pre"]),
    ],
)
