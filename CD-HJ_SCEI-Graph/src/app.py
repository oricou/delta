import warnings

warnings.filterwarnings("ignore")

import dash_layout

flask_app = dash_layout.flask_app
dash_app = dash_layout.dash_app

if __name__ == "__main__":
    dash_app.run_server(debug=True)
