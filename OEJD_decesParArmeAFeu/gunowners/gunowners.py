import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from scipy import stats
from scipy import fft
import datetime
import plotly.express as px
from urllib.request import urlopen
import json
from OEJD_decesParArmeAFeu.data.get_data import GunOwnersData

def get_years_dic(begin, end):
    years = {}
    for year in range(begin, end + 1, 1):
        years[year] = str(year)
    return years

class Gunowners():
    def __init__(self, application = None):
        self.begin = 1980
        self.end = 2016
        self.years = get_years_dic(self.begin, self.end)

        datas = GunOwnersData(self.begin, self.end)
        self.df_wages = datas.init_wages()
        self.df_gowners = datas.init_gowners()

        self.main_layout = html.Div(children=[
            html.Div([
                html.H3("Possession d'arme à feu aux Etats-Unis"),
                dcc.Graph(id="oejd--graph-plot-line"),
                dcc.RadioItems(id='oejd--check-plot-line',
                                         options=[{'label':'Moyenne de chaque état', 'value':0},
                                                  {'label':'Moyenne du pays', 'value':1}],
                                         value=1,
                                         labelStyle={'display':'block'}),
                html.Br(),
                html.Br(),
                dcc.Markdown("""
                            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.
                            En cliquant ou double-cliquant sur les lignes de la légende lorsque le graphique est affiché en fonction des états, vous choisissez les courbes à afficher.

                            Notes :
                               * Il y a un pourcentage d'erreur estimé entre 2 à 4 points, selon l'état et l'année.
                            """),
                html.Br()
                ])
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        self.app.callback(
                    dash.dependencies.Output("oejd--graph-plot-line", "figure"),
                    dash.dependencies.Input("oejd--check-plot-line", "value"))(self.update_plotline)

    def update_plotline(self, value):
        df = self.df_gowners
        states_showed = ["Alabama", "California", "New Jersey",
            "New York", "Mississippi", "Nevada"]
        fig = px.line(df, x="Year", y="HFR", color='STATE', labels= {
                     "Year": "Année",
                     "HFR": "Adultes possédant une arme à feu (En %)",
                     "STATE": "États sélectionnés"
                 })
        fig = fig.for_each_trace(lambda trace: trace.update(visible="legendonly")
               if trace.name not in states_showed else ())
        if value == 1:
            df = df.groupby('Year').mean()
            fig = px.line(df, x=df.index, y="HFR", labels= {
                         "Year": "Année",
                         "HFR": "Adultes possédant une arme à feu (En %)"
                     })
        fig.update_layout(title="Pourcentage d'adultes possédant une arme à feu au fil des années aux États-Unis")
        return fig


if __name__ == '__main__':
    mpj = Gunowners()
    mpj.app.run_server(debug=True, port=8051)
