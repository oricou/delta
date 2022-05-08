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
        
        inventory = (pd.read_csv('australiaweather/data/stations_mesures.csv', sep = ' '
                ,names = ['ID', 'lat', 'long', 'info', 'from', 'to']
                ,usecols=['ID', 'lat', 'long', 'info', 'from', 'to']))

        num_df = (pd.DataFrame({'year':list(range(
                                            min(inventory['from']), 
                                            max(inventory['to'])))})) #liste les annés entre les permières et les dernières mesures
        num_df['number'] = 0 #initialise le nombre total de mesures
        num_df[inventory['info'].unique()] = 0 #Crée un colone pour chaque type de mesure
        for  index, r in inventory.iterrows():
            num_df.loc[(num_df["year"] >= r['from']) & (num_df["year"] <= r['to']), r['info']] += 1
            #^^ Sélectionne les annés tu df entre 'from' et 'to' puis incrépente la mesure 'info'
            num_df.loc[(num_df["year"] >= r['from']) & (num_df["year"] <= r['to']), 'number'] += 1
        #idem mais avec la colone number
        self.df = num_df
        
        self.data_colors = {'PRCP':'blues', 'DAPR':'red', 'DWPR':'green', 'MDPR':'brown', 'TMAX':'navy', 'TMIN':'pink', 'DATX':'magenta', 'MDTX':'orange', 'DATN':'purple', 'MDTN':'peach', 'TAVG':'magma'}
        self.data = {'PRCP':'Precipitation', 'DAPR':'DAPR', 'DWPR':'DWPR', 'MDPR':'MDPR', 'TMAX':'Temperature maximum', 'TMIN':'Temperature minimum', 'DATX':'DATX', 'MDTX':'MDTX', 'DATN':'DATN', 'MDTN':'MDTN', 'TAVG':'Temperature moyenne'}

        self.main_layout = html.Div(children=[
            html.H3(children='Test'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 

            html.Div([
                    html.Div([ dcc.Graph(id='sws-main-graph'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Type de donnée'),
                        dcc.Checklist(
                            id='sws-crossfilter-which-data',
                            options=[{'label': self.data[i], 'value': i} for i in self.data_colors.keys()],
                            value=self.data_colors.keys(),
                        ),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
        
            html.Br(),
            dcc.Markdown("""
            À propos
                *DAPR = Number of days included in the multiday precipiation 
                *DWPR = Number of days with non-zero precipitation included in multiday precipitation total (MDPR)
                *MDPR = Multiday precipitation total
                *DATX = Number of days included in the multiday maximum temperature
                *MDTX = Multiday maximum temperature
                *DATN = Number of days included in the multiday minimum temperature
                *MDTN = Multiday minimum temperature 
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
        dfg = self.df
        column = ['year', 'number']
        column = column.extend(datatype)
        fig = px.bar(df, x = 'year', y = df.columns[2:], title = "Number of measure depending the year")
        
        return fig

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = WorldStats()
    ws.run(port=8055)
