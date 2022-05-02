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

        pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')
        pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "GDP"})
        pib = pib.sort_values(by = ['Year'])
        pib = pib.drop_duplicates(subset=['Code'], keep='last')

        self.pib = pib

        self.data = dict(
        type = 'choropleth',
        locationmode = 'country names',
        ) 

        self.layout = dict(
            geo = dict(
            showframe = False,
            projection = {'type':'natural earth'}
            )
        )


        self.main_layout = html.Div(children=[
            html.H3(children='Planisphère'),
            html.Div([ dcc.Graph(id='pla-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='pla-mean', 
                                     options=[{'label':'Prix moyen des bières par pays', 'value':0},
                                              {'label':'Prix moyen des vins par pays', 'value':1},
                                              {'label':'Prix moyen des spiritueux par pays', 'value':2},], 
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
                    dash.dependencies.Output('pla-main-graph', 'figure'),
                    dash.dependencies.Input('pla-mean', 'value'))(self.update_graph)

    def update_graph(self, mean):
        if mean == 0:
            self.change_df('beer', 'bières')
        elif mean == 1:
            self.change_df('wine', 'vins')
        elif mean == 2:
            self.change_df('spirits', 'spiritueux')

        choromap = go.Figure(data = [self.data],layout = self.layout)
        choromap.update_layout(margin=dict(l=0, r=0, t=50, b=0, autoexpand=True))
        return choromap

    def change_df(self, alcohol_type, french_name):
        df_alcohol = pd.read_csv('data/gho_average_price_500_mls_' + alcohol_type + '_in_us$.csv')
        df_alcohol.dropna(how='all', axis=1, inplace=True)
        df_alcohol[['Location', 'SpatialDimValueCode', 'Value']]
        df_alcohol= df_alcohol.rename(columns = {"SpatialDimValueCode": "Code"})
        df_alcohol = df_alcohol[df_alcohol['Value'].notna()]

        self.df = pd.merge(df_alcohol, self.pib, on = 'Code')
        self.df['Ratio'] = self.df.apply(lambda row: row.GDP / row.Value, axis=1)

        self.data['locations'] = self.df['Location']
        self.data['z'] = self.df['Ratio']
        self.data['text'] = self.df['Location']
        self.data['colorbar'] = {'title' : 'Prix de l\'alcool en fonction du PIB'}

        self.layout['title'] = 'Prix moyen des '  + french_name + ' par pays'
        
if __name__ == '__main__':
    pla = Planisphere()
    pla.app.run_server(debug=True, port=8051)
