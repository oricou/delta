import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
import json
import matplotlib.pyplot as plt

def convert_genres(s):
	l = json.loads(s.replace('\'', '"'))
	ret = []
	for d in l:
		ret.append(d['name'])
	return ret

class ThemeAnalysis():

    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):

        self.df = pd.read_csv('theme_popularite/data/theme_popularite.csv')
        self.df.genres = self.df.genres.apply(convert_genres)
        df_exploded = self.df.explode('genres')
        self.df_year = df_exploded.groupby(["release_year","genres"], as_index=False).agg({"budget":"sum", "revenue":"sum", "popularity":"mean", "vote_average":"mean", "vote_count":"mean", "title":"count"})
        self.df_year = self.df_year.set_index('release_year')
        self.years = sorted(set(self.df_year.index.values))

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution des revenus des films par rapport à leurs genres et au budget alloué'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du thème en bas. Pour chaque graphique, cliquez sur autoscale.'), 

            html.Div([
                    html.Div([ dcc.Graph(id='wps-main-graph', animate=True), ], style={'width':'90%', }),

                    html.Div([
                        # html.Div('Continents'),
                        # dcc.Checklist(
                        #     id='wps-crossfilter-which-continent',
                        #     options=[{'label': self.french[i], 'value': i} for i in sorted(self.continent_colors.keys())],
                        #     value=sorted(self.continent_colors.keys()),
                        #     labelStyle={'display':'block'},
                        # ),
                        html.Br(),
                        html.Div('Échelle en X'),
                        dcc.RadioItems(
                            id='wps-crossfilter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                            value='Log',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            self.START,
                            id='wps-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='wps-crossfilter-year-slider',
                            min=self.years[0],
                            max=self.years[-1],
                            step = 1,
                            value=self.years[0],
                            marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='wps-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Br(),
            html.Div(id='wps-div-theme'),

            html.Div([
                dcc.Graph(id='wps-revenue-time-series', 
                          style={'width':'33%', 'display':'inline-block'}),
                dcc.Graph(id='wps-budget-time-series',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='wps-moviecount-time-series',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Br(),
            dcc.Markdown("""
            #### À propos
            * Données : [Kaggle / TMdB](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
            * (c) 2022 Charlie Brosse
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
            dash.dependencies.Output('wps-main-graph', 'figure'),
            [ dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value'),
              dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('wps-div-theme', 'children'),
            dash.dependencies.Input('wps-main-graph', 'hoverData'))(self.theme_chosen)
        # self.app.callback(
        #     dash.dependencies.Output('wps-button-start-stop', 'children'),
        #     dash.dependencies.Input('wps-button-start-stop', 'n_clicks'),
        #     dash.dependencies.State('wps-button-start-stop', 'children'))(self.button_on_click)
        # # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        # self.app.callback(
        #     dash.dependencies.Output('wps-auto-stepper', 'max_interval'),
        #     [dash.dependencies.Input('wps-button-start-stop', 'children')])(self.run_movie)
        # # triggered by previous
        # self.app.callback(
        #     dash.dependencies.Output('wps-crossfilter-year-slider', 'value'),
        #     dash.dependencies.Input('wps-auto-stepper', 'n_intervals'),
        #     [dash.dependencies.State('wps-crossfilter-year-slider', 'value'),
        #      dash.dependencies.State('wps-button-start-stop', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('wps-revenue-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graph', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_revenue_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-budget-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graph', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_budget_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-moviecount-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graph', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_moviecount_timeseries)


    def update_graph(self, xaxis_type, year):
        print(f" yoyo {year}") 
        size = self.df_year.loc[year]['title'].to_numpy()
        nb_films = size.sum()
        s = [((s/nb_films) * 100)*2 + 10 for s in size]

        dfg = self.df_year.loc[year]
        fig = px.scatter(dfg, x = "budget", y = "revenue", 
                        size = s, 
                        color = "genres",
                        hover_name="genres")
        fig.update_layout(
                    xaxis = dict(title='Budget moyen par film',
                      type= 'linear' if xaxis_type == 'Linéaire' else 'log',
                      range=(0,3000000000) if xaxis_type == 'Linéaire' 
                                      else (np.log10(1000000), np.log10(1000000000)) 
                     ),
         yaxis = dict(title="Revenu moyen par film", range=(0,1000000000)),
         margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
         hovermode='closest',
         showlegend=False,
         )
        # plt.autoscale(enable=True, axis="both")
        return fig

    def create_time_series(self, genre, what, axis_type, title):
        return {
            'data': [go.Scatter(
                x = self.years,
                y = self.df_year[self.df_year["genres"] == genre][what],
                mode = 'lines+markers',
            )],
            'layout': {
                'height': 325,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title':title,
                          'type': 'linear' if axis_type == 'Linéaire' else 'log'},
                'xaxis': {'showgrid': False}
            }
        }


    def get_theme(self, hoverData):
        if hoverData == None:  # init value
            return self.df['genres'].iloc[np.random.randint(len(self.df_year))]
        return hoverData['points'][0]['hovertext']

    def theme_chosen(self, hoverData):
        return self.get_theme(hoverData)

    # graph movie revenue vs years
    def update_revenue_timeseries(self, hoverData, xaxis_type):
        theme = self.get_theme(hoverData)
        return self.create_time_series(theme, 'revenue', xaxis_type, 'Revenu moyen généré par le film (US $)')

    # graph movie budget vs years
    def update_budget_timeseries(self, hoverData, xaxis_type):
        theme = self.get_theme(hoverData)
        return self.create_time_series(theme, 'budget', xaxis_type, "Budget moyen du film (US $)")

    # graph movie count vs years
    def update_moviecount_timeseries(self, hoverData, xaxis_type):
        theme = self.get_theme(hoverData)
        return self.create_time_series(theme, 'title', xaxis_type, 'Nombre de films')

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
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    tmA = ThemeAnalysis()
    tmA.run(port=8055)