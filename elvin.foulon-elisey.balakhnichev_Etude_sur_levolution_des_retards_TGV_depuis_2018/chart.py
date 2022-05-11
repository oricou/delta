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
        self.df = pd.read_pickle('data/df.pkl')
        self.df.set_index('Date')
        self.df_everywhere = self.df[self.df['connid'] == 'LYON PART DIEU→RENNES']
        self.dates = self.df['Date'].unique()
        self.allconnids = self.df['connid'].unique()

        self.main_layout = html.Div(children=[
            html.H3(children='Étude des retards SNCF par itinéraire'),
            html.Div(
                [
                    dcc.Graph(id='chart-evolution'),
                ],
                style={
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'flex-start',
                    'width': '100%',
                }
            ),

            html.Div([
                html.Div([ html.Div('Critères d\'affichage:'),
                           dcc.Dropdown(
                               id='chart-sel-column',
                               options=[{'label': i, 'value': i} for i in self.df.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns],
                               value='Retard moyen des trains en retard au départ',
                               disabled=False,
                           ),
                         ], style={'width': '32em', 'margin':"0px 0px 0px 40px"}),
                html.Div(style={'width':'2em'}),                html.Div([ html.Div('Choix des itinéraires'),
                    dcc.Checklist(
                        id='chart-items-category',
                        options=[{'label': self.allconnids[i], 'value': i }
                            for i in range(len(self.allconnids))],
                        value=[0],
                        inline=False),],
                    style={
                        'margin':"0px 0px 0px 40px",
                        'max-height': '40vh',
                        'overflow-y': 'auto',    
                    }),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='chart-yaxis-type',
                               options=[{'label': i, 'value': i != 'Linéaire'} for i in ['Linéaire', 'Logarithmique']],
                               value=False,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ),
                html.Div(style={'width':'2em'}),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""
#### Informations utilisateur
Le grahpique ci-dessus est interactif: en passant la souris par dessus les itinéraires, vous pouvez afficher une infobulle dans laquelle vous trouverez l'itinéraire concerné, la date pointée, et les critères d'affichage.
Vous pouvez changer les itinéraires étudiés en utilisant la liste à choix multiples sous la carte. Il n'y a pas de limite au nombre d'itinéraires affichables.
Le menu déroulant vous permet de choisir parmi une liste de critères quelles données afficher, selons vos préférences.

#### Sources
*Note : Nous avons pris soin d'utiliser des bases de données mises à jour régulièrement et à ce que notre travail supporte toute mise à jour de base de données future.*

* Base de données contenant les informations de retards : [ressources.data.sncf.com](https://ressources.data.sncf.com/explore/dataset/liste-des-gares/table/?location=9,46.83295,0.68115&basemap=jawg.transports)
* Base de données contenant les informations géographiques : [ressources.data.sncf.com](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/table/?sort=date)
* © 2022 Olivier Ricou pour le site internet d'affichage : [github.com/oricou](https://github.com/oricou/delta)
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
                dash.dependencies.Output('chart-evolution', 'figure'),
                dash.dependencies.Input('chart-sel-column', 'value'),
                dash.dependencies.Input('chart-items-category', 'value'),
                dash.dependencies.Input('chart-yaxis-type', 'value'),
                )(self.update_evolution)

    def update_evolution(self, col, items, scale_log):
        df = self.df[self.df['connid'].isin([self.allconnids[i] for i in items])][['Date', 'connid', col]]
        if scale_log:
            df[col] = np.log(df[col] + 1)
        fig = px.line(
                df,
                x='Date',
                y=col,
                color='connid',
                title="Évolution du critère sélectionné en fonction du temps",
        )

        return fig


if __name__ == '__main__':
    chart = Chart()
    chart.app.run_server(debug=True, port=8051)
