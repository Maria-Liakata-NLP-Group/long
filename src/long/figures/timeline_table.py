from dash import dcc, html
from icecream import ic
from data import catalogue
from data.source import Source
import pandas as pd


def get_table(
    # datasource: Source,
    user_df: pd.DataFrame,
    # selected_cmocs,
    # cmoc_options_state,
    # radius_width,
    # radius_opacity,
    # xrange,
):
    if user_df is None:
        ic("no table to build")
        table_cells = html.P("Full Timeline data not avilable")
    else:
        ic("building table")
        table_cells = build_cells(user_df)

    table_div = html.Div(table_cells)

    return table_div


def build_cells(user_df):
    user_df.sort_values(by="timestamp", inplace=True)
    table_cells = []
    for row in user_df.iterrows():
        ic(row)
        row_id, series = row
        ic(type(row_id))
        ic(type(series))
        # thread_id, msg_id, username, text, timestamp, date, Name = row
        u = series["username"]

        thread_id = series["thread_id"]
        username = series["username"]
        text = series["text"]
        timestamp = series["timestamp"]
        date = series["date"]

        cell = html.Div(
            [
                html.P(f"------"),
                html.P(
                    f"username = {username}, timestamp = {timestamp}, thread = {thread_id}"
                ),
                html.P(f"{text}"),
            ]
        )
        table_cells.append(cell)

    return table_cells
