import sys, os
import dash, flask

from dash import dcc, html

import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px

import dateutil as du

# Manipulation du path pour ajouter le chemin relatif et
# empecher des erreurs peu importe le chemin de la source
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from get_data import df_hr, df_cc, df_hr_col_en, df_hr_col_fr
from utils import *


class Bonheur():
    
    continent_list_en = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"] 
    continent_list_fr = ["Afrique", "Asie", "Europe", "Amérique du Nord", "Océanie", "Amérique du Sud"]
    
    graph_types = ["PIB par habitant", "Support social", "Espérance de vie", "Liberté de vivre",
                   "Générosité", "Perception de la corruption", "Effets positifs", "Effets négatifs"]
    
    
    def __init__(self, application = None):
        
        self.mode = 1
        self.filter = ""
        self.graph_type_default = "PIB par habitant"

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
                        options = list(map(lambda s: {'label': s, 'value': s}, self.graph_types)),
                        value = self.graph_type_default,
                        labelStyle = {'display':'block'},
                    ),
                    html.Button('Réinitialiser le graphe', id='bnh-btn', n_clicks=0),
                ], style = {'width' : '23%', 'display': 'inline-block'})
            ]),
            html.Div([
                
            ], 
            id = 'bnh-description',
            style = {'width': '100%'})
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
                self.mode = 2
                self.filter = self.continent_list_en[self.continent_list_fr.index(value)]
                return self._init_graph_secondary(graphtype)
            if self.mode == 2 :
                self.mode = 3
                self.filter = value
                return self._init_graph_tertiary(graphtype)
            if self.mode == 3 :
                self.fitler = value
                return self._init_graph_tertiary(graphtype)

        # in case of error, return default graph
        self.mode = 1
        return self._init_graph_primary(self.graph_type_default)

            
    def _upgrade_description(self, graphtype):
        match graphtype:
            case "Echelle de vie" :
                return md_life_ladder
            case "PIB par habitant" :
                return md_gdp
            case "Support social" :
                return md_social_support
            case "Espérance de vie" :
                return md_life_expectancy
            case "Liberté de vivre" :
                return md_freedom
            case "Générosité" :
                return md_generosity
            case "Perception de la corruption" :
                return md_corruption
            case "Effets positifs" :
                return md_positive
            case "Effets négatifs" :
                return md_negative
    
    def _init_graph_primary(self, graphtype):
        print("_init_graph_primary")
        df_hr_ex = df_hr.groupby("Continent").mean()
        df_hr_ex.index = self.continent_list_fr
        print(df_hr_ex)
        primary_figure = px.bar(
            df_hr_ex[[graphtype]],
            title = f'{graphtype}, ',
            labels=dict(x = graphtype, y = "Continents"),
            template='plotly_white'
        )
        return primary_figure
        
        
        
    def _init_graph_secondary(self, graphtype):
        df_hr_ex = df_hr[df_hr["Continent"] == self.filter].groupby("Pays").mean()
        primary_figure = px.bar(
            df_hr_ex[[graphtype]],
            title = f'{graphtype}, {self.filter}',
            labels=dict(x = graphtype, y = "Pays"),
            template='plotly_white'
        )
        return primary_figure
    
    def _init_graph_tertiary(self, graphtype):
        print("_init_graph_tertiary")
        df_hr_ex = df_hr[df_hr["Pays"] == self.filter]
        primary_figure = px.line(
            df_hr_ex[[graphtype]],
            title = f'{graphtype}, {self.filter}',
            labels=dict(x = graphtype, y = "Pays"),
            template='plotly_white'
        )
        return primary_figure
        
    
if __name__ == '__main__':
    nrg = Bonheur()
    nrg.app.run_server(debug=True, port=8051)
    
    
    
    
    
    
    
    
    
    
    
    
# <------------------------------------------------------->
md_introduction = """
Gallup Organization est une entreprise américaine offrant de nombreux services de recherche concernant le managment, les ressources humaines et les statistiques. Cette entité est particulièrement connue pour efféctuer différents sondages souvent médiatisés.
"""


md_life_ladder = """
### Life Ladder :

Il s'agit d'une mesure du bien-être subjectif. Le rapport du 18 février 2022 signé par le GWP couvrant de 2005 à 2021 correspond à la moyenne nationale de réponse à la question d'évaluation du niveau de vie. La version en anglais est : "Please imagine a ladder, with steps numbered from 0 at the bottom to 10 at the top. The top of the ladder represents the best possibe life for you and the bottom of the ladder represents the worst possible life for you. On which step of the ladder would you say you personally feel you stand at this time ?". On appelle également cette mesure l'échelle de Cantril.
"""

md_gdp = """
### <span style="color:green">Log GDP (Gross Domestic Product) per capita (in purchasing power parity):</span> 

Il s'agit du logarithme du PIB par habitants en parité de pouvoir d'achat en dollar (dollar constant fixé à 2017), venant du rapport du World Development Indicator du 16 décembre 2021.

Il peut être intéressant de noter que les PIBs de l'année 2021 n'étant pas encore disponible, des données ont dû être extrapolées en ce basnat sur des prévisions spécifiques à chaque pays ainsi que sur des rapports de l'OECD et du WBGEP.
"""

md_social_support = """
### <span style="color:green">Social Support :</span>

Il s'agit de la mesure de la moyenne nationale à la question binaire (0 ou 1) : "If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not".
"""

md_life_expectancy = """
### <span style="color:green">Healthy Life expectancy at birth :</span>

Espérance de vie calculée sur les données extraites du repo de l'OMS Global Health Observatory à la granularité de 5 années, ensuite extrapolées pour correspondre au dataset.
"""

md_freedom = """
### <span style="color:green">Freedom to make life choice :</span>

Il s'agit de la mesure de la moyenne nationale à la question "Are you satisfied or dissatisfied with your freedom to choose what you do with your life ?"
"""

md_generosity = """
### <span style="color:green">Generosity :</span>

Il s'agit de la mesure de la moyenne nationale à la question "Have you donated mo,ey to charity in the mast month ?". Cependant la donnée n'est pas basée sur la moyenne simple mais est le résidu d'une régression linéaire, c'est à dire qu'une valeur positive veut dire qu'il y a eu plus de générosité que ce à quoi on s'attendait, et une valeur négative veut dire moins que ce à quoi on s'attendait.
"""

md_corruption = """
### <span style="color:green">Perceptions of corruption :</span>

Il s'agit de la mesure de la moyenne nationale aux questions :
- "Is corruption widespread throughout the government or not"
- "Is corruption widespread within businesses or not ?"
En resulte la moyenne des deux réponses binaires (On peut noter qu'on utilise la perception de la corruption privée quand la perception de la corruption publique est manquante (certains pays n'apprécient pas de parler de corruption publique)).
"""

md_positive = """
### <span style="color:green">Positive affect :</span>

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