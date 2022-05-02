import sys
import glob
import dash
import flask
import chart_studio.plotly as py
import plotly.graph_objs as go 
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import dateutil as du
from scipy import stats
from scipy import fft

class Planisphere():
    def __init__(self, application = None):


        df_crimes = pd.read_csv('data/gho_alcohol_related_crimes.csv')
        df_crimes.dropna(how='all', axis=1, inplace=True)
        df_crimes = df_crimes[df_crimes['FactValueNumeric'].notna()]

        self.data = dict(
        type = 'choropleth',
        locations = df_crimes['Location'],
        locationmode = 'country names',
        z = df_crimes['Value'],
        text = df_crimes['Location'],
        colorbar = {'title' : 'alcohol related crimes per country'},
        ) 

        self.layout = dict(
            title = 'alcohol related crimes per country',
            geo = dict(
            showframe = False,
            projection = {'type':'natural earth'}
            )
        )

        self.df = df_crimes

        self.main_layout = html.Div(children=[
            html.H3(children='Planisphère'),
            html.Div([ dcc.Graph(id='cpp-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='cpp-mean', 
                                     options=[{'label':'Crimes liés à l\'alcool', 'value':0}], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
            blabla

            Sources : https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-related-crimes-(-of-all-crimes)
            
            Notes :
               * 1
               * 2
   
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
                    dash.dependencies.Output('cpp-main-graph', 'figure'),
                    dash.dependencies.Input('cpp-mean', 'value'))(self.update_graph)

    def update_graph(self, mean):
        #if mean == 1:
        choromap = go.Figure(data = [self.data],layout = self.layout)
        return choromap
        
if __name__ == '__main__':
    cpp = Planisphere()
    cpp.app.run_server(debug=True, port=8051)
