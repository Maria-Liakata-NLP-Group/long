from datetime import date

# from data import tl_generation_wrapper as long_data
import distinctipy
import plotly.graph_objects as go
from dash import html, dcc
from icecream import ic
from plotly.graph_objects import scatter
from plotly.subplots import make_subplots
from data.source import Source
import plotly.express as px
from pandas import DataFrame
from numpy import NaN

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
    datasource: Source,
    user_df,
    selected_cmocs,
    cmoc_options_state,
    radius_width,
    radius_opacity,
    xrange,
):
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{}], [{"secondary_y": True}]],
        shared_xaxes=True,
        row_heights=[0.25, 0.75],
    )

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
        row=2,
        col=1,
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

    fig = _create_rug_plot(fig, datasource, user_df)

    fig.add_trace(
        go.Scatter(
            mode="lines",
            x=user_df.index,
            y=user_df["posts"],
            name="Timeline",
            xperiod=(24 * 60 * 60 * 1000),
        ),
        secondary_y=False,
        row=2,
        col=1,
    )

    fig.update_yaxes(
        dtick=1,
        showgrid=False,
        fixedrange=True,
        domain=[0, 1],
        range=[0, 1],
        visible=False,
        secondary_y=True,
        row=2,
        col=1,
    )

    fig.update_layout(
        height=800,
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
        items.append(
            _create_cmoc_checklist_item(
                method_name,
                datasource.cmoc_method_friendly_names(method_name),
                color=cmoc_color,
            )
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

    # rug_df = user_df.copy()
    # rug_df = rug_df[rug_df[method_name]>0]
    # # ic(rug_df.head(10))
    # index_value = ic(list(user_df.columns).index(method_name))
    # rug_df = rug_df.apply(lambda x: index_value if x[method_name] else None, axis=1)
    # ic(rug_df.head(10))

    # cmoc_rug_fig = px.scatter(
    #     rug_df,
    #     x=rug_df.index,
    #     # y=method_name,
    #     # markers=True, lines=False,
    #     marginal_x="rug"
    # )

    # ic(cmoc_rug_fig)

    # fig.add_trace(cmoc_rug_fig.data[1], row=1, col=1)
    # fig.add_trace(cmoc_rug_fig.data[2], row=1, col=1)

    # ic(cmoc_scatter)

    if show_radius:
        fig.add_trace(cmoc_bar, secondary_y=True, row=2, col=1)
    if show_points:
        fig.add_trace(cmoc_scatter, secondary_y=True, row=2, col=1)

    return fig


def _apply_rangeslider(fig):

    # Add range slider
    fig.update_layout(
        xaxis2=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
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


def _create_rug_plot(fig, datasource: Source, user_df):

    # fig,
    # user_df,
    # method_name,
    # friendly_name,
    # color,
    # visible,
    # show_points: bool,
    # show_radius: bool,
    # radius,
    # radius_opacity,

    # datasource: Source,
    # user_df,
    # selected_cmocs,
    # cmoc_options_state,
    # radius_width,
    # radius_opacity,
    # xrange,

    rug_df = user_df.copy()
    ic(len(rug_df))
    # ic(rug_df.head(5))

    # rug_df = rug_df[rug_df[method_name]>0]

    for method_name in datasource.cmoc_methods:

        # ic(rug_df.head(10))
        index_value = ic(list(user_df.columns).index(method_name))
        rug_df[method_name] = rug_df.apply(
            (lambda x: method_name if x[method_name] > 0 else NaN), axis=1
        )

    # ic(rug_df.head(100))

    melt_df = rug_df.melt(id_vars=["posts"], var_name="CMoCs", ignore_index=False)

    melt_df = melt_df.dropna(how="any")
    # ic(melt_df)

    ic(melt_df.describe(include="all"))

    cmoc_rug_fig = px.scatter(
        melt_df,
        x=melt_df.index,
        y=melt_df["posts"],
        color="CMoCs",
        # markers=True, lines=False,
        marginal_x="rug",
        render_mode="line",
    )

    # # ic(user_df.columns)
    # # ic(user_df[1:10])
    # cmoc_rug_fig = px.scatter(
    #     user_df[1:100],
    #     x=user_df[1:100].index,
    #     # y=user_df[method_name],
    #     # markers=True, lines=False,
    #     marginal_x="rug"
    # )

    for d in cmoc_rug_fig.data:
        ic(type(d), isinstance(d, go.Box))
        ic(d)
        if isinstance(d, go.Box):
            fig.add_trace(d, row=1, col=1)

    # ic(len(cmoc_rug_fig.data))

    # ic(type(cmoc_rug_fig.data[1]))
    # fig.add_trace(cmoc_rug_fig.data[1], row=1, col=1)
    # # ic(fig)
    # fig.add_trace(cmoc_rug_fig.data[3], row=1, col=1)
    # fig.add_trace(cmoc_rug_fig.data[5], row=1, col=1)

    return fig
