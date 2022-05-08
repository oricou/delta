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
from OEJD_decesParArmeAFeu.data.get_data import GunDeathsData

def get_years_dic(begin, end):
    years = {}
    for year in range(begin, end + 1, 1):
        years[year] = str(year)
    return years


class Gundeaths():
    def init_fig_cod(self):
        df = self.df_cod
        names = ["Suicide", "Homicide", "Évitable/Accident", "Autre"]
        fig = px.pie(df, values='Total', names=names)
        fig.update_layout(legend_x=0, legend_y=1)
        fig.update_layout(title="Raisons des décès par arme à feu aux États-Unis en 2020")
        return fig

    def __init__(self, application = None):
        self.begin = 1999
        self.end = 2020
        datas = GunDeathsData(self.begin, self.end)
        self.gundeaths = datas.init_gundeaths()
        self.df_agedeaths = datas.init_agedeaths()
        self.df_cod = datas.init_cod()
        self.years = get_years_dic(self.begin, self.end)

        self.main_layout = html.Div(children=[html.Div([
            html.Div(html.H3("Raisons et victimes des meurtres avec une arme à feu aux États-Unis")),
            html.Br(),
            html.Div([
                dcc.Graph(id='graph-cod', figure=self.init_fig_cod()),
                dcc.Markdown('Le graphique représente les raisons principales ayant causé des morts avec arme à feu\
                aux États-Unis en 2020. Le total sur cette année est de 45 222, ce qui est 13,9 % de plus par rapport à 2019 (39 707).\
                 86% des 45 222 défunts sont des hommes.')
            ]),
            html.Br(),
            html.Div([
            html.Div([
                dcc.Graph(id='graph-agedeaths'), ], style={'width':'90%', }),
            html.Div([
                html.Br(),
                html.Br(),
                html.Br(),
                dcc.Checklist(
                               options={
                                    'Male': 'Hommes',
                                    'Female': 'Femmes',
                               },
                               value=['Male', 'Female'],
                               labelStyle={'display':'block'},
                               id='checklist'
                            )], style={'margin-left':'2px', 'width': '6em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px',
                    'display':'flex',
                    'justifyContent':'center'
                }),
            html.Div([
                html.Div([dcc.Slider(self.begin, self.end, 1, value=self.begin, id='my-slider-deaths', marks=self.years),
                    html.Div(id='slider-output-deaths')]),
                html.Br(),
                dcc.Markdown("""
                            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.
                            En utilisant les icônes en haut à droite, on peut agrandir une zone, réinitialiser.
                            L'échelle n'est pas dynamique pour mettre en valeur les différences (notamment entre les hommes et les femmes)
                            mais il est possible de zoomer sur le graphique et de faire une mise à l'échelle automatique en appuyant sur le bouton Autoscale au dessus du graphique.
                            Il est possible de sélectionner le sexe que vous souhaitez observer ainsi que les différentes raisons de décès avec les cases à cocher/cliquer à droite du graphique.

                            Notes :
                               * À partir de 2019 les raisons "Indéterminé" et "Intervention judiciaire" ne sont pas présentes.

                            #### À propos
                            * Sources : 
                               * database de National Safety Council créé à partir de [CDC Wonder](https://wonder.cdc.gov/mcd-icd10.html)
                               * [base des salaires moyens](https://data.bls.gov/maps/cew/US?period=2021-Q3&industry=10&geo_id=US000&chartData=3&distribution=1&pos_color=blue&neg_color=orange&showHideChart=show&ownerType=0) du U.S. BUREAU OF LABOR STATISTICS
                               * [base des morts par arme à feu](https://usafacts.org/data/topics/security-safety/crime-and-justice/firearms/firearm-deaths/) de US gun deaths créée à partir de la base du [Centers for Disease Control and Prevention](https://wisqars.cdc.gov/data/explore-data/home).
                               * [base du rescensement](https://www2.census.gov/programs-surveys/popest/tables/) du US CENSUS BUREAU.
                               * [State-Level Estimates of Household Firearm Ownership](https://www.rand.org/pubs/tools/TL354.html) sur le site de RAND Corporation
                            * (c) 2022 Joseph Durand et Othman Elbaz
                            """)
            ])
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )])
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('graph-agedeaths', 'figure'),
                    [dash.dependencies.Input('my-slider-deaths', 'value'),
                    dash.dependencies.Input('checklist', 'value')])(self.update_fig_agedeaths)



    def update_fig_agedeaths(self, year, sex):
        df = self.df_agedeaths[year]
        if (len(sex) == 1):
            df = df[df['Sex'] == sex[0]]
        elif (len(sex) == 2):
            df = df[(df['Sex'] == sex[0]) | (df['Sex'] == sex[1])]
        else:
            df = df[df['Sex'] == ""]
        fig = px.bar(df, x='variable', y='value', color='Intent', barmode='group',
                        labels = {'variable': 'Âge', 'value':'Nombre de décès causés par une arme à feu',
                        'Intent':'Raisons'},
                        range_y = [0, 10500])
        newnames = {'Suicide':'Suicide', 'Total - all intents':'Tout', 'Assault':'Homicide',
                        'Preventable/accidental':'Évitable/accidentel', 'Legal intervention':'Intervention judiciaire',
                        'Undetermined':'Indéterminé'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                        legendgroup = newnames[t.name],
                        hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name]))
        )
        fig.update_layout(title="Tranches d'âge des morts par arme à feu aux États-Unis par sexe avec leurs raisons")
        return fig

