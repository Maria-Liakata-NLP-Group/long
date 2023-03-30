from dash import dcc, html, dash_table
from icecream import ic
from data import catalogue
from data.source import Source
import pandas as pd


def get_table(user_df: pd.DataFrame):
    if user_df is None:
        ic("no table to build")
        my_table = html.P("Full Timeline data not available")
    else:
        ic("building table")
        # See https://github.com/Maria-Liakata-NLP-Group/long/issues/55#issuecomment-1434516796 for description of these options
        my_table = get_table_native_layout(user_df)
        # my_table = get_table_alternative_rows(user_df)
        # my_table = get_table_combine_metadata(user_df)

    return my_table


def get_table_native_layout(user_df: pd.DataFrame):
    ic("get_table_native_layout")
    col_details = [
        {"id": "thread_id", "name": "thread_id".capitalize()},
        {"id": "msg_id", "name": "msg_id".capitalize()},
        {"id": "username", "name": "username".capitalize()},
        {"id": "timestamp", "name": "timestamp"},
        # {'id': 'date', 'name': 'date'},
        {"id": "text", "name": "text"},
    ]

    my_table = dash_table.DataTable(
        style_data={
            "whiteSpace": "normal",
            "height": "auto",
        },
        data=user_df.to_dict("records"),
        # data = split_rows(user_df),
        # columns = ic([{"name": i, "id": i} for i in user_df.columns])
        columns=col_details,
        style_data_conditional=[
            # {
            #     'if': {
            #         'column_id': ['thread_id', 'msg_id', 'username', 'timestamp'],
            #     },
            #     'backgroundColor': 'rgb(220, 220, 220)',
            # },
            {
                "if": {
                    "row_index": "odd",
                },
                "backgroundColor": "rgb(220, 220, 220)",
            },
            {
                "if": {
                    "column_id": "text",
                },
                "textAlign": "left",
            },
        ],
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=10,
    )

    table_div = html.Div(my_table)

    return table_div


def get_table_combine_metadata(user_df: pd.DataFrame):
    ic("get_table_combine_metadata")
    col_details = [
        {"id": "metadata", "name": "Metadata"},
        {"id": "text", "name": "Text"},
    ]

    my_table = dash_table.DataTable(
        style_data={"whiteSpace": "pre-wrap", "height": "auto", "textAlign": "left"},
        data=combine_metadata_columns(user_df),
        # columns = ic([{"name": i, "id": i} for i in user_df.columns])
        columns=col_details,
        style_data_conditional=[
            {
                "if": {
                    "column_id": "metadata",
                },
                "backgroundColor": "rgb(220, 220, 220)",
            },
            {
                "if": {
                    "column_id": "text",
                },
                "textAlign": "left",
            },
        ],
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=10,
    )

    table_div = html.Div(my_table)

    return table_div


def get_table_alternative_rows(
    # datasource: Source,
    user_df: pd.DataFrame,
    # selected_cmocs,
    # cmoc_options_state,
    # radius_width,
    # radius_opacity,
    # xrange,
):
    ic("get_table_alternative_rows")
    col_details = [
        {"id": "thread_id", "name": "thread_id".capitalize()},
        {"id": "msg_id", "name": "msg_id".capitalize()},
        {"id": "username", "name": "username".capitalize()},
        {"id": "timestamp", "name": "timestamp"},
        # {'id': 'date', 'name': 'date'},
        {"id": "text", "name": "text"},
    ]

    my_table = dash_table.DataTable(
        style_data={
            "whiteSpace": "normal",
            "height": "auto",
        },
        # data = user_df.to_dict('records'),
        data=split_rows(user_df),
        # columns = ic([{"name": i, "id": i} for i in user_df.columns])
        columns=col_details,
        style_data_conditional=[
            {
                "if": {"row_index": "even"},
                "backgroundColor": "rgb(220, 220, 220)",
            },
            {
                "if": {"column_id": "thread_id"},
                "width": "5%",
            },
            {
                "if": {"row_index": "even", "column_id": "msg_id"},
                "width": f"{10}%",
            },
            {
                "if": {
                    "row_index": "even",
                    "column_id": "username",
                },
                "width": f"{20}%",
                "textAlign": "left",
            },
            {
                "if": {
                    "row_index": "even",
                    "column_id": "timestamp",
                },
                "width": f"{65}%",
                "textAlign": "left",
            },
            {
                "if": {
                    "row_index": "even",
                    "column_id": "text",
                },
                "width": f"{0}%",
                "textAlign": "left",
            },
            {
                "if": {"row_index": "odd", "column_id": "text"},
                "width": "95%",
                "textAlign": "left",
            },
        ],
        css=[
            {
                "selector": ".dash-spreadsheet tr",
                "rule": """
                display: block;
                width: 100%;
                table-layout: fixed;
                empty-cells: show;
                border-spacing: 0px;
                min-height: 30px;
                padding: 0px;
                border: 0px;
                margin: 0px;
                height: auto;
                border-spacing: 0px;
            """,
            },
            {
                "selector": ".dash-spreadsheet tbody",
                "rule": """
                width: 100%;
                table-layout: fixed;
                border-spacing: 0px;
                border-collapse: separate;
                border-spacing: 0px;
                padding: 0px;
                margin: 0px;
            """,
            },
        ],
        style_as_list_view=True,
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=20,
    )

    table_div = html.Div(my_table)

    return table_div


def combine_metadata_columns(df: pd.DataFrame):
    _data = (df.to_dict("records"),)
    result = []
    ic(type(_data))
    for row in _data[0]:
        # ic(len(row))
        ic(row)
        # metadata_value = str(html.Div([
        #     html.P(row['thread_id']),
        #     html.P(row['msg_id']),
        #     html.P(row['username']),
        #     html.P(row['timestamp']),
        # ]))

        metadata_value = f"{row['thread_id']}\n{row['msg_id']}\n{row['username']}\n{row['timestamp']}"
        ic(metadata_value)
        new_dict = {"metadata": metadata_value, "text": row["text"]}

        result.append(new_dict)

    return result


def split_rows(df: pd.DataFrame):
    _data = (df.to_dict("records"),)
    result = []
    ic(type(_data))
    for row in _data[0]:
        # ic(len(row))
        # ic(row)
        meta_data_row = row.copy()
        del meta_data_row["text"]

        text_row = row.copy()
        del text_row["thread_id"]
        del text_row["msg_id"]
        del text_row["username"]
        del text_row["timestamp"]
        del text_row["date"]

        result.append(meta_data_row)
        result.append(text_row)

    return result


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
                # html.P(f"------"),
                # html.P(
                #     f"username = {username}, timestamp = {timestamp}, thread = {thread_id}"
                # ),
                html.Span(f"username = {username}", className="username"),
                html.Span(f"timestamp = {timestamp}", className="timestamp"),
                html.Span(f"thread_id = {thread_id}", className="thread_id"),
                html.P(f"{text}", className="thread_text"),
            ],
            className="thread_row",
        )
        table_cells.append(cell)

    return table_cells
