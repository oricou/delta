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

        data_brevet_par_annee_par_secteur = self.brevet_data[self.brevet_data['Secteur d\'enseignement'] != "-"].groupby(['Session', 'Secteur d\'enseignement'])

        data_brevet_par_annee_par_secteur = data_brevet_par_annee_par_secteur.agg(Presents = ('Presents', 'sum'),
                                      Admis = ('Admis', 'sum'),
                                      AvecMention = ('Admis Mention AB+', 'sum'),
                                      B_TB = ('Admis Mention B+', 'sum'),
                                      TB = ('Admis Mention TB', 'sum'))

        cols_to_divide = ['Admis', 'AvecMention', 'B_TB', 'TB']
        data_brevet_par_annee_par_secteur.loc[:, cols_to_divide] = data_brevet_par_annee_par_secteur.loc[:, cols_to_divide].div(data_brevet_par_annee_par_secteur['Presents'], axis=0)
        data_brevet_par_annee_par_secteur = data_brevet_par_annee_par_secteur.reset_index()
        return data_brevet_par_annee_par_secteur


    def __init__(self, application = None):

        dbpath = 'brevet/data/fr-en-dnb-par-etablissement.csv'
        self.brevet_data = pd.read_csv(dbpath, sep=';')

        ## CLEANING DATA ##
        self.data_brevet_par_annee_par_secteur = self.clean_brevet_data()

        self.df = self.brevet_data

        self.main_layout = html.Div(children=[
            html.H3(children='Taux de réussite et de mentions au brevet'),
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
               * A partir de l'année 2017, on observe un pic de taux de mentions très bien.


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
        """
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
        """
        fig = px.line(self.data_brevet_par_annee_par_secteur, x='Session', y='Admis', color="Secteur d'enseignement", symbol="Secteur d'enseignement")
        return fig

if __name__ == '__main__':
    tr = Brevet()
    tr.app.run_server(debug=True, port=8051)
