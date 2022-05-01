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

class Brevet():


    def clean_brevet_data(self):
        # On enlève les 0z devant les codes des départements
        self.brevet_data['Code département'] = self.brevet_data['Code département'].map(lambda x: str(x)[1:])

        # On renomme les colonnes des mentions
        self.brevet_data.rename(columns = {'Nombre_d_admis_Mention_AB':'Admis Mention AB', 'Admis Mention bien':'Admis Mention B', 'Admis Mention très bien':'Admis Mention TB'}, inplace = True)

        # Admis avec mention bien ou plus
        self.brevet_data['Admis Mention B+'] = self.brevet_data['Admis Mention B'] + self.brevet_data['Admis Mention TB']

        # Admis avec mention  assez bien ou plus (avec mention)
        self.brevet_data['Admis Mention AB+'] = self.brevet_data['Admis Mention AB'] + self.brevet_data['Admis Mention B+']

        # Taux de réussite
        self.brevet_data['Taux de réussite'] =  self.brevet_data['Admis'] / self.brevet_data['Presents']


    def __init__(self, application = None):

        dbpath = 'brevet/data/fr-en-dnb-par-etablissement.csv'
        self.brevet_data = pd.read_csv(dbpath, sep=';')

        ## CLEANING DATA ##
        self.clean_brevet_data()


        self.df = self.brevet_data

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de décès par jour en France'),
            html.Div([ dcc.Graph(id='tr-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='tr-mean', 
                                     options=[{'label':'Courbe seule', 'value':0},
                                              {'label':'Courbe + Tendence générale', 'value':1}, 
                                              {'label':'Courbe + Moyenne journalière (les décalages au 1er janv. indique la tendence)', 'value':2}], 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.

            Notes :
               * La grippe de l'hiver 1989-1990 a fait 20 000 morts (4,6 millions de malades en 11 semaines). La chute de la courbe au premier janvier 1990 est quand même très surprenante.
               * On repère bien les hivers avec grippe.
               * L'année 1997 est étrange, peut-être un problème de recensement.
               * La canicule d'août 2003 a fait 15 000 morts (ce qui a généré la journée de travail non payé dite journée Raffarin).
               * Les 120 000 morts dus au Covid-19 en 2020 et 2021 sont bien visibles, d'autant qu'il n'y a pas eu de grippe durant les hivers 19-20 et 20-21.
               * On note une progression constante du nombre de morts, avec environ 1000 morts par jour en dehors de pics durant les années 70 
                 pour environ 1700 morts par jour après 2015. Il s'agit d'une augmentation de plus de 70 %, soit plus du double que l'augmentation de la population sur la même période. Le saut visible en 1990 peut aussi traduire un recensement plus complet après cette année.
               * Les derniers mois doivent être pris avec précaution car tous les morts ne sont pas encore recensés.

            #### À propos

            * Sources : https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/
            * (c) 2022 Olivier Ricou
            """)
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
                    dash.dependencies.Output('tr-main-graph', 'figure'),
                    dash.dependencies.Input('tr-mean', 'value'))(self.update_graph)

    def update_graph(self, mean):
        fig = px.line(self.df, template='plotly_white')
        fig.update_traces(hovertemplate='%{y} décès le %{x:%d/%m/%y}', name='')
        fig.update_layout(
            #title = 'Évolution des prix de différentes énergies',
            xaxis = dict(title=""), # , range=['2010', '2021']), 
            yaxis = dict(title="Nombre de décès par jour"), 
            height=450,
            showlegend=False,
        )
        if mean == 1:
            reg = stats.linregress(np.arange(len(self.df)), self.df.morts)
            fig.add_scatter(x=[self.df.index[0], self.df.index[-1]], y=[reg.intercept, reg.intercept + reg.slope * (len(self.df)-1)], mode='lines', marker={'color':'red'})
        elif mean == 2:
            fig.add_scatter(x=self.df.index, y=self.day_mean, mode='lines', marker={'color':'red'})

        return fig

        
if __name__ == '__main__':
    tr = Brevet()
    tr.app.run_server(debug=True, port=8051)
