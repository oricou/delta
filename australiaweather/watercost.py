import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class WaterCostMapping():
    START = 'Start'
    STOP  = 'Stop'
    
    def __init__(self, application = None):
        self.df = pd.read_pickle('australiaweather/data/mesures_by_stations.csv')
        self.price = pd.read_pickle('australiaweather/data/prices.pkl')
        
        self.years = self.df["date"].unique()
        self.y_start = self.years.min()
        self.y_end = self.years[:-2]
        self.main_layout = html.Div(children=[
            html.H3(children='Précipitation et prix de l\'eau'),

            html.Div([ dcc.Graph(id='pem-main-graph'), ], style={'width':'90%', }),
            html.Div([ dcc.Graph(id='ppm-main-graph'), ], style={'width':'90%', }),
                

            html.Br(),
            
            html.Br(),
            dcc.Markdown("""
            Dans notre étude nous avons essayé de mettre en valeur la corrélation entre le prix de l'eau et les précipitations en fonction de différentes zones. Dans les cartes suivantes, chaque point représente une station de mesure, sa couleur représente le total de précipitation enregistré durant le mois. Sur la seconde carte, on peut voir la moyenne du prix d'échange du Megalitre (1 million de litre) dans l'état. 

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
            dash.dependencies.Output('pem-main-graph', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.plotEvolutionMap)
        self.app.callback(
            dash.dependencies.Output('ppm-main-graph', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.plotPrices)
        self.app.callback(
            dash.dependencies.Output('wps-button-start-stop', 'children'),
            dash.dependencies.Input('wps-button-start-stop', 'n_clicks'),
            dash.dependencies.State('wps-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('wps-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('wps-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('wps-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('wps-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('wps-crossfilter-year-slider', 'value'),
             dash.dependencies.State('wps-button-start-stop', 'children')])(self.on_interval)

    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
            return 0 
        else:
            return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-2]:
                return self.years[0]
            else:
                return self.year[self.year.index(year) + 1]
        else:
            return year  # nothing changes

    def plotPrices(self, date):
        '''
        Plots the territories' water price evoluting by month
        '''
        geo_json='data/geo_datas/states.geojson'
        fig = (px.choropleth(self.price,
                    geojson=geo_json,
                    locations=self.price['dest_state'],
                    featureidkey="properties.STATE_NAME",
                    color="price_per_ML",
                    animation_frame='date_of_approval',
                    projection="mercator",
                    range_color=[0,500]))

        fig.update_geos(fitbounds="locations", visible=True)
        return fig

    def plotEvolutionMap(self, date):
        '''
        Plots the map of all the stations and their precipitation evoluting by month

        '''
        fig = (px.scatter_mapbox(self.df, lat='lat', lon='long',
        hover_name="ID",
        animation_group="ID",
        animation_frame="date",
        color='value',
        range_color = [0,6000],
        zoom=3, height=500))
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    
    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)
    

if __name__ == '__main__':
    ws = WorldStats()
    ws.run(port=8055)
