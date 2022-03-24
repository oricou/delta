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

class Bonheur():
    
    
    
    def __init__(self, application = None):
        self.df = df_hr
        

        
        self.main_layout = html.Div()

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == '__main__':
    nrg = Bonheur()
    nrg.app.run_server(debug=True, port=8051)
