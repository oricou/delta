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
            html.H3(children='Prix des alcools face aux revenus'),
            html.Div([ dcc.Graph(id='pla-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='pla-mean', 
                                     options=[{'label':'Bières', 'value':0},
                                              {'label':'Vins', 'value':1},
                                              {'label':'Spiritueux', 'value':2},], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
            #### À propos
            * Sources : [Observatoire mondial de la Santé](https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/economic-aspects)
            * (c) 2022 Vincent Courty, Luca Moorghen
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
        self.df['Ratio'] = self.df.apply(lambda row: row.Value / row.GDP * 100, axis=1)

        self.data['locations'] = self.df['Location']
        self.data['z'] = self.df['Ratio']
        self.data['text'] = self.df['Location']
        self.data['colorbar'] = {'title' : 'Prix de l\'alcool par rapport au PIB'}

        #self.layout['title'] = 'Prix moyen des '  + french_name + ' par rapport au PIB'
        
if __name__ == '__main__':
    pla = Planisphere()
    pla.app.run_server(debug=True, port=8051)
