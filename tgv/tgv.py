import os
import dash
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from typing import List, Dict, Callable, Any
import folium
import branca.colormap as cm
import utils


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
            .sum()
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

    def update_map_visibility(self, map) -> go.Figure:
        if (map == 'Trajet'):
            return {'display': 'block'}
        else:
            return {'display': 'none'}
        
    def update_hist_visibility(self, map) -> go.Figure:
        if (map == 'Trajet'):
            return {'display': 'none'}
        else:
            return {'display': 'block'}
        
    def update_map(self, year, colonne, filter) -> go.Figure:
        """
        Create graph mapping train stations and lines to the lateness of the trains
        """

        year += 2018
        france_line = folium.Map(location=[46.8, 2], zoom_start=6)
        max_traffic = self.df_trajet[colonne].max()
        min_traffic = self.df_trajet[colonne].min()
        df_trajet = self.df_trajet[(self.df_trajet.index == str(year)) & (self.df_trajet[colonne] >= filter[0]) & (self.df_trajet[colonne] <= filter[1])]
        colormap = cm.LinearColormap(
            ["green", "orange", "red"], vmin=min_traffic, vmax=max_traffic
        )
        france_line.add_child(colormap)

        for i in range(len(self.df_gares["WGS 84"])):
            france_line.add_child(
                folium.Marker(
                    location=self.df_gares["WGS 84"].iloc[i],
                    popup="Gare: {}<br>Région SNCF: {}<br>Coordonnées: {}".format(
                        self.df_gares["Gare"].iloc[i],
                        self.df_gares["Région SNCF"].iloc[i],
                        self.df_gares["WGS 84"].iloc[i],
                    ),
                    icon=folium.Icon(color="green"),
                )
            )

        for i in range(len(df_trajet["Coord_départ"])):

            traffic = df_trajet[colonne].iloc[i]
            folium.PolyLine(
                (
                    df_trajet["Coord_départ"].iloc[i],
                    df_trajet["Coord_arrivée"].iloc[i],
                ),
                color=colormap.rgb_hex_str(traffic),
                weight=traffic / max_traffic * 2 + 1,
                opacity=1,
                popup="{}: {}<br>Départ: {}<br>Arrivée: {}".format(
                    colonne,
                    df_trajet[colonne].iloc[i],
                    df_trajet["Gare de départ"].iloc[i],
                    df_trajet["Gare d'arrivée"].iloc[i],
                ),
            ).add_to(france_line)

        france_line.save("mymapnew.html")
        return open("mymapnew.html", "r").read()
    
    def update_hist(self, year, colonne, filter) -> go.Figure:
        year += 2018
        df_grouped =self.df_trajet[self.df_trajet.index == str(year)].groupby('Gare de départ').sum().reset_index()
        return px.histogram(df_grouped[(df_grouped[colonne] >= filter[0]) & (df_grouped[colonne] <= filter[1])], x='Gare de départ', y=colonne, histfunc='sum')
        # return px.histogram(self.df_trajet[(self.df_trajet.index == str(year)) & (self.df_trajet[colonne] >= filter[0]) & (self.df_trajet[colonne] <= filter[1])], x='Gare de départ', y=colonne, histfunc='sum')
    
    def update_filter(self, year, colonne, map) -> go.Figure:
        year += 2018
        if (map == 'Trajet'):
            df = self.df_trajet[self.df_trajet.index == str(year)][colonne]
        else :
            df = self.df_trajet[self.df_trajet.index == str(year)].groupby('Gare de départ').sum()[colonne]
        return df.min(), df.max()

    def __init__(self, application: dash.Dash = None):
        self.main_layout = utils.make_layout()
        self.make_df()
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
            
        self.app.callback(
            Output("tgv-main-graph", "style"),
			[Input("plot-switch", "value")]
		)(self.update_map_visibility)
        
        self.app.callback(
            Output("hist-graph", "style"),
			[Input("plot-switch", "value")]
		)(self.update_hist_visibility)

        self.app.callback(
            Output("tgv-main-graph", "srcDoc"),
            [Input("tgv-year-slider", "value"), Input("tgv-y-axis-dropdown", "value"), Input("debit-filter-type-slider", "value")],
        )(self.update_map)
        
        self.app.callback(
            Output("hist-graph", "figure"),
            [Input("tgv-year-slider", "value"), Input("tgv-y-axis-dropdown", "value"), Input("debit-filter-type-slider", "value")],
        )(self.update_hist)
        
        self.app.callback(
            Output("debit-filter-type-slider", "min"),
            Output("debit-filter-type-slider", "max"),
            [Input("tgv-year-slider", "value"), Input("tgv-y-axis-dropdown", "value"), Input("plot-switch", "value")],
        )(self.update_filter)

        

if __name__ == "__main__":
    tgv = TGV()
    tgv.app.run_server(debug=True, port=8051)
