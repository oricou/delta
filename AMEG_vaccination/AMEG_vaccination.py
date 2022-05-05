import sys
import dash
import flask
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du


def load_data(filename):
    df = pd.read_csv(filename)
    #df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


def load_pib(filename):
    df = pd.read_csv(filename)
    df = df[df["Year"] == 2016]
    df = df.drop(["Country Name", "Year"], axis=1)
    df = df.rename(columns={"Country Code": "iso_code", "Value": "PIB"})
    return df


class Vaccinations:

    def __init__(self, application=None):
        vacc = load_data("data/vaccinations.csv")
        #pib = load_pib("data/gdp.csv")

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
            'Personnes vaccinées quotidiennement pour 100 habitants'
        ]
        #self.vacc = vacc.merge(pib, how="left", on="iso_code")
        self.vacc = vacc

        self.pays = self.vacc['location'].unique()
        self.dates = self.vacc.index.unique().sort_values()

        self.START = "Play"
        self.PAUSE = "Pause"

        # HTML components
        self.main_layout = html.Div(children=[
            # Titre
            html.H1(children='Vaccinations contre le COVID-19 par pays en fonction du temps',
                    style={'font-family': 'Helvetica', 'color': '#ffffff', 'text-align': 'center'}),
            html.P(children='''On va présenter ci-dessous les liens entre les taux de vaccinations contre le COVID-19
            et le PIB des pays.'''),

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

    # Update methods

    def update_graph_1(self, pays):
        df = self.vacc.loc[self.vacc['location'] == pays]
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})

        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations totales",
            "Personnes vaccinées",
            "Personnes totalement vaccinées",
            "Total de boosters",
        ]]

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
        df = self.vacc.loc[self.vacc['location'] == pays]
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})

        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations quotidiennes brutes",
            "Vaccinations quotidiennes nettes",
            "Vaccinations quotidiennes pour 1M habitants",
            "Personnes vaccinées quotidiennement",
            "Personnes vaccinées quotidiennement pour 100 habitants",
        ]]
            
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
        df = self.vacc.loc[self.vacc['location'] == pays]
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})

        df = df[[
            "Code ISO Pays",
            "Date",
            "Vaccinations pour 100 habitants",
            "Personnes vaccinées pour 100 habitants",
            "Personnes totalement vaccinées pour 100 habitants",
            "Total de boosters pour 100 habitants",
            "Personnes vaccinées quotidiennement pour 100 habitants",
        ]]
            
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

        df = self.vacc[self.vacc['location'].isin(regions)]
        df.sort_values('date')

        fig = px.bar(
            df, x='location', y='people_vaccinated_per_hundred', color='location',
            animation_frame=df.index, range_y=[0, 100]
        )

        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10

        fig.update_layout(
            template='plotly_dark', title='Évolution de la population vaccinée par continent',
            xaxis=dict(title='Continents'), yaxis=dict(title='Pourcentage de la population vaccinée'),
        )

        return fig


if __name__ == '__main__':
    vacci = Vaccinations()
    vacci.app.run_server(debug=True, port=8051)
