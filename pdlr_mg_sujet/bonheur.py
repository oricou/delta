import sys, os
import math

import dash
# import flask
from dash import dcc, html

import pandas as pd
import numpy as np

# import plotly.graph_objs as go
import plotly.express as px
# import plotly.graph_objects as go

# import dateutil as du

# Manipulation du path pour ajouter le chemin relatif et
# empêcher des erreurs peu importe le chemin de la source
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from get_data import df_hr, df_cc
from utils import *

class Bonheur():

    radioItems = [
        {'label': "PIB par habitant", 'value': "GDP"},
        {'label': "Support social", 'value': "Social support"},
        {'label': "Espérance de vie", 'value': "Life expectancy"},
        {'label': "Liberté de vivre", 'value': "Freedom of life"},
        {'label': "Générosité", 'value': "Generosity"},
        {'label': "Perception de la corruption", 'value': "Corruption"},
        {'label': "Effets positifs", 'value': "Positive affect"},
        {'label': "Effets négatifs", 'value': "Negative affect"},
    ]

    def __init__(self, application = None):

        self.mode = 1
        self.filter = ""
        self.graph_type_default = "GDP"

        self.main_layout = html.Div([
            html.H3("Étude du bonheur mondial de 2005 à 2020"),
            dcc.Markdown(md_introduction),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id = 'bnh-graph',
                        config = {'displayModeBar': False},
                    ),
                ], style = {'width' : '75%', 'display': 'inline-block'}),
                html.Div([
                    dcc.RadioItems(
                        id = 'bnh-graph-type',
                        options = self.radioItems,
                        value = self.graph_type_default,
                        labelStyle = {'display':'block'},
                    ),
                    html.Button('Réinitialiser le graphe', id='bnh-btn', n_clicks=0),
                ], style = {'width' : '23%', 'display': 'inline-block'})
            ]),
            dcc.Markdown("", id = 'bnh-description', style = {'width': '100%'})
        ], style = {
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # update graph
        self.app.callback(
            dash.dependencies.Output('bnh-graph', 'figure'),
            [
                dash.dependencies.Input('bnh-graph', 'clickData'),
                dash.dependencies.Input('bnh-graph-type', 'value'),
                dash.dependencies.Input('bnh-btn', 'n_clicks'),
            ]
        )(self._update_graph)

        # update graph type
        self.app.callback(
            dash.dependencies.Output('bnh-graph-type', 'value'),
            [
                dash.dependencies.Input('bnh-btn', 'n_clicks'),
            ]
        )(self._reset_graph_type)

        # update graph description
        self.app.callback(
            dash.dependencies.Output('bnh-description', 'children'),
            [
                dash.dependencies.Input('bnh-graph-type', 'value'),
            ]
        )(self._upgrade_description)

        # on reset button clicked or graph-type clicked : reset clickdata value
        self.app.callback(
            dash.dependencies.Output('bnh-graph', 'clickData'),
            [
                dash.dependencies.Input('bnh-graph-type', 'value'),
                dash.dependencies.Input('bnh-btn', 'n_clicks')
            ]
        )(self._reset_graph_values)

    def _reset_graph(self, btn):
        self.mode = 1
        return self._update_graph(self, None, self.graph_type_default)

    def _reset_graph_type(self, btn):
        return self.graph_type_default

    def _reset_graph_values(self, graphtype, btn):
        return None

    def _update_graph(self, point, graphtype, _):
        ctx = dash.callback_context
        # in case of error, return default graph
        if not ctx.triggered:
            self.mode = 1
            return self._init_graph_primary(self.graph_type_default)
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # if the trigger is the reset button
        if trigger_id == 'bnh-btn':
            self.mode = 1
            return self._init_graph_primary(self.graph_type_default)

        # if the trigger is the graph type
        if trigger_id == 'bnh-graph-type' and graphtype:
            if self.mode == 1 : return self._init_graph_primary(graphtype)
            if self.mode == 2 : return self._init_graph_secondary(graphtype)
            if self.mode == 3 : return self._init_graph_tertiary(graphtype)

        # if the trigger is the graph
        if trigger_id == 'bnh-graph' and point:
            value = point["points"][0].get("x")
            if self.mode == 1 :
                self.filter = value
                self.mode = 2
                return self._init_graph_secondary(graphtype)
            if self.mode == 2 :
                self.filter = value
                self.mode = 3
                return self._init_graph_tertiary(graphtype)
            if self.mode == 3:
                return self._init_graph_tertiary(graphtype)

        # in case of error, return default graph
        self.mode = 1
        return self._init_graph_primary(self.graph_type_default)

    def _upgrade_description(self, graphtype):
        match graphtype:
            case "GDP" :
                return md_gdp
            case "Social support" :
                return md_social_support
            case "Life expectancy" :
                return md_life_expectancy
            case "Freedom of life" :
                return md_freedom
            case "Generosity" :
                return md_generosity
            case "Corruption" :
                return md_corruption
            case "Positive affect" :
                return md_positive
            case "Negative affect" :
                return md_negative

    def _init_graph_primary(self, graphtype):
        print("_init_graph_primary")

        # Get label based on the value in the self.radioItems list ("GDP" => "PIB par habitant")
        axisName = next(filter(lambda element : element["value"] == graphtype, self.radioItems), None)
        axisName = axisName["label"] if axisName else ""

        df_hr_ex = df_hr.groupby("Continent").mean()[[graphtype, "Life ladder"]]
        df_hr_ex = df_hr_ex.sort_values(by = "Life ladder", ascending = True)

        # If the value is NaN for graphtype, add the red color
        def lbd(index):
            if math.isnan(df_hr_ex.loc[[index]][graphtype]):
                return f'<span style="color:red">{index}</span>'
            return index
        df_hr_ex.rename(lbd, axis = "index", inplace = True)

        figure = px.bar(
            data_frame = df_hr_ex,
            y = graphtype,
            custom_data = [df_hr_ex["Life ladder"]],

            color = "Life ladder",
            range_color = [0, 10],
        )

        # Add template for hover menu with filter, graphtype, axisName and Life ladder value
        figure.update_traces(
            hovertemplate =
                '<i>Continent</i>: %{x}<br>' +
                '<b>' + axisName + '</b> : ' + ('$' if graphtype == 'GDP' else '') + '%{y:.2f}<br>' +
                '<b>Échelle de vie</b> : %{customdata[0]:.2f}',
        )

        # Update layout : add title, template, hover menu font text, color range title, axis titles
        figure.update_layout(
            title = f'{axisName}',
            template = 'plotly_white',
            hoverlabel = dict(
                font = dict(color = "white")
            ),
            coloraxis = dict(
                colorbar = dict(title = "Échelle<br>de vie")
            ),
            xaxis = dict(title = "Continents"),
            yaxis = dict(title = f'{axisName}')
        )

        return figure

    def _init_graph_secondary(self, graphtype):
        print("_init_graph_secondary")

        # Get label based on the value in the self.radioItems list ("GDP" => "PIB par habitant")
        axisName = next(filter(lambda element : element["value"] == graphtype, self.radioItems), None)
        axisName = axisName["label"] if axisName else ""

        df_hr_ex = df_hr[df_hr["Continent"] == self.filter].groupby("Country").mean()[[graphtype, "Life ladder"]]
        df_hr_ex = df_hr_ex.sort_values(by = "Life ladder", ascending = True)

        # If the value is NaN for graphtype, add the red color
        def lbd(index):
            if math.isnan(df_hr_ex.loc[[index]][graphtype]):
                return f'<span style="color:red">{index}</span>'
            return index
        df_hr_ex.rename(lbd, axis = "index", inplace = True)

        figure = px.bar(
            data_frame = df_hr_ex,
            y = graphtype,
            custom_data = [df_hr_ex["Life ladder"]],

            color = "Life ladder",
            range_color = [0, 10],
        )

        # Add template for hover menu with filter, graphtype, axisName and Life ladder value
        figure.update_traces(
            hovertemplate =
                '<b><i>' + self.filter + '</i></b><br><br>' +
                '<i>Pays</i>: %{x}<br>' +
                '<b>' + axisName + '</b> : ' + ('$' if graphtype == 'GDP' else '') + '%{y:.2f}<br>' +
                '<b>Échelle de vie</b> : %{customdata[0]:.2f}',
        )

        # Update layout : add title, template, hover menu font text, color range title, axis titles
        figure.update_layout(
            title = f'{axisName}, {self.filter}',
            template = 'plotly_white',
            hoverlabel = dict(
                font = dict(color = "white")
            ),
            coloraxis = dict(
                colorbar = dict(title = "Échelle<br>de vie")
            ),
            xaxis = dict(title = "Pays"),
            yaxis = dict(title = f'{axisName}')
        )

        return figure

    def _init_graph_tertiary(self, graphtype):
        print("_init_graph_tertiary")

        # Get label based on the value in the self.radioItems list ("GDP" => "PIB par habitant")
        axisName = next(filter(lambda element : element["value"] == graphtype, self.radioItems), None)
        axisName = axisName["label"] if axisName else ""

        # Get wanted dataframe with str years and merge it with the [2005-2020] to fill data in missing years
        df_hr_ex = df_hr[df_hr["Country"] == self.filter][["Year", graphtype, "Life ladder"]]
        df_hr_ex["Year"] = df_hr_ex["Year"].apply(str)
        xAxis = pd.Series(df_hr["Year"].unique(), name = "Year").apply(str)
        df_hr_ex = df_hr_ex.merge(xAxis, on = "Year", how = "right")

        # Sort list and set Year as Index
        df_hr_ex = df_hr_ex.sort_values(by = "Year", ascending = True)
        df_hr_ex.set_index("Year", inplace = True)

        # Add red color when graphtype value is missing for a specific year
        def lbd(index):
            if math.isnan(df_hr_ex.loc[[index]][graphtype]):
                return f'<span style="color:red">{index}</span>'
            return index
        df_hr_ex.rename(lbd, axis = "index", inplace = True)

        figure = px.bar(
            data_frame = df_hr_ex,
            y = graphtype,
            custom_data = [df_hr_ex["Life ladder"]],

            # Add color range for Life Ladder
            color = "Life ladder",
            range_color = [0, 10],
        )

        # Add template for hover menu with filter, graphtype, axisName and Life ladder value
        figure.update_traces(
            hovertemplate =
                '<b><i>' + self.filter + '</i></b><br><br>' +
                '<i>Année</i>: %{x}<br>' +
                '<b>' + axisName + '</b> : %{y:.2f}<br>' +
                '<b>Échelle de vie</b> : %{customdata[0]:.2f}',
        )

        # Update layout : add title, template, hover menu font text, color range title, axis titles
        figure.update_layout(
            title = f'{axisName}, {self.filter}',
            template = 'plotly_white',
            hoverlabel = dict(
                font = dict(color = "white")
            ),
            coloraxis = dict(
                colorbar = dict(title = "Échelle<br>de vie")
            ),
            xaxis = dict(title = "Années"),
            yaxis = dict(title = f'{axisName}')
        )

        return figure

if __name__ == '__main__':
    nrg = Bonheur()
    nrg.app.run_server(debug=True, port=8051)

# <------------------------------------------------------->
md_introduction = """
Gallup Organization est une entreprise américaine offrant de nombreux services de recherche concernant le management, les ressources humaines et les statistiques. Cette entité est particulièrement connue pour efféctuer différents sondages souvent médiatisés. Dans le cadre du programme Gallup Happiness Poll, l'entreprise recueille des informations et des avis d'habitants de pays du monde entier sur le ressentis de leur vie, et si ils se considèrent comme heureux. Il en résulte un rapport qui s'étend sur plusieurs années et contient des informations particulièrement intéressantes.

#### Échelle de vie
L'Échelle de vie est une mesure du bien-être subjectif. Le rapport du 18 février 2022 signé par le GWP couvrant de 2005 à 2021 correspond à la moyenne nationale de réponse à la question d'évaluation du niveau de vie. La question (traduite de l'anglais) est : "Imaginez une échelle, avec des marches numérotées de 0 en bas jusqu'à 10 en haut. Le haut de l'échelle représente les meilleures conditions de vies pour vous et le bas représente les pires conditions de vies. Sur quelle marche de l'échelle vous pensez personnellement être actuellement ?". On appelle également cette mesure l'échelle de Cantril.

Le but de ce graph est donc d'exprimer les différentes corrélations entre cette fameuse Échelle de vie, et différentes métriques exprimées dans le GWP : si l'évolution de la métrique est croissante de manière visible, cela veut dire qu'elle est proportionnelle à l'Échelle de vie et donc au bonheur.

---

La navigation dans le graphe est possible en cliquant sur les barres pour ouvrir le détails des valeurs par pays et continents.
"""

md_life_ladder = """
### Life Ladder :
"""

md_gdp = """
### Produit Intérieur Brut Par habitant (en parité de pouvoir d'achat):

Il s'agit du PIB par habitants en parité de pouvoir d'achat en dollar (dollar constant fixé à la valeur de 2017), venant du rapport du World Development Indicator du 16 décembre 2021.
La parité de pouvoir d'achat (PPA) est un taux de conversion monétaire qui permet d'exprimer dans une unité commune les pouvoirs d'achat des différentes monnaies. Ce taux exprime le rapport entre la quantité d'unités monétaires nécessaire dans des pays différents pour se procurer le même « panier » de biens et de services.
Ce taux de conversion peut être différent du « taux de change » ; en effet, le taux de change d'une monnaie par rapport à une autre reflète leurs valeurs réciproques sur les marchés financiers internationaux et non leurs valeurs intrinsèques pour un consommateur.
"""

md_social_support = """
### Social Support :

Il s'agit de la mesure de la moyenne nationale à la question binaire (0 ou 1) : "If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not".
"""

md_life_expectancy = """
### Healthy Life expectancy at birth :

Espérance de vie calculée sur les données extraites du repo de l'OMS Global Health Observatory à la granularité de 5 années, ensuite extrapolées pour correspondre au dataset.
"""

md_freedom = """
### Freedom to make life choice :

Il s'agit de la mesure de la moyenne nationale à la question "Are you satisfied or dissatisfied with your freedom to choose what you do with your life ?"
"""

md_generosity = """
### Generosity :

Il s'agit de la mesure de la moyenne nationale à la question "Have you donated money to charity in the mast month ?". Cependant la donnée n'est pas basée sur la moyenne simple mais est le résidu d'une régression linéaire, c'est à dire qu'une valeur positive veut dire qu'il y a eu plus de générosité que ce à quoi on s'attendait, et une valeur négative veut dire moins que ce à quoi on s'attendait.
"""

md_corruption = """
### Perceptions of corruption :

Il s'agit de la mesure de la moyenne nationale aux questions :
- "Is corruption widespread throughout the government or not"
- "Is corruption widespread within businesses or not ?"
En resulte la moyenne des deux réponses binaires (On peut noter qu'on utilise la perception de la corruption privée quand la perception de la corruption publique est manquante (certains pays n'apprécient pas de parler de corruption publique)).
"""

md_positive = """
### Positive affect :

L'effet positif est définit par la moyenne des questions binaires suivantes :
- "Did you smile or laugh a lot yerterday ?"
- "Did you experience the following feelings during A LOT OF THE DAY yesterday? How about Enjoyment ?"
- "Did you learn or do something interesting yesterday ?"
"""

md_negative = """
### <span style="color:green">Negative affect :</span>

L'effet positif est définit par la moyenne des questions binaires suivantes :
- "Did you experience the following feelings during A LOT OF THE DAY yesterday ? How about Worry ?"
- "Did you experience the following feelings during A LOT OF THE DAY yesterday ? How about Sadness ?"
- "Did you experience the following feelings during A LOT OF THE DAY yesterday ? How about Anger ?"
"""
