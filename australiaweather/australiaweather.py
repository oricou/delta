import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class DataDetail():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        
        df = pd.read_csv('data/stations_mesures.csv', sep=' ', names=['ID', 'lat','long','info','from','to'])
        df = df.drop(columns=['lat','long','info'])
        df = df.groupby('ID', as_index =False).agg({'from' : 'min', 'to' : 'max'})#.sort_values(by=['from','to'], ascending=True)
        self.df = df
        
        self.number = len(df.index) - 150

        self.main_layout = html.Div(children=[
            html.H3(children='temps de diffusion des données des stations météos d\'Australie'),

            html.Div([
                    html.Div([ dcc.Graph(id='sls-main-graph'), ], style={'width':'90%', }),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),
            html.Div([
                html.Div(
                    html.Button(
                            self.START,
                            id='sls-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                    html.Br(),
                    dcc.Slider(
                            id='sls-crossfilter-number-slider',
                            min=0,
                            max=self.number,
                            step = 1,
                            value= (self.number + self.number % 2) / 2,
                            marks={str(number): str(number) for number in range(0, self.number, 150)},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='sls-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),
                
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
            dash.dependencies.Output('sls-main-graph', 'figure'),
            [ dash.dependencies.Input('sls-crossfilter-number-slider', 'value')])(self.dash_plotStationLifeSpan)
        self.app.callback(
            dash.dependencies.Output('sls-button-start-stop', 'children'),
            dash.dependencies.Input('sls-button-start-stop', 'n_clicks'),
            dash.dependencies.State('sls-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('sls-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('sls-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('sls-crossfilter-number-slider', 'value'),
            dash.dependencies.Input('sls-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('sls-crossfilter-number-slider', 'value'),
             dash.dependencies.State('sls-button-start-stop', 'children')])(self.on_interval)
      
    def dash_plotStationLifeSpan(self, num_stations):
        df = self.df
        df_plot = df.copy() if num_stations == None else df.head(num_stations).copy()
        df_plot['timespan'] = df['to']-df['from']
        df_plot = df_plot.sort_values(by='timespan', ascending=True)
        fig = px.bar(df_plot, x='ID', y='timespan', base = 'from',  barmode = 'group',
                     labels = {'ID':'Stations','timespan':'Years of existence'}, title = "Stations' lifespans",
                     range_x=(0,df_plot.shape[0]),opacity=1) 
        fig.update_traces(marker_color='green')
        fig.update_xaxes(ticktext=[], tickvals=[])
        fig.update_layout(yaxis_range=[min(df_plot['from'])*0.99, max(df_plot['to']*1.01)])
        fig.update_xaxes(constrain='range')
        fig.update_traces(hovertemplate ='<b>ID</b>: %{x}'+'<br>from : %{base}'+'<br>to : %{y}')

        return fig

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
    def on_interval(self, n_intervals, number, text):
        if text == self.STOP:  # then we are running
            if number + 150 >= self.number:
                return 0
            else:
                return number + 150
        else:
            return number  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)
    
if __name__ == '__main__':
    ws = WorldStats()
    ws.run(port=8055)