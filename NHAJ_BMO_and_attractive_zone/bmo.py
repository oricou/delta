import sys
import flask
import json
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import dateutil as du


class Bmo():
    def _make_dataframe_from_csv(filename):
        df = pd.read_csv(filename)
        return df

    def __init__(self, application=None):

        self.data = Bmo._make_dataframe_from_csv(
            "NHAJ_BMO_and_attractive_zone/data/population_et_projets_recrutement_2015_2021.csv")

        self.departements = json.load(
            open("NHAJ_BMO_and_attractive_zone/data/departements-avec-outre-mer.geojson"))

        self.main_layout = html.Div(
            [
                html.H1('Besoin en main d\'oeuvre et population en France'),

                html.H4("Repartition des offres d'emplois en France."),
                dcc.Graph(id="graph", figure=self.display_map()),

                html.H4("Repartion du nombre d'offres par habitant en France."),
                dcc.Graph(id="graph 2", figure=self.display_map_jobs_to_pop()),
                html.P("Ici on observe le ratio entre les offre d'emplois et la population pour chaques départements."
                       "On pourra remarquer que les départementss avec le moins d'offres ne sont pas forcement les moins attractif quand on prend en compte le nombre d'habitants"),

                html.H4("Pourcentage de population pour chaque département en"
                        "fonction du temps."),
                html.P(
                    "Choisissez la prioprioté par rapport a laquelle vous souhaitez trier les données"),
                dcc.Dropdown(["population", "projets de recrutement totaux",
                             "job offers to population ratio"], 'population', id='dropdown'),
                dcc.Graph(id="graph 3"),
                html.P("On voit encore une fois ici que les zones les plus peuplé (Paris par exemple) ne sont pas forcement les plus attractive si l'on souhaite répondre a une offre d'emploi."),

                dcc.Markdown("""
                        #### À propos

                        * Repartition de la Population : [Insee](https://www.insee.fr/fr/statistiques/1893198)
                        * Répartition des offres d'emploi : [Pole Emploi](https://www.data.gouv.fr/en/datasets/enquete-besoins-en-main-doeuvre-bmo/)
                        * (c) 2022 Nathan Habib - Alexis Julien
                        """),
            ])

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(Output('graph 3', 'figure'), Input(
            'dropdown', 'value'))(self.get_fig_pop_recrutement)

    def display_map(self):

        fig = px.choropleth_mapbox(
            self.data,
            geojson=self.departements,
            locations="code departement",
            featureidkey="properties.code",
            color="projets de recrutement %",
            color_continuous_scale="Bluered",
            mapbox_style="carto-positron",
            zoom=4.2,
            center={"lat": 47, "lon": 2},
            animation_frame="année",
            opacity=0.5,)

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(height=600)

        return fig

    def get_fig_pop_recrutement(self, value):
        fig = px.scatter(self.data.sort_values(by=value), x="nom departement_x", y=[
                         "population %", "projets de recrutement %"], animation_frame="année")
        return fig

    def display_map_jobs_to_pop(self):

        fig = px.choropleth_mapbox(
            self.data,
            geojson=self.departements,
            locations="code departement",
            featureidkey="properties.code",  # join keys
            color="job offers to population ratio",
            color_continuous_scale="Bluered",
            mapbox_style="carto-positron",
            zoom=4.2,
            center={"lat": 47, "lon": 2},
            animation_frame="année",
            opacity=0.5,)

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(height=600)

        return fig


if __name__ == '__main__':
    nrg = Bmo()
    nrg.app.run_server(debug=True, port=8051)
