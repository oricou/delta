import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import dateutil as du
import plotly.express as px 
from scipy import stats
from scipy import fft

class Consommation():
    def __init__(self, application = None):


        alcohol_consumption = pd.read_csv('data/gho_alcohol_consumer_past_12months.csv')
        alcohol_consumption.dropna(how='all', axis=1, inplace=True)
        alcohol_consumption = alcohol_consumption.rename(columns = {"SpatialDimValueCode": "Code"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Location": "Country"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Value": "% of alcohol drinkers"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Dim1ValueCode": "Sex"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"ParentLocationCode": "Zone"})
        pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')
        pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "GDP"})
        del pib['Entity']
        pib = pib.sort_values(by = ['Year'])
        pib = pib.drop_duplicates(subset=['Code'], keep='last')
        self.df_consumption_pib = pd.merge(alcohol_consumption, pib, on = 'Code')

        self.main_layout = html.Div(children=[
            html.H3(children='Consommation d\'alcool selon le PIB'),
            html.Div([ dcc.Graph(id='con-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='con-mean', 
                                     options=[{'label':'Option 1', 'value':0}], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
            blabla

            Sources : 
            
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
                    dash.dependencies.Output('con-main-graph', 'figure'),
                    dash.dependencies.Input('con-mean', 'value'))(self.update_graph)

    def update_graph(self, mean):
        #if mean == 1:
        fig = px.scatter(self.df_consumption_pib[self.df_consumption_pib == 'BTSX'], x='GDP', y= '% of alcohol drinkers',  hover_name="Country")
        return fig

        
if __name__ == '__main__':
    con = Consommation()
    con.app.run_server(debug=True, port=8051)