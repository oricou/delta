import http
import sys
import dash
import flask
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from typing import List, Dict, Callable, Any

class TGV:
    
    callbacks = [
        #{'callback': self.updater, 'input': [Input(), ], 'output': Output},
    ]
    
    def make_df(self) -> pd.DataFrame:
        return pd.DataFrame()

    def make_layout(self) -> html.Component:
        return html.Div()
        
        
    def __init__(self, application: dash.Dash = None):
        self.main_layout = self.make_layout()
        self.df = self.make_df()
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
            
        for callback in self.callbacks:
            self.app.callback(callback['output'], callback['input'])(callback['callback'])

if __name__ == '__main__':
    nrg = TGV()
    nrg.app.run_server(debug=True, port=8051)
