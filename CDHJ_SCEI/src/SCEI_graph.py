import flask
import dash_bootstrap_components as dbc
from dash import (
    Dash,
    html,
)

from tab_classes_preparatoires.classes_preparatoires import Tab_classes_preparatoires
from tab_grandes_ecoles.grandes_ecoles import Tab_grandes_ecoles
from tab_a_propos.a_propos import Tab_a_propos


class SCEI_graph:
    def __init__(self, dash_app=None):
        if dash_app is not None:
            self.app = dash_app
        else:
            flask_app = flask.Flask(__name__)
            self.app = Dash(
                "SCEI", server=flask_app, external_stylesheets=[dbc.themes.ZEPHYR]
            )

        self.tab_classes_preparatoires = Tab_classes_preparatoires(dash_app)
        self.tab_grandes_ecoles = Tab_grandes_ecoles(dash_app)
        self.tab_a_propos = Tab_a_propos(dash_app)

        self.main_layout = html.Div(
            [
                html.H1(
                    "Impact du lieu de formation sur les intégrations aux Grandes Ecoles",
                    style={"text-align": "center"},
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(
                            self.tab_classes_preparatoires.layout,
                            label="Classes préparatoires",
                        ),
                        dbc.Tab(self.tab_grandes_ecoles.layout, label="Grandes Ecoles"),
                        dbc.Tab(self.tab_a_propos.layout, label="A propos"),
                    ]
                ),
            ]
        )

        self.app.layout = self.main_layout
