import flask
from dash import (
    Dash,
)

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from CDHJ_SCEI.src.SCEI_graph import SCEI_graph

flask_app = flask.Flask(__name__)
app = Dash("SCEI", server=flask_app)

SCEI_graph(app)

if __name__ == "__main__":
    app.run_server(debug=True)
