import pandas as pd
import dash
from dash import html
from dash import dcc

import plotly.express as px
import json


class Birth_Map:
    START = 'Start'
    STOP = 'Stop'

    def __init__(self, application=None):

        self.df_naiss = pd.read_pickle('data/naissances_par_dep_1970_2020.pkl')
        self.years = sorted(set(self.df_naiss.index.values))
        self.year = self.years[0]
        self.df_dict = {}
        self.departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        for year in self.df_naiss.index.values:
            self.df_dict.update({year: pd.read_pickle(f'data/population_birth_rate/{year}.pkl')})

        self.main_layout = html.Div(id='main-layout-page', children=[

            html.Div('Carte du taux de natalité par départements en France de 1970 à 2020'),
            html.Div([
                html.Div([dcc.Graph(id='map-selected-year'), ], style={'width': '90%', }),

                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(id='selected-year-slider', ),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Button(
                        self.START,
                        id='bmap-button-start-stop',
                        style={'display': 'inline-block'}
                    ),

                ], style={'margin-left': '15px', 'width': '7em', 'float': 'right'}),

            ], style={
                'padding': '10px 50px',
                'display': 'flex',
                'justifyContent': 'center'
            }),
            html.Div([
                html.Div(
                    dcc.Slider(
                        id='map-year-slider',
                        min=self.years[0],
                        max=self.years[-1],
                        step=1,
                        value=self.years[0],
                        marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display': 'inline-block', 'width': "90%"}
                ),
                dcc.Interval(  # fire a callback periodically
                    id='bmap-auto-stepper',
                    interval=5000,  # in milliseconds
                    max_intervals=-1,  # start running
                    n_intervals=0
                ),
            ], style={
                'padding': '0px 50px',
                'width': '100%'
            }),

            html.Div([
                dcc.Graph(id='bmap-population-graph',
                          style={'width': '50%', 'display': 'inline-block'}),
                dcc.Graph(id='bmap-naissances-graph',
                          style={'width': '50%', 'display': 'inline-block', 'padding-left': '0.5%'}),
            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),

            html.Br(),
            html.Br(),

            dcc.Markdown("""
            Déplacez le slider pour afficher la carte de l'année correspondante, ou laissez le avancer tout seul.
            Survolez un département avec votre souris pour afficher plus d'informations.
            
            Note:
               * Le taux de natalité correspond au nombre de naissances par rapport au nombre total de la population
               * Lecture: une couleur foncé signifie un faible taux de natalité (peu de naissances par rapport à la population), une couleur claire un haut taux de natalité.
               * En 1970, le taux de natalité dans le département de la Cher (18) est de 12,3 pour 1000. La population y est de 304400 et les naissances sur l'année s'élèvent à 3759.
            
            Sources:
               * Naissances: https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262
               * Population: https://www.insee.fr/fr/statistiques/1893204#consulter.

            A noter que les données sources des naissances sont celle des prénoms attribués sur l'année,
            mais qu'elle est présentée comme ne présentant pas d'écart significatifs aux naissances sur l'année
            à partir de 1946 [sur le site de l'INSEE.](https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262#documentation).
            Cependant, au vu de l'incohérence de ces données avec d'autres que j'ai pu trouvé sur des années spécifique,
            les valeurs pour les naissances annuelles sont à prendre avec précaution.
            """),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px'
        }
                                    )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('map-selected-year', 'figure'),
            dash.dependencies.Input('map-year-slider', 'value'))(self.update_map)

        self.app.callback(
            dash.dependencies.Output('selected-year-slider', 'children'),
            dash.dependencies.Input('map-year-slider', 'value'))(self.update_year)

        self.app.callback(
            dash.dependencies.Output('bmap-button-start-stop', 'children'),
            dash.dependencies.Input('bmap-button-start-stop', 'n_clicks'),
            dash.dependencies.State('bmap-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('bmap-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('bmap-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('map-year-slider', 'value'),
            dash.dependencies.Input('bmap-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('map-year-slider', 'value'),
             dash.dependencies.State('bmap-button-start-stop', 'children')])(self.on_interval)

        self.app.callback(
            dash.dependencies.Output('bmap-population-graph', 'figure'),
            dash.dependencies.Input('map-selected-year', 'hoverData'))(self.update_pop_graph)
        self.app.callback(
            dash.dependencies.Output('bmap-naissances-graph', 'figure'),
            dash.dependencies.Input('map-selected-year', 'hoverData'))(self.update_naiss_graph)

    def update_year(self, year):
        self.year = year
        return f'Année selectionnée {self.year}'

    def update_map(self, year):
        if year == None:
            year = self.year
        year_df = self.df_dict.get(year)

        fig = px.choropleth_mapbox(year_df, geojson=self.departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='tx_nat_p_1000',
                                   hover_name='DEPNAME',
                                   hover_data=['tx_nat_p_1000', 'naissances', 'Total'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   labels={'DEP': 'Numéro du département',
                                           'tx_nat_p_1000': 'Taux de natalité (pour 1000)',
                                           'naissances': 'Nombre de naissances',
                                           'Total': 'Population du département'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig



    def update_pop_graph(self, hoverData):
        if hoverData == None:
            return self.create_naiss_graph(1, 'Ain')
        hover = hoverData['points'][0]
        dep = hover['location']
        depname = hover['hovertext']
        return self.create_naiss_graph(1, 'Ain')


    def create_naiss_graph(self, dep, depname):
        return px.line(self.df_naiss[dep], title=f'Evolution des naissances en {depname}',
                       hover_data=['value'],
                       labels={'annais': 'Années', 'value': 'Naissances', 'variable': 'Département'})

    def update_naiss_graph(self, hoverData):
        if hoverData == None:
            return self.create_naiss_graph(1, 'Ain')
        hover = hoverData['points'][0]
        dep = hover['location']
        depname = hover['hovertext']
        try:
            dep = int(dep)
        except ValueError:
            dep = 20
        return self.create_naiss_graph(dep, depname)


    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:  # then it means we are stopped
            return 0
        else:
            return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year  # nothing changes
