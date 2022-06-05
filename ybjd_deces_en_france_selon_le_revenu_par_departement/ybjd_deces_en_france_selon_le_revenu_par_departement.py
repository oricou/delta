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
import json
import ybjd_deces_en_france_selon_le_revenu_par_departement.data.get_data as get_data


class DecesFranceRevenu():
    departements = json.load(open('ybjd_deces_en_france_selon_le_revenu_par_departement/data/departements-version-simplifiee.geojson'))

    def __init__(self, application = None):
        self.df = get_data.get_data()

        self.main_layout = html.Div(children=[
            html.H3(children='Décès en France selon le revenu par département'),
            html.Div('Yann Buisson & Julien Delaforge'),
            html.Div([ dcc.Graph(id='drd-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='drd-value',
                                     options=[{'label':'Revenu/Pourcentage de morts', 'value':0},
                                              {'label':'Revenu/Nombre de morts', 'value':1}],
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
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
                dash.dependencies.Output('drd-main-graph', 'figure'),
                dash.dependencies.Input('drd-value', 'value'))(self.update_graph)


    def update_graph(self, value):
        if value == 0:
            fig = px.choropleth_mapbox(self.df,
                    geojson=self.departements,
                    locations='Numéro département',
                    featureidkey = 'properties.code',
                    color='Revenu/Pourcentage de morts',
                    color_continuous_scale="Viridis",
                    mapbox_style="carto-positron",
                    zoom=4.6, center = {"lat": 47, "lon": 2},
                    opacity=0.5,
                    labels={'Revenu/Pourcentage de morts':'Revenu/Pourcentage de morts'}
                    )
        else:
            fig = px.choropleth_mapbox(self.df,
                    geojson=self.departements,
                    locations='Numéro département',
                    featureidkey = 'properties.code',
                    color='Revenu/Nombre de morts',
                    color_continuous_scale="Viridis",
                    mapbox_style="carto-positron",
                    zoom=4.6, center = {"lat": 47, "lon": 2},
                    opacity=0.5,
                    labels={'Revenu/Nombre de morts':'Revenu/Nombre de morts'}
                    )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
        
if __name__ == '__main__':
    drd = DecesFranceRevenu()
    drd.app.run_server(debug=True, port=8051)
