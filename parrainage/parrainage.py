import sys
import dash
import flask
from dash import dcc
from dash import html
from matplotlib.pyplot import title
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import json

class Parrainage():

    def __init__(self, application = None):
        self.df = pd.read_csv("parrainage/data/parrainagestotal.csv", sep=";", infer_datetime_format=True)
        self.df['Date de publication'] = pd.to_datetime(self.df['Date de publication'], format='%d/%m/%Y')
        self.candidats_occurences = self.df['Candidat'].value_counts()
        self.candidats_list = self.candidats_occurences[self.candidats_occurences > 500].keys()

        with open("parrainage/data/departements.geojson") as f:
            self.departements_json = json.load(f)
        
        self.main_layout = html.Div(children=[
            html.H3(children='Parrainages des candidats à la présidentielle 2022'),
            html.Div([
                    html.Div([ dcc.Graph(id='par-main-graph'), ], style={'width':'80%', }),
                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.Div('Candidat'),
                        dcc.RadioItems(
                            id='par-candidat',
                            options=[{'label': candidat, 'value': candidat} for candidat in self.candidats_list],
                            value=self.candidats_list[0],
                            labelStyle={'display':'block'},
                        ),
                        html.Br()
                    ], style={'margin-left':'15px', 'width': '15em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            html.Br(),
            html.Div([ dcc.Graph(id='par-main-map') ], style={'width':'100%'}),    
            dcc.Markdown("""
                ### Commentaires
                - Bénéficiant d'un fort ancrage territoriale, Valérie PÉCRESSE fait partie des candidats ayant rapidement atteint le seuil des 500 signatures. C'est elle qui parvient à récolter le plus de parrainages au total. On peut constater qu'un grand nombre de ces signatures provient de son fief, l'Île-de-France, où elle est présidente de région.
                - Emmanuel MACRON récolte également un grand nombre de signatures dés le début de la course, bénéficiant de son status de président sortant.
                - Anne HIDALGO bénéficie de l'ancrage territoriale du Parti Socialiste. On peut remarquer le nombre élevé de parrainages dans le sud-ouest, où de nombreux élus socialistes siègent.
                - Jean-Luc MÉLENCHON parvient à obtenir les 500 signatures plus tardivement et bénéficie d'une accélération sur la fin de la période. Il ne dispose pas d'ancrage territorial particulier.
                - Malgré son omni-présence médiatique, Éric ZEMMOUR obtient ses 500 signatures avec difficulté. La plupart proviennent de zones rurales : on peut par exemple remarquer qu'il n'a reçu aucun parrainage d'élus Parisiens, et un très faible nombre en Île-de-France.
                - Yanick JADOT reçoit un grand nombre de parrainages dans le département du Rhône. Cela s'explique par le fait que la métropole de Lyon est administrée par son parti, Europe Écologie les Verts.
                - Jean LASSALLE bénéficie d'un grand nombre de signatures depuis le département où il a été maire puis député. Par ailleurs, il est intéressant de remarquer qu'il est le candidat à obtenir le plus de parrainages depuis la Corse.
                - Fabien ROUSSEL obtient son plus grand de parrainages dans le département du Nord, qu'il représente en tant que député.
                - Marine LE PEN reçoit la plupart de ses signatures depuis des départements ruraux. Elle réunit le plus de parrainages dans le département du Pas-de-Calais, où elle est député.
            """),
            dcc.Markdown("""
                # Sources
                    * [Jeu de données parrainage des candidats pour l'élection présidentielle 2022](https://www.data.gouv.fr/fr/datasets/parrainages-des-candidats-a-lelection-presidentielle-francaise-de-2022/)
                    * [GeoJSON France (délimitations géographiques des départements)](https://france-geojson.gregoiredavid.fr/)
                # Auteurs
                    * Nathan Cabasso (<nathan.cabasso@epita.fr>)
                    * Ferdinand Mom (<ferdinand.mom@epita.fr>)
            """),
        ], style={
                #'backgroundColor': 'rgb(240, 240, 240)',
                 'padding': '10px 50px 10px 50px',
                 }
        )

        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('par-main-graph', 'figure'),
            [dash.dependencies.Input('par-candidat', 'value')]
        )(self.update_graph)

        self.app.callback(
            dash.dependencies.Output('par-main-map', 'figure'),
            [dash.dependencies.Input('par-candidat', 'value')]
        )(self.display_map)
    
        

    def update_graph(self, candidat):
        # Select candidate
        parrainages = self.df[self.df['Candidat'] == candidat]

        count_by_date = parrainages.groupby(["Date de publication"]).size()
        count_by_date = count_by_date.to_frame(name="size").reset_index().sort_values(by="Date de publication").set_index("Date de publication")

        index = count_by_date.index
        index.name = 'date'


        df_count_by_date = pd.DataFrame(
            {"Nouveaux parrainages": count_by_date["size"], "Parrainages au total": count_by_date["size"].cumsum()}, index=index)

        df_count_by_date = df_count_by_date.reset_index().melt('date', var_name="Catégorie", value_name="y")

        fig = px.line(df_count_by_date, template='plotly_white', x='date', y='y', color='Catégorie', line_shape='spline')
        fig.update_traces(hovertemplate='%{y} parrainages le %{x:%d/%m/%y}', mode="lines+markers")
        fig.update_layout(hovermode="x unified", title="Évolution du nombre de parrainages par candidat à la présidentielle")
        fig.update_layout(
            xaxis = dict(title="Date de publication", tickformat="%d-%m-%Y"),
            yaxis = dict(title="Nombre parrainages"), 
            height=450,
            showlegend=True,
        )
        return fig
    
    def display_map(self, candidat):
        
        candidat_df = self.df[self.df['Candidat'] == candidat]
        department_candidat_df = candidat_df.groupby("Département")
        candidat_repertition_per_departement = department_candidat_df["Département"].count().to_frame(name="Parrainages").reset_index()

        fig_map = px.choropleth_mapbox(
            candidat_repertition_per_departement,
            geojson=self.departements_json,
            locations='Département',
            featureidkey="properties.nom",
            mapbox_style='carto-positron',
            color="Parrainages",
            color_continuous_scale=px.colors.sequential.Blues,
            hover_data={'Parrainages': True},
            zoom=3.8,
            center={'lat': 47, 'lon': 2},
            opacity=1.0,
        )

        fig_map.update_layout(
            title={
                'text': f'Parrainage de "{candidat}" par département',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        return fig_map

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = Parrainage()
    ws.run(port=8055)
