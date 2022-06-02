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



class TvSubject():
    def __init__(self, application=None):

        # # # # # # # # # # # # # # #
        # Download data             #
        # # # # # # # # # # # # # # #

        column_names = ['MOIS', 'THEMATIQUES', 'TF1', 'France 2', 'France 3', 'Canal +', 'Arte', 'M6', 'TOTAUX']

        data_watchtime = pd.read_csv('data/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv', sep=";",
                                     skipinitialspace=True,
                                     quotechar="'", header=0, skiprows=1, names=column_names, encoding='latin-1',
                                     parse_dates=[1])
        data_count = pd.read_csv('data/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv', sep=";",
                                 skipinitialspace=True,
                                 quotechar="'", header=0, skiprows=1, names=column_names, encoding='iso8859_15',
                                 parse_dates=[1])
        # # # # # # # # # # # # # # #
        # Data Cleaning             #
        # # # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # #
        # Change the date to datetime #
        # # # # # # # # # # # # # # # #
        def month_to_number(months):
            if months == 'janvier':
                return "01"
            elif months[0] == 'f':
                return "02"
            elif months == 'mars':
                return "03"
            elif months == 'avril':
                return "04"
            elif months == 'mai':
                return "05"
            elif months == 'juin':
                return "06"
            elif months[0] == 'j':
                return "07"
            elif months[0] == 'a':
                return "08"
            elif months[0] == 's':
                return "09"
            elif months[0] == 'o':
                return "10"
            elif months[0] == 'n':
                return "11"
            elif months[0] == 'd':
                return "12"
            return "ERROR"

        def string_to_date_time(date):
            L = date.split("-")
            L[1] = "20" + L[1]
            L = L[1] + "-" + month_to_number(L[0])
            return L

        data_count["MOIS"] = data_count["MOIS"].apply(lambda date: string_to_date_time(date))
        data_watchtime["MOIS"] = data_watchtime["MOIS"].apply(lambda date: string_to_date_time(date))

        # # # # # # # # # # # # # # #
        # CLean Data Accent         #
        # # # # # # # # # # # # # # #

        def clean_accent(string):
            if (string.startswith("Sant")):
                string = "Sante"
            if (string.startswith("Soci")):
                string = "Societe"
            return string

        data_watchtime["THEMATIQUES"] = data_watchtime["THEMATIQUES"].apply(lambda string: clean_accent(string))
        data_count["THEMATIQUES"] = data_count["THEMATIQUES"].apply(lambda string: clean_accent(string))

        # # # # # # # # # # # # # # #
        # CLean Column type         #
        # # # # # # # # # # # # # # #
        # clean count df

        data_count["MOIS"] = data_count["MOIS"].apply(pd.to_datetime)
        data_count[["TF1", "France 2", "France 3", "Canal +", "Arte", "M6", "TOTAUX"]] = data_count[
            ["TF1", "France 2", "France 3", "Canal +", "Arte", "M6", "TOTAUX"]].apply(pd.to_numeric)

        # clean watchtime df
        data_watchtime["MOIS"] = data_watchtime["MOIS"].apply(pd.to_datetime)
        for col in data_watchtime.columns[2:]:
            data_watchtime[col] = pd.to_timedelta(data_watchtime[col]) / pd.Timedelta('1s')
            data_watchtime[col] = data_watchtime[col].apply(int)
        data_watchtime = data_watchtime.set_index("MOIS")


        # # # # # # # # # # # # # # # # # # #
        # Other table due to multi-index    #
        # # # # # # # # # # # # # # # # # # #
        thematiques_names = ["Catastrophes", "Culture-loisirs", "Economie", "Education", "Environnement",
                             "Faits divers", "Histoire-hommages", "International", "Justice", "Politique France",
                             "Sante", "Sciences et techniques", "Societe", "Sport"]

        data_watchtime_tot = data_watchtime.drop(["TF1", "France 2", "France 3", "Canal +", "Arte", "M6"], axis=1)
        for i in thematiques_names:
            data_watchtime_tot[i] = data_watchtime_tot[data_watchtime_tot["THEMATIQUES"] == i]["TOTAUX"]
        data_watchtime_tot = data_watchtime_tot.drop(["THEMATIQUES", "TOTAUX"], axis=1).drop_duplicates()

        data_count_ind = data_count.set_index("MOIS")
        data_count_tot = data_count_ind.drop(["TF1", "France 2", "France 3", "Canal +", "Arte", "M6"], axis=1)
        for i in thematiques_names:
            data_count_tot[i] = data_count_tot[data_count_tot["THEMATIQUES"] == i]["TOTAUX"]
        data_count_tot = data_count_tot.drop(["THEMATIQUES", "TOTAUX"], axis=1).drop_duplicates()


        self.data_count = data_count
        self.data_watchtime = data_watchtime
        self.thematiques_name = thematiques_names = ["Catastrophes", "Culture-loisirs", "Economie", "Education", "Environnement",
                             "Faits divers", "Histoire-hommages", "International", "Justice", "Politique France",
                             "Sante", "Sciences et techniques", "Societe", "Sport"]
        self.data_count_tot = data_count_tot
        self.data_watchtime_tot = data_watchtime_tot

        self.main_layout = html.Div(children=[
            html.H3(children='Quelques statistiques sur les sujets télévisés francais entre 2005 et 2020'),
            html.Div([dcc.Graph(id='sujet-main-graph'), ], style={'width': '100%', }),
            html.Div([
                html.Div([dcc.RadioItems(id='sujet-mean',
                                         options=[{'label': 'Courbes du total des sujets', 'value': 1},
                                                  {'label': 'Courbes détaillées pour chaque sujet (choisi ton sujet ->)', 'value': 0},
                                                  {'label': "Temps moyen d'un programme TV en fonction de la chaine",
                                                   'value': 2},
                                                  {'label': "Temps moyen d'un programme TV en fonction du thème",
                                                   'value': 3}],
                                         value=1,
                                         labelStyle={'display': 'block'})], style={'width': '40em'}),
                html.Div(style={'width': '2em'}),
                html.Div(style={'width': '2em'}),
                html.Div(style={'width': '2em'}),
                html.Div(style={'width': '2em'}),
                html.Div([html.Div('Theme'),
                          dcc.Dropdown(
                              id='sujet-theme',
                              options=[{'label': i, 'value': i} for i in self.thematiques_name],
                              value=2000,
                              disabled=True,)
                          ], style={'width': '10em', 'padding': '0em 10px 0px 0px'}),
            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'flex-start',
            }),

            html.Br(),
            dcc.Markdown("""
            - Observation :
                * La fin d'année 2020 est marqué par le covid ce qui fausse les données...
                * Canal + n'apparait plus en 2020 car a arreté ces JT.
                * La définition des sujets est explicité sur le site de l'INA
            - Notes :
                * Cette premiere séries de graph présente les sujets prédominants dans les journeaux télévisés comme 
                Societe,International ou l'international. On peut voir que sur le long terme aucune tendance ne s impose vraiment.
                * Quelque soit le sujet les différentes chaines suivent globalement des tendances: la préoccupation actuelle
                * Nous pouvons observer que les temps moyens des sujets des journeaux télévisés varient beaucoup en
                fonction de la chaine et du sujet. Canal+ et M6 font des sujets beacoup plus court que la moyenne donc 
                plus condensés. Des sujets comme le sport ou les catastrophes sont simples et ne nécessite pas beaucoup 
                d'explications d'ou le temps.
                
            - A vous de jouer! Saurez vous reconnaitre ces evenements? :
                * Fukushima
                * Coupe du monde de 2018
                * Emeute France banlieu 2005
                * Crises financières 
                * Procès de DSK

            #### À propos

            * Sources : 
                * https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv
                * https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114231/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv

            * 2022 Romain Cazin, Nicolas Trabet
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
            dash.dependencies.Output('sujet-main-graph', 'figure'),
            [dash.dependencies.Input('sujet-mean', 'value'),
            dash.dependencies.Input('sujet-theme', 'value')])(self.update_graph)

        self.app.callback(
            dash.dependencies.Output('sujet-theme', 'disabled'),
            dash.dependencies.Input('sujet-mean', 'value'))(self.disable_theme)

    def update_graph(self, mean, theme_choose):
        themes = self.data_watchtime.groupby('THEMATIQUES').sum() / 3600  # en heure
        if mean == 0:
            if not theme_choose in self.thematiques_name:
                theme_choose = "Education"
            fig = px.line(self.data_watchtime[self.data_watchtime["THEMATIQUES"] == theme_choose].drop(["THEMATIQUES"] , axis=1)/ 3600)
            fig.update_layout(
                title='Graphiques du temps télévisé pour les différents sujets: ici ' + theme_choose ,
                yaxis=dict(title='Total en heure')
            )


        elif mean == 1:
            fig = px.line(self.data_watchtime_tot / 3600)
            fig.update_layout(
                title='Graphique pour chaque sujet détaillé en fonction des différentes chaines',
                yaxis=dict(title='Total en heure')
            )

        elif mean == 2:
            graph = (self.data_watchtime.drop(["THEMATIQUES"], axis=1) / self.data_count.set_index("MOIS").drop(["THEMATIQUES"], axis=1)).mean()
            layout_histo = dict(
                title='Temps moyen des programmes télévisées francais entre 2005 et 2020 en fonction de la chaine TV',
                xaxis=dict(title='Thèmes'),
                yaxis=dict(title='Combien de temps (en sec)'),
            )
            fig = px.bar(graph)
            fig.update_layout(layout_histo)
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

        elif mean == 3:
            graph = (self.data_watchtime_tot / self.data_count_tot).mean()
            layout_histo = dict(
                title='Temps moyen des programmes télévisées francais entre 2005 et 2020 en fonction du thème',
                xaxis=dict(title='Thèmes'),
                yaxis=dict(title='Combien de temps (en sec)'),
            )
            fig = px.bar(graph)
            fig.update_layout(layout_histo)
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

        return fig

    def disable_theme(self, option):
        if option == 0:
            return False
        else:
            return True

if __name__ == '__main__':
    sujet = TvSubject()
    sujet.app.run_server(debug=True, port=8051)
