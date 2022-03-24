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
from get_data import df_hr, df_cc, df_hr_col_en, df_hr_col_fr
from utils import *


class Bonheur():
    
    continent_list_en = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"] 
    continent_list_fr = ["Afrique", "Asie", "Europe", "Amérique du Nord", "Océanie", "Amérique du Sud"]
    
    primary_default = "Echelle de vie"
    
    def __init__(self, application = None):
        self.mode = 1
        self.main_layout = html.Div([
            html.H3("Étude du bonheur mondial de 2005 à 2020"),
            dcc.Markdown(md_introduction),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id = 'bnh-graph',
                        config={'displayModeBar': False},
                    )
                ], style = {'width' : '75%', 'display': 'inline-block'}),
                html.Div([
                    dcc.RadioItems(
                        id='bnh-graph-type',
                        options=[
                            {'label':'Echelle de vie', 'value':"Echelle de vie"},
                            {'label':'PIB par habitant','value':"PIB par habitant"},
                            {'label':'Support social', 'value':"Support social"},
                            {'label':'Espérance de vie','value':"Espérance de vie"},
                            {'label':'Liberté de vivre', 'value':"Liberté de vivre"},
                            {'label':'Générosité','value':"Générosité"},
                            {'label':'Perception de la corruption','value':"Perception de la corruption"},
                            {'label':'Effets positifs','value':"Effets positifs"},
                            {'label':'Effets négatifs','value':"Effets négatifs"},
                        ],
                        value = "Echelle de vie",
                        labelStyle={'display':'block'},
                    ),
                    dcc.Markdown(md_introduction)
                ], style = {'width' : '23%', 'display': 'inline-block'})
            ]),
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
            dash.dependencies.Output('bnh-graph', 'figure'),
            [
                dash.dependencies.Input('bnh-graph', 'clickData'),
                dash.dependencies.Input('bnh-graph-type', 'value'),
            ])(self._update_graph)
            
    
    def _update_graph(self, point, graphtype):
        # Ce moyen de faire est un cul de sac, j'ai besoin de recup l'état du graphe (sinon refresh => self.mode pas maj)  
        if not point:
            return self._init_graph_primary(graphtype)
        else :
            print(point, self.mode)
            clicked = point["points"][0].get("pointNumber")
            value = point["points"][0].get("x")
            if self.mode == 1 :
                self.mode = 2
                return self._init_graph_secondary(graphtype, self.continent_list_en[clicked])
            if self.mode == 2 or self.mode == 3:
                self.mode = 3
                return self._init_graph_tertiary(graphtype, value)

    
    
    def _init_graph_primary(self, graphtype):
        # Since the primary figure needs no input, it is considered as static
        primary_figure_values = pd.pivot_table(
            df_hr,
            values=graphtype,
            columns="Continent",
            aggfunc=np.mean).values.tolist()[0]
        primary_figure = px.bar(
            x = self.continent_list_fr,
            y = primary_figure_values,
            title = f'{graphtype}',
            labels=dict(x = graphtype, y = "Continents"),
            template='plotly_white'
        )
        return primary_figure
    
    def _init_graph_secondary(self, graphtype, continent):
        # Since the primary figure needs no input, it is considered as static
        df_hr_cn = df_hr[df_hr["Continent"] == continent]
        df_hr_cnpv = pd.pivot_table(
            df_hr_cn,
            values = graphtype,
            columns = "Pays",
            aggfunc=np.mean
        )
        primary_figure = px.histogram(
            x = df_hr_cnpv.columns,
            y = df_hr_cnpv.values.tolist()[0],
            title = f'{graphtype}, {continent}',
            labels=dict(x = graphtype, y = "Pays"),
            template='plotly_white'
        )
        return primary_figure
    
    def _init_graph_tertiary(self, graphtype, country):
        # Since the primary figure needs no input, it is considered as static
        df_hr_py = df_hr[df_hr["Pays"] == country]
        df_hr_pypv = pd.pivot_table(
            df_hr_py,
            values = graphtype,
            columns = "Année",
            aggfunc=np.mean
        )
        primary_figure = px.line(
            x = df_hr_pypv.columns,
            y = df_hr_pypv.values.tolist()[0],
            title = f'{graphtype}, {country}',
            labels=dict(x = graphtype, y = "Années"),
            template='plotly_white'
        )
        return primary_figure
        
    
if __name__ == '__main__':
    nrg = Bonheur()
    nrg.app.run_server(debug=True, port=8051)
    
    
    
    
    
    
    
    
    
    
    
    
# <------------------------------------------------------->
md_introduction = """
Gallup Organization est une entreprise américaine offrant de nombreux services de recherche concernant le managment, les ressources humaines et les statistiques. Cette entité est particulièrement connue pour efféctuer différents sondages souvent médiatisés.
"""


