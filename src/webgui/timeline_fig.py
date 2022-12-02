from datetime import date

# from data import tl_generation_wrapper as long_data
import distinctipy
import plotly.graph_objects as go
from dash import dcc
from icecream import ic
from plotly.graph_objects import scatter
from plotly.subplots import make_subplots

from data import catalogue

# long_data = catalogue.get_all_sources()[0]
long_data = catalogue.get_source("random_data")

# This is used to prevent the default plotly controls from appearing in the top-right corner of the figure.
fig_config = {
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": True,
    "locale": "en-GB",
}


def _get_cmoc_colors():
    # rng is a random seed. We fix it here so that the same set of colors will be produced on each call.
    # See https://distinctipy.readthedocs.io/en/latest/api.html#distinctipy.distinctipy.get_colors
    return distinctipy.get_colors(
        len(long_data.cmoc_methods), pastel_factor=0.0, rng=123
    )


def create_user_id_dropdown():
    return dcc.Dropdown(
        id="user_id_dropdown",
        options=long_data.user_ids,
        value=long_data.user_ids[0],
        clearable=False,
    )


def get_graph(user_df):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]], shared_xaxes=True)

    # fig.add_trace(go.Scatter(
    #     mode="lines",
    #     x=user_df.index,
    #     y=user_df["posts"],
    #     name="Timeline",
    #     xperiod=(24*60*60*1000)
    #     ), secondary_y=False)

    fig.update_yaxes(
        fixedrange=True,
        secondary_y=False,
        range=[0, max(user_df["posts"])],
        title="number of posts per day",
    )

    cmoc_colors = _get_cmoc_colors()
    for method_name in long_data.cmoc_methods:
        cmoc_color = f"rgb{distinctipy.get_rgb256(cmoc_colors.pop())}"
        fig = _apply_cmoc(fig, user_df, method_name, color=cmoc_color)

    fig.add_trace(
        go.Scatter(
            mode="lines",
            x=user_df.index,
            y=user_df["posts"],
            name="Timeline",
            xperiod=(24 * 60 * 60 * 1000),
        ),
        secondary_y=False,
    )

    fig.update_yaxes(
        dtick=1,
        showgrid=False,
        fixedrange=True,
        domain=[0, 1],
        range=[0, 1],
        visible=False,
        secondary_y=True,
    )

    fig.update_layout(height=600, modebar_orientation="v", modebar_activecolor="green")

    fig = _apply_rangeslider(fig)

    ic(fig.to_dict().keys())

    return fig


def _apply_timeline(fig):
    pass


def _apply_cmoc(fig, user_df, method_name, color):
    """
    The first CMOC method is made visible by default. All subsequent CMOCs are set to "legendonly" visibility be default.
    """
    cmoc_marker = scatter.Marker(
        symbol="square",
        size=1,
        # color=user_df["cmoc"],
        # color=user_df[method_name],
        # colorscale= [[0, 'black'], [1, color]]
        color=color,
    )

    width_as_error = scatter.ErrorX(
        symmetric=True,
        type="constant",
        # value=5*(24*60*60*1000),
        # valueminus=5,
        width=5,
    )

    hight_as_error = scatter.ErrorY(
        symmetric=False,
        type="percent",
        value=0,
        valueminus=100,
        width=1,
        # color='red',
        color=color,
        thickness=1,
    )

    # width_as_error = None
    # hight_as_error = None

    cmoc_scatter = go.Scatter(
        mode="markers",
        # name="CMOCs",
        name=long_data.cmoc_method_friendly_names(method_name),
        x=user_df.index,
        # y=user_df["cmoc"],
        y=user_df[method_name],
        line=None,
        marker=cmoc_marker,
        connectgaps=False,
        error_x=width_as_error,
        error_y=hight_as_error,
        xperiod=(24 * 60 * 60 * 1000),
        visible=True if method_name == long_data.cmoc_methods[0] else "legendonly",
        showlegend=True,
    )

    cmoc_bar = go.Bar(
        # mode="markers",
        # name="CMOCs",
        name=long_data.cmoc_method_friendly_names(method_name),
        x=user_df.index,
        # y=user_df["cmoc"],
        y=user_df[method_name],
        # line=None,
        # marker=cmoc_marker,
        # connectgaps=False,
        # error_x=width_as_error,
        # error_y=hight_as_error,
        width=2.0 * (24 * 60 * 60 * 1000),
        xperiod=(24 * 60 * 60 * 1000),
        visible=True if method_name == long_data.cmoc_methods[0] else "legendonly",
        showlegend=True,
    )

    ic(cmoc_scatter)

    fig.add_trace(cmoc_bar, secondary_y=True)
    fig.add_trace(cmoc_scatter, secondary_y=True)

    return fig


def _apply_rangeslider(fig):
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True, range=[date(2017, 1, 1), date(2021, 1, 1)]),
            type="date",
        )
    )

    return fig
