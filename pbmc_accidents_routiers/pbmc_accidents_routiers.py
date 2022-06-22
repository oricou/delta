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
import pbmc_accidents_routiers.data.get_data as dp

class Pbmc():
    def __init__(self, application = None):
        self.src = 'https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/'
        self.DATA = None
        self.main_layout = html.Div([
            html.H3("Accident routiers en France"),
            html.Div([
                html.Div(dcc.Graph(id='pbmc-hist'), style={'width':'100%'}),
                html.Div(dcc.RadioItems(
                    id='hist-opts', 
                    value=2,
                    labelStyle={'display':'block'})),
                html.Div([
                    html.Div("Nous pouvons constater que la majorité des accidents sont causés par les véhicules de tourisme d'après les 3 graphes ci-dessus."),
                    html.Div("Ceci peut être du au fait que les véhicules de tourisme sont les plus communs en circulation parmi tout les autres véhicules.")
                    ], style={"text-align":"center"}),
                ], style={"margin-bottom": "10px"}),
            html.Div([
                html.Div(dcc.Graph(id='pbmc-scatter'), style={'width':'100%'}),
                html.Div(dcc.RadioItems(
                    id='scatter-opts', 
                    value=2,
                    labelStyle={'display':'block'})),
                html.Div([
                    html.Div("En observant le graphe 3D, nous pouvons aussi remarquer que des véhicules entre l'age de 0 et 20 ans sont à l'origine de la plupart des accidents."),
                    html.Div("Nous pouvons assumer que la raison pour cela est du au fait que les conducteurs à l'origine de la plupart des accidents ont besoin de changer de véhicules plus fréquemment que des conducteurs attentifs.")
                ], style={"text-align":"center"})
            ], style={"margin-bottom": "10px"}),
            html.H4('A propos'),
            html.Div([
                html.Div(['Source des données:'], style={'margin-right': '5px'}),
                html.A('ici', href=self.src),
            ],style={'display': 'flex'}),
            html.Div('auteurs: Philippe Bouchet, Michail Chatzizacharias  © 2022 ')
        ])

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        self.app.callback(
                    dash.dependencies.Output('pbmc-hist', 'figure'),
                    dash.dependencies.Input('hist-opts', 'value'))(self.show_hist)
        self.app.callback(
                    dash.dependencies.Output('pbmc-scatter', 'figure'),
                    dash.dependencies.Input('scatter-opts', 'value'))(self.show_scatter)

    def load_data(self):
        if self.DATA is None:
            self.DATA = dp.loadData()
        return self.DATA

    def show_hist(self, mean):    
        data = self.load_data()
        fig = px.histogram(    
            data,    
            x = data["Année"],    
            color = data["Catégorie véhicule"],    
            facet_col = "Type Accident",    
            facet_col_wrap = 3,    
            title="Gravité des accidents en relation avec les catégories des véhicules",
        )
        fig.update_layout(barmode="stack", bargap=0.2)    
        fig.for_each_annotation(
                lambda a: a.update(
                    text=a.text.replace("Type Accident=", "Accidents ")
                )
        )
        return fig

    def show_scatter(self, mean):    
        color = {    
            "léger" : "#00cc96",    
            "mortel" : "#ef553b",    
            "grave non mortel" : "#636efa"    
        }
        data = self.load_data()

        fig2 = px.scatter_3d(    
             dp.getMortality(data),
             x = 'Année',    
             y = 'Age véhicule',    
             z = 'count',    
             color = 'Type Accident',    
             color_discrete_map=color,    
             title="Gravité des accidents en relation avec l'age des véhicules"
        )    

        return fig2
 
if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)
