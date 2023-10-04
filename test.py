import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dash_table,dcc
import dash_bootstrap_components as dbc
from functions import *
from dash import Input, Output, html

nav = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Internal link", href="/l/components/nav"),
                dbc.NavLink("External link", href="https://github.com"),
                dbc.NavLink(
                    "External relative",
                    href="/l/components/nav",
                    external_link=True,
                ),
                dbc.NavLink("Button", id="button-link", n_clicks=0),
            ]
        ),
        html.Br(),
        html.P(id="button-clicks"),
    ]
)

app = Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(nav, md=3),
            dbc.Col(html.Div(id="content")),
        ]
    ),
)

@app.callback(
    Output("button-clicks", "children"), [Input("button-link", "n_clicks")]
)
def show_clicks(n):
    return "Button clicked {} times".format(n)

if __name__ == '__main__':
    app.run(debug=True)

