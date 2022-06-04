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

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import get_data

class Map():

    def __init__(self, application = None):
        # download data if needed
        get_data.main()
        self.ts_df = pd.read_pickle('data/ts_db.pkl')
        self.departament = self.ts_df[(self.ts_df['Département'] != 'France_Métro') & (self.ts_df['Département'] != 'France_Entière')]
        with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
            self.counties = json.load(response)

        self.years = self.ts_df.index.unique().sort_values()

        self.main_layout = html.Div(children=[
            html.H3(children='Carte sur l\'évolution du nombre de crimes en France.'),
            html.A(children='lien vers les graphiques (deuxième partie)', href='/EMMH_chart'),
            html.Div([ dcc.Graph(id='map-main-graph'), ], style={'width':'100%', }),

            html.Br(),
            html.Div([ # slider
                html.Div(
                    dcc.Slider(
                            id='map-year-slider',
                            min=0,
                            max=len(self.years) -1,
                            value=0,
                            marks={i: str(self.years[i].year) for i in range(0,len(self.years), 12) },
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='map-auto-stepper',
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
                    id='map-button-start-stop', 
                    n_clicks=0,
                    style={'display':'inline-block'}
                ),
                html.Div([ html.Div('Choix du type de crime:'),
                           dcc.Dropdown(
                               id='map-which-crime',
                               options=[{'label': i, 'value': i} for i in self.ts_df.columns[:-1]],
                               value='Autres délits',
                               disabled=False,
                           ),
                         ], style={'width': '32em', 'margin':"0px 0px 0px 40px"}), # bas D haut G
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='map-xaxis-type',
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
                Le graphique est interactif. En passant la souris sur les départements vous aurez une infobulle.  
                En faisant défiler le curseur sur la frise vous pouvez le mois et l'année qui vous intéresse.  
                Cette map représente le nombre de crimes déclarés chaque mois dans chaque département de France.  

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
                    dash.dependencies.Output('map-main-graph', 'figure'),
                    [ dash.dependencies.Input('map-year-slider', 'value'),
                      dash.dependencies.Input('map-which-crime', 'value'),
                      dash.dependencies.Input('map-xaxis-type', 'value'),])(self.update_graph)

        self.app.callback(
                dash.dependencies.Output('map-year-slider', 'value'),
                dash.dependencies.Input ('map-auto-stepper', 'n_intervals'),
                dash.dependencies.State('map-year-slider', 'value'))(self.on_interval)

        self.app.callback(
                dash.dependencies.Output('map-auto-stepper', 'disabled'),
                dash.dependencies.Output('map-button-start-stop', 'children'),
                dash.dependencies.Input('map-button-start-stop', 'n_clicks'),
                dash.dependencies.State('map-auto-stepper', 'disabled'),
                )(self.on_click)


    def update_graph(self, date_index, crime, xaxis_type):
        name_ladder = "Nombre de crimes" if not xaxis_type else "Log du nombre de crimes"

        df = self.departament[['Département', crime]]

        df.rename(columns={crime:name_ladder}, inplace=True)
        crime = name_ladder

        val_max = df[crime].max()
        val_min = 0

        date = self.years[date_index]

        df = df.loc[date]

        if xaxis_type:
            val_max = np.log(val_max + 1)
            df[crime] = np.log(1 + df[crime])

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
        if year >= len(self.years) - 1:
            return 0
        else:
            return year + 1

    def on_click(self, n_clicks, disabled):
        return (not disabled, ("STOP" if disabled else "START"))


if __name__ == '__main__':
    map = Map()
    map.app.run_server(debug=True, port=8051)
