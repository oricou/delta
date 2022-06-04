#!/usr/bin/env python3

from typing import Tuple

import dash
from dash import dcc, html, Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .get_data import get_train_data, get_population_data, get_cities, Coords


pd.options.plotting.backend = "plotly"


class TBGT:
    FRANCE_CENTER = (46.7110, 1.7191)
    RELATION_DEFAULT = "TOUTES LES LIGNES"
    COMMENT = """Sur le graphique de l'évolution du temps de trajet moyen des grandes lignes, nous pouvons observer 3 éléments interessants:
- La partie croissante et linéaire entre 1939 et 1950 est due au manque de données durant la seconde guerre mondiale et à la destruction d'une partie du réseau ferroviaire due à cette dernière
- La partie fluctuante vers la fin des années 50 est due à l'apparition de nombreuses nouvelles grandes lignes qui viennent chambouler la moyenne
- La forte décroissance à partir des années 80 peut être attribuée au déploiment du réseau TGV qui a fortement accéléré les trajets


Sur le graphique comparant la croissance démographique de Paris et des autres grandes villes, on peut observer que les deux courbes ont une forte corrélation inversement proportionnnelle. Par exemple, vers la fin des années 50, lorsque Paris souffrait d'une forte décroissance démographique, on observe l'effet inverse dans autres grandes villes de France. La création de nombreuses grandes lignes vers la fin des années 50 a sans doute faciliter l'émigration de nombreux parisiens, expliquant ainsi partiellement ce phénomène.

Regardons plus en détail la ligne `Paris - Montpellier` par exemple. On s'appercoit que dans les années 60, un développement significatif de cette ligne a permis de faire gagner à ses usagers 1h de temps de transports. Sur le plan démographique, la ville de Montpellier a dans les années qui ont suivi profiter d'une croissance importante. Cette corrélation semble assez forte et vaudrait le coup d'être étudier plus en détail pour mettre en évidence un potentiel lien de cause à effet."""

    def _get_relations_radio(self) -> dcc.RadioItems:
        relations = np.insert(pd.unique(self.train_df["Relations"]), 0, self.RELATION_DEFAULT)
        return html.Div([
            "Grandes lignes SNCF:",
            dcc.RadioItems(
                relations,
                value=self.RELATION_DEFAULT,
                id="relations",
                style={"font-size": "10px", "margin": "10px"}
            )
        ], style={"margin": "10px", "display": "inline-block", "width": "15%"})

    def _get_coords(self, src: str, dst: str) -> Tuple[Coords, Coords]:
        return (
            (self.cities[src][0], self.cities[dst][0]),
            (self.cities[src][1], self.cities[dst][1])
        )

    def _get_map_fig(self, relation: str = RELATION_DEFAULT) -> go.Figure:
        lat_coords, lon_coords = [], []
        cities_name = []
        if (relation != self.RELATION_DEFAULT):
            cities_name = relation.split(" - ")
            lat_coords, lon_coords = self._get_coords(*cities_name)

        with open("TBGT_population_vs_train_speed/.mapbox_token") as f:
            mapbox_access_token = f.read()

        fig = go.Figure(go.Scattermapbox(
            lat=[*lat_coords],
            lon=[*lon_coords],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(size=14),
            text=[*cities_name],
        ))

        fig.update_layout(
            margin=dict(l=30, r=10, t=100, b=100),
            title=f"Ligne: {relation}",
            hovermode="closest",
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=self.FRANCE_CENTER[0],
                    lon=self.FRANCE_CENTER[1]
                ),
                pitch=0,
                zoom=4.5
            )
        )

        return fig

    def _set_legend_and_margin(self, fig: go.Figure) -> None:
        fig.update_layout(
            margin=dict(l=30, r=30, t=60, b=10),
            legend=dict(yanchor="top", xanchor="right")
        )

    def _get_global_line_speed_fig(self) -> go.Figure:
        fig = self.train_df.groupby("Année").mean().interpolate(method='linear').plot()
        fig.update_xaxes(title_text="Années")
        fig.update_yaxes(title_text="Minutes")
        fig.update_layout(title="Evolution du temps de trajet moyen des grandes lignes en Frances")
        self._set_legend_and_margin(fig)

        return fig

    def _get_line_speed_fig(self, relation: str = RELATION_DEFAULT) -> go.Figure:
        if (relation == self.RELATION_DEFAULT):
            return self._get_global_line_speed_fig()

        relations_groups = self.train_df.groupby("Relations")
        relation_df = relations_groups.get_group(relation)
        relation_df = relation_df.set_index("Année")
        relation_df = relation_df.drop(columns="Relations").dropna()
        relation_df = relation_df.interpolate(method='spline', order=3)

        fig = relation_df.plot()
        fig.update_xaxes(title_text="Années")
        fig.update_yaxes(title_text="Minutes")
        fig.update_layout(title=f"Evolution du temps de trajet sur la ligne {relation}")
        self._set_legend_and_margin(fig)

        return fig

    def _get_global_pop_fig(self) -> go.Figure:
        category = {'0':'Province', 'PARIS': 'Paris'}
        global_pop_df = pd.concat([self.pop_df.loc[:, self.pop_df.columns != "PARIS"].mean(axis=1), self.pop_df["PARIS"]], axis=1)

        fig = global_pop_df.plot()
        fig.update_xaxes(title_text="Années", range=[1920, 2019])
        fig.update_yaxes(title_text="Croissance en %")
        fig.update_layout(title="Croissance de la population parisienne et provinciale")
        fig.for_each_trace(
            lambda t: t.update(name = category[t.name],
                               legendgroup = category[t.name],
                               hovertemplate = t.hovertemplate.replace(t.name, category[t.name]))
        )
        self._set_legend_and_margin(fig)

        return fig

    def _get_pop_fig(self, relation: str = RELATION_DEFAULT) -> go.Figure:
        if (relation == self.RELATION_DEFAULT):
            return self._get_global_pop_fig()

        min_date = self.train_df.groupby("Relations").get_group(relation).dropna()["Année"].iloc[0]

        fig = self.pop_df[relation.split(" - ")].plot()
        fig.update_xaxes(title_text="Années", range=[min_date, 2019])
        fig.update_yaxes(title_text="Croissance en %")
        fig.update_layout(title="Croissance de la population des deux villes")
        self._set_legend_and_margin(fig)

        return fig

    def _get_statistics_graph(self) -> html.Div:
        return html.Div([
            dcc.Graph(id="line_speed_fig", figure=self._get_line_speed_fig()),
            dcc.Graph(id="pop_fig", figure=self._get_pop_fig())
        ], style={"display": "inline-block", "width": "40%",
                  "position": "relative", "vertical-align": "top"})

    def __init__(self, application = None):
        self.train_df = get_train_data()
        self.pop_df = get_population_data()
        self.cities = get_cities()

        self.main_layout = html.Div(children=[
            html.H3(
                "Évolution de la population des villes françaises "
                "vis-à-vis du développement des grandes lignes SNCF"
            ),
            html.Div([
                self._get_relations_radio(),
                dcc.Graph(id="map_fig", figure=self._get_map_fig(),
                          style={"display": "inline-block", "width": "40%",
                                 "position": "relative", "vertical-align": "top",
                                 "height": "900px"}),
                self._get_statistics_graph()
            ]),
            dcc.Markdown(self.COMMENT)
        ], style={
            "backgroundColor": "white",
            "padding": "10px 50px 0px 0px",
        })

        if (application is not None):
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


        ### CALLBACKS ###
        self.app.callback(
            Output("map_fig", "figure"),
            Input("relations", "value")
        )(self._get_map_fig)

        self.app.callback(
            Output("pop_fig", "figure"),
            Input("relations", "value")
        )(self._get_pop_fig)

        self.app.callback(
            Output("line_speed_fig", "figure"),
            Input("relations", "value")
        )(self._get_line_speed_fig)
