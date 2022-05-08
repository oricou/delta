import numpy as np
import pandas as pd
import dash
from dash import html
from dash import dcc

import plotly.express as px
import json


class Carte(object):
    def __init__(self, application=None):

        self.df = pd.read_pickle('data/deces_par_departements2020.pkl')

        self.df_naiss = pd.read_pickle('data/naissances_par_departements2020.pkl')

        departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        fig = px.choropleth_mapbox(self.df, geojson=departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='deces pour 10000',
                                   hover_name='DEP_NAME',
                                   hover_data=['deces pour 10000', 'DECES', 'population'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   labels={'DEP': 'Numéro du département',
                                           'deces pour 10000': 'Part des décès pour 1000',
                                           'DECES': 'Nombre de décès',
                                           'population': 'Population du département'}
                                   )

        fig2 = px.choropleth_mapbox(self.df_naiss, geojson=departements,
                                    locations='DEP', featureidkey='properties.code',  # join keys
                                    color='Naissances pour 10000',
                                    hover_name='DEP_NAME',
                                    hover_data=['Naissances pour 10000', 'NAISSANCES', 'population'],
                                    color_continuous_scale="Viridis",
                                    mapbox_style="carto-positron",
                                    zoom=4.6, center={"lat": 47, "lon": 2},
                                    opacity=0.5,
                                    labels={'DEP': 'Numéro du département',
                                            'Naissances pour 10000': 'Part des naissances pour 1000',
                                            'NAISSANCES': 'Nombre de naissances',
                                            'population': 'Population du département'}
                                    )

        self.main_layout = html.Div(children=[
            html.Br(),
            html.Div(children=[
                html.Div(children=[
                    html.Div('Carte du taux de mortalité par département en France en 2020'),
                    dcc.Graph(
                        id='wps-main-graph',
                        figure=fig
                    )
                ], style={'flex': 1}),
                html.Div(children=[
                    html.Div('Carte du taux de natalité par département en France en 2020'),
                    dcc.Graph(
                        id='wps-main-graph2',
                        figure=fig2
                    )
                ], style={'flex': 1}),

            ], style={
                'padding': '5',
                'display': 'flex',
                'flex-direction': 'row',
                'justifyContent': 'center'}
            ),
            html.Br(),

            dcc.Markdown("""
        Survolez un département avec votre souris pour afficher plus d'informations.

        Note:
           * Le taux de natalité correspond au nombre de naissances par rapport au nombre total de la population
           * Lecture: une couleur foncé signifie un faible taux de natalité (peu de naissances par rapport à la population), une couleur claire un haut taux de natalité.
           * Lecture: En 2020, le taux de mortalité dans le département de la Charente (16) est de 12,1 pour 1000. La population y est de 348180 et les décès sur l'année s'élèvent à 4225.

        Sources:
           * Décès 2020: https://www.insee.fr/fr/statistiques/5431034?sommaire=5419788&q=d%C3%A9c%C3%A8s
           * Naissances 2020: https://www.insee.fr/fr/statistiques/5419785
           * Population 2020: https://www.insee.fr/fr/statistiques/fichier/4277596/T20F013.xlsx\
        """),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 30px 10px 30px'
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
