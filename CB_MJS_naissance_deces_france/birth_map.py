import pandas as pd
import dash
from dash import html
from dash import dcc

import plotly.express as px
import json


class Birth_Map:
    def __init__(self, application=None):

        self.df = pd.read_pickle('data/naissances_par_dep_1970_2020.pkl')
        self.years = sorted(set(self.df.index.values))
        self.year = self.years[0]
        self.df_dict = {}
        self.departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        for year in self.df.index.values:
            self.df_dict.update({year: pd.read_pickle(f'data/population_birth_rate/{year}.pkl')})

        self.main_layout = html.Div(children=[
            html.H2(children='Cartes de France'),
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
            )

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
