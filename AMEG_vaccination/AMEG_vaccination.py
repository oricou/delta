import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du


def load_data(filename):
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


def load_PIB(filename):
    df = pd.read_csv(filename)
    df = df[df["Year"] == 2016]
    df = df.drop(["Country Name", "Year"], axis=1)
    df = df.rename(columns={"Country Code": "iso_code", "Value": "PIB"})
    return df


class Vaccinations():

    def __init__(self, application=None):
        vacc = load_data("data/vaccinations.csv")
        pib = load_PIB("data/gdp.csv")

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
        self.main_layout = html.Div(children=[
            # Titre
            html.H1(children='Vaccination contre le COVID-19 par pays en fonction du temps',
                    style={'font-family': 'Helvetica', 'color': '#ffffff', 'text-align': 'center'}),

            # Selecteur de pays
            html.P(children='Sélectionner un pays :'),
            dcc.Dropdown(self.pays, id='pays', value='World', style={'margin': '20px 0px', 'width': '300px', 'color': 'black'}),

            # Graph
            html.Div([dcc.Graph(id='vac-main-graph'), ], style={'width': '100%', }),
            html.Div([dcc.Graph(id='vac-total'), ], style={'width': '100%', }),
            html.Div([dcc.Graph(id='vac-quotidien'), ], style={'width': '100%', }),
            html.Div([dcc.Graph(id='vac-pourcentage'), ], style={'width': '100%', }),
        ], style={
            'backgroundColor': '#222222',
            'padding': '10px 50px 10px 50px',
            'margin': '0px 0px 0px 0px',
            'font-family': 'Helvetica',
            'color': '#ffffff',
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('vac-main-graph', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_main_graph_countries)

        self.app.callback(
            dash.dependencies.Output('vac-total', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_per_country_total)

        self.app.callback(
            dash.dependencies.Output('vac-quotidien', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_per_country_quotidien)

        self.app.callback(
            dash.dependencies.Output('vac-pourcentage', 'figure'),
            dash.dependencies.Input('pays', 'value'),
        )(self.update_graph_per_country_pourcentage)

    def update_main_graph_countries(self, pays):
        df = self.vacc.loc[self.vacc['location'] == pays]
        df = df.rename(columns={df.columns[i]: self.cols[i] for i in range(len(df.columns))})

        fig = px.line(df[df.columns[2]], template='plotly_dark')
        for c in df.columns[3:]:
            fig.add_scatter(x=df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')

        fig.update_layout(
            title='Vaccinations contre le COVID-19',
            xaxis=dict(title='Temps'),
            yaxis=dict(title='Vaccinations'),
            height=600,
            showlegend=True,
        )
        return fig

    def update_graph_per_country_total(self, pays):
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

    def update_graph_per_country_quotidien(self, pays):
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

    def update_graph_per_country_pourcentage(self, pays):
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
            title='Vaccinations pour 100 contre le COVID-19',
            xaxis=dict(title='Temps'),
            yaxis=dict(title='Vaccinations'),
            height=600,
            showlegend=True,
        )
        return fig


if __name__ == '__main__':
    vacci = Vaccinations()
    vacci.app.run_server(debug=True, port=8051)
