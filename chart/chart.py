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
        self.ts_df = pd.read_pickle('data/ts_db.pkl')
        self.all_france = self.ts_df[(self.ts_df['Département'] == 'France_Entière')]

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

            html.Div([
                html.Div([ html.Div('Sélectionner catégorie'),
                    dcc.Checklist(
                        id='chart-items-crimes',
                        options=[{'label': self.ts_df.columns[i], 'value': i }
                            for i in range(len(self.ts_df.columns) - 1)],
                        value=[0, 1, 2, 3],
                        inline=False),],
                    style={'margin':"0px 0px 0px 40px"}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='chart-xaxis-type',
                               options=[{'label': i, 'value': i != 'Linéaire'} for i in ['Linéaire', 'Logarithmique']],
                               value=True,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                html.Div(style={'width':'2em'}),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.  
                En sélectionnant les différentes catégories, vous pouvez choisir
                celles corréllées et affichées sur les graphiques.  

                #### À propos

                Cette base de donnée est mise à jour mensuellement, aussi nous avons fait attention à ce que notre site tienne compte de nouvels ajouts de données.

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
                dash.dependencies.Input('chart-items-crimes', 'value'),
                )(self.update_heatmap)

        self.app.callback(
                dash.dependencies.Output('chart-evolution', 'figure'),
                dash.dependencies.Input('chart-items-crimes', 'value'),
                dash.dependencies.Input('chart-xaxis-type', 'value'),
                )(self.update_evolution)

    def update_heatmap(self, items):
        df = self.all_france[self.ts_df.columns[items]]
        corr = df.sort_index().corr(method='pearson')
        fig = px.imshow(
                corr,
                zmin = -1,
                zmax = 1,
        )
        fig.update_yaxes(matches=None, visible=False)
        fig.update_xaxes(matches=None, visible=False)

        return fig

    def update_evolution(self, items, xaxis_type):
        df = self.all_france[self.ts_df.columns[items]]
        if xaxis_type:
            df = np.log(df+1)

        fig = px.line(
                df,
                title="Evolution au cours du temps",
        )

        fig.update(layout_showlegend=False)

        return fig


if __name__ == '__main__':
    chart = Chart()
    chart.app.run_server(debug=True, port=8051)
