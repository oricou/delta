import flask

flask_app = flask.Flask(__name__)
import dash_bootstrap_components as dbc
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)

dash_app = Dash("SCEI", server=flask_app, external_stylesheets=[dbc.themes.ZEPHYR])

from tab_classes_preparatoires.classes_preparatoires import tab_classes_preparatoires
from tab_grandes_ecoles.grandes_ecoles import tab_grandes_ecoles
from tab_a_propos.a_propos import tab_a_propos

dash_app.layout = html.Div(
    [
        html.H1(
            "Impact du lieu de formation sur les intégrations aux Grandes Ecoles",
            style={"text-align": "center"},
        ),
        dbc.Tabs(
            [
                dbc.Tab(tab_classes_preparatoires, label="Classes préparatoires"),
                dbc.Tab(tab_grandes_ecoles, label="Grandes Ecoles"),
                # dbc.Tab(tab_classes_preparatoires, label="Synthèse"),
                dbc.Tab(tab_a_propos, label="A propos"),
            ]
        ),
    ]
)
