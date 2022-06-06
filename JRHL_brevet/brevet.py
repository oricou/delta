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
import json

class Brevet():
    START = 'Start'
    STOP = 'Stop'

    def generate_data_brevet_par_annee_par_secteur(self, df):
        data_brevet_par_annee_par_secteur = df.copy().groupby(['Session', 'Secteur d\'enseignement'])
        data_brevet_par_annee_par_secteur = data_brevet_par_annee_par_secteur.agg(Presents = ('Presents', 'sum'),
                                      Admis = ('Admis', 'sum'),
                                      AvecMention = ('Admis Mention AB+', 'sum'),
                                      B_TB = ('Admis Mention B+', 'sum'),
                                      TB = ('Admis Mention TB', 'sum'))

        cols_to_divide = ['Admis', 'AvecMention', 'B_TB', 'TB']
        data_brevet_par_annee_par_secteur.loc[:, cols_to_divide] = data_brevet_par_annee_par_secteur.loc[:, cols_to_divide].div(data_brevet_par_annee_par_secteur['Presents'], axis=0)
        data_brevet_par_annee_par_secteur = data_brevet_par_annee_par_secteur.reset_index()
        # Taux vers pourcentage
        data_brevet_par_annee_par_secteur[['Admis', 'AvecMention', 'B_TB', 'TB']] = data_brevet_par_annee_par_secteur[['Admis', 'AvecMention', 'B_TB', 'TB']].applymap(lambda a : a * 100)
        return data_brevet_par_annee_par_secteur


    def generate_data_brevet_par_annee_par_departement(self, df):
        data_brevet_par_annee_par_departement = df.copy().groupby(['Session', 'Code département'])
        data_brevet_par_annee_par_departement = data_brevet_par_annee_par_departement.agg(Presents = ('Presents', 'sum'),
                                      Admis = ('Admis', 'sum'),
                                      AvecMention = ('Admis Mention AB+', 'sum'),
                                      B_TB = ('Admis Mention B+', 'sum'),
                                      TB = ('Admis Mention TB', 'sum'))

        cols_to_divide = ['Admis', 'AvecMention', 'B_TB', 'TB']
        data_brevet_par_annee_par_departement.loc[:, cols_to_divide] = data_brevet_par_annee_par_departement.loc[:, cols_to_divide].div(data_brevet_par_annee_par_departement['Presents'], axis=0)
        data_brevet_par_annee_par_departement = data_brevet_par_annee_par_departement.reset_index()
        # Taux vers pourcentage
        data_brevet_par_annee_par_departement[['Admis', 'AvecMention', 'B_TB', 'TB']] = data_brevet_par_annee_par_departement[['Admis', 'AvecMention', 'B_TB', 'TB']].applymap(lambda a : a * 100)
        return data_brevet_par_annee_par_departement


    def generate_df(self):
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

        # On remplace les arrondissements de Paris, Lyon et Marseille par leurs villes respectives
        self.brevet_data['Libellé commune'] = self.brevet_data['Libellé commune'].replace(to_replace=r"([A-Z]+)[ ]+([0-9]+.*)", value=r"\1", regex=True)

        self.brevet_data = self.brevet_data[self.brevet_data['Secteur d\'enseignement'] != "-"]

        data_brevet_par_annee_par_secteur = self.generate_data_brevet_par_annee_par_secteur(self.brevet_data)
        data_brevet_par_annee_par_departement = self.generate_data_brevet_par_annee_par_departement(self.brevet_data)

        return (data_brevet_par_annee_par_secteur, data_brevet_par_annee_par_departement)



    def load_grandes_villes(self):
        habitant_ville = pd.read_csv('JRHL_brevet/data/data.csv', sep=';')
        grandes_villes = habitant_ville[habitant_ville["Population municipale (historique depuis 1876) 2018"] >= 50000]["Libellé"]

        # On passe les noms des villes en majuscule et on enlève les accents (ex : Besançon -> BESANCON)
        def my_upper(word):
            normal_map = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
                          'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
                          'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                          'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                          'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
                          'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
                          'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
                          'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
                          'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
                          'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
                          'Ñ': 'N', 'ñ': 'n',
                          'Ç': 'C', 'ç': 'c',
                          '§': 'S',  '³': '3', '²': '2', '¹': '1'}
            normalize = str.maketrans(normal_map)
            return word.translate(normalize).upper()

        grandes_villes = grandes_villes.map(lambda x: my_upper(x))

        grandes_villes = grandes_villes.to_frame()

        # On remplace "SAINT-OUEN-SUR-SEINE par "SAINT-OUEN" pour avoir les memes noms des villes dans les deux dataframes
        grandes_villes['Libellé'] = grandes_villes['Libellé'].replace(to_replace=r"SAINT-OUEN-SUR-SEINE", value=r"SAINT-OUEN", regex=True)

        brevet_data_grandes_villes = self.brevet_data[self.brevet_data['Libellé commune'].isin(grandes_villes['Libellé'])]

        brevet_data_grandes_villes = brevet_data_grandes_villes.groupby('Session')

        brevet_data_grandes_villes = brevet_data_grandes_villes.agg(PresentsGrandesVilles = ('Presents', 'sum'))
        brevet_data_grandes_villes["Presents France"] = self.brevet_data.groupby('Session')['Presents'].sum()
        brevet_data_grandes_villes["Taux Presents Grandes Villes"] = brevet_data_grandes_villes["PresentsGrandesVilles"] / brevet_data_grandes_villes["Presents France"]

        brevet_data_grandes_villes = brevet_data_grandes_villes.reset_index()

        return brevet_data_grandes_villes


    def __init__(self, application = None):
        self.years = [*range(2006, 2021)]
        self.departements = json.load(open('JRHL_brevet/data/departements-version-simplifiee.geojson'))

        dbpath = 'JRHL_brevet/data/fr-en-dnb-par-etablissement.csv'
        self.brevet_data = pd.read_csv(dbpath, sep=';')

        self.brevet_data_grandes_villes = self.load_grandes_villes()

        ## GENERATE ANALYSED DF##
        self.data_brevet_par_annee_par_secteur, self.data_brevet_par_annee_par_departement = self.generate_df()

        # ==================== HTML ==================== 
        self.main_layout = html.Div(children=[
            html.H3(children='Taux de réussite et de mentions au brevet selon le secteur (Public / Privé)'),

            ##
            html.Div([
                    html.Div([ dcc.Graph(id='tr-main-graph'), ], style={'width':'80%', }),

                    html.Div([
                        html.Div('Critère de réussite'),
                        html.Div([ dcc.RadioItems(id='tr-mean',
                                                 options=[{'label':'Admis', 'value':0},
                                                          {'label':'Taux de mention Assez Bien et plus', 'value':1},
                                                          {'label':'Taux de mention Bien et plus', 'value':2},
                                                          {'label':'Taux de mention Très Bien', 'value':3},],
                                                 value=0,
                                                 labelStyle={'display':'block'}) ,
                                                 ]),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br()
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '0px 0px',
                    'display':'flex',
                    'justifyContent':'center'
                }),
            ##

            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.

            Notes :
               * Comme attendu, on peut observer une légère augmentation du taux d'admis au brevet année après année
               * Une différence entre les secteurs public et privé est notable : les établissements privés ont environ 10% de taux d'admis de plus que les établissements publics
               * On observe également un léger pic de taux d'admis dans le secteur public en 2017.
               * Bien que le taux d'admis est en légère augmentation, le taux de mentions augmente plus, et cette tendance est encore plus importante sur le taux de mentions Très Bien.
               * En moyenne, les taux d'élèves inscrits dans les secteurs privé et public ayant obtenu la mention Très Bien au brevet sont égaux entre 2006 et 2016 (de 5% à 12%), puis l'écart se creuse à partir de l'année 2017, où les taux de mentions Très Bien doublent par rapport à l'année précédente.
               * A partir de l'année 2017, on observe une forte augmentation du taux de mentions Très Bien, qui se ressent moins sur le taux de mentions Bien et mieux.
               * Cette augmentation est corrélée avec la réforme du brevet de 2017.

            """
            ),
            ## ================  Taux de réussite départemental ================
            # Graph

            html.H3(children="Taux de réussite au brevet en France et nombre d'inscrits"),
            html.Div([
                    html.Div([ dcc.Graph(id='tr-dep-graph'), ], style={'width':'80%', }),

                    html.Div([
                        dcc.RadioItems(id='tr-dep-mention',
                                     options=[{'label':'Admis', 'value':0},
                                              {'label':'Taux de mention Assez Bien et plus', 'value':1},
                                              {'label':'Taux de mention Bien et plus', 'value':2},
                                              {'label':'Taux de mention Très Bien', 'value':3},
                                              {'label':"Nombre d'inscrits", 'value':4}],
                                     value=0,
                                     labelStyle={'display':'block'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br()
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '0px 0px',
                    'display':'flex',
                    'justifyContent':'center'
                }),


            # Slider
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='tr-dep-year-slider',
                            min=self.years[0],
                            max=self.years[-1],
                            step = 1,
                            value=self.years[0],
                            marks={str(year): str(year) for year in self.years},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='tr-dep-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px',
                    'width':'100%'
                }),

            html.H4(children="Etude du taux de réussite selon les départements"),
            dcc.Markdown("""
            On peut remarquer que le taux de réussite au brevet est contrasté selon les départements.
            Globalement, le département 75 (Paris) a un taux de mentions Très Bien beaucoup plus élevé que les autres départements.
            Par exemple en 2017, on observe un taux relativement élevé de mentions Très Bien dans le 75 (40%), contrairement au 93 (Seine-Saint-Denis), avec un taux de mentions Très Bien de 18%.
            """
            ),
            html.H4(children="Etude du taux de l'évolution démographique départementale"),
            dcc.Markdown("""
            On peut remarquer des dynamiques démographiques dans quelques départements, notamment dans le 69(Rhône), le 76(Seine Maritime), et le 33(Gironde), où le nombre d'inscrits au brevet a plus augmenté que dans les autres départements.
            """
            ),

            #  ================ Etude démographique ================
            html.H3(children='Etude démographique'),
            html.Div([
                # Graph
                html.Div([ dcc.Graph(id='tr-dem-graph'), ], style={'width':'100%', }),
                # Bouton
                html.Div([ dcc.RadioItems(id='tr-sec-mean',
                                         options=[{'label':"Taux d'inscrits dans les grandes villes", 'value':0},
                                                  {'label':"Nombre d'inscrits en France", 'value':1}],
                                         value=0,
                                         labelStyle={'display':'block'}) ,
                                         ]),
                html.Br(),

                dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.
                En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.
                Notes :
                   * De 2006 à 2020 le nombre d'inscrits au brevet dans les grandes villes reste constant environ 19-20%.
                   * Le nombre d'inscrits au brevet en France a augmenté de 11% (+ 80 000) en 14 ans, ce qui traduit une augmentation de la population nationale.
                #### À propos
                * Sources : https://data.education.gouv.fr/explore/dataset/fr-en-dnb-par-etablissement/
                * (c) 2022 Hugo Levy & Jacques Ren
                """
                )
                ], style={
                    'backgroundColor': 'white',
                     'padding': '10px 50px 10px 50px',
                     }
                )
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             },
        )



        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # ============== CALLBACKS ==============

        ## Graph taux de réussite
        self.app.callback(
                    dash.dependencies.Output('tr-main-graph', 'figure'),
                    dash.dependencies.Input('tr-mean', 'value'))(self.update_main_graph)

        # Evolution démographique
        self.app.callback(
                    dash.dependencies.Output('tr-dem-graph', 'figure'),
                    dash.dependencies.Input('tr-sec-mean', 'value'))(self.update_dem_graph)

        # Taux de réussite par département
        self.app.callback(
            dash.dependencies.Output('tr-dep-graph', 'figure'),
            [ dash.dependencies.Input('tr-dep-mention', 'value'),
              dash.dependencies.Input('tr-dep-year-slider', 'value')])(self.update_dep_graph)


    # ============== FONCTIONS UPDATE GRAPH ==============

    # Graph démographie
    def update_dem_graph(self, mean):
        fig = px.line(self.brevet_data_grandes_villes, x='Session', y='Taux Presents Grandes Villes')
        if mean == 1:
            fig = px.line(self.brevet_data_grandes_villes, x='Session', y='Presents France')

        return fig

    # Graph principal
    def update_main_graph(self, choix):
        col_name = ['Admis', 'AvecMention', 'B_TB', 'TB', 'Presents']
        col = col_name[choix]

        return px.line(self.data_brevet_par_annee_par_secteur, x='Session', y=col, color="Secteur d'enseignement", symbol="Secteur d'enseignement")

    # Carte départements
    def update_dep_graph(self, mention, session):
        col_name = ['Admis', 'AvecMention', 'B_TB', 'TB', 'Presents']
        col = col_name[mention]

        range_colors = [0, self.data_brevet_par_annee_par_departement[col].max()]
        fig = px.choropleth_mapbox(self.data_brevet_par_annee_par_departement[self.data_brevet_par_annee_par_departement['Session'] == session], geojson=self.departements,
                           locations= 'Code département', featureidkey = 'properties.code', # join keys
                           color= col_name[mention], color_continuous_scale=px.colors.sequential.YlOrRd,
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={'prix':'Prix E10'},
                           range_color = range_colors
                          )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

if __name__ == '__main__':
    tr = Brevet()
    tr.app.run_server(debug=True, port=8051)
