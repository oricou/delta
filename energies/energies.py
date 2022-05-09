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
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            self.counties = json.load(response)

        self.mois = {'janv':'01', 'févr':'02', 'mars':'03', 'avr':'04', 'mai':'05', 'juin':'06', 'juil':'07', 'août':'08', 'sept':'09', 'oct':'10', 'nov':'11', 'déc':'12'}
        self.years =np.arange(self.pn_df.index.min().year, self.pn_df.index.max().year+1)

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution des prix de différentes énergies en France'),
            html.Div([ dcc.Graph(id='nrg-main-graph'), ], style={'width':'100%', }),
            html.Div([
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
                html.Div([ html.Div('Mois ref.'),
                           dcc.Dropdown(
                               id='nrg-which-month',
                               options=[{'label': i, 'value': i} for i in self.mois],
                               value="01",
                               disabled=False,
                           ),
                         ], style={'width': '16em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                html.Div([ html.Div('Annee ref.'),
                           dcc.Dropdown(
                               id='nrg-which-year',
                               options=[{'label': i, 'value': i} for i in self.years],
                               value=2000,
                               disabled=False,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
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
                               options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                               value='Logarithmique',
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
                    [ dash.dependencies.Input('nrg-which-month', 'value'),
                      dash.dependencies.Input('nrg-which-year', 'value'),
                      dash.dependencies.Input('nrg-which-crime', 'value'),
                      dash.dependencies.Input('nrg-xaxis-type', 'value'),])(self.update_graph)

    def update_graph(self, month, year, crime, xaxis_type):
        
        df = self.pn_df[['Département', crime]]

        if not month in self.mois:
            month = '01'
        if not year in self.years:
            year = 2001
        if not crime in df.columns:
            crime = 'Autres délits'
        date = str(year) + "-" + month + "-01"
        df = df.loc[date]

        val_min = df[crime].min()
        val_max = df[crime].mean()

        fig = px.choropleth_mapbox(df, geojson=self.counties,
                                   featureidkey='properties.code',
                                   locations='Département',
                                   color='Autres délits',
                                   color_continuous_scale="Viridis",
                                   range_color=(val_min, val_max),
                                   mapbox_style="carto-positron",
                                   zoom=4.3, center = {"lat": 46, "lon": 2.349014},
                                   opacity=0.5,
                                   labels={'unemp':'unemployment rate'}
                                  )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig


if __name__ == '__main__':
    nrg = Energies()
    nrg.app.run_server(debug=True, port=8051)
