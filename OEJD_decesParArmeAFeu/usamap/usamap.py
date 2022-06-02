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
import plotly.express as px
from urllib.request import urlopen
import json
from OEJD_decesParArmeAFeu.gunowners.gunowners import Gunowners
from OEJD_decesParArmeAFeu.gundeaths.gundeaths import Gundeaths
from OEJD_decesParArmeAFeu.data.get_data import FirearmDeathData

def get_years_dic(begin, end):
    years = {}
    for year in range(begin, end + 1, 1):
        years[year] = str(year)
    return years

class Usamap():

    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):

        self.begin = 2001
        self.end = 2020
        self.years = get_years_dic(self.begin, self.end)

        datas = FirearmDeathData(self.begin, self.end)
        self.df_wages = datas.init_wages()
        self.df_crimes = datas.init_crimes()
        self.df_pops = datas.init_population()
        self.df_indexes = datas.init_indexes()

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de morts par arme à feu en fonction du niveau de richesse aux Etats-Unis'),
            html.Div([ dcc.Graph(id='oejd--mpj-main-graph_usamap'), ], style={'width':'100%', }),

            html.Div([dcc.Slider(self.begin, self.end, 1, value=self.begin, id='oejd--my-slider', marks=self.years),
                html.Div(id='oejd--slider-output-container')]),
            dcc.Interval(            # fire a callback periodically
                id='oejd--auto-stepper',
                interval=500,       # in milliseconds
                max_intervals = -1,  # start running
                n_intervals = 0
            ),
            html.Button(
                            self.START,
                            id='oejd--button-start-stop',
                            style={'display':'inline-block'}
                        ),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les états vous avez une infobulle.
                En cliquant sur les points de la barre du bas, vous pouvez choisir sur quelles années afficher les données.

                Notes :
                   * MAF est l'indice du nombre de morts par arme à feu par habitants(/100_000).
                   * L'indice de richesse utilisé est le salaire moyen hebdomadaire.
                   * Nous pouvons voir que globalement, les états avec l'indice de richesse le plus bas ont un MAF plus élevé.
                """)
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        self.gunowners = Gunowners(application)
        self.gundeaths = Gundeaths(application)
        self.main_layout.children.append(self.gunowners.main_layout.children[0])
        self.main_layout.children.append(self.gundeaths.main_layout.children[0])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


        self.app.callback(
                    dash.dependencies.Output('oejd--mpj-main-graph_usamap', 'figure'),
                    [dash.dependencies.Input('oejd--my-slider', 'value')])(self.update_graph)


        self.app.callback(
            dash.dependencies.Output('oejd--button-start-stop', 'children'),
            dash.dependencies.Input('oejd--button-start-stop', 'n_clicks'),
            dash.dependencies.State('oejd--button-start-stop', 'children'))(self.button_on_click)

        self.app.callback(
            dash.dependencies.Output('oejd--my-slider', 'value'),
            dash.dependencies.Input('oejd--auto-stepper', 'n_intervals'),
            [dash.dependencies.State('oejd--my-slider', 'value'),
             dash.dependencies.State('oejd--button-start-stop', 'children')])(self.on_interval)

        self.app.callback(
            dash.dependencies.Output('oejd--auto-stepper', 'max_interval'),
            [dash.dependencies.Input('oejd--button-start-stop', 'children')])(self.run_movie)

    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
            return 0
        else:
            return -1

    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:
            if year == self.end:
                return self.begin
            else:
                return year + 1
        else:
            return year

    def update_graph(self, value):
        df_wage = self.df_wages[value]
        df_index = self.df_indexes[value]

        fig = go.Figure(data=go.Choropleth(
            locations=df_wage['USPS'],
            hoverinfo = "text",
            z=df_wage['Average Weekly Wages'].astype(float),
            locationmode='USA-states',
            colorscale='greens',
            autocolorscale=False,
            text=df_wage['text'], # hover text
            marker_line_color='white', # line markers between states
            showlegend=False,
            colorbar=dict(
                title={'text': 'Salaire moyen/semaine ($)'},
                thickness=35,
                len=1.0,
                bgcolor='rgba(255,255,255,0.6)',

                xanchor='right',
                x=0.0,
                yanchor='bottom',
                y=0.0
            )
        ))

        fig2 = go.Figure(data=go.Scattergeo(locations=df_index["USPS"], locationmode="USA-states",
             showlegend=False,
             hoverinfo = "text",
             text=df_index['text'],
             mode = 'markers',
             marker = dict(
                size=df_index["index"]*333,
                color = df_index["index"],
                line_width = 0,
                sizeref = 9,
                sizemode = "area",
                reversescale = False
             )
        ))

        fig2.update_traces(marker_colorbar=dict(
                title={'text': "MAF"},
                thickness=35,
                len=1.0,
                bgcolor='rgba(255,255,255,0.6)'
            ),
            selector=dict(type='scattergeo')
        )

        fig.add_trace(fig2.data[0])

        fig.update_layout(
            height=700,
            margin=dict(l=0, r=0),
            title_text='Evolution du taux de morts à l\'arme à feu par habitant vs salaire moyen, aux Etats-Unis, en fonction du temps',
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'),
        )

        return fig

if __name__ == '__main__':
    mpj = Usamap()
    mpj.app.run_server(debug=True, port=8051)
