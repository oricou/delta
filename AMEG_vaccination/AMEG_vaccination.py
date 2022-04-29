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
    # print(df)
    # print("Number of NaN : ", df.isna().sum().sum())
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

        self.vacc = vacc.merge(pib, how="left", on="iso_code")

        self.main_layout = html.Div(children=[
            html.H3(children='Vaccination contre le COVID-19 par pays et par date'),
            html.Div([dcc.Graph(id='ngr-main-graph'), ], style={'width':'100%', }),
        ], style={
            'backgroundColor': '#f5f5f5',
            'padding':'10px 50px 10px 50px',
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == '__main__':
    Vaccinations()
