from distutils.command.clean import clean
from email.mime import application
from re import S
from statistics import mean
from sys import maxsize
import dash
from dash import Dash, dcc, html, Input, Output
from pyparsing import col
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from .data.get_data import *

# La donnée est téléchargeable au lien suivant : https://www.kaggle.com/datasets/zynicide/wine-reviews/download

class WineStats():

    def __init__(self, application = None):
        wine_df = pd.concat([
            get_dataframe1(),
            get_dataframe2()
        ]) 
        self.df = wine_df
    
        self.figure = px.scatter_geo()
        self.figure2 = self.second_graph()

        self.main_layout = html.Div(children=[
            html.H2(children="Production mondiale du vin", style={"text-align": "center"}),
            html.Div([dcc.Graph(id = 'main-graph', figure=self.figure)]),
            html.Div([dcc.Dropdown(['Production', 'Prix', 'Score (sur WineEnthusiastic)'], 'Production', id='dropdown')], 
                style={'margin': 'auto', 'width': '200px'}),
            html.Div([dcc.Graph(id = 'second-graph', figure=self.figure2), ],
                style={'margin': 'auto', "width": "50%"}),
            html.Br(),
            dcc.Markdown("""
            Les graphiques sont interactifs. En passant la souris sur les bulles vous auvez une infobulle.
            Vous avez la possibilité de vous déplacer à la souris dans la carte ainsi que de zoomer et dézoomer avec
            la roulette de la souris. Même chose pour le graphique.

            #### Notes : 
                * D'après le dataset les Etats-Unis sont les plus gros producteurs de vins. Suivi par la France et l'italie.
                * En termes de continents, l'europe est le plus gros producteurs de vin dans le monde.
                * La moyenne de prix la plus haute est en Suisse, suivi par la france et la Hongrie.
                  Ces valeurs peuvent sans doute être croisée avec le coût de la vie dans ces pays pour comprendre les chiffres. (notamment pour la suisse et la france)
                * Les moyennes de score sont à mettre en question vis à vis du nombre de data dans certains pays, 
                  cependant on remarque une tendance à avoir de meilleurs résultats dans l'ouest de l'europe.
                
                * On peut remarquer que aux prix les plus bas on retrouve de tout les scores. Plus le prix augmente, plus la tendance à avoir de bons scores s'accentue.
            
            #### À propos
                Données: https://www.kaggle.com/datasets/zynicide/wine-reviews

            * (c) 2022 Paul Renoux - Paul Messéant
            """)
        ], style={
            'horizontal-align': 'center'
        })

        if application:
            self.app = application        
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        self.app.callback(
            dash.dependencies.Output('main-graph', 'figure'),
            dash.dependencies.Input('dropdown', 'value')
        )(self.update_graph)

    def update_graph(self, value):
        count_sf = self.df['country'].value_counts()
        count_df = pd.DataFrame({'pays':count_sf.index, 'nombre de bouteilles produites':count_sf.values})
        count_df = count_df.round()

        price_mean_sf = self.df[~self.df['price'].isnull()].groupby('country')['price'].mean()
        price_mean_df = pd.DataFrame({'pays':price_mean_sf.index, 'moyenne des prix':price_mean_sf.values})
        price_mean_df = price_mean_df.round(2)

        score_mean_sf = self.df[~self.df['points'].isnull()].groupby('country')['points'].mean()
        score_mean_df = pd.DataFrame({'pays':score_mean_sf.index, 'moyenne des scores':score_mean_sf.values})
        score_mean_df = score_mean_df.round(2)

        fig = px.scatter_geo()

        fig1 = px.scatter_geo(count_df, 
            locations="pays", 
            size="nombre de bouteilles produites", 
            locationmode="country names",
            color="nombre de bouteilles produites"
        )

        fig2 = px.scatter_geo(price_mean_df,
            locations="pays",
            size="moyenne des prix",
            locationmode="country names",
            color="moyenne des prix"
        )

        fig3 = px.scatter_geo(score_mean_df,
            locations="pays",
            size="moyenne des scores",
            locationmode="country names",
            color="moyenne des scores",
        )

        if (value == "Production"):
            fig.add_traces(fig1.data)
        elif (value == "Prix"):
            fig.add_traces(fig2.data)
        elif (value == "Score (sur WineEnthusiastic)"):
            fig.add_traces(fig3.data)
        return fig

    def second_graph(self):

        clean_df = self.df[~self.df['price'].isnull()]
        clean_df = clean_df[~clean_df['points'].isnull()]

        fig = px.scatter(clean_df, 
            x=clean_df['price'], 
            y=clean_df['points'], 
            hover_data=['designation', 'taster_name'],
            title="Les scores des vins en fonction de leurs prix",
        )
        return fig

    def run(self, debug=False, port=8050):
        self.app.run_server(host="127.0.0.1", debug=debug, port=port)

if __name__ == '__main__':
    ws = WineStats()
    ws.run(port=8055)  
