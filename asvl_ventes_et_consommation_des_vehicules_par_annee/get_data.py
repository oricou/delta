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
import plotly.tools as tls
import dateutil as du
from scipy import stats
from scipy import fft
import datetime

import matplotlib.pyplot as plt


class Vehicules():
    def __init__(self, application = None):

        #Création de data

        df = pd.read_excel("asvl_ventes_et_consommation_des_vehicules_par_annee/data/carlabelling-28-04-2022-12-36-pandas-friendly.xlsx")
        df['Marque + Modele'] = df['Marque + Modele'].apply(lambda x: x.split(' ', 1))
        df['Marque'] = df['Marque + Modele'].apply(lambda x: x[0])
        df['Modele'] = df['Marque + Modele'].apply(lambda x: x[1])
        df: pd.DataFrame = df.drop(['Marque + Modele'], axis=1)
        tmp: pd.DataFrame = df.groupby("Marque").size()
        tmp.sort_values(ascending=False)
        df = df.drop(
            ["Malus (+)/  Bonus (-)", "Coût énergie Max.", "BV", "Carrosserie", "Norme Euro", "Consommation  Unité"],
            axis=True)

        df["Consommation Max"] = pd.to_numeric(df["Consommation Max"].str.replace(",", "."))
        df["Consommation Min"] = pd.to_numeric(
            df["Consommation Min"].str.replace("-", '').str.replace(",", ".")).fillna(
            df["Consommation Max"])
        # df["Rejets CO2 Min"] = pd.to_numeric(df["Rejets CO2 Min"].str.replace("-",'').str.replace(",",".")).fillna(df["Rejets CO2 Max"])

        df["Rejets CO2 Max"] = pd.to_numeric(df["Rejets CO2 Max"].replace({"-": "0"}))
        df["Rejets CO2 Min"] = pd.to_numeric(df["Rejets CO2 Min"].replace({"-": ""})).fillna(df["Rejets CO2 Max"])

        df["Consommation"] = (df["Consommation Min"] + df["Consommation Max"]) / 2
        df["Rejets CO2"] = (df["Rejets CO2 Min"] + df["Rejets CO2 Max"]) / 2

        def get_co2_class(rejets: float):
            if rejets <= 100:
                return "A"
            elif rejets <= 120:
                return "B"
            elif rejets <= 140:
                return "C"
            elif rejets <= 160:
                return "D"
            elif rejets <= 200:
                return "E"
            elif rejets <= 250:
                return "F"
            else:
                return "G"

        df["Rejets CO2 Classe"] = df["Rejets CO2"].map(lambda x: get_co2_class(x))

        df = df.drop(columns=["Consommation Min", "Consommation Max", "Rejets CO2 Min", "Rejets CO2 Max",
                              "Rejets CO2 Classe Min", "Rejets CO2 Classe Max", "Rejets CO2 Classe Max"])

        df_resume_pollution = df[["Modele", "Marque", "Energie", "Consommation", "Rejets CO2", "Rejets CO2 Classe"]]

        #df_resume_pollution["Consommation"] = df_resume_pollution["Consommation"].fillna(0)
        #df_resume_pollution.isna().sum()

        df_resume_pollution.to_csv('asvl_ventes_et_consommation_des_vehicules_par_annee/data/analyse_ADEME.csv', index=False, header=True)

        tmp = \
        df_resume_pollution[["Energie", "Rejets CO2"]].groupby("Energie").agg([np.mean, np.median, np.std, np.size])[
            "Rejets CO2"]

        dfConsommation = pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/analyse_ADEME.csv")
        dfConsommation['Marque'] = dfConsommation['Marque'].apply(str.lower)
        dfConsommation['Modele'] = dfConsommation['Modele'].apply(str.lower)
        dfConsommation['Modele'] = dfConsommation['Modele'].apply(lambda x: x.split(' '))

        dfSalesTotal = pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes-par-année.csv", index_col='Année')

        ##Comme les db ont par défaut la marque et le modèle collés on rectifie ça pour faciliter les choses
        def dfpreperator(dfsales: pd.DataFrame, year: int, dfsalestotal: pd.DataFrame, dfconsommation: pd.DataFrame):

            dfsales['Modele'] = dfsales['Modele'].apply(str.lower)
            dfsales['Modele'] = dfsales['Modele'].apply(lambda x: x.split(' '))
            dfsales['Marque'] = dfsales['Modele'].apply(lambda x: x[0])
            dfsales['Modele'] = dfsales['Modele'].apply(lambda x: x[1])

            dfsales['Part de marché'] = (dfsales['Ventes'] / dfSalesTotal.at[year, 'Ventes totales']) * 100

            dfcombination = pd.merge(dfsales, dfConsommation, how='inner', left_on=['Marque'], right_on=['Marque'])

            for index, row in dfcombination.iterrows():
                if (not row['Modele_x'] in row['Modele_y']):
                    dfcombination = dfcombination.drop(index)
            dfcombination = dfcombination.groupby(['Modele_x', 'Marque']).median()

            return (dfsales, dfcombination)

        (dfSales2017, dfcombination2017) = dfpreperator(pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes2017.csv"), 2017, dfSalesTotal,
                                                        dfConsommation)
        (dfSales2018, dfcombination2018) = dfpreperator(pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes2018.csv"), 2018, dfSalesTotal,
                                                        dfConsommation)
        (dfSales2019, dfcombination2019) = dfpreperator(pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes2019.csv"), 2019, dfSalesTotal,
                                                        dfConsommation)
        (dfSales2020, dfcombination2020) = dfpreperator(pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes2020.csv"), 2020, dfSalesTotal,
                                                        dfConsommation)
        (dfSales2021, dfcombination2021) = dfpreperator(pd.read_csv("asvl_ventes_et_consommation_des_vehicules_par_annee/data/Ventes2021.csv"), 2021, dfSalesTotal,
                                                        dfConsommation)

        years = [2017, 2018, 2019, 2020, 2021]

        def ponderationofco2(dfcombination: pd.DataFrame):
            dfcombination['CO2 * ventes'] = dfcombination['Rejets CO2'] * dfcombination['Part de marché'] / \
                                            dfcombination2021.sum()['Part de marché']

            return dfcombination

        ponderationofco22021 = ponderationofco2(dfcombination2021)
        ponderationofco22020 = ponderationofco2(dfcombination2020)
        ponderationofco22019 = ponderationofco2(dfcombination2019)
        ponderationofco22018 = ponderationofco2(dfcombination2018)
        ponderationofco22017 = ponderationofco2(dfcombination2017)

        Co2ventes2021 = dfcombination2021.sum()['CO2 * ventes']
        Co2ventes2020 = dfcombination2020.sum()['CO2 * ventes']
        Co2ventes2019 = dfcombination2019.sum()['CO2 * ventes']
        Co2ventes2018 = dfcombination2018.sum()['CO2 * ventes']
        Co2ventes2017 = dfcombination2017.sum()['CO2 * ventes']

        y = [Co2ventes2017, Co2ventes2018, Co2ventes2019, Co2ventes2020, Co2ventes2021]

        toshow = plt.plot(years, y)
        

        self.df = df
        #self.day_mean = prediction

        #Création de layout

        figure = go.Figure(data=[go.Scatter(x=years, y=y)])

        self.main_layout = html.Div(children=[
            html.H3(children='Evolution de la moyenne de la consommation des véhicules les plus vendus au fil des années'),

            dcc.Markdown("""
### Introduction :
Notre projet consistait à la base à analyser si les français achetaient plutôt des voitures polluantes ou plutôt écologiques. Nous avions à disposition de nombreuses données,
comme le type de carburant des dits véhicules, grâce à l'ADEME qui recense les modèles de véhicules actuellement en vente et leur emprunte écologique (https://carlabelling.ademe.fr/)
et le CCFA, qui regroupe les véhicules les plus vendus par année et par catégorie en France (https://ccfa.fr/dossiers-de-presse/).
                                 """),

            dcc.Markdown("""
### Analyse :
Commençons par voir notre objectif initial : est-ce que au fil des années les français achètent plus de voitures polluantes
ou bien cette courbe va-t-elle à la baisse ? Pour celà pondérons les rejets de CO2 de chaque véhicule pour chaque année en
fonction de ses parts de marché français et traçons une courbe pour voir cela :
                         """),
            html.Div([dcc.Graph(id='veh-main-graph', figure=figure),], style={'width': '100%', }),
            html.Div([dcc.RadioItems(id='veh-mean',
                                     value=2,
                                     labelStyle={'display': 'block'}),
                      ]),
            html.Br(),
            dcc.Markdown("""
            On peut donc voir que, d'après nos données, les Français achètent globalement des voitures de plus en plus 
            polluantes entre 2017 et 2020 mais cette tendance est à la baisse entre 2020 et 2021. Une belle perspective pour l'avenir.
                                 """),
            html.Br(),
            dcc.Markdown("""### Critique des résultats :

On pourrait critiquer ces résultats sur plusieurs points.

Tout d'abord, si les sources des données semblent fiables (L'ADEME et le CCFA sont des organismes reconnus),
l'extraction des données pourrait être incomplète. Pour plus de simplicité nous nous sommes limités aux voitures légères.
Les voitures industrielles et utilitaires sont donc exclus.
En outre pour fusionner les deux databases nous avons été contraints de faire des sacrifices dans leurs données.
Nous avons dit dans la partie sur la création du panda issu de la fusion des databases qu'il y avait des difficultés pour cette fusion.
En effet à un modèle cité dans la base du CCFA pouvait correspondre plusieurs modèles dans la base de l'ADEME,
et donc plusieurs consommations potentielles (surtout aujourd'hui maintenant que les véhicules sont plus souvent hybrides).
C'est pourquoi lorsqu'une hésitation du genre avait lieu, nous faisions une médiane du rejet CO2 des dits modèles.
Cela pourrait perturber les résultats. Enfin les bases de données du CCFA sont incomplètes.
En les utilisant on arrive globalement à un total de 50 % (variable selon les années) de parts du marché français,
ce qui omet la moitié des véhicules en circulation. Il est à noter qu'à l'origine nous voulions utiliser la base de données de la SIV auto,
plus complète que celle du CCFA, mais nous nous sommes heurtés à de trop grandes difficultés administratives.

Alain Salanié et Victor Litoux
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
            dash.dependencies.Output('veh-main-graph', 'figure'),
            dash.dependencies.Input('veh-mean', 'value'))#(self.update_graph)
"""
    def update_graph(self, mean):
        fig = px.line(self.df, template='plotly_white')
        fig.update_traces(hovertemplate='%{y} décès le %{x:%d/%m/%y}', name='')
        fig.update_layout(
            # title = 'Évolution des prix de différentes énergies',
            xaxis=dict(title=""),  # , range=['2010', '2021']),
            yaxis=dict(title="Nombre de décès par jour"),
            height=450,
            showlegend=False,
        )
        if mean == 1:
            reg = stats.linregress(np.arange(len(self.df)), self.df.morts)
            fig.add_scatter(x=[self.df.index[0], self.df.index[-1]],
                            y=[reg.intercept, reg.intercept + reg.slope * (len(self.df) - 1)], mode='lines',
                            marker={'color': 'red'})
        elif mean == 2:
            fig.add_scatter(x=self.df.index, mode='lines', marker={'color': 'red'})

        return fig
"""

if __name__ == '__main__':
    mpj = Vehicules()
    mpj.app.run_server(debug=True, port=8051)