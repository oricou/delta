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
            html.H3(children='Évolution du taux de natalité vs le niveau moyen de revenu par pays'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 
            html.Div([ dcc.Graph(id='pem-main-graph'), ], style={'width':'90%', }),
            html.Div([ dcc.Graph(id='ppm-main-graph'), ], style={'width':'90%', }),
                   
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='wps-crossfilter-year-slider',
                            min=2008,
                            max=2022,
                            step = 1,
                            value=2010,
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Br(),
            
            html.Br(),
            dcc.Markdown("""
            #### À propos

            * Inspiration initiale : [conférence de Hans Rosling](https://www.ted.com/talks/hans_rosling_new_insights_on_poverty)
            * [Version Plotly](https://plotly.com/python/v3/gapminder-example/)
            * Données : [Banque mondiale](https://databank.worldbank.org/source/world-development-indicators)
            * (c) 2022 Olivier Ricou
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
