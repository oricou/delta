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
class Obesity_calories():
    def __init__(self, application = None):
        self.df_obesity = pd.read_csv('TFRT_obesity/data/df_obesity.csv')
        self.df_calories = pd.read_csv('TFRT_obesity/data/df_calories.csv')

        self.main_layout = html.Div([
            html.H3('Corrélation entre obésité et apport calorique'),
            dcc.Markdown("""La carte montrant le pourcentage d'obèses ci-dessous montre la proportion d'adultes obèses dans les différents pays. 
                            Dans l'ensemble, nous observons un schéma qui correspond à peu près à la prospérité : 
                            la prévalence de l'obésité tend à être plus élevée dans les pays riches d'Europe, 
                            d'Amérique du Nord et d'Océanie. Les taux d'obésité sont beaucoup plus faibles en Asie du Sud 
                            et en Afrique subsaharienne.
                            
                            Aux États-Unis, plus d'un adulte sur trois (36 %) était obèse en 2016. En Inde, cette part était environ 10 fois plus faible (3,9%).
                            """),
            dcc.RadioItems(
                id='candidate_graph', 
                options=["Obésité", "Apport calorique"],
                value="Obésité",
                inline=True
            ),
            dcc.Graph(id='graph_world_obesity_calories'),
            dcc.Markdown("""
            Sur la carte montrant l'apport calorique on peut voir que dans l'ensemble nous constatons que l'apport calorique par habitant a augmenté de manière constante au niveau mondial au cours de cette période. Cependant, ces tendances varient selon les régions du monde.

            Nous avons constaté une augmentation significative de l'apport calorique en Asie et en Afrique au cours des dernières décennies.

            L'augmentation plus marquée dans les régions les plus pauvres du monde signifie qu'au cours des dernières décennies, les tendances mondiales en matière d'apport calorique ont convergé. En termes d'approvisionnement alimentaire, nous vivons aujourd'hui dans un monde plus égalitaire qu'au siècle dernier.
            """),
            html.H3("Pays développés vs tiers-monde"),
            dcc.Markdown("""La relation entre l'apport calorique et l'obésité se vérifie généralement - comme nous le voyons dans 
                            la comparaison ici. Mais il y a quelques exceptions notables. Les petits États insulaires du 
                            Pacifique se distinguent clairement : ils ont des taux d'obésité très élevés - 61% à Nauru et 
                            55% à Palau. À l'autre extrémité du spectre, le Japon, la Corée du Sud 
                            et Singapour ont des taux d'obésité très faibles.
            La hausse plus marquée dans les régions les plus pauvres du monde signifie qu'au cours des dernières décennies, les tendances mondiales en matière d'apport calorique ont convergé. En termes d'approvisionnement alimentaire, nous vivons aujourd'hui dans un monde plus égalitaire qu'au siècle précédent."""),
            dcc.RadioItems(
                id='candidate_bar',
                options=["Obésité", "Apport calorique"],
                value="Obésité",
                inline=True
            ),
            dcc.Graph(id='bar_world_obesity_calories'),
        ])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('graph_world_obesity_calories', 'figure'),
                    dash.dependencies.Input("candidate_graph", "value"))(self.display_choropleth),

        self.app.callback(
                    dash.dependencies.Output('bar_world_obesity_calories', 'figure'),
                    dash.dependencies.Input("candidate_bar", "value"))(self.display_bar)
    
    def display_choropleth(self, candidate):
        df = self.df_obesity if candidate == "Obésité" else self.df_calories
        range_color = [0,40] if candidate == "Obésité" else [0,4000]
        color = "Prevalence of obesity among adults" if candidate == "Obésité" else "Food supply (kcal per capita per day)"
        color_continuous_scale = "Blues" if candidate == "Obésité" else "Reds"
        title_text = 'Share of adults that are obese | 1975-2016' if candidate == "Obésité" else "Caloric supply by country | 1961-2016"
        fig = px.choropleth(
            df, color=color,
            locations="Country",
            hover_name="Country",
            hover_data=[color],
            locationmode="country names",
            animation_frame='Year',
            projection="natural earth",
            range_color=range_color,
            color_continuous_scale = color_continuous_scale)
        fig.update_layout(margin=dict(l=20,r=0,b=0,t=70,pad=0),paper_bgcolor="white",height= 600, width=1100,title_text = title_text,font_size=18)
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
        return fig
    
    def display_bar(self, candidate):
        df = self.df_obesity if candidate == "Obésité" else self.df_calories
        value_to_display = "Prevalence of obesity among adults" if candidate == "Obésité" else "Food supply (kcal per capita per day)"
        title_text = "Pourcentage d'obèses parmi les adultes en 2016" if candidate == "Obésité" else "Apport calorique par pays en 2016"
        df_obesity_2016 =  df.loc[df['Year'] == 2016].sort_values([value_to_display], ascending=False)
        range = [0, 100] if candidate == "Obésité" else [0,6000]
        fig = px.bar(df_obesity_2016.head(50), y='Country', x=value_to_display, text_auto='.2s',
            title=title_text, height=1000)
        fig.update_xaxes(range=range)
        return fig

if __name__ == '__main__':
    mpj = Obesity_calories()
    mpj.app.run_server(debug=True, port=8051)
