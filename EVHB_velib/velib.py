import functools
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
import glob


print("zbruh")


class Velib:
    START = "Start"
    STOP = "Stop"

    def left_axis(self):
        csv_day_usage = pd.read_csv("data/EVHB_velib/col_sum_velib.csv", sep=";")

        def convert_date(x: str):
            _, a, b = x.split("_")
            a, b = float(a), float(b)
            return str(int(a)) + "h00"

        csv_day_usage["hour"] = csv_day_usage["hour"].apply(convert_date)
        fig_day_usage = px.line(
            csv_day_usage, x="hour", y="avail. bike", title="Disponibilité des vélibs (24h)",
            labels={"hour": "Horaire", "avail. bike": "Vélo(s) disponible(s)"}
        )
        fig_day_usage.update_xaxes(tickformat=f"%{{hour}}", nticks=6)
        return fig_day_usage

    def right_axis(self):
        csv_diff = pd.read_csv("data/EVHB_velib/col_diff_velib.csv", sep=";")

        def convert_date(x: str):
            _, a, b = x.split("_")
            a, b = float(a), float(b)
            return str(int(a)) + "h" + ("00" if b < 30 else "30")

        csv_diff["hour"] = csv_diff["hour"].apply(convert_date)
        fig_day_usage = px.line(
            csv_diff, x="hour", y="diff", title="Évolution d'usage (24h)",
            labels={"hour": "Horaire", "diff": "Variations(s) en vélo"}
        )
        fig_day_usage.update_xaxes(tickformat=f"%{{hour}}", nticks=6)
        return fig_day_usage

    def update_graph(self, time, key="ratio_avail"):
        if not type(time) in [int, float]:
            print("ERROR", time)
            return self.fig_map

        idx = int(self.len_map * (min(time, 24) / 24))

        self.fig_map["data"][0]["z"] = self.map_df[idx][key] * 100
        self.fig_map.update_traces(
            hovertemplate=f"Disponibilité station: <b>%{{z:.2f}}%</b><br>Vélo(s) disponilible(s): %{{customdata}}",
            customdata=self.map_df[idx]["avail. bike"],
        )

        return self.fig_map

    def on_interval(self, n_intervals, hour, text):
        if text == self.STOP:
            if hour >= 24:
                return 0
            return hour + 0.5
        return hour

    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    def __init__(self, application=None):
        with open("data/EVHB_velib/communes.json") as f:
            communes = json.load(f)

        key = "ratio_avail"
        sorted_files = sorted(
            glob.glob("data/EVHB_velib/data_2022_03_11_*[05]_velib.csv")
        )
        map_df = [pd.read_csv(f, sep=";", dtype={"arrond": str}) for f in sorted_files]
        len_map = len(map_df) - 1
        zmin = min(map(lambda x: x[key].sort_values()[2:-2].min(), map_df)) * 100
        zmax = max(map(lambda x: x[key].sort_values()[2:-2].max(), map_df)) * 100

        fig_map = go.Figure(
            go.Choroplethmapbox(
                geojson=communes,
                locations=map_df[0].arrond,
                z=map_df[0][key],
                colorscale="Viridis",
                zmin=zmin,
                zmax=zmax,
                colorbar=dict(title="Disponibilité station en %"),
                marker_opacity=0.5,
                marker_line_width=0,
            )
        )

        # 48.852966,2.349902,11z (Notre-Dame de Paris)
        fig_map.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=11,
            mapbox_center={"lat": 48.859966, "lon": 2.349902},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        self.len_map = len_map
        self.map_df = map_df
        self.fig_map = fig_map
        self.fig_day_usage = self.left_axis()
        self.fig_day_update = self.right_axis()

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)

        # Auto stepper
        self.app.callback(
            dash.dependencies.Output("velib-button-start-stop", "children"),
            dash.dependencies.Input("velib-button-start-stop", "n_clicks"),
            dash.dependencies.State("velib-button-start-stop", "children"),
        )(self.button_on_click)

        self.app.callback(
            dash.dependencies.Output("velib-crossfilter-year-slider", "value"),
            dash.dependencies.Input("velib-auto-stepper", "n_intervals"),
            dash.dependencies.Input("velib-crossfilter-year-slider", "value"),
            dash.dependencies.Input("velib-button-start-stop", "children"),
        )(self.on_interval)

        # # Slider
        self.app.callback(
            dash.dependencies.Output("velib-main-graph", "figure"),
            [dash.dependencies.Input("velib-crossfilter-year-slider", "value")],
        )(self.update_graph)

        self.main_layout = html.Div(
            children=[
                html.H3(
                    "Évolution de la répartition des vélibs' sur une journée en Île-de-France"
                ),
                html.Br(),
                html.P(
                    "La carte est interactive. Passer le curseur sur les communes indiquera leur code postal. Le slider situé en-dessous permet de visualiser l'évolution de l'utilisation des Vélibs' selon la zone.",
                    style={"textAlign": "center"},
                ),
                dcc.Markdown(
                    """
                ⚠️ **Attention** à ne pas faire défiler le curseur trop rapidement auquel cas les données n'auront pas le temps de charger.
                """,
                    style={"textAlign": "center"},
                ),
                html.Br(),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="velib-main-graph",
                                    figure=self.update_graph(0),
                                    style={"height": "60vh"},
                                )
                            ],
                            style={"width": "90%"},
                        )
                    ],
                    style={
                        "padding": "10px 50px",
                        "display": "flex",
                        "justifyContent": "center",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            self.START,
                            id="velib-button-start-stop",
                            style={"display": "inline-block"},
                        ),
                        html.Div(
                            dcc.Slider(
                                updatemode="drag",
                                id="velib-crossfilter-year-slider",
                                min=0,
                                max=24,
                                step=0.05,
                                value=5,
                                marks={
                                    str(year): str(year) + "h00"
                                    for year in range(0, 25)
                                },
                            ),
                            style={"display": "inline-block", "width": "90%"},
                        ),
                        dcc.Interval(  # fire a callback periodically
                            id="velib-auto-stepper",
                            interval=750,  # in milliseconds
                            n_intervals=0,
                        ),
                    ],
                    style={"padding": "0px 50px", "width": "100%"},
                ),
                html.Br(),
                html.Div(
                    [
                        dcc.Graph(
                            id="wps-income-time-series",
                            style={"width": "50%", "display": "inline-block"},
                            figure=self.fig_day_usage,
                        ),
                        dcc.Graph(
                            id="wps-fertility-time-series",
                            style={
                                "width": "50%",
                                "display": "inline-block",
                                "paddingLeft": "0.5%",
                            },
                            figure=self.fig_day_update,
                        ),
                    ],
                    style={
                        "display": "flex",
                        "borderTop": "thin lightgrey solid",
                        "borderBottom": "thin lightgrey solid",
                        "justifyContent": "center",
                    },
                ),
                html.Br(),
                dcc.Markdown(
                    """
                    # Motivations
                    Nous étions intéressés dès le début par une étude géographique. Les déplacements quotidiens, notamment ceux à vélos nous semblaient être pertinents à présenter.

                    C'est ainsi que nous avons choisi d'observer l'évolution de l'utilisation des stations vélibs en Île-de-France sur une journée.

                    # Sources
                    * [OpenData Vélib en temps réel](https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/information/) (emplacement des stations Vélib, capacité, emplacement et disponibilité)
                    * [OpenData Communes de France](https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/api/) (superficie et population des communes)
                    * [GeoJSON France](https://france-geojson.gregoiredavid.fr/) (délimitations géographiques des communes)

                    # Notes
                    * Différentes étapes ont été nécessaires au processus de récupération et d'interprétation des données, tout d'abord avec sa collecte.
                    * La Ville de Paris propose un accès à de nombreuses données des stations Vélib, dont leur capacité, leur utilisation, les vélos disponibles, etc.
                    * Plusieurs scripts ont été nécessaires afin de *nettoyer* ces données, que nous avons récupéré continuellement sur une période de 2 jours à 1 minute d'intervalle (~850Mo).
                    * Pour chacune des stations Vélib, nous avons fait correspondre les coordonnées géographiques avec celles issues de GeoJSON pour les localiser sur le viewer.
                    * Enfin, il a fallu à partir d'une autre API récupérer la superficie et population totale de ces communes pour les mettre en lien avec les données des stations Vélib.

                    # Auteurs
                    * Erwan VIVIEN (<erwan.vivien@epita.fr>)
                    * Hugo BOIS (<hugo.bois@epita.fr>)
                    """
                ),
                html.Br(),
                html.Br(),
                dcc.Markdown("© 2022 Erwan Vivien & Hugo Bois")

            ],
            style={
                "backgroundColor": "white",
                "padding": "10px 50px 10px 50px",
            },
        )
        if not application:
            self.app.layout = self.main_layout


if __name__ == "__main__":
    velib = Velib()
    velib.app.run_server(debug=True, port=8051)
