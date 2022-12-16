from datetime import date

# from data import tl_generation_wrapper as long_data
import distinctipy
import plotly.graph_objects as go
from dash import html, dcc
from icecream import ic
from plotly.graph_objects import scatter
from plotly.subplots import make_subplots
from data.source import Source

from data import catalogue

# Hardcoded data source selection here
# long_data = catalogue.get_source("random_data")
# long_data = catalogue.get_source("talklife-aggregated")


# This is used to prevent the default plotly controls from appearing in the top-right corner of the figure.
fig_config = {
    "displayModeBar": False,
    "displaylogo": False,
    "scrollZoom": True,
    "locale": "en-GB",
}


def _get_cmoc_colors(datasource: Source):
    # rng is a random seed. We fix it here so that the same set of colors will be produced on each call.
    # See https://distinctipy.readthedocs.io/en/latest/api.html#distinctipy.distinctipy.get_colors
    return distinctipy.get_colors(
        len(datasource.cmoc_methods), pastel_factor=0.0, rng=123
    )


def get_graph(
    datasource: Source, user_df, selected_cmocs, cmoc_options_state, radius_width, radius_opacity, xrange
):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]], shared_xaxes=True)

    # Set some defaults
    radius_width = radius_width if radius_width else 7
    radius_opacity = radius_opacity if radius_opacity else 0.7

    show_points = (
        True
        if cmoc_options_state and "cmoc_midpoint_visible" in cmoc_options_state
        else False
    )
    show_radius = (
        True
        if cmoc_options_state and "cmoc_radius_visible" in cmoc_options_state
        else False
    )

    # fig.add_trace(go.Scatter(
    #     mode="lines",
    #     x=user_df.index,
    #     y=user_df["posts"],
    #     name="Timeline",
    #     xperiod=(24*60*60*1000)
    #     ), secondary_y=False)

    if xrange:
        fig.update_xaxes(range=xrange)

    fig.update_yaxes(
        fixedrange=True,
        secondary_y=False,
        range=[0, max(user_df["posts"])],
        title="number of posts per day",
    )

    cmoc_colors = _get_cmoc_colors(datasource)
    for method_name in datasource.cmoc_methods:
        visible = True if method_name in selected_cmocs else "legendonly"

        cmoc_color = f"rgb{distinctipy.get_rgb256(cmoc_colors.pop())}"
        fig = _apply_cmoc(
            fig,
            user_df,
            method_name,
            friendly_name=datasource.cmoc_method_friendly_names(method_name),
            color=cmoc_color,
            visible=visible,
            show_points=show_points,
            show_radius=show_radius,
            radius=radius_width,
            radius_opacity=radius_opacity,
        )

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

    fig.update_layout(
        height=600,
        modebar_orientation="v",
        modebar_activecolor="green",
        showlegend=False,
    )

    fig = _apply_rangeslider(fig)

    return fig


def _apply_timeline(fig):
    pass


def get_cmoc_checklist(datasource: Source, cmoc_options_state):
    cmoc_colors = _get_cmoc_colors(datasource)
    items = []
    for method_name in datasource.cmoc_methods:
        cmoc_color = f"rgb{distinctipy.get_rgb256(cmoc_colors.pop())}"
        items.append(_create_cmoc_checklist_item(
            method_name,
            datasource.cmoc_method_friendly_names(method_name),
            color=cmoc_color)
        )

    return dcc.Checklist(
        id={"type": "cmoc_visible_checklist", "name": "cmoc_visible_selection"},
        options=items,
        style={"display": "row", "align-items": "left", "justify-content": "left"},
        value=cmoc_options_state,
    )


def _create_cmoc_checklist_item(method_name, friendly_name, color):
    #   &#x26AA; ==> white circle
    # 25A0 black square

    return {
        # "label": long_data.cmoc_method_friendly_names(method_name),
        # "label": html.Div(
        #     [
        #         html.P("&#x26AA;", style={'font-size': 15, 'padding-left': 10, "color": color}),
        #         html.P(method_name, style={'font-size': 15, 'padding-left': 10}),
        #     ], style={'display': 'flex', "flex-direction": "row", 'align-items': 'left', 'justify-content': 'left'}
        # ),
        # "label": dcc.Markdown(f"&#x26AA; {method_name}", style={'font-size': 15, 'padding-left': 10}),
        "label": html.Span(
            [
                # 25A0 black square
                html.Span("■", style={"color": color, "font-size": 20}),
                f" {friendly_name}",
            ]
        ),
        "value": method_name,
    }


def _apply_cmoc(
    fig,
    user_df,
    method_name,
    friendly_name,
    color,
    visible,
    show_points: bool,
    show_radius: bool,
    radius,
    radius_opacity,
):
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
        # name=long_data.cmoc_method_friendly_names(method_name),
        name=friendly_name,
        x=user_df.index,
        # y=user_df["cmoc"],
        y=user_df[method_name],
        line=None,
        marker=cmoc_marker,
        connectgaps=False,
        error_x=width_as_error,
        error_y=hight_as_error,
        xperiod=(24 * 60 * 60 * 1000),
        # visible=True if method_name == long_data.cmoc_methods[0] else "legendonly",
        # visible=True if show_points else "legendonly",
        visible=visible,
        showlegend=True,
    )

    cmoc_bar = go.Bar(
        # mode="markers",
        # name="CMOCs",
        # name=long_data.cmoc_method_friendly_names(method_name),
        name=friendly_name,
        x=user_df.index,
        # y=user_df["cmoc"],
        y=user_df[method_name],
        opacity=radius_opacity,
        # line=None,
        # marker=cmoc_marker,
        # connectgaps=False,
        # error_x=width_as_error,
        # error_y=hight_as_error,
        width=radius * (24 * 60 * 60 * 1000),
        xperiod=(24 * 60 * 60 * 1000),
        # visible=True if method_name == long_data.cmoc_methods[0] else "legendonly",
        # visible=True if show_radius else "legendonly",
        visible=visible,
        showlegend=True,
    )

    # ic(cmoc_scatter)

    if show_radius:
        fig.add_trace(cmoc_bar, secondary_y=True)
    if show_points:
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
