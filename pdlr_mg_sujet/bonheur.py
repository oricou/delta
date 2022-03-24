import sys, os
import dash, flask

from dash import dcc, html

import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px

import dateutil as du

# Manipulation du path pour ajouter le chemin relatif et
# empecher des erreurs peu importe le chemin de la source
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from get_data import df_hr, df_cc
from utils import *


class Bonheur():
    
    continent_list_en = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"] 
    continent_list_fr = ["Afrique", "Asie", "Europe", "Amérique du Nord", "Océanie", "Amérique du Sud"]
    
    def __init__(self, application = None):
        
        self.main_layout = html.Div([
            html.H3("Étude du bonheur mondial de 2005 à 2020"),
            dcc.Markdown(md_introduction),
            html.Div([
                dcc.Graph(
                    id='bnh-primary-graph', 
                    config={'displayModeBar': False},
                )
            ], style = {'width' : '100%'}),
            html.Div([
                dcc.RadioItems(
                    id='bnh-continent',
                     options=[
                         {'label':'Afrique', 'value':'Africa'}, 
                         {'label':'Amérique du Nord','value':'North America'}, 
                         {'label':'Amérique du Sud','value':'South America'}, 
                         {'label':'Asie','value':'Asia'}, 
                         {'label':'Europe','value':'Europe'}, 
                         {'label':'Océanie','value':'Oceania'},
                    ],
                    labelStyle={'display':'block'},
                )
            ])
        ], style = {
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


        self.app.callback(
            dash.dependencies.Output('bnh-primary-graph', 'figure'),
            [
                dash.dependencies.Input('bnh-continent', 'value')
            ])(self.update_graph)
            
            
    def update_graph(self, _, param = "Echelle de vie"):
        values = pd.pivot_table(df_hr, values="Echelle de vie", columns="Continent", aggfunc=np.mean).values.tolist()[0]
        fig = px.bar(
            x = self.continent_list_fr,
            y = values,
            labels=dict(x = param, y = "Continents"),
            template='plotly_white'
        )
        return fig

    
if __name__ == '__main__':
    nrg = Bonheur()
    nrg.app.run_server(debug=True, port=8051)
    
    
    
    
    
    
    
    
    
    
    
    
# <------------------------------------------------------->
md_introduction = """
Gallup Organization est une entreprise américaine offrant de nombreux services de recherche concernant le managment, les ressources humaines et les statistiques. Cette entité est particulièrement connue pour efféctuer différents sondages souvent médiatisés.
"""


