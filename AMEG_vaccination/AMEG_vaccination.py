import sys
import dash
import flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from text import *


def load_vaccinations(filename):
    df = pd.read_csv(filename)
    # On supprime les vaccinations datant d'avant le 1er janvier 2021 pour éviter des bugs
    df = df[df['date'] >= '2021-01-01']
    # On met la date en index
    df = df.set_index('date')
    return df


def load_pib(filename):
    df = pd.read_csv(filename)
    df = df[df["Year"] == 2016]
    df = df.drop(["Country Name", "Year"], axis=1)
    df = df.rename(columns={"Country Code": "iso_code", "Value": "PIB"})
    df['PIB'] = df['PIB'].astype(float) / 1e9
    return df


class Vaccinations:

    def __init__(self, application=None):

        self.cols = [
            'Code ISO Pays',
            'Date',
            'Vaccinations totales',
            'Personnes vaccinées',
            'Personnes totalement vaccinées',
            'Total de boosters',
            'Vaccinations quotidiennes brutes',
            'Vaccinations quotidiennes nettes',
            'Vaccinations pour 100 habitants',
            'Personnes vaccinées pour 100 habitants',
            'Personnes totalement vaccinées pour 100 habitants',
            'Total de boosters pour 100 habitants',
            'Vaccinations quotidiennes pour 1M habitants',
            'Personnes vaccinées quotidiennement',
            'Personnes vaccinées quotidiennement pour 100 habitants',
            "PIB",
        ]
        # Chargement des données
        self.vaccinations = load_vaccinations("data/vaccinations.csv")
        self.pib = load_pib("data/gdp.csv")
        self.data = self.vaccinations.merge(self.pib, how="left", on="iso_code")

        self.pays = self.vaccinations['location'].unique()
        self.dates = self.vaccinations.index.unique().sort_values()

        # HTML
        self.main_layout = html.Div(children=[
            # Titre
            html.H1(children=txt_title,
                    style={'font-family': 'Helvetica', 'color': '#ffffff', 'text-align': 'center'}),
            html.P(children='''On va présenter ci-dessous les liens entre les taux de vaccinations contre le COVID-19
            et le PIB des pays.'''),

            # Analyse du dataset de vaccinations
            html.H2(children='1. Vaccinations contre le COVID-19 par pays en fonction du temps'),
            html.P(children='''Nous commençons par afficher l'évolution des taux de vaccination par pays en fonction du
            temps.'''),
            # Sélecteur de pays
            html.P(children='Sélectionner un pays ou une zone géographique :'),
            dcc.Dropdown(self.pays, id='pays', value='World',
                         style={'margin': '20px 0px', 'width': '300px', 'color': 'black'}),
            # Graphiques par pays
            html.Div([dcc.Graph(id='graph-1'), ], style={'width': '100%', }),
            html.Div([dcc.Graph(id='graph-2'), ], style={'width': '100%', }),
            html.Div([dcc.Graph(id='graph-3'), ], style={'width': '100%', }),

            html.H2(children='2. Evolution de la vaccination en fonction des pays'),
            dcc.Loading(dcc.Graph(id='graph-4'), type='cube', style={'width': '100%', }),
            
            #html.H2(children='3. Evolution de la vaccination en fonction du PIB'),
            #dcc.Loading(dcc.Graph(id='graph-5'), type='cube', style={'width': '100%', }),
        ],)

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Callbacks

        # First three graphs
        self.app.callback(
            dash.dependencies.Output('graph-1', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_1)

        self.app.callback(
            dash.dependencies.Output('graph-2', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_2)

        self.app.callback(
            dash.dependencies.Output('graph-3', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_3)
        
        # Graph vaccination per continent
        self.app.callback(
            dash.dependencies.Output('graph-4', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_4)

        # Graph PIB-vaccination
        '''self.app.callback(
            dash.dependencies.Output('graph-5', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_5)'''

    # Update methods

    def update_graph_1(self, pays):
        # Récupération des données correspondant au pays sélectionné
        df = self.vaccinations.loc[self.vaccinations['location'] == pays]
        # Renommage des colonnes pour avoir des noms plus lisibles
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})
        # Sélection des colonnes à afficher sur le graphique
        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations totales",
            "Personnes vaccinées",
            "Personnes totalement vaccinées",
            "Total de boosters",
        ]]

        # Création du graphique
        fig = px.line(df[df.columns[2]], template='plotly_dark')

        for c in df.columns[3:]:
            fig.add_scatter(x=df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')

        fig.update_layout(
            title='Vaccinations totales contre le COVID-19',
            xaxis=dict(title='Temps'),
            yaxis=dict(title='Vaccinations'),
            height=600,
            showlegend=True,
        )
        return fig

    def update_graph_2(self, pays):
        # Récupération des données correspondant au pays sélectionné
        df = self.vaccinations.loc[self.vaccinations['location'] == pays]
        # Renommage des colonnes pour avoir des noms plus lisibles
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})
        # Sélection des colonnes à afficher sur le graphique
        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations quotidiennes brutes",
            "Vaccinations quotidiennes nettes",
            "Vaccinations quotidiennes pour 1M habitants",
            "Personnes vaccinées quotidiennement",
            "Personnes vaccinées quotidiennement pour 100 habitants",
        ]]

        # Création du graphique
        fig = px.line(df[df.columns[2]], template='plotly_dark')

        for c in df.columns[3:]:
            fig.add_scatter(x=df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')

        fig.update_layout(
            title='Vaccinations quotidiennes contre le COVID-19',
            xaxis=dict(title='Temps'),
            yaxis=dict(title='Vaccinations'),
            height=600,
            showlegend=True,
        )
        return fig

    def update_graph_3(self, pays):
        # Récupération des données correspondant au pays sélectionné
        df = self.vaccinations.loc[self.vaccinations['location'] == pays]
        # Renommage des colonnes pour avoir des noms plus lisibles
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})
        # Sélection des colonnes à afficher sur le graphique
        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations pour 100 habitants",
            "Personnes vaccinées pour 100 habitants",
            "Personnes totalement vaccinées pour 100 habitants",
            "Total de boosters pour 100 habitants",
            "Personnes vaccinées quotidiennement pour 100 habitants",
        ]]

        # Création du graphique
        fig = px.line(df[df.columns[2]], template='plotly_dark')

        for c in df.columns[3:]:
            fig.add_scatter(x=df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')

        fig.update_layout(
            title='Vaccinations contre le COVID-19 pour 100 habitant',
            xaxis=dict(title='Temps'),
            yaxis=dict(title='Vaccinations'),
            height=600,
            showlegend=True,
        )

        return fig

    def update_graph_4(self, _):
        regions = [
            "Europe",
            "Asia",
            "North America",
            "South America",
            "Africa",
            "Oceania",
        ]

        # Récupération des données correspondant aux régions sélectionnées ci-dessus
        df = self.vaccinations[self.vaccinations['location'].isin(regions)]
        df = df[['location', 'people_vaccinated_per_hundred']]
        df.fillna(method='ffill', inplace=True)
        # df.sort_index(inplace=True)

        # Création du graphique
        fig = px.bar(
            df, x='location', y='people_vaccinated_per_hundred', color='location',
            animation_frame=df.index, range_y=[0, 100]
        )

        # Contrôle de la vitesse de l'animation via le temps entre deux frames
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10  # millisecondes

        fig.update_layout(
            template='plotly_dark', title='Évolution de la population vaccinée par continent',
            xaxis=dict(title='Continents'), yaxis=dict(title='Pourcentage de la population vaccinée'),
        )

        return fig

    def update_graph_5(self, _):
        # Récupération des données correspondant aux régions sélectionnées ci-dessus
        df = self.data[['location', 'people_vaccinated_per_hundred', 'PIB']]
        df = df.fillna(method='ffill')

        # Création du graphique
        fig = px.scatter(
            df, x='PIB', y='people_vaccinated_per_hundred', color='location',
            animation_frame=df.index, range_y=[0, 100], hover_name='location',
            range_x=[1000000000000, 1000000000000000]
        )

        # Contrôle de la vitesse de l'animation via le temps entre deux frames
        # fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10  # millisecondes

        fig.update_layout(
            template='plotly_dark', title='Évolution de la population vaccinée par continent',
            xaxis=dict(title='PIB'), yaxis=dict(title='Pourcentage de la population vaccinée'),
        )


if __name__ == '__main__':
    vaccinations = Vaccinations()
    vaccinations.app.run_server(debug=True, port=8051)
