import json

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from data import catalogue

from .header import header, left_menu, right_menu
from .timeline_fig import create_user_id_dropdown, fig_config, get_graph

# from data import tl_generation_wrapper as long_data


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

long_data = catalogue.get_source("random_data")
# user_df = long_data.get_user_df(361767)


@app.callback(Output("main_graph", "figure"), Input("user_id_dropdown", "value"))
def get_user_tl_graph(user_id):
    user_df = long_data.get_user_df(user_id)
    return get_graph(user_df)


app.layout = html.Div(
    [
        header,
        html.Div(
            [
                left_menu,
                html.Div(
                    [
                        html.P("Select User ID"),
                        create_user_id_dropdown(),
                        dcc.Graph(
                            id="main_graph",
                            figure=get_user_tl_graph(long_data.user_ids[0]),
                            config=fig_config,
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
            style={"display": "flex", "flex-direction": "row", "hieght": "400px"},
        ),
    ]
)
