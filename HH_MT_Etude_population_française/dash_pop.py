# Dash app to display it
import json

import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


class Population():
    year_list = [
        '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
        '2009', '2010', '2011'
    ]

    regions_list = [
        'Auvergne-Rhône-Alpes', 'Bourgogne-Franche-Comté', 'Bretagne',
        'Centre-Val-de-Loire', 'Corse', 'Grand Est', 'Hauts-de-France',
        'Île-de-France', 'Normandie', 'Nouvelle-Aquitaine', 'Occitanie',
        'Pays de la Loire', "Provence-Alpes-Côted'Azur",
        'France métropolitaine', 'Guadeloupe', 'Martinique', 'Guyane',
        'La Réunion', 'DOM', 'France métropolitaine et DOM'
    ]

    map_data_types = ["taxes", "salary"]

    def __init__(self, application=None):
        df_histo = pd.read_csv('HH_MT_Etude_population_française/data/data_histo_population.csv').drop(
            columns="Unnamed: 0")

        df_map_lines = pd.read_csv('HH_MT_Etude_population_française/data/data_map_lines.csv')

        regions_map = json.load(open('HH_MT_Etude_population_française/data/regions.geojson'))
        self.regions_map = regions_map

        slider_dict = dict(zip(list(range(1, 13)),
                               sorted(set(self.year_list))))

        self.slider_dict = slider_dict
        self.data_histo = df_histo
        self.data_map_lines = df_map_lines

        self.main_layout = html.Div(children=[
            html.H3(children="Evolution des salaires et des impôts.",
                    style={
                        "text-align": "center",
                    }, ),
            html.Div(
                [
                    html.H4(["Evolution des impôts et des salaires entre 2000 et 2010", ], className="container_title",
                            style={"text-align": "center"}),
                    html.
                        P(
                        "Nous pouvons remarquer que malgré l’augmentation des salaires, les impôts n’ont pas augmenté entre 2000 et 2010. Nous pouvons néanmoins remarquer que les salaires suivent les impôts, Après l’augmentation des impôts en 2005, les salaires ont augmenté.",
                        style={
                            "text-align": "center",
                            "font-size": "10pt"
                        }),
                    html.
                        P(
                        "La baisse d’impôts en 2004 puis une augmentation en 2005 se traduit par deux lois de l’été 2004 qui augmente les impôts.",
                        style={
                            "text-align": "center",
                            "font-size": "10pt"
                        }),
                ],
                className="pretty_container twelve columns",
            ),
            html.Div(
                [
                    html.Div([
                        html.Div('Choix des régions'),
                        dcc.RadioItems(
                            id='radio-region-lines',
                            options=[{
                                'label': reg,
                                'value': reg
                            } for reg in self.regions_list],
                            value='Auvergne-Rhône-Alpes',
                            labelStyle={'display': 'block'},
                        ),
                    ],
                        style={
                            'margin-left': '5px',
                            'width': '15em',
                            'float': 'right'
                        }),
                    html.Div([
                        dcc.Graph(id='lines-plot-graph'),
                    ],
                        style={
                            'width': '80%',
                        }),
                ],
                className="ten columns pretty_container",
                style={
                    'padding': '10px 50px',
                    'display': 'flex',
                    'justifyContent': 'center'
                }),
            html.Div(
                [
                    html.H4(["Répartition des taxes et des salaires dans les régions de France.", ],
                            className="container_title", style={"text-align": "center"}),
                    html.
                        P(
                        "Nous avons ici voulus représenter de manière plus visuelle les taxes et salaires entre les différentes régions de France.",
                        style={
                            "text-align": "center",
                            "font-size": "10pt"
                        }),
                ],
                className="pretty_container twelve columns",
            ),
            html.Div([
                dcc.Slider(1,
                           12,
                           step=None,
                           marks=self.slider_dict,
                           value=1,
                           id='slider-date-map'),
            ],
                className="ten columns pretty_container",
                style={
                    'display': 'inline-block',
                    'width': "95%"
                }),
            html.Div(
                [
                    html.Div([
                        dcc.Graph(id='map-plot'),
                    ],
                        style={
                            'width': '90%',
                        }),
                    html.Div([
                        dcc.RadioItems(
                            id='radio-data-type',
                            options=[{
                                'label': type_data,
                                'value': type_data
                            } for type_data in self.map_data_types],
                            value='taxes',
                            labelStyle={'display': 'block'},
                        ),
                    ],
                        style={
                            'margin-left': '5px',
                            'width': '15em',
                            'float': 'right'
                        }),
                ],
                className="ten columns pretty_container",
                style={
                    'padding': '10px 50px',
                    'display': 'flex',
                    'justifyContent': 'center'
                }),
            html.Div(
                [
                    html.H4(["Population par région entre 2000 et 2011", ], className="container_title",
                            style={"text-align": "center"}),
                    html.
                        P(
                        "Nous voulions ici représenter les différentes populations, leur répartition et leur total par région avec certains paramètres.",
                        style={
                            "text-align": "center",
                            "font-size": "10pt"
                        }),
                ],
                className="pretty_container twelve columns",
            ),
            html.Div([
                dcc.Slider(1,
                           12,
                           step=None,
                           marks=self.slider_dict,
                           value=1,
                           id='slider-date-histo'),
            ],
                className="ten columns pretty_container",
                style={
                    'display': 'inline-block',
                    'width': "95%"
                }),
            html.Div(
                [
                    html.Div([
                        dcc.RadioItems(
                            id='radio-population-histo',
                            options=[{
                                'label': reg,
                                'value': reg
                            } for reg in self.regions_list],
                            value='Auvergne-Rhône-Alpes',
                            labelStyle={'display': 'block'},
                        ),
                    ],
                        style={
                            'margin-left': '5px',
                            'width': '15em',
                            'float': 'right'
                        }),
                    html.Div([
                        dcc.Graph(id='histo-plot-graph-eh'),
                    ],
                        style={
                            'width': '80%',
                        }),
                ],
                className="ten columns pretty_container",
                style={
                    'padding': '10px 50px',
                    'display': 'flex',
                    'justifyContent': 'center'
                }),
            html.Div(
                [
                    html.H4(["Auteurs.", ], className="container_title", style={"text-align": "center"}),
                    html.
                        P("Mélanie Tchéou et Erwann Harris.",
                          style={
                              "text-align": "center",
                              "font-size": "10pt"
                          }),
                ],
                className="pretty_container twelve columns",
            ),
        ])

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output(component_id='lines-plot-graph',
                   component_property='figure'), [
                Input(component_id='radio-region-lines',
                      component_property='value')
            ])(self.update_region_lines)

        self.app.callback(
            Output(component_id='map-plot', component_property='figure'), [
                Input(component_id='slider-date-map',
                      component_property='value'),
                Input(component_id='radio-data-type',
                      component_property='value')
            ])(self.update_map_data_type)

        self.app.callback(
            Output(component_id='histo-plot-graph-eh',
                   component_property='figure'), [
                Input(component_id='slider-date-histo',
                      component_property='value'),
                Input(component_id='radio-population-histo',
                      component_property='value')
            ])(self.update_population_histo)

    def update_population_histo(self, num_year, region):
        year = int(self.slider_dict.get(num_year))
        df_histo = self.data_histo.copy()
        population_df = df_histo[(df_histo["region"] == region)
                                 & (df_histo["year"] == year)]
        data_dict = {
            'Influences': ['Total', 'Hommes', 'Femmes'],
            'Values': [
                population_df['total'].values[0],
                population_df['men'].values[0],
                population_df['women'].values[0]
            ]
        }
        fig = px.bar(data_dict,
                     x="Influences",
                     y="Values",
                     title="Répartition de la population dans la région " +
                           region + " le " + str(year) + ".",
                     color="Values")
        return fig

    def update_map_data_type(self, num_year, type_data):
        year = int(self.slider_dict.get(num_year))
        df_map = self.data_map_lines.copy()
        maps = self.regions_map
        df_map = df_map.set_index("year")
        df_map = df_map.loc[year]
        if type_data == 'taxes':
            df_map = df_map.drop(columns=["salary"])
        elif type_data == 'salary':
            df_map = df_map.drop(columns=["taxes"])
        fig = px.choropleth_mapbox(df_map, geojson=maps,
                                   locations='regions', featureidkey='properties.nom',  # join keys
                                   color=type_data, color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 46.5, "lon": 2},
                                   opacity=0.5,
                                   labels={'valeur': 'Valeur '}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def update_region_lines(self, region):
        df_region_lines = self.data_map_lines.copy()
        df_region_lines = df_region_lines[df_region_lines.regions == region]
        df_region_lines.index = df_region_lines.year
        data_list = ['taxes', 'salary']
        df_region_lines = df_region_lines.drop(columns=['regions'])
        fig = px.line(df_region_lines, x=df_region_lines.index, y=data_list, title="Machine en " + region)
        return fig


if __name__ == '__main__':
    pop = Population()
    pop.app.run_server(port=8051)
