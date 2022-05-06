import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

class Anthroponymie():
    def __init__(self, application=None):
        self.df = pd.read_csv('PSJCD_Anthroponymie/data/nomsParDpt.txt', sep='\t', lineterminator='\n')
        a = pd.DataFrame(self.getPopWithDate("COQUEL"))
        fig = px.scatter(a)
        self.main_layout = html.Div(children=[
            html.H3(children='Anthroponymie par département'),
            html.Div([dcc.Graph(figure=fig), ], style={'width': '100%', }),
            dcc.Input(id="input2", type="text", placeholder="", debounce=True),
            html.Br(),                    
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
    
    def getPopWithDate(self, name):
        return self.df[self.df["NOM"] == name].sum(numeric_only=True)

if __name__ == '__main__':
    atr = Anthroponymie()
    atr.app.run_server(debug=True, port=8051)
