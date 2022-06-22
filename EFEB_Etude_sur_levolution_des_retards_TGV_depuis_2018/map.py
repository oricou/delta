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

import json

class Map():
    def __init__(self, application = None):
        self.df = pd.read_pickle('data/df.pkl')
        with open("data/connpolys.geojson") as f:
            self.conns = json.load(f)
        self.df.set_index('Date')
        self.dates = self.df['Date'].unique()

        self.main_layout = html.Div(children=[
            html.H3(children='Étude des retards SNCF par itinéraire'),
            html.Div([ dcc.Graph(id='map-main-graph'), ], style={'width':'100%', }),

            html.Br(),
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='map-date-slider',
                            min=0,
                            max=len(self.dates) -1,
                            value=0,
                            marks={i: str(self.dates[i]) for i in range(0,len(self.dates), 12) },
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(
                    id='map-auto-stepper',
                    interval=1000,
                    max_intervals = -1,
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
                html.Div([ html.Div('Critères d\'affichage:'),
                           dcc.Dropdown(
                               id='map-sel-column',
                               options=[{'label': i, 'value': i} for i in self.df.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns],
                               value='Retard moyen des trains en retard au départ',
                               disabled=False,
                           ),
                         ], style={'width': '32em', 'margin':"0px 0px 0px 40px"}),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='map-scale-type',
                               options=[{'label': i, 'value': i != 'Linéaire'} for i in ['Linéaire', 'Logarithmique']],
                               value=False,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""
#### Informations utilisateur
La carte affichée ci-dessus représente les retards SNCF selon leur itinéraire. 
Cette carte est interactive: en passant la souris par dessus les itinéraires, vous pouvez afficher une infobulle dans laquelle vous trouverez l'itinéraire concerné, ainsi que son nombre de circulations prévues pour le mois.
Vous pouvez changer la date étudiée en utilisant le curseur sous la carte. Les données sont échantillonnées tous les mois.
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
                    dash.dependencies.Output('map-main-graph', 'figure'),
                    [ dash.dependencies.Input('map-date-slider', 'value'),
                      dash.dependencies.Input('map-sel-column', 'value'),
                      dash.dependencies.Input('map-scale-type', 'value'),])(self.update_graph)

        self.app.callback(
                dash.dependencies.Output('map-date-slider', 'value'),
                dash.dependencies.Input ('map-auto-stepper', 'n_intervals'),
                dash.dependencies.State('map-date-slider', 'value'))(self.on_interval)

        self.app.callback(
                dash.dependencies.Output('map-auto-stepper', 'disabled'),
                dash.dependencies.Output('map-button-start-stop', 'children'),
                dash.dependencies.Input('map-button-start-stop', 'n_clicks'),
                dash.dependencies.State('map-auto-stepper', 'disabled'),
                )(self.on_click)

    def update_graph(self, date_i, col, scale_is_log):
        namel = ("Log de " if scale_is_log else "") + col

        df = self.df[['Date', 'connid', col]]

        # df.rename(columns={col:namel}, inplace=True)
        col = namel

        val_max = df[col].max()
        val_min = 0

        date = self.dates[date_i]

        df = df[df['Date'] == date]

        if scale_is_log:
            val_max = np.log(val_max + 1)
            df[col] = np.log(1 + df[col])
        
        fig = px.choropleth_mapbox(df, geojson=self.conns,
                                   featureidkey='properties.connid',
                                   locations='connid',
                                   color=col,
                                   color_continuous_scale="Viridis",
                                   range_color=(val_min, val_max),
                                   mapbox_style="carto-positron",
                                   zoom=4.3, center = {"lat": 46, "lon": 2.349014},
                                   opacity=0.5,
                                  )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig
    
    def on_interval(self, _, date_i):
        if date_i >= len(self.dates) - 1:
            return 0
        else:
            return date_i + 1

    def on_click(self, n_clicks, disabled):
        return (not disabled, ("⏸️" if disabled else "▶️"))

if __name__ == '__main__':
    map = Map()
    map.app.run_server(debug=True, port=8051)
