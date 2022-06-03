import flask
import dash_bootstrap_components as dbc
import dash

from tab_classes_preparatoires.classes_preparatoires import Tab_classes_preparatoires
from tab_grandes_ecoles.grandes_ecoles import Tab_grandes_ecoles
from tab_a_propos.a_propos import Tab_a_propos


class SCEI_graph:
    def __init__(self, dash_app=None):
        if dash_app is not None:
            self.app = dash_app
        else:
            flask_app = flask.Flask(__name__)
            self.app = dash.Dash(
                "SCEI", server=flask_app, external_stylesheets=[dbc.themes.ZEPHYR]
            )

        self.tab_classes_preparatoires = Tab_classes_preparatoires(dash_app)
        self.tab_grandes_ecoles = Tab_grandes_ecoles(dash_app)
        self.tab_a_propos = Tab_a_propos(dash_app)

        self.main_layout = dash.html.Div(
            [
                dash.html.H1(
                    "Impact du lieu de formation sur les intégrations aux Grandes Ecoles",
                    style={"text-align": "center"},
                ),
                dash.dcc.Tabs(
                    id="tabs",
                    value="tab-classes-preparatoires",
                    children=[
                        dash.dcc.Tab(
                            label="Classes préparatoires",
                            value="tab-classes-preparatoires",
                        ),
                        dash.dcc.Tab(
                            label="Grandes Ecoles", value="tab-grandes-ecoles"
                        ),
                        dash.dcc.Tab(label="A propos", value="tab-a-propos"),
                    ],
                ),
                dash.html.Div(id="tab-content"),
            ]
        )

        self.app.layout = self.main_layout

        @self.app.callback(
            dash.Output("tab-content", "children"),
            dash.Input("tabs", "value"),
        )
        def render_content(tab):
            if tab == "tab-classes-preparatoires":
                return self.tab_classes_preparatoires.layout
            elif tab == "tab-grandes-ecoles":
                return self.tab_grandes_ecoles.layout
            elif tab == "tab-a-propos":
                return self.tab_a_propos.layout
