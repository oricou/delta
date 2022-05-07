import sys
import glob
from tkinter import W
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
import xarray as xr

import numpy as np

class Chloro():
    def create_fig(self, chldf, fapardf, chl_colormap, fapar_colormap):

        data = []

        data.append(
            go.Scattermapbox(
                lon=fapardf['lonbin'].values,
                lat=fapardf['latbin'].values,
                mode='markers',
                name="FAPAR",
                text=[str(fapardf['FAPAR'].iloc[i]) for i in range(fapardf.shape[0])],
                marker=go.Marker(
                    showscale=True,
                    cmax=1,
                    cmin=0,
                    color=fapardf['FAPAR'].values,
                    colorscale=fapar_colormap,
                    colorbar=dict(title='FAPAR', x=1)
                ),
            )
        )
        data.append(
            go.Scattermapbox(
                lon=chldf['lonbin'].values,
                lat=chldf['latbin'].values,
                mode='markers',
                name="CHL (mg/m³)",
                text=[str(chldf['chl'].iloc[i]) for i in range(chldf.shape[0])],
                marker=go.Marker(
                    showscale=True,
                    cmax=4,
                    cmin=0,
                    color=chldf['chl'].values,
                    colorscale=chl_colormap,
                    colorbar=dict(title='CHL (mg/m³)', x=1.05)
               ),
            )
        )
 
        layout = go.Layout(
            margin=dict(t=0,b=0,r=0,l=0),
            autosize=True,
            hovermode='closest',
            showlegend=False,
            mapbox=dict(
                accesstoken=self.mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=44,
                    lon=2
                ),
                pitch=0,
                zoom=2,
                style='dark'
            ),
        )

        fig = dict(data=data, layout=layout)
        return fig



    def __init__(self, application = None):


        self.LESSER = -1
        self.NONE = 0
        self.GREATER = 1

        self.SUMMER = 1
        self.WINTER = 0

        self.COASTLINE = 1
        self.NO_COASTLINE = 0

        self.mapbox_access_token = 'pk.eyJ1IjoiZ2NhcnJpZXJlIiwiYSI6ImNsMmI1c3p3ejAxNmEzaW51MXBta2N6bTcifQ.f_MlUBEyToUp92xcCOwF0g'

        self.chldf = pd.read_pickle("data/chldf_2020-06-30.pkl")
        self.fapardf = pd.read_pickle("data/fapardf_2020-06-30.pkl")
 
        self.chldf_coastline = pd.read_pickle("data/chldf_coastline_2020-06-30.pkl")
        self.fapardf_coastline = pd.read_pickle("data/fapardf_coastline_2020-06-30.pkl")
        
        self.chldf_hiver = pd.read_pickle("data/chldf_2019-12-31.pkl")
        self.fapardf_hiver = pd.read_pickle("data/fapardf_2019-12-31.pkl")
 
        self.chldf_coastline_hiver = pd.read_pickle("data/chldf_coastline_2019-12-31.pkl")
        self.fapardf_coastline_hiver = pd.read_pickle("data/fapardf_coastline_2019-12-31.pkl")
       

        colormaps = ["viridis", "plasma", "bluered_r", "algae_r", "gray"]
      
        self.main_layout = html.Div(children=[
            html.H3(children='FAPAR x Chlorophylle'),
            html.Br(),
            html.Div([ dcc.Graph(id='map'), ], style={'width':'100%',}),
            html.Br(),
            html.Div([
                html.Div([ html.Div('Filtrage des points'),
                           dcc.RadioItems(id='map_mode', 
                                     options=[{'label':'Carte complète', 'value':self.NO_COASTLINE},
                                              {'label':'Côtes uniquement', 'value':self.COASTLINE}],
                                     value=self.COASTLINE,
                                     labelStyle={'display':'block'})
                            ], style={'width': '12em'} ),

                html.Div([ html.Div('Période des données'),
                           dcc.RadioItems(id='map_period', 
                                     options=[{'label':'Eté', 'value':self.SUMMER},
                                              {'label':'Hiver', 'value':self.WINTER}],
                                     value=self.SUMMER,
                                     labelStyle={'display':'block'})
                            ], style={'width': '12em'} ),

                html.Div([ html.Div('Seuillage FAPAR'),
                           dcc.RadioItems(id='map_fapar_treshold_type', 
                                     options=[{'label':'Aucun', 'value':self.NONE},
                                              {'label':'Supérieur à', 'value':self.GREATER},
                                              {'label':'Inférieur à', 'value':self.LESSER}],
                                     value=self.NONE,
                                     labelStyle={'display':'block'}),
                            dcc.Input(
                                    id="map_fapar_treshold", 
                                    type="number",
                                    debounce=True, 
                                    placeholder="Seuil", 
                                    min = 0, max = 4
                                )
                           ], style={'width': '17em'} ),

                html.Div([ html.Div('Seuillage chlorophylle'),
                           dcc.RadioItems(id='map_chl_treshold_type', 
                                     options=[{'label':'Aucun', 'value':self.NONE},
                                              {'label':'Supérieur à', 'value':self.GREATER},
                                              {'label':'Inférieur à', 'value':self.LESSER}],
                                     value=self.NONE,
                                     labelStyle={'display':'block'}),
                            dcc.Input(
                                    id="map_chl_treshold", 
                                    type="number",
                                    debounce=True, 
                                    placeholder="Seuil", 
                                    min = 0, max = 4
                                )
                            ], style={'width': '17em'} ),


                html.Div([ html.Div('Colormap FAPAR'),
                           dcc.Dropdown(
                               id='map_fapar_colormap',
                               options=[{'label': item, 'value': item} for item in colormaps],
                               value="bluered_r",
                               clearable=False,
                               style={'margin' : '0px 0px 14px 0px'}
                           ),
                           
                           html.Div('Colormap Chlorophylle'),
                           dcc.Dropdown(
                               id='map_chl_colormap',
                               options=[{'label': item, 'value': item} for item in colormaps],
                               value="viridis",
                               clearable=False
                          ),
                         ], style={'width': '12em'}),

                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
 
            html.Br(),
            dcc.Markdown("""
            Lorem Ipsum blablabla
            * Sources : 
                * [Copernicus Land Service](https://land.copernicus.eu/global/products/fapar) pour récupérer les données sur le FAPAR
                * [Copernicus Marine Service](https://resources.marine.copernicus.eu/product-detail/GLOBAL_MULTIYEAR_BGC_001_029/INFORMATION) pour récupérer les données sur la chlorophylle

            """)
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
                    dash.dependencies.Output('map', 'figure'),
                    [dash.dependencies.Input('map_mode', 'value'),
                     dash.dependencies.Input('map_period', 'value'), 
                     dash.dependencies.Input('map_chl_treshold_type', 'value'),
                     dash.dependencies.Input('map_fapar_treshold_type', 'value'),
                     dash.dependencies.Input('map_chl_treshold', 'value'),
                     dash.dependencies.Input('map_fapar_treshold', 'value'),
                     dash.dependencies.Input('map_chl_colormap', 'value'),
                     dash.dependencies.Input('map_fapar_colormap', 'value')])(self.update_graph)



    def update_graph(self, mode, period, chl_treshold_type, fapar_treshold_type, chl_treshold, fapar_treshold, chl_colormap, fapar_colormap) :
        
        if (mode == self.COASTLINE):
            chldf = self.chldf_coastline if period == self.SUMMER else self.chldf_coastline_hiver
            fapardf = self.fapardf_coastline if period == self.SUMMER else self.fapardf_coastline_hiver
        else :
            chldf = self.chldf if period == self.SUMMER else self.chldf_hiver
            fapardf = self.fapardf if period == self.SUMMER else self.fapardf_hiver


        if (chl_treshold != None):
            if (chl_treshold_type == self.LESSER) :
                chldf = chldf.loc[chldf["chl"] < chl_treshold]
            elif (chl_treshold_type == self.GREATER) :
                chldf = chldf.loc[chldf["chl"] > chl_treshold]

        if (fapar_treshold != None):
            if (fapar_treshold_type == self.LESSER) :
                fapardf = fapardf.loc[fapardf["FAPAR"] < fapar_treshold]
            elif (fapar_treshold_type == self.GREATER) :
                fapardf = fapardf.loc[fapardf["FAPAR"] > fapar_treshold]

        return self.create_fig(chldf, fapardf, chl_colormap, fapar_colormap)

        
if __name__ == '__main__':
    chl = Chloro()
    chl.app.run_server(debug=True, port=8051)
