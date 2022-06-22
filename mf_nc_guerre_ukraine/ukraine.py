import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from scipy import stats
from scipy import fft
import datetime
import os
import mf_nc_guerre_ukraine.data.get_data as gd

class Ukraine():
    def __init__(self, application = None):
        self.START = "START"
        self.STOP = "STOP"
        self.equipement = gd.get_data('mf_nc_guerre_ukraine/data/russia_losses_equipment.pkl', ffill=True)
        self.personnel = gd.get_data('mf_nc_guerre_ukraine/data/russia_losses_personnel.pkl', ffill=True)
        self.personnel.rename({'POW':'Prisonnier de guerre', 'personnel':'Armee' },axis = 1, inplace = True)

        self.threads = gd.get_tweeter_threads('mf_nc_guerre_ukraine/data/threads.pkl')

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution du Stock d\'armement de la Russie'),
            html.Div([ dcc.Graph(id='equipement-main-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('equipement'),
                           dcc.Dropdown(
                               id='equipement-dropdown',
                               options= [label for label in self.equipement.columns[2:]],
                               value=[label for label in self.equipement.columns[2:5]],
                               multi=True,
                           )
                         ], style={'width': '15em'} ),
                html.Div([ html.Div('Échelle en y'),
                                dcc.RadioItems(
                                    id='equipement-yaxis-type',
                                    options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                                    value='Logarithmique',
                                    labelStyle={'display':'block'},
                                )
                              ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} )
                              ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

                html.Br(),
                dcc.Markdown("""
                Ce graphique represente l'evolution du materiel militaire Russie de puis le debut de la guerre.
                Sans surprise, on peut constater un pique d'achats d'armes des Russes au moment de l'attaque avec une evolution lineaire pour chaque equipement.
            
                """),
                html.Br(),
                html.Br(),
                html.Br(),





                html.H3(children='Évolution de l\'armee Russe'),

                 html.Div([ dcc.Graph(id='armee-main-graph'), ], style={'width':'100%', }),

                 html.Div([
                    html.Div([ html.Div('type'),
                                dcc.RadioItems(
                                    id='personnel-type',
                                    options=[{'label':'armee', 'value':0}, 
                                             {'label':'prisonier de guerre','value':1},
                                             {'label':'armee + prisonier de guerre','value':2}],
                                    value=1,
                                    labelStyle={'display':'block'},
                                )
                              ], style={'width': '15em'} ),
                              ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

                     html.Br(),
                     dcc.Markdown("""
                     Nous pour regarder ici l'evolution de l'armee Russe et de ses prisonnier des guerres depuis le debut de la guerre
                     Notes :
                        * A partir du 31 Mars, nous n'avons plus d'informations sur les prisonniers de guerres en Russie et c'est pour cela qu'il n'y pas d'evolution des batonnets mais nous pouvons supposer une importante evolution de cette courbe
                     

                     """),


                html.Br(),
                html.Br(),
                html.Br(),
                html.H3(children='Evolution des Threads Tweeter'),
                html.Div([ dcc.Graph(id='Tweet-main-graph'), ], style={'width':'100%', }),
                html.Div([
                    html.Div(
                        dcc.Slider(
                                id='tweets-slider',
                                min=0,
                                max=len(self.threads.index),
                                step = 5,
                                value=45,
                                marks={str("day " + str(i)): str("day " + str(i)) for i in range(0,len(self.threads.index),10)},
                        ),
                        style={'display':'inline-block', 'width':"90%"}
                    ),
                    dcc.Interval(            # fire a callback periodically
                        id='mf-auto-stepper',
                        interval=500,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                ),
                html.Button(
                            self.START,
                            id='mf-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                html.Div([ dcc.RadioItems(id='tweet-format', 
                                     options=[{'label':'Tweet', 'value':0},
                                              {'label':'Score', 'value':1}, 
                                              {'label':'Ratio', 'value':2}], 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),
                html.Br(),
                html.Br(),
                dcc.Markdown("""
                Ici nous pouvons observer l'evolution des Threads portant du la guerre en Ukraine sur Tweeter.
                On peut constater un pique de re-tweet le 24 fevrier qui represente le jour de l'invasion

                #### À propos
                * Données : 
                    * [2022 ukraine russian war stat](https://www.kaggle.com/datasets/piterfm/2022-ukraine-russian-war)
                    * [Russian Invasion of Ukraine](https://www.kaggle.com/datasets/ioexception/rworldnews-russian-invasion-of-ukraine)
                * (c) 2022 Massil Ferhani - Nikoloz Chaduneli
                """),
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

        self.app.callback(
                    dash.dependencies.Output('equipement-main-graph', 'figure'),
                    [dash.dependencies.Input('equipement-dropdown', 'value'),
                     dash.dependencies.Input('equipement-yaxis-type', 'value')])(self.update_equipement)
        
        self.app.callback(
                    dash.dependencies.Output('armee-main-graph', 'figure'),
                    [dash.dependencies.Input('personnel-type', 'value')])(self.update_personnel)
        
        self.app.callback(
            dash.dependencies.Output('mf-button-start-stop', 'children'),
            dash.dependencies.Input('mf-button-start-stop', 'n_clicks'),
            dash.dependencies.State('mf-button-start-stop', 'children'))(self.button_on_click)
        
        self.app.callback(
            dash.dependencies.Output('mf-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('mf-button-start-stop', 'children')])(self.run_movie)
        
        self.app.callback(
            dash.dependencies.Output('tweets-slider', 'value'),
            dash.dependencies.Input('mf-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('tweets-slider', 'value'),
             dash.dependencies.State('mf-button-start-stop', 'children')])(self.on_interval)

        self.app.callback(
                    dash.dependencies.Output('Tweet-main-graph', 'figure'),
                    [dash.dependencies.Input('tweet-format', 'value'),
                        dash.dependencies.Input('tweets-slider', 'value'), ])(self.update_tweet)

    def update_equipement(self, equipement, axis):
        if not isinstance(equipement, list) or not len(equipement):
            return {}
        else:
            equipement = ["date"] + equipement
        df = self.equipement[equipement]
        df = df.set_index('date')
        fig = px.line(df[df.columns[0]], template='plotly_white')

        for c in df.columns[1:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
            fig.update_layout(
                yaxis = dict(type= 'linear' if axis == 'Linéaire' else 'log',),
                height=450,
                hovermode='closest',
                legend = {'title': "equipement"},
                )
        return fig

    def update_personnel(self, personnel):
        if personnel == 0:
            select = ["date", "Armee"] 
        elif personnel == 1:
            select = ["date", "Prisonnier de guerre"]
        else:
            select = ["date", 'Prisonnier de guerre', 'Armee']
        df = self.personnel[select]
        df = df.set_index('date')
        fig = px.bar(df, x=df.index, y=df.columns)
        fig.update_layout(
            yaxis = dict(type= 'log'),
        )
        return fig
    
    def on_interval(self, n_intervals, step, text):
        if text == self.STOP:  # then we are running
            return (step + 1) % len(self.threads.index)
        else:
            return step  # nothing changes
    
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

    def update_tweet(self, button, slider):
        tab = ""
        x = ""
        if  button == 0 :
            tab = "num_comments"
            x = "Nombre de re-tweet par jour"
        elif button == 1 :
            tab = "score"
            x = "Score"
        else:
            tab = "upvote_ratio"
            y = "Ratio"
        df = self.threads[[tab]].head(slider)
        fig = px.line(df, template='plotly_white')
        fig.update_layout(
            #title = 'Évolution des prix de différentes énergies',
            xaxis = dict(title=""), # , range=['2010', '2021']), 
            yaxis = dict(title=x, type='log'), 
            height=450,
            showlegend=False,
        ) 

        return fig


        
if __name__ == '__main__':
    mpj = Ukraine()
    mpj.app.run_server(debug=True, port=8051)