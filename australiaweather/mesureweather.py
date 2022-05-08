import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class StationStats():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        
        self.df = pd.read_pickle('australiaweather/data/data_inventory.pkl')
        
        self.data_colors = {'PRCP':'darkblue', 'DAPR':'red', 'DWPR':'green', 'MDPR':'brown', 'TMAX':'navy', 'TMIN':'crimson', 'DATX':'magenta', 'MDTX':'cyan', 'DATN':'purple', 'MDTN':'gray', 'TAVG':'coral'}
        self.data = {'PRCP':'Precipitation', 'DAPR':'DAPR', 'DWPR':'DWPR', 'MDPR':'MDPR', 'TMAX':'Temperature maximum', 'TMIN':'Temperature minimum', 'DATX':'DATX', 'MDTX':'MDTX', 'DATN':'DATN', 'MDTN':'MDTN', 'TAVG':'Temperature moyenne'}

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition et quantité des mesures'),
            html.Div([
                    html.Div([ dcc.Graph(id='sws-main-graph'), ], style={'width':'80%', }),

                    html.Div([
                        html.Div('Type de donnée'),
                        dcc.Checklist(
                            id='sws-crossfilter-which-data',
                            options=[{'label': self.data[i], 'value': i} for i in sorted(self.data_colors.keys())],
                            value=sorted(self.data_colors.keys()),
                        )
                    ], style={'margin-left':'15px', 'width': '12em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
        
            html.Br(),
            dcc.Markdown("""
                * DAPR = Number of days included in the multiday precipiation 
                * DWPR = Number of days with non-zero precipitation included in multiday precipitation total (MDPR)
                * MDPR = Multiday precipitation total
                * DATX = Number of days included in the multiday maximum temperature
                * MDTX = Multiday maximum temperature
                * DATN = Number of days included in the multiday minimum temperature
                * MDTN = Multiday minimum temperature
                
                Comme constaté précédement le nombre de station est élevé, Cependant chacune n'effectue pas les mêmes mesures. nous avons voulue vérifier que la mesure qui nous interesse (les précipitations) était assez représenté.

Nous disposons donc de nombreuses mesures pour étudier les précipitations et les phénomènes météorologiques. Le nombre de stations ainsi que leurs activités sont montrés dans les graphiques suivants.
(c) 2022 Martin Poulard
(c) 2022 Grégoire Gally
            """),
           

        ], style={
                #'backgroundColor': 'rgb(240, 240, 240)',
                 'padding': '10px 50px 10px 50px',
                 }
        )
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('sws-main-graph', 'figure'),
            [ dash.dependencies.Input('sws-crossfilter-which-data', 'value')])(self.update_graph)


    def update_graph(self, datatype):
        column = ['year', 'number']
        column = column.extend(datatype)
        dfg = self.df
        fig = px.bar(dfg, x = 'year', y = dfg.columns[2:], title = "Number of measure depending the year")
        
        return fig

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = WorldStats()
    ws.run(port=8055)
