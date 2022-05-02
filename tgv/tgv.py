import os
from re import X
from threading import local
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
import folium


class TGV:

    cur_path = os.path.dirname(__file__)
    regu_data_path = os.path.join(cur_path, "data", "regularite-mensuelle-tgv-aqst.csv")
    gares_data_path = os.path.join(cur_path, "data", "referentiel-gares-voyageurs.csv")
    a_propos_path = os.path.join(cur_path, "a-propos.md")

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
        )

        coord["Région SNCF"] = (
            coord["Région SNCF"]
            .astype(str)
            .map(
                lambda s: "ILE DE FRANCE" if "PARIS" in s else s.replace("REGION ", "")
            )
        )
        coord["UT"] = coord["UT"].astype(str).map(lambda s: s.replace(" GARE", ""))
        coord["Intitulé fronton de gare"] = (
            coord["Intitulé fronton de gare"].astype(str).map(lambda s: s.upper())
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

        gares["WGS 84"] = gares["WGS 84"].map(lambda x: tuple(map(float, x.split(","))))
        df_coord["Date"] = pd.to_datetime(df_coord["Date"])
        df_coord.set_index("Date", inplace=True)

        df_trajet = (
            df_coord.groupby(
                [df_coord.index.to_period("Y"), "Gare de départ", "Gare d'arrivée"]
            )
            .mean()
            .reset_index()
        )
        df_trajet = (
            pd.merge(
                df_trajet,
                gares[["Gare", "WGS 84"]],
                left_on="Gare de départ",
                right_on="Gare",
                how="left",
            )
            .drop("Gare", axis=1)
            .dropna()
            .drop_duplicates()
        )
        df_trajet.rename({"WGS 84": "Coord_départ"}, axis=1, inplace=True)
        df_trajet = (
            pd.merge(
                df_trajet,
                gares[["Gare", "WGS 84"]],
                left_on="Gare d'arrivée",
                right_on="Gare",
                how="left",
            )
            .drop("Gare", axis=1)
            .dropna()
            .drop_duplicates()
            .set_index("Date")
        )
        df_trajet.rename({"WGS 84": "Coord_arrivée"}, axis=1, inplace=True)

        self.df_coord = df_coord
        self.df_gares = gares
        self.df_trajet = df_trajet

    def make_layout(self) -> html.Div:
        return html.Div(
            children=[
                html.H3(children="Régularité des Grandes Lignes de TGV de la SNCF"),
                html.Div(
                    [
                        html.Iframe(
                            id="tgv-main-graph", srcDoc=None, width="100%", height="600"
                        ),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Div(
                    [
                        dcc.Slider(
                            0,
                            4,
                            1,
                            id="year-slider",
                            marks={i: str(i) for i in range(4)},
                            value=2,
                            updatemode='drag'
                        )
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

    def update_graph(self, year) -> go.Figure:
        """
        Create graph mapping train stations and lines to the lateness of the trains
        """

        year += 2018
        france_line = folium.Map(location=[46.8, 2], zoom_start=6)        
        df_trajet = self.df_trajet[self.df_trajet.index == str(year)]
        type_color = "green"
        
        for i in range(len(self.df_gares["WGS 84"])):
            france_line.add_child(
                folium.Marker(
                    location=self.df_gares["WGS 84"].iloc[i],
                    popup="Gare: "
                    + self.df_gares["Gare"].iloc[i]
                    + "<br>"
                    + "Région SNCF: "
                    + self.df_gares["Région SNCF"].iloc[i]
                    + "<br>"
                    + "Coordinates: "
                    + str(self.df_gares["WGS 84"].iloc[i]),
                    icon=folium.Icon(color="%s" % type_color),
                )
            )

        max_traffic = df_trajet["Nombre de circulations prévues"].max()

        list_colors = [
            "#0000FF",
            "#1200FF",
            "#2400FF",
            "#3500FF",
            "#4700FF",
            "#5800FF",
            "#6A00FF",
            "#7C00FF",
            "#8D00FF",
            "#9F00FF",
            "#B000FF",
            "#C200FF",
            "#D400FF",
            "#E500FF",
            "#F700FF",
            "#FF00F6",
            "#FF00E4",
            "#FF00D3",
            "#FF00C1",
            "#FF00AF",
            "#FF009E",
            "#FF008C",
            "#FF007B",
            "#FF0069",
            "#FF0057",
            "#FF0046",
            "#FF0034",
            "#FF0023",
            "#FF0011",
            "#FF0000",
        ]
        color_dict = {i: list_colors[i] for i in range(len(list_colors))}
        for i in range(len(df_trajet["Coord_départ"])):
            
            traffic = df_trajet['Nombre de circulations prévues'].iloc[i]
            folium.PolyLine(
                (
                    df_trajet["Coord_départ"].iloc[i],
                    df_trajet["Coord_arrivée"].iloc[i],
                ),
                color=color_dict[round(traffic/max_traffic * (len(list_colors)-1))],
                weight=df_trajet["Nombre de circulations prévues"].iloc[i]
                / max_traffic
                * 3,
                opacity=1,
            ).add_to(france_line)

        france_line.save("mymapnew.html")
        return open("mymapnew.html", "r").read()

    def __init__(self, application: dash.Dash = None):
        self.main_layout = self.make_layout()
        self.make_df()
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output("tgv-main-graph", "srcDoc"),
            [dash.dependencies.Input("year-slider", "value")],
        )(self.update_graph)


if __name__ == "__main__":
    tgv = TGV()
    tgv.app.run_server(debug=True, port=8051)
