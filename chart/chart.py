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

from urllib.request import urlopen
import json

class Chart():

    def __init__(self, application = None):
        self.pn_df = pd.read_pickle('data/pn_db.pkl')
        self.departament = self.pn_df[(self.pn_df['Département'] != 'France_Métro') & (self.pn_df['Département'] != 'France_Entière')]
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            self.counties = json.load(response)

        self.years = self.pn_df.index.unique().sort_values()

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution du nombre de crimes en France.'),
            html.Div(
                [
                    dcc.Graph(id='chart-heatmap'),
                    dcc.Graph(id='chart-evolution'),
                ],
                style={
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'flex-start',
                }
            ),

            html.Br(),
            html.Div([ # slider
                html.Div(
                    dcc.Slider(
                            id='chart-year-slider',
                            min=0,
                            max=len(self.years) -1,
                            value=0,
                            marks={i: str(self.years[i].year) for i in range(0,len(self.years), 12) },
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='chart-auto-stepper',
                    interval=1000,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0,
                    disabled=True,
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Div([
                html.Button(
                    'START',
                    id='chart-button-start-stop', 
                    n_clicks=0,
                    style={'display':'inline-block'}
                ),
                html.Div([ html.Div('Choix du type de crime:'),
                           dcc.Dropdown(
                               id='chart-which-crime',
                               options=[{'label': i, 'value': i} for i in self.pn_df.columns[:-1]],
                               value='Autres délits',
                               disabled=False,
                           ),
                         ], style={'width': '32em', 'margin':"0px 0px 0px 40px"}), # bas D haut G
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='chart-xaxis-type',
                               options=[{'label': i, 'value': i != 'Linéaire'} for i in ['Linéaire', 'Logarithmique']],
                               value=True,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""
                # TODO: correct all following
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
                En cliquant ou double-cliquant sur les lignes de la légende, vous choisissez les courbes à afficher.
                
                Notes :
                   * FOD est le fioul domestique.
                   * Pour les prix relatifs, seules les énergies fossiles sont prises en compte par manque de données pour les autres.

                #### À propos

                * Sources : 
                   * [data.gouv.fr](https://www.data.gouv.fr/datasets/chiffres-departementaux-mensuels-relatifs-aux-crimes-et-delits-enregistres-par-les-services-de-police-et-de-gendarmerie-depuis-janvier-1996/)
                   chiffres departementaux mensuels relatifs aux crimes et delits enregistres par les services de police et de gendarmerie depuis janvier 1996
                * (c) 2022 Olivier Ricou
                """)
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                dash.dependencies.Output('chart-heatmap', 'figure'),
                dash.dependencies.Input('chart-year-slider', 'value'),
                )(self.update_heatmap)

        self.app.callback(
                dash.dependencies.Output('chart-evolution', 'figure'),
                dash.dependencies.Input('chart-year-slider', 'value'),
                )(self.update_evolution)

        self.app.callback(
                dash.dependencies.Output('chart-year-slider', 'value'),
                dash.dependencies.Input ('chart-auto-stepper', 'n_intervals'),
                dash.dependencies.State('chart-year-slider', 'value'))(self.on_interval)

        self.app.callback(
                dash.dependencies.Output('chart-auto-stepper', 'disabled'),
                dash.dependencies.Output('chart-button-start-stop', 'children'),
                dash.dependencies.Input('chart-button-start-stop', 'n_clicks'),
                dash.dependencies.State('chart-auto-stepper', 'disabled'),
                )(self.on_click)

    def update_heatmap(self, date_index):
        fig = px.imshow([[1, 20, 30],
                 [20, 1, 60],
                 [30, 60, 1]])

        return fig

    def update_evolution(self, date_index):
        fig = px.line(x=["a","b","c"], y=[1,3,2], title="sample figure")

        return fig

    def on_interval(self, _, year):
        if year == self.years[-1]:
            return self.years[0]
        else:
            return year + 1

    def on_click(self, n_clicks, disabled):
        return (not disabled, ("STOP" if disabled else "START"))


if __name__ == '__main__':
    chart = Chart()
    chart.app.run_server(debug=True, port=8051)
