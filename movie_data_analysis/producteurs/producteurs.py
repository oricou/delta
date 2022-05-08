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
import ast

def convert_production(s):
    l = ast.literal_eval(s)
    return l[0]["name"]

def transform_df_prd(df, value_metric, label_metric):
    res = df.copy()
    res[label_metric] = res[label_metric].apply(convert_production)
    if value_metric == "budget":
        res = res.drop(res[res[value_metric] == 0].index)
    
    res = res.groupby(["release_year", label_metric], as_index=False).agg({"title":"count", "revenue":"sum", "budget":"sum"})
    percent_col_name = "percent_of_total_movies" if value_metric == "title" else "percent_of_total_budget"

    res[percent_col_name] = res.groupby("release_year", as_index=False)[value_metric].transform(sum)
    res[percent_col_name] = res[value_metric] / res[percent_col_name]
    res = res.groupby(["release_year", label_metric, value_metric], as_index=False).agg({percent_col_name:"sum"})
    res.loc[res[percent_col_name] < 0.01, label_metric] = "Other"
    res = res.set_index("release_year")

    return res

class Producer():

    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        
        df_entreprises = pd.read_csv("movie_data_analysis/producteurs/data/entreprises_producteurs.csv")
        df_pays = pd.read_csv("movie_data_analysis/producteurs/data/pays_producteurs.csv")
        dfpb = df_pays.copy()

        self.df_producer_budget = transform_df_prd(df_entreprises, "budget", "production_companies") 
        self.df_country_budget = transform_df_prd(dfpb, "budget", "production_countries")
        self.df_country_movies = transform_df_prd(df_pays, "title", "production_countries")

        self.years = sorted(set(self.df_country_movies.index.values))
        self.last_working_year = [1874, 1902, 1902]


        self.main_layout = html.Div(children=[
            html.H3(children='Évolution de la répartition de la production de films par pays et entreprises de production'),

            html.Div('Veuillez attendre une dizaine de secondes que les diagrammes s\'affichent.'), 
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),


            html.Div([

                html.Div([
                    dcc.Graph(id='wps-country-movie-pie', 
                            style={'width':'33%', 'display':'inline-block'}),
                    dcc.Graph(id='wps-country-budget-pie',
                            style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                    dcc.Graph(id='wps-producer-budget-pie',
                            style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                ], style={ 'display':'flex', 
                        'borderTop': 'thin lightgrey solid',
                        'borderBottom': 'thin lightgrey solid',
                        'justifyContent':'center', }),
                    
                html.Div([
                    
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
                'justifyContent':'center'}),

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
            dcc.Markdown("""
            #### À propos
            * Données : [Kaggle / TMdB](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
            * (c) 2022 Adrien Huet et Charlie Brosse
            """),
           

        ], style={
                 'padding': '10px 50px 10px 50px',
                 }
        )
        
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('wps-button-start-stop', 'children'),
            dash.dependencies.Input('wps-button-start-stop', 'n_clicks'),
            dash.dependencies.State('wps-button-start-stop', 'children'))(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output('wps-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('wps-button-start-stop', 'children')])(self.run_movie)
        self.app.callback(
            dash.dependencies.Output('wps-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('wps-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('wps-crossfilter-year-slider', 'value'),
             dash.dependencies.State('wps-button-start-stop', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('wps-country-budget-pie', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.update_country_budget_pie)
        self.app.callback(
            dash.dependencies.Output('wps-country-movie-pie', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.update_country_movie_pie)
        self.app.callback(
            dash.dependencies.Output('wps-producer-budget-pie', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.update_producer_budget_pie)


    # graph movie count per country vs years
    def update_country_movie_pie(self, year):
        try:
            fig = px.pie(self.df_country_movies.loc[[year]], values="title", names="production_countries", title="Répartition de la production de films par pays", width=500, height=500)
            self.last_working_year[0] = year
            return fig
        except:
            return px.pie(self.df_country_movies.loc[[self.last_working_year[0]]], values="title", names="production_countries", title="Répartition de la production de films par pays", width=500, height=500)

    # graph movie budget per country vs years
    def update_country_budget_pie(self, year):
        try:
            fig = px.pie(self.df_country_budget.loc[[year]], values="budget", names="production_countries", title="Répartition du budget des films par pays", width=500, height=500)
            self.last_working_year[1] = year
            return fig
        except Exception as e:
            return px.pie(self.df_country_budget.loc[[self.last_working_year[1]]], values="budget", names="production_countries", title="Répartition du budget des films par pays", width=500, height=500)

    # graph movie budget per producer vs years
    def update_producer_budget_pie(self, year):

        try:
            fig = px.pie(self.df_producer_budget.loc[[year]], values="budget", names="production_companies", title="Répartition du budget de films par producteurs", width=500, height=500)
            self.last_working_year[2] = year
            return fig

        except Exception as e:
            return px.pie(self.df_producer_budget.loc[[self.last_working_year[2]]], values="budget", names="production_companies", title="Répartition du budget de films par producteurs", width=500, height=500)
            
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
    prd = Producer()
    prd.run(port=8055)