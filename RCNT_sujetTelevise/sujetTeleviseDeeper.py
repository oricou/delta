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



class TvSubjectDeeper():
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

        self.data_count_tot = data_count_tot
        self.data_watchtime_tot = data_watchtime_tot

        self.main_layout = html.Div(children=[
            html.H3(children='Quelques statistiques plus poussées sur les sujets télévisés francais entre 2005 et 2020'),
            html.Div([dcc.Graph(id='sujetp-main-graph'), ], style={'width': '100%', }),
            html.Div([dcc.RadioItems(id='sujetp-mean',
                                     options=[{'label': 'Graphique à barres en fonction des chaines TV', 'value': 0},
                                              {'label': 'Graphique à barres en fonction des chaines TV par an', 'value': 1},
                                              {'label': 'Graphique à barres en fonction des chaines TV sur chaque mois par an', 'value': 2}],
                                     value=0,
                                     labelStyle={'display': 'block'}),
                      ]),
            html.Br(),
            dcc.Markdown("""
            + Notes :
               * On peut analyser les enjeux societaux de chaque année en regardant les données. Meme si beaucoup de 
               variations sont notables, un socle Société et International prédomine.
               * Nous pouvons voir les sujets récurrents et les cycles dans les différents sujets.

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
            dash.dependencies.Output('sujetp-main-graph', 'figure'),
            dash.dependencies.Input('sujetp-mean', 'value'))(self.update_graph)

    def update_graph(self, mean = 0):
        themes = self.data_watchtime.groupby('THEMATIQUES').sum() / 3600  # en heure
        column_names = ['MOIS', 'THEMATIQUES', 'TF1', 'France 2', 'France 3', 'Canal +', 'Arte', 'M6', 'TOTAUX']
        if mean == 1:
            temp = self.data_watchtime.reset_index()
            temp["YEAR"] = temp["MOIS"].dt.year
            themes_dyn = temp  # en heure
            layout_histo = dict(
                title="Nombre d'heures par theme entre 2005 et 2020 année après année",
                xaxis=dict(title='Thèmes'),
                yaxis=dict(title="Nombre d'heures"),
            )
            themesdynbis = themes_dyn.reset_index()
            themesdynbis = themesdynbis.groupby(["YEAR", "THEMATIQUES"]).sum() / 3600
            themesdynbis = themesdynbis.reset_index()
            fig = px.bar(themesdynbis, x="THEMATIQUES", y=column_names[2:9], barmode="group", animation_frame="YEAR",
                         animation_group="THEMATIQUES",
                         hover_name="THEMATIQUES", range_y=[0, 190])
            fig.update_layout(layout_histo)


        elif mean == 0:  # en heure
            layout_histo = dict(
                title="Nombre d'heures par thème entre 2005 et 2020",
                xaxis=dict(title='Thèmes'),
                yaxis=dict(title="Nombre d'heures"),
            )
            themesbis = themes.reset_index()
            fig = px.bar(themesbis, x="THEMATIQUES", y=column_names[2:9], barmode="group")
            fig.update_layout(layout_histo)
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

        elif mean == 2:
            data_count_month_and_year = self.data_count
            data_count_month_and_year['Year'] = data_count_month_and_year['MOIS'].dt.year
            data_count_month_and_year['Mois'] = data_count_month_and_year['MOIS'].dt.month

            month_dico = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet",
                          8: "Aout", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}

            tab = data_count_month_and_year
            tab["Mois"] = tab["Mois"].apply(lambda date: month_dico[date])

            fig = px.histogram(tab, x=tab["THEMATIQUES"], y=["TF1", "France 2", "France 3", "Canal +", "Arte", "M6"],
                               animation_frame="Year",
                               # color = tab["lum"].apply(lambda i: luminosité[i-1]),
                               color_discrete_sequence=['blue', 'red', 'violet', 'black', 'orange', 'green'],
                               facet_col='Mois', facet_col_wrap=3,
                               category_orders={"mois": range(1, 13)},  # , "x":thematiques, "color":chaine},
                               labels={'x': 'Thematique', "y": 'Chaine Télévision'},
                               title="Nombre d'heures par mois par thème entre 2005 et 2020 année après année"
                               )
            # let move the legend above the figure
            fig.update_layout(
                              legend=dict(orientation="h",
                                          yanchor="bottom", y=1.05,
                                          xanchor="right", x=1),

                              autosize=False,
                              width=1500,
                              height=800)

        return fig


if __name__ == '__main__':
    sujetp = TvSubjectDeeper()
    sujetp.app.run_server(debug=True, port=8051)
