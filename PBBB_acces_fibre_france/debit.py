import sys
import dash
import flask
import json
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px

from typing import List


class HautDebit():
    dossier_data = "./PBBB_acces_fibre_france/data/"
    paths = ['2021t4-obs-hd-thd-deploiement.xlsx',
             'departements.geojson',
             'operator-id.xlsx']

    def load_operator_by_dep(self):
        """
        Cette fonction permet de connaître le nombre d'opérateur dans chaque département.        
        """
        ope = pd.read_excel(self.dossier_data + self.paths[2],
                            sheet_name='Liste des OI',
                            usecols="C,E",
                            names=["couverture", "OI"])

        metro_dep = ["2A", "2B"] + ["{:02d}".format(i) for i in range(1, 96)]
        all_dep = metro_dep + [str(i) for i in range(971, 979)]

        ope["couverture"] = np.where(
            ope["couverture"] == "Nationale", ",".join(all_dep), ope["couverture"])
        ope["couverture"] = np.where(ope["couverture"].str.startswith(
            "Métropole", na=False), ",".join(metro_dep), ope["couverture"])
        ope["couverture"] = np.where(ope["couverture"].str.contains(
            "Saint-Martin", na=False), "978", ope["couverture"])

        def str_to_list(l) -> List[str]:
            """ Cette fonction permet de transformer une string contenant des departement en une liste de string

                Avant de faire la transformation, les données sont uniformisées en remplacant les ' ' (espaces) et '.' (point)
                par des ',' (virgules). 

            """
            return list(filter(None, str(l).replace(".", ",").replace(" ", ",").split(",")))

        ope["couverture"] = ope["couverture"].apply(str_to_list)
        # Permet de transformer les listes de département par Opérateur en nouvelles lignes pour chaque département-opérateur
        ope = ope.set_index("OI")["couverture"].apply(
            pd.Series).stack().reset_index()
        # On renome les colonnes
        ope.columns = ["OI", "dep_index", "dep"]
        ret = pd.DataFrame(ope.groupby('dep').size(),
                           columns=['Nombre d\'opérateur'])

        return ret

    def init_departement(self):
        return pd.read_excel(self.dossier_data + self.paths[0],
                             sheet_name='Départements',
                             header=4,
                             usecols="A,B,G,H:X"), json.load(open(self.dossier_data + self.paths[1]))

    def init_graph_departement(self):
        nombre_d_operateur = self.load_operator_by_dep()
        tmp_data = self.df_departement.copy()

        data = tmp_data.join(nombre_d_operateur, on='Code département')

        col = list(data.columns)
        data = pd.melt(data, id_vars=col[:3] + [col[-1]], value_vars=col[3:-1])

        data.rename(columns={'variable': 'Temps'}, inplace=True)
        data.sort_values(['Code département', 'Temps'])

        return data

    def __init__(self, application=None):
        self.df_departement, self.geojson_departement = self.init_departement()
        self.year = self.df_departement.columns[3:]

        self.graph_departement = self.init_graph_departement()

        self.main_layout = html.Div(children=[
            html.H3(
                children='Évolution de l\'accès à la fibre optique en France Métropolitaine de 2018 à 2021'),

            html.Div([
                html.Div([
                    html.H6(
                        'Carte de la couverture fibre optique en France métropolitaine par département en fonction du temps'),
                    dcc.Graph(id='debit-main-map'),
                ], style={'width': '90%', }),

                html.Div([
                    html.Div('Type'),
                    dcc.RadioItems(
                        id='debit-crossfilter-type-type',
                        options=[{'label': i, 'value': i}
                                 for i in ['Taux', 'Brute']],
                        value='Taux',
                        labelStyle={'display': 'block'},
                    ),
                ], style={'margin-left': '20px', 'width': '7em', 'float': 'right'}),
            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'justifyContent': 'center'
            }),

            html.Br(),
            html.Div([
                html.Div(
                    dcc.Slider(
                        id='debit-crossfilter-year-slider',
                        min=0,
                        max=len(self.year) - 1,
                        step=1,
                        value=0,
                        marks={i: self.year[i]
                               for i in range(len(self.year))},
                    ),
                    style={'display': 'inline-block', 'width': "90%"}
                ),
            ], style={
                'padding': '0px 50px',
                'width': '100%'
            }),

            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les régions/départements, vous avez une infobulle.
            On peut observer qu'au cours du temps, tous les départements ont gagné en haut débit.

            Grâce au graphe ci-dessous, on peut essayer de comprendre quels facteurs ont un impact sur le taux de couverture haut-débit.
            """),

            html.Br(),
            html.Div([

                html.Div([
                    html.H6(
                        'Graphe de l\'évolution de la couverture haut-débit en France métropolitaine par département en fonction du temps'),
                    dcc.Graph(id='debit-graph'), ], style={'width': '90%', }),

                html.Div([
                    html.Div('Type'),
                    dcc.RadioItems(
                        id='debit-crossfilter-type-couleur',
                        options=[{'label': i, 'value': i}
                                 for i in ['logement', 'opérateur']],
                        value='logement',
                        labelStyle={'display': 'block'},
                    ),
                    html.Br(),
                    html.Div('Filtre'),
                    html.Div([
                        html.Div([
                            html.Br(), html.Br(), html.Br(), html.Br(), html.Br(
                            ), html.Br(), html.Br(), html.Br(), html.Br(),
                            html.Br(), html.Br(), html.Br(), html.Br(), html.Br(
                            ), html.Br(), html.Br(), html.Br(), html.Br(),
                        ], style={'background-image': 'linear-gradient(rgb(0, 255, 0), rgb(0, 0, 255))',
                                  'width': '40%',
                                  'float': 'left',
                                  'height': '100%',
                                  'padding': '0 0'}),
                        html.Div([
                            dcc.RangeSlider(
                                id='debit-filter-type-slider',
                                min=0,
                                max=1,
                                value=[0, 1],
                                vertical=True,
                            )
                        ], style={'width': '60%', 'float': 'right'}),
                    ]),
                ], style={'margin-left': '20px', 'width': '7em', 'float': 'right'}),
            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'justifyContent': 'center'
            }),

            html.Br(),
            dcc.Markdown("""
            Vous pouvez choisir la caractéristique mise en valeur par la couleur de la courbe.
            On peut voir :
            - le nombre d'opérateur dans le département ne semble pas influer sur la couverture
            - le nombre de logement dans le département semble impacter la couverture. En effet, les départements où il y a plus de logemment ont une meilleure couverture

            #### À propos

            Sources :
            - nombre d'opérateur par département : https://www.arcep.fr/fileadmin/reprise/dossiers/fibre/liste-gestion-identifiants-prefixe-ligne-fibre-2.xlsx
            - nombre de logement par département : https://www.data.gouv.fr/fr/datasets/r/d538685a-b9cb-4a3e-b90d-ad6f0a13920b
            """)
        ], style={
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Map
        self.app.callback(
            dash.dependencies.Output('debit-main-map', 'figure'),
            [dash.dependencies.Input('debit-crossfilter-type-type', 'value'),
             dash.dependencies.Input('debit-crossfilter-year-slider', 'value')])(self.update_map)

        # Graphe
        self.app.callback(
            dash.dependencies.Output('debit-graph', 'figure'),
            [dash.dependencies.Input('debit-crossfilter-type-couleur', 'value'),
             dash.dependencies.Input('debit-filter-type-slider', 'value')])(self.update_graph)

        # Filtre
        self.app.callback(
            dash.dependencies.Output('debit-filter-type-slider', 'max'),
            [dash.dependencies.Input('debit-crossfilter-type-couleur', 'value')])(self.update_slider_max)
        self.app.callback(
            dash.dependencies.Output('debit-filter-type-slider', 'value'),
            [dash.dependencies.Input('debit-crossfilter-type-couleur', 'value')])(self.update_slider_value)

    def update_map(self, type, year):
        data, goejson = self.df_departement.copy(), self.geojson_departement

        if type == 'Taux':
            data[data.columns[3:]] = data[data.columns[3:]].div(
                data[data.columns[2]], axis=0)
            range_col = (0, 1)
        else:
            range_col = (0, data[data.columns[3:]].max().max())

        fig = px.choropleth_mapbox(data, geojson=goejson,
                                   locations='Nom département', featureidkey='properties.nom',
                                   color=self.year[year], color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.2, center={"lat": 47, "lon": 2},
                                   range_color=range_col,
                                   opacity=0.5,
                                   labels={self.year[year]: type})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    def update_graph(self, couleur, filter_value):
        df = self.graph_departement

        def gradient_scale(rgbmin, rgbmax, nom):
            col = df[nom].unique()
            cmax, cmin = col.max(), col.min()

            def color(x, n): return rgbmin[x] + (n - cmin) * \
                (rgbmax[x] - rgbmin[x]) / (cmax - cmin)
            return {n: f'rgb({color(0,n)},{color(1,n)},{color(2,n)})' for n in col}

        dcouleur = {'logement': 'Meilleure estimation des locaux T4 2021 ',
                    'opérateur': 'Nombre d\'opérateur'}
        nom = dcouleur[couleur]

        fig_col_dic = gradient_scale((0, 0, 255), (0, 255, 0), nom)

        m, M = filter_value
        fig = px.line(df, x=df['Temps'],
                      template='plotly_white', range_y=(0, 1))
        for key, group in df.groupby(['Nom département']):
            col = group[nom].unique()[0]
            if not (m <= col <= M):
                continue
            fig.add_scatter(x=group['Temps'],
                            y=(group['value'] /
                               group['Meilleure estimation des locaux T4 2021 ']),
                            line=dict(
                                color=fig_col_dic[group[nom].unique()[0]],
                                width=2),
                            mode='lines',
                            name=key, text=key, hoverinfo='x+y+text')
        fig.update_layout(legend_x=1, legend_y=0)
        fig.update_yaxes(title_text="Couverture haut-débit")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    def update_slider_max(self, type):
        if type == 'logement':
            return self.graph_departement['Meilleure estimation des locaux T4 2021 '].unique().max()
        elif type == 'opérateur':
            return self.graph_departement['Nombre d\'opérateur'].unique().max()

    def update_slider_value(self, type):
        return [0, self.update_slider_max(type)]

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = HautDebit()
    ws.run(port=8055)
