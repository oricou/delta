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

class Energies():

    def __init__(self, application = None):
        self.pn_df = pd.read_pickle('pn_db.pkl')
        self.departament = self.pn_df[(self.pn_df['Département'] != 'France_Métro') & (self.pn_df['Département'] != 'France_Entière')]
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            self.counties = json.load(response)

        self.years = self.pn_df.index.unique().sort_values()

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution des prix de différentes énergies en France'),
            html.Div([ dcc.Graph(id='nrg-main-graph'), ], style={'width':'100%', }),

            html.Br(),
            html.Div([ # slider
                html.Div(
                    dcc.Slider(
                            id='nrg-year-slider',
                            min=0,
                            max=len(self.years) -1,
                            value=0,
                            marks={i: str(self.years[i].year) for i in range(0,len(self.years), 12) },
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='nrg-auto-stepper',
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
                    id='nrg-button-start-stop', 
                    n_clicks=0,
                    style={'display':'inline-block'}
                ),
                html.Div([ html.Div('Prix'),
                           dcc.RadioItems(
                               id='nrg-price-type',
                               options=[{'label':'Absolu', 'value':0}, 
                                        {'label':'Équivalent J','value':1},
                                        {'label':'Relatif : 1 en ','value':2}],
                               value=1,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div([ html.Div('crime'),
                           dcc.Dropdown(
                               id='nrg-which-crime',
                               options=[{'label': i, 'value': i} for i in self.pn_df.columns[:-1]],
                               value='Autres délits',
                               disabled=False,
                           ),
                         ], style={'width': '32em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='nrg-xaxis-type',
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
                   * [base Pégase](http://developpement-durable.bsocom.fr/Statistiques/) du ministère du développement durable
                   * [tarifs réglementés de l'électricité](https://www.data.gouv.fr/en/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/) sur data.gouv.fr
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
                    dash.dependencies.Output('nrg-main-graph', 'figure'),
                    [ dash.dependencies.Input('nrg-year-slider', 'value'),
                      dash.dependencies.Input('nrg-which-crime', 'value'),
                      dash.dependencies.Input('nrg-xaxis-type', 'value'),])(self.update_graph)

        self.app.callback(
                dash.dependencies.Output('nrg-year-slider', 'value'),
                dash.dependencies.Input ('nrg-auto-stepper', 'n_intervals'),
                dash.dependencies.State('nrg-year-slider', 'value'))(self.on_interval)

        self.app.callback(
                dash.dependencies.Output('nrg-button-start-stop', 'disabled'),
                dash.dependencies.Output('nrg-button-start-stop', 'children'),
                dash.dependencies.Input('nrg-button-start-stop', 'n_clicks'),
                dash.dependencies.State('nrg-button-start-stop', 'disabled'),
                )(self.on_click)


    def update_graph(self, date_index, crime, xaxis_type):
        
        df = self.departament[['Département', crime]]

        date = self.years[date_index]
        df = df.loc[date]

        if xaxis_type:
            df[crime] += 1
            df[crime] = np.log(df[crime])

        val_min = df[crime].min()
        val_max = df[crime].max()

        fig = px.choropleth_mapbox(df, geojson=self.counties,
                                   featureidkey='properties.code',
                                   locations='Département',
                                   color=crime,
                                   color_continuous_scale="Viridis",
                                   range_color=(val_min, val_max),
                                   mapbox_style="carto-positron",
                                   zoom=4.3, center = {"lat": 46, "lon": 2.349014},
                                   opacity=0.5,
                                  )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig


    def on_interval(self, _, year):
        if year == self.years[-1]:
            return self.years[0]
        else:
            return year + 1

    def on_click(self, disabled, n_clicks):
        print('test')
        return not disabled, str(n_clicks)


if __name__ == '__main__':
    nrg = Energies()
    nrg.app.run_server(debug=True, port=8051)
