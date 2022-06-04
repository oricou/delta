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
from plotly.subplots import make_subplots
import dateutil as du
from scipy import stats
from scipy import fft

class Abih():
    def __init__(self, application = None):
        self.mf = pd.read_csv('abih/data/meteorite-landings.csv')
        self.pf = pd.read_csv('abih/data/geonames-all-cities-with-a-population-1000.csv', sep=';', on_bad_lines='skip')

        #Setup longitude & latitude
        self.pf['lat'] = pd.NaT
        self.pf['lon'] = pd.NaT
        self.pf = self.pf.reset_index()  # make sure indexes pair with number of rows
        for index, row in self.pf.iterrows():
            coord = row['Coordinates'].split(',')
            self.pf.at[index, 'lat'] = float(coord[0])
            self.pf.at[index, 'lon'] = float(coord[1])

        #Clean dubious data as per NASA recommendation
        self.mf = self.mf.dropna()
        self.mf = self.mf[(self.mf.year >= 860) & (self.mf.year <= 2016)]
        self.mf = self.mf[((self.mf.reclong <= 180) & (self.mf.reclong >= -180)) & ((self.mf.reclat != 0) | (self.mf.reclong != 0))]
           
        meteor_dist = dcc.Graph(id='meteor-year-distrib')
        meteor_dist.figure = px.histogram(self.mf.year, labels={
                     "value": "année",
                     "count": "nombre de météorites"})

        self.populationFig = px.scatter_mapbox(self.pf, lat="lat", lon="lon", size_max = 0.1)

        meteor_heatmap = dcc.Graph()
        meteor_heatmap.figure = self.populationFig
        meteor_heatmap.figure.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])

        self.main_layout = html.Div(children=[
            html.H3(children='Introduction'),
            dcc.Markdown("""
                Notre projet consiste à mettre en avant plusieurs charactéristiques du dataset 'météorites' produit par la NASA.
            """),
            html.H6(children='Auteurs'),
            dcc.Markdown("""
                ANDRE Benoist
                HUSAK Ihor
            """),
            html.H3(children='Distribution des météorites sur le temps'),
            html.Div([ meteor_dist, ], style={'width':'100%', }),
            html.Br(),
            dcc.Markdown("""
                On voit très rapidemment que la plupart des météorites recensées ont été trouvé il ya moins de 200 ans.
                Ce graphe implique donc deux choses :
                - Les météorites se dégradent très rapidemment
                - Il y'a une potentielle corrélation entre densité de population et la densité de recensement
            """),
            html.H3(children='Heatmap météorites & population'),
            html.Div([ dcc.Graph(id='meteor-heat-map') ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='meteor-heat-map-option', 
                            options=[{'label':'Observées + Non observées', 'value': 0},
                                    {'label':'Observées', 'value': 1},
                                    {'label':'Trouvées (non observées)', 'value': 2}], 
                            value=0,
                            labelStyle={'display':'block'}) ,
                        dcc.RadioItems(id='meteor-heat-map-pop-option', 
                            options=[{'label':'Sans Population', 'value': 0},
                                    {'label':'Avec Population', 'value': 1}], 
                            value=0,
                            labelStyle={'display':'block'}) ,
                            ]),
            html.Br(),
            dcc.Markdown("""
                Sources :
                - https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000
                - https://www.kaggle.com/datasets/nasa/meteorite-landings
                
                Notes :
                - On voit que les météorites trouvées (non observées) se trouve dans des régions du globe à tendance désertique
                - Les météorites trouvées (non observées) se situent loin des régions à forte densité de population, donc préservé
                - Les météorites observées quant à elle se stiuent près des régions à forte populations, plus d'observateurs donc plus de chance d'être observé 
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
                    dash.dependencies.Output('meteor-heat-map', 'figure'),
                    [dash.dependencies.Input('meteor-heat-map-option', 'value'),
                    dash.dependencies.Input('meteor-heat-map-pop-option', 'value')])(self.update_graph)

    def update_graph(self, option, popOption):
        dataToDeal = []
        if option == 0:
            dataToDeal = self.mf
        if option == 1:
            dataToDeal = self.mf[self.mf.fall == 'Fell']
        if option == 2:
            dataToDeal = self.mf[self.mf.fall == 'Found']

        fig = px.density_mapbox(dataToDeal, lat = 'reclat', lon = 'reclong', radius=5,
                        center=dict(lat=0, lon=180), zoom=0, mapbox_style="stamen-terrain",color_continuous_scale= [
                [0.0, "black"],
                [0.5, "orange"],
                [0.6, "yellow"],
                [0.7, "red"],
                [1, "red"]])
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])

        if popOption != 0:
            fig.add_trace(self.populationFig.data[0])
            fig.add_trace(fig.data[0])
        return fig
        
if __name__ == '__main__':
    mpj = Abih()
    mpj.app.run_server(debug=True, port=8051)
