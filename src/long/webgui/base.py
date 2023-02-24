import json

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State, ALL

from data import catalogue
from icecream import ic

from .header import header, left_menu, right_menu
from .timeline_fig import create_user_id_dropdown
from figures.timeline_table import get_table
from figures.timeline import fig_config, get_graph, get_cmoc_checklist

# from data import tl_generation_wrapper as long_data


# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

ic(__name__)

app = Dash(
    __name__,
    title="LoNG",
    # assets_url_path="/assets/",
    assets_folder="../assets/",
    # external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

# Hardcoded data source selection here
# long_data = catalogue.get_source("random_data")
# long_data = catalogue.get_source("talklife-aggregated")


@app.callback(
    Output("user_id_dropdown_container", "children"),
    # Output("user_id_dropdown", "select"),
    Input("datasource_id_dropdown", "value"),
)
def update_user_id_dropdown(datasource_name):
    ic(datasource_name)

    return create_user_id_dropdown(datasource_name)


# @app.callback(
#     Output("main_graph", "figure"),
#     Input("user_id_dropdown", "value"),
#     Input("datasource_id_dropdown", "value"),
#     Input({"type": "cmoc_visible_checklist", "name": ALL}, "value"),
#     Input("cmoc_options_checklist", "value"),
#     Input("cmoc_options_radius_width", "value"),
#     Input("cmoc_options_radius_translucency", "value"),
#     State("main_graph", "relayoutData"),
# )
def get_user_tl_graph(
    user_id,
    datasource_name,
    cmoc_selection,
    cmoc_options_state,
    radius_width,
    radius_translucency,
    main_graph_layout,
):
    # ic(cmoc_options_state)
    ic(cmoc_selection)
    # ic(radius_width)
    # ic(radius_translucency)
    selected_cmocs = []
    # Work around for the fact that the CMOC select checklist might exist when this callback is first called
    if cmoc_selection:
        # selected_cmocs = cmoc_selection.get("props", {}).get("value", [])
        selected_cmocs = cmoc_selection[0]

    ic(main_graph_layout)
    xrange = []
    if main_graph_layout and "xaxis.range[0]" in main_graph_layout:
        xrange = [
            main_graph_layout.get("xaxis.range[0]"),
            main_graph_layout.get("xaxis.range[1]"),
        ]
    ic(xrange)
    ic(selected_cmocs)

    datasource = catalogue.get_source(datasource_name)

    user_df = datasource.get_user_df(user_id)
    return get_graph(
        datasource,
        user_df,
        selected_cmocs,
        cmoc_options_state,
        radius_width,
        radius_translucency,
        xrange,
    )


@app.callback(
    Output("timeline_table_container", "children"),
    Input("user_id_dropdown", "value"),
    Input("datasource_id_dropdown", "value"),
    Input({"type": "cmoc_visible_checklist", "name": ALL}, "value"),
    Input("cmoc_options_checklist", "value"),
    Input("cmoc_options_radius_width", "value"),
    Input("cmoc_options_radius_translucency", "value"),
    State("main_graph", "relayoutData"),
)
def get_user_timetime_table(
    user_id,
    datasource_name,
    cmoc_selection,
    cmoc_options_state,
    radius_width,
    radius_translucency,
    main_graph_layout,
):
    datasource = catalogue.get_source(datasource_name)
    user_df = datasource.get_full_user_timeline(user_id)

    return get_table(user_df=user_df)


@app.callback(
    Output("legend_cmocs_container", "children"),
    Input("user_id_dropdown", "value"),
    State("datasource_id_dropdown", "value"),
    State("legend_cmocs_container", "children"),
)
def get_tl_cmoc_checklist(user_id, datasource_name, cmoc_selection):
    # ic(cmoc_options_state)
    # ic(cmoc_selection)
    # ic(radius_width)
    # ic(radius_translucency)
    selected_cmocs = []
    # Work around for the fact that the CMOC select checklist might exist when this callback is first called
    if cmoc_selection:
        selected_cmocs = cmoc_selection.get("props", {}).get("value", [])

    # ic(selected_cmocs)
    datasource = catalogue.get_source(datasource_name)

    return get_cmoc_checklist(datasource, selected_cmocs)


def filter_legend_state_changes(cmoc_selection, cmoc_options_state):
    ic(cmoc_options_state)
    ic(cmoc_selection)

    output = {}
    if cmoc_selection:
        output["selected_cmocs"] = cmoc_selection.get("props", {}).get("value", [])
    # if cmoc_options_state:
    #     output["show_radius"] = True if "cmoc_radius_visible" in (cmoc_options_state["props"].get("value", [])) else False
    #     output["show_point"] = True if "cmoc_midpoint_visible" in (cmoc_options_state["props"].get("value", [])) else False

    ic(output)


@app.callback(
    Output("relayout_data", "children"),
    Input("main_graph", "relayoutData"),
    Input("main_graph", "restyleData"),
)
def display_changed_fig_data(relayoutData, restyleData):
    output = {}
    output["relayoutData"] = relayoutData
    output["restyleData"] = restyleData
    return json.dumps(output, indent=2)


# @app.callback(
#     Output('legend_cmocs_data', 'children'),
#     Input('main_graph', 'relayoutData'),
#     State('legend_cmocs_container', 'children'))
# def display_dropdowns(relayoutData, checklist_state):
#     # ic(relayoutData)
#     # ic(checklist_state)
#     output = {}
#     output["relayoutData"] = relayoutData
#     output["checklist_state"] = checklist_state
#     return json.dumps(output, indent=2)


# @app.callback(
#     Output('dropdown-container-output', 'children'),
#     Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
# )
# def display_output(values):
#     return html.Div([
#         html.Div('Dropdown {} = {}'.format(i + 1, value))
#         for (i, value) in enumerate(values)
#     ])


app.layout = html.Div(
    [
        header,
        html.Div(
            [
                left_menu,
                html.Div(
                    [
                        html.P("Select User ID"),
                        # create_user_id_dropdown([*catalogue.list_source_names()][0]),
                        html.Div(id="user_id_dropdown_container"),
                        # dcc.Dropdown(
                        #     id="user_id_dropdown",
                        #     clearable=False,
                        # ),
                        dcc.Graph(
                            id="main_graph",
                            # figure=get_user_tl_graph(
                            #     long_data.user_ids[0], None, None, None, None, None
                            # ),
                            config=fig_config,
                        ),
                        # html.Div([
                        #     html.Img(src='/assets/image.png')
                        # ]),
                        html.Div(id="timeline_table_container"),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                                **JSON params:**
                            """
                                ),
                                html.Pre(id="relayout_data", style=styles["pre"]),
                            ]
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "width": "1200px",
                    },
                ),
                right_menu,
            ],
            style={"display": "flex", "flex-direction": "row", "height": "400px"},
        ),
    ]
)
