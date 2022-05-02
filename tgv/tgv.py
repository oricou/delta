import os
import dash
import flask
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from typing import List, Dict, Callable, Any


class TGV:

    cur_path = os.path.dirname(__file__)
    regu_data_path = os.path.join(cur_path, "data", "regularite-mensuelle-tgv-aqst.csv")
    gares_data_path = os.path.join(cur_path, "data", "referentiel-gares-voyageurs.csv")
    a_propos_path = os.path.join(cur_path, "data", "a-propos.md")

    def make_df(self) -> pd.DataFrame:
        df = (
            pd.read_csv(self.regu_data_path, delimiter=";")
            .dropna(axis=1)
            .drop_duplicates()
            .drop("Service", axis=1)
        )
        coord = (
            pd.read_csv(self.gares_data_path, delimiter=";")
            .drop(["Date fin validité plateforme", "SOPs"], axis=1)
            .dropna()
            .transform(
                {
                    "Région SNCF": lambda s: "ILE DE FRANCE"
                    if "PARIS" in s
                    else s.replace("REGION ", ""),
                    "UT": lambda s: str(s).replace(" GARE", ""),
                    "Intitulé fronton de gare": lambda s: str(s).upper(),
                }
            )
        )

        gares = pd.DataFrame(df["Gare de départ"].unique(), columns=["Gare"])
        gares_1 = (
            pd.merge(
                gares,
                coord[["UT", "Région SNCF", "WGS 84"]],
                left_on="Gare",
                right_on="UT",
                how="left",
            )
            .drop("UT", axis=1)
            .dropna()
            .drop_duplicates()
        )
        gares_2 = (
            pd.merge(
                gares,
                coord[["Intitulé fronton de gare", "Région SNCF", "WGS 84"]],
                left_on="Gare",
                right_on="Intitulé fronton de gare",
                how="left",
            )
            .drop("Intitulé fronton de gare", axis=1)
            .dropna()
            .drop_duplicates()
        )
        gares = pd.concat([gares_1, gares_2]).drop_duplicates()

        df_coord = (
            pd.merge(
                df,
                gares,
                left_on="Gare de départ",
                right_on="Gare",
                how="left",
                suffixes=(None, "_départ"),
            )
            .drop("Gare", axis=1)
            .dropna()
            .drop_duplicates()
            .rename(
                {"WGS 84": "Coord_départ", "Région SNCF": "Région_départ"},
                axis=1,
            )
        )
        df_coord = (
            pd.merge(
                df_coord, gares, left_on="Gare d'arrivée", right_on="Gare", how="left"
            )
            .drop("Gare", axis=1)
            .dropna()
            .drop_duplicates()
            .rename(
                {"WGS 84": "Coord_arrivée", "Région SNCF": "Région_arrivée"},
                axis=1,
            )
        )

    def make_layout(self) -> html.Divt:
        return html.Div(
            children=[
                html.H3(children="Régularité des Grandes Lignes de TGV de la SNCF"),
                html.Div(
                    [
                        dcc.Graph(id="tgv-main-graph"),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Div(
                    [
                        dcc.RadioItems(
                            id="tgv-mean",
                            options=[
                                {"label": "Courbe seule", "value": 0},
                                {"label": "Tendence générale", "value": 1},
                                {
                                    "label": "Moyenne journalière (les décalages au 1er janv. indique la tendence)",
                                    "value": 2,
                                },
                            ],
                            value=0,
                            labelStyle={"display": "block"},
                        ),
                    ]
                ),
                html.Br(),
                dcc.Markdown(open(self.a_propos_path).read()),
            ],
            style={
                "backgroundColor": "white",
                "padding": "10px 50px 10px 50px",
            },
        )

    def update_graph(self):
        pass

    def __init__(self, application: dash.Dash = None):
        self.main_layout = self.make_layout()
        self.df = self.make_df()

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(Output("tgv-main-graph", "figure"), [])(self.update_graph)


if __name__ == "__main__":
    nrg = TGV()
    nrg.app.run_server(debug=True, port=8051)
