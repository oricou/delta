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
from scipy import signal

import ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant.get_data # à commenter pour tests (pas besoin de regénérer les données à chaque fois)


class Pollution():
    def __init__(self, application=None):

        # getting pollution
        pollution = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/pollution.pkl')

        pollution.rename(columns={'Concentration moyenne en CO': 'Concentration moyenne en CO x 40'}, inplace=True)
        pollution['Concentration moyenne en CO x 40'] = pollution['Concentration moyenne en CO x 40'] * 40

        pollution.rename(columns={'Concentration moyenne en O3': 'Concentration moyenne en O3 x 700'}, inplace=True)
        pollution['Concentration moyenne en O3 x 700'] = pollution['Concentration moyenne en O3 x 700'] * 700

        pollution.rename(columns={'Concentration moyenne en SO2': 'Concentration moyenne en SO2 x 5'}, inplace=True)
        pollution['Concentration moyenne en SO2 x 5'] = pollution['Concentration moyenne en SO2 x 5'] * 5

        # pollution figure
        figPollution = go.Figure()

        figPollution.add_trace(go.Scatter(
        x=pollution.index,
        y=pollution['Concentration moyenne en CO x 40'],
        name='CO'))
        figPollution.add_trace(go.Scatter(
        x=pollution.index,
        y=pollution['Concentration moyenne en NO2'],
        name='NO2'))
        figPollution.add_trace(go.Scatter(
        x=pollution.index,
        y=pollution['Concentration moyenne en O3 x 700'],
        name='03'))
        figPollution.add_trace(go.Scatter(
        x=pollution.index,
        y=pollution['Concentration moyenne en SO2 x 5'],
        name='SO2'))

        figPollution.update_layout(
        title='Concentration moyenne de SO2, NO2, O3 et CO de 2000 à 2022 en ppmd',
        xaxis_title='Date',
        yaxis_title='Molécule en ppmd',
        legend_title='Molécule')
        
        # smoothed pollution figure
        figPollutionSmoothed = go.Figure()

        figPollutionSmoothed.add_trace(go.Scatter(
        x=pollution.index,
        y=signal.savgol_filter(pollution['Concentration moyenne en CO x 40'], 101, 3),
        name='CO'))
        figPollutionSmoothed.add_trace(go.Scatter(
        x=pollution.index,
        y=signal.savgol_filter(pollution['Concentration moyenne en NO2'], 101, 3),
        name='NO2'))
        figPollutionSmoothed.add_trace(go.Scatter(
        x=pollution.index,
        y=signal.savgol_filter(pollution['Concentration moyenne en O3 x 700'], 101, 3),
        name='03'))
        figPollutionSmoothed.add_trace(go.Scatter(
        x=pollution.index,
        y=signal.savgol_filter(pollution['Concentration moyenne en SO2 x 5'], 101, 3),
        name='SO2'))

        figPollutionSmoothed.update_layout(
        title='Concentration moyenne de SO2, NO2, O3 et CO de 2000 à 2022 en ppmd, version graphique lissée',
        xaxis_title='Date',
        yaxis_title='Molécule en ppmd',
        legend_title='Molécule')

        # getting prices
        prices = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/prices.pkl')
        pricesFig = px.line(prices, x='Date', y='Prix moyen en dollar du gallon de gazole', title='Prix moyen du gazole de 2000 à 2022')

        # getting average temp + precipitation
        average_cities = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/average_cities.pkl')

        celsiusFig = px.line(average_cities, x='Date', y='Température moyenne en °C', title='Température moyenne (°C) de 2000 à 2022')

        prcpFig = px.line(average_cities, x='Date', y='Précipitation moyenne en cm', title='Précipitation moyenne (cm) de 2000 à 2022')

        self.main_layout = html.Div(children=[
            html.H3(children='Pollution/Petrole'),
            dcc.Markdown("""Le but de ce sujet va être de regarder et tenter de comprendre les valeurs de pollution atmosphérique moyennes aux Etats-Unis relatives aux gas émis par la combustion d'hydrocarbures. Bien que portant sur l'étude de données recueillies aux Etats-Unis, la compréhension de l'évolution de ces valeurs pourra facilement être généralisée aux autres pays développés."""),
            dcc.Markdown("""Voici donc les valeurs sur lesquelles nous allons travailler :"""),
            html.Div([ dcc.Graph(figure=figPollution), ], style={'width':'100%', }),
            dcc.Markdown("""Comme cela manque de clareté on lisse donc les valeurs :"""),
            html.Div([ dcc.Graph(figure=figPollutionSmoothed), ], style={'width':'100%', }),
            dcc.Markdown("""Nous avons donc la concentration moyenne de SO2 (dioxyde de soufre), NO2 (dioxyde d'azote), O3 (ozone), et CO (monoxyde de carbone) de 2000 à 2022 en parties par milliard. Le NO2 et CO étants des gazs émis par la combustion d'hydrocarbures, l'O3 un sous produits de dégration des gazs de type NOx et COV, et le SO2 un gaz témoin qui nous servira par la suite. Ce dernier est surtout utilisé comme désinfectant, antiseptique, antibactérien, gaz réfrigérant, agent de blanchiment, catalyseur en fonderie et conservateur (https://fr.wikipedia.org/wiki/Dioxyde_de_soufre)."""),
            dcc.Markdown("""Immédiatemment on remarque une périodicité saisonnière."""),
            html.Div([ dcc.Graph(figure=pricesFig), ], style={'width':'100%', }),
            dcc.Markdown("""Nous pensions au début montrer que l'utilisation d'hydrocarbures changeait en fonction de leur prix mais il n'en est rien, aucune corrélation n'est véritablement visible."""),
            html.Div([ dcc.Graph(figure=prcpFig), ], style={'width':'100%', }),
            dcc.Markdown("""Aucune corrélation non plus avec les précipitation qui sont de toute manière réparties assez aléatoirement et ne semblent ni croître ni décroître."""),
            html.Div([ dcc.Graph(figure=celsiusFig), ], style={'width':'100%', }),
            dcc.Markdown("""La courbe des températures semble suivre le même cycle saisonnier que les valeurs de concentration des gazs étudiés. Alors s'agit-il d'une simple coïncidence ? Eh bien pas tout à fait. Tout d'abord le chauffage au fioul implique une consommation plus grande d'hydrocarbures en hiver qu'en été, mais les basses températures favorisent également la stagnation des polluants dans l'air : http://www.atmo-grandest.eu/actualite/pourquoi-le-froid-favorise-la-pollution-atmospherique. Cela est notamment appuyé par les concentration en SO2 également en hausse en hiver alors que sa production reste relativement stable au cours de l'année."""),
            dcc.Markdown("""Maintenant comment expliquer la courbe de l'O3 qui ne semble pas suivre celle du NO2 et du CO alors que ce gaz est un sous produit de dégradation de ces 2 derniers lorsque exposés aux ultraviolets ? Il se trouve que l'O3 n'est pas seulement créé à partir de NO2 et de CO, ces gazs peuvent aussi le dégrader lorsque les ultraviolets permettant sa création ne suffisent pas à compenser sa dégradation. Lorsque l'intensité des ultraviolets est basse comme en hiver ou ces derniers doivent pénétrer une couche plus grande d'atmosphère à cause de l'inclinaison de la Terre, les NOx et COV dégradent donc plus l'ozone qu'ils ne participent à sa production : https://www.irceline.be/fr/documentation/faq/pourquoi-les-concentrations-d2019ozones-sont-elles-plus-elevees-dans-les-campagnes-que-dans-les-villes"""),
            dcc.Markdown("""Les concentrations d'O3 baissent donc en hiver et augmentent en été."""),
        ],
        style={'backgroundColor': 'white','padding': '10px 50px 10px 50px',}
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == '__main__':
    pol = Pollution()
    pol.app.run_server(debug=True, port=8051)
