import pandas as pd
import dash
from dash import html
from dash import dcc
from CB_MJS_naissance_deces_france import maps_2020

import plotly.express as px
import json


class Birth_Map:
    def __init__(self, application=None):

        self.carte_2020 = maps_2020.Carte(application)

        self.df = pd.read_pickle('data/naissances_par_dep_1970_2020.pkl')
        self.years = sorted(set(self.df.index.values))
        self.year = self.years[0]
        self.df_dict = {}
        self.departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        for year in self.df.index.values:
            self.df_dict.update({year: pd.read_pickle(f'data/population_birth_rate/{year}.pkl')})

        self.main_layout = html.Div(id='main-layout-page', children=[
            html.H2(children='Cartes des taux de natalité et mortalité par départements en France'),
            html.Br(),

            html.Div('Carte du taux de natalité par départements en France de 1970 à 2020'),
            html.Div([
                html.Div([dcc.Graph(id='map-selected-year'), ], style={'width': '90%', }),

                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(id='selected-year-slider', ),

                ], style={'margin-left': '15px', 'width': '7em', 'float': 'right'}),

            ], style={
                    'padding': '10px 50px',
                    'display':'flex',
                    'justifyContent':'center'
            }),
            dcc.Slider(
                id='map-year-slider',
                min=self.years[0],
                max=self.years[-1],
                step=1,
                value=self.years[0],
                marks={str(year): str(year) for year in self.years[::5]},
            ),

            html.Br(),
            html.Br(),

            dcc.Markdown("""
            Déplacez le slider pour afficher la carte de l'année correspondante.
            Survolez un département avec votre souris pour afficher plus d'informations.
            
            Note:
               * Le taux de natalité correspond au nombre de naissances par rapport au nombre total de la population
               * Lecture: une couleur foncé signifie un faible taux de natalité (peu de naissances par rapport à la population), une couleur claire un haut taux de natalité.
               * En 1970, le taux de natalité dans le département de la Cher (18) est de 12,3 pour 1000. La population y est de 304400 et les naissances sur l'année s'élèvent à 3759.
            
            Sources:
               * Naissances: https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
               * Population: https://www.insee.fr/fr/statistiques/1893204#consulter.

            A noter que les données sources des naissances sont celle des prénoms attribués sur l'année, mais qu'elle est présentée comme correspondant aux naissances sur l'année [sur le site de data.gouv](https://www.data.gouv.fr/fr/datasets/fichier-des-prenoms-de-1900-a-2019/).
            Cependant, au vu de l'incohérence de ces données avec d'autres que j'ai pu trouvé sur des années spécifique, les valeurs pour les naissances annuelles sont à prendre avec beaucoup de précaution.
            """),

            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

            html.Div(children=self.carte_2020.main_layout),

        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px'
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('map-selected-year', 'figure'),
            dash.dependencies.Input('map-year-slider', 'value'))(self.update_map)

        self.app.callback(
            dash.dependencies.Output('selected-year-slider', 'children'),
            dash.dependencies.Input('map-year-slider', 'value'))(self.update_year)


    def update_year(self, year):
        self.year = year
        return f'Année selectionnée {self.year}'


    def update_map(self, year):
        if year == None:
            year = self.year
        year_df = self.df_dict.get(year)

        fig = px.choropleth_mapbox(year_df, geojson=self.departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='tx_nat_p_1000',
                                   hover_name='DEPNAME',
                                   hover_data=['tx_nat_p_1000', 'naissances', 'Total'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   labels={'DEP': 'Numéro du département',
                                           'tx_nat_p_1000': 'Taux de natalité (pour 1000)',
                                           'naissances': 'Nombre de naissances',
                                           'Total': 'Population du département'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
