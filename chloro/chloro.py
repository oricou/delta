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
    def create_fig(self):
        mapbox_access_token = 'pk.eyJ1IjoiZ2NhcnJpZXJlIiwiYSI6ImNsMmI1c3p3ejAxNmEzaW51MXBta2N6bTcifQ.f_MlUBEyToUp92xcCOwF0g'

        data = []

        data.append(
            go.Scattermapbox(
                lon=self.gdmpdf['lonbin'].values,
                lat=self.gdmpdf['latbin'].values,
                mode='markers',
                text=["GDMP" + '<br>' + str(self.gdmpdf['GDMP'].iloc[i]) for i in range(self.gdmpdf.shape[0])],
                marker=go.Marker(
                    cmax=330,
                    cmin=0,
                    color=self.gdmpdf['GDMP'].values,
                    colorscale='viridis'
                ),
            )
        )
        data.append(
            go.Scattermapbox(
                lon=self.chldf['lonbin'].values,
                lat=self.chldf['latbin'].values,
                mode='markers',
                text=["Chlorophylle" + '<br>' + str(self.chldf['chl'].iloc[i]) for i in range(self.chldf.shape[0])],
                marker=go.Marker(
                    cmax=2.5,
                    cmin=-2.5,
                    color=self.chldf['chl'].values,
                    colorscale='viridis',
                ),
            )
        )
 
        layout = go.Layout(
            margin=dict(t=0,b=0,r=0,l=0),
            autosize=True,
            hovermode='closest',
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=38,
                    lon=-94
                ),
                pitch=0,
                zoom=0,
                style='dark'
            ),
        )

        fig = dict(data=data, layout=layout)
        return fig



    def __init__(self, application = None):
        
        self.chldf = pd.read_pickle("data/chldf.pkl")
        self.gdmpdf = pd.read_pickle("data/gdmpdf.pkl")
        fig = self.create_fig()
        self.main_layout = html.Div(children=[
            html.H3(children='Chlorophylle x GDMP'),
            html.Div([ dcc.Graph(figure=fig)], style={'width':'100%', }),
            html.Br(),
            dcc.Markdown("""
            Lorem Ipsum blablabla
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



        
if __name__ == '__main__':
    chl = Chloro()
    chl.app.run_server(debug=True, port=8051)
