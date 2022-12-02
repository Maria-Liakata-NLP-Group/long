from dash import Dash, dcc, html, Input, Output

header = html.Div([
        html.Button("Home", id="home_btn", disabled = True),
        html.Button("Data Inventory", id="data_btn", disabled = True),
        html.Button("Timeline Selection", id="timeline_btn", disabled = True),
        html.Button("Annotation Preparation", id="annotate_prep_btn", disabled = True),
        html.Button("Advanced", id="advanced_btn", disabled = True),
        html.Button("Help", id="help_btn", disabled = True),
    ])

left_menu = html.Div([
    html.H4("Timeline View"),
    html.Br(),
    html.A("List Users"),
    html.Br(),
    html.A("User's Timeline"),
    html.Br(),
    html.A("Raw Text"),
])

right_menu = html.Div()
