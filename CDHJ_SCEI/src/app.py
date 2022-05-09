import flask
import dash_bootstrap_components as dbc
from dash import (
    Dash,
)

from CDHJ_SCEI.src.SCEI_graph import SCEI_graph

flask_app = flask.Flask(__name__)
app = Dash("SCEI", server=flask_app, external_stylesheets=[dbc.themes.ZEPHYR])

SCEI_graph(app)

if __name__ == "__main__":
    app.run_server(debug=True)
