import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import json

class UrbanPolutionStats():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.map = json.load(open('tc_urban/data/custom.geo.json'))
        self.df = pd.read_pickle('tc_urban/data/countriesData.pkl')
        self.french = {'Asia':'Asie', 'Europe':'Europe', 'Africa':'Afrique', 'Oceania':'Océanie', 'Americas':'Amériques'}
        self.region_colors = {'Asia':'gold', 'Europe':'green', 'Africa':'brown', 'Oceania':'red', 'Americas':'navy'}
        self.years = sorted(set(self.df.index.values))

        self.main_layout = html.Div(
            children = [
                html.H3('Analyse graphique des émissions de CO₂ à travers les différents pays du monde'),

                html.Br(),
                html.Br(),

                # Years slider
                html.Div(
                    children = [
                        html.Div(
                            dcc.Slider(
                                id='ups-crossfilter-year-slider',
                                min=self.years[0],
                                max=self.years[-1],
                                step = 1,
                                value=self.years[0],
                                marks={str(year): str(year) for year in self.years[::5]},
                            ),
                            style = {
                                'display':'inline-block',
                                'width':"80%"
                            }
                        ),
                        dcc.Interval(
                            id='ups-auto-stepper',
                            interval=500,
                            max_intervals = -1,
                            n_intervals = 0
                        ),
                        html.Button(
                            self.START,
                            id='ups-button-start-stop', 
                            style = {
                                'display':'inline-block',
                                'width':"10%",
                                'vertical-align':'top'
                            }
                        ),
                    ],
                    style = {
                        'padding': '0px 50px', 
                        'width':'100%'
                    }
                ),

                html.Br(),
                html.Br(),

                # Maps
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                html.H5('Évolution du pourcentage de population urbaine par pays'),
                                dcc.Graph(id='ups-urbanpop-map', style={'display':'inline-block'})
                            ],
                            style = {
                                'display':'flex',
                                'flex-direction':'column',
                                'justifyContent':'center',
                                'width':'50%'
                            }
                        ),
                        html.Div(
                            children = [
                                html.H5('Évolution des émissions de CO₂ par personne par pays'),
                                dcc.Graph(id='ups-emission-map', style={'display':'inline-block'})
                            ],
                            style = {
                                'display':'flex',
                                'flex-direction':'column',
                                'justifyContent':'center',
                                'width':'50%'
                            }
                        )
                    ],
                    style = {
                        'display':'flex',
                        'flex-direction':'row',
                        'borderTop': 'thin lightgrey solid',
                        'borderBottom': 'thin lightgrey solid',
                        'justifyContent':'center'
                    }
                ),

                html.Br(),

                # Main graph
                html.Div(
                    children = [
                        html.H5('Évolution des émissions de CO₂ vs la population en zone urbaine par pays'),
                        html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'),
                        html.Br(),
                        html.Div(
                            children = [
                                html.Div(dcc.Graph(id='ups-main-graph'), style={'width':'90%'}),
                                html.Div(
                                    children = [
                                        html.Div('Region'),
                                        dcc.Checklist(
                                            id='ups-crossfilter-which-region',
                                            options=[{'label': self.french[i], 'value': i} for i in sorted(self.region_colors.keys())],
                                            value=sorted(self.region_colors.keys()),
                                            labelStyle={'display':'block'},
                                        ),
                                        html.Br(),
                                        dcc.RadioItems(
                                            id='ups-crossfilter-xaxis-type',
                                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                                            value='Linéraire',
                                            labelStyle={'display':'none'},
                                        ),
                                    ],
                                    style = {
                                        'margin-left':'15px',
                                        'width': '7em',
                                        'float':'right'
                                    }
                                )
                            ],
                            style = {
                                'display':'flex',
                                'flex-direction':'row',
                                'width':'100%'
                            }
                        )
                    ],
                    style={
                        'padding': '10px 50px', 
                        'display':'flex',
                        'flex-direction':'column',
                        'justifyContent':'center'
                    }
                ),

                html.Br(),
                html.Div(id='ups-div-country'),

                html.Div(
                    children = [
                        dcc.Graph(id='ups-emission-time-series', style={'width':'33%', 'display':'inline-block'}),
                        dcc.Graph(id='ups-urbanpop-time-series', style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                        dcc.Graph(id='ups-pop-time-series', style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                    ],
                    style = {
                        'display':'flex', 
                        'borderTop': 'thin lightgrey solid',
                        'borderBottom': 'thin lightgrey solid',
                        'justifyContent':'center'
                    }
                ),

                html.Br(),
                dcc.Markdown("""
                    #### Analyse

                    D'après les deux premiers graphes, on peut remarquer que plus la population urbaine est grande,
                    plus elle émet de CO₂ par personne. Par exemple, le continent africain regroupe une faible
                    population urbaine et elle émet peu de CO₂ par habitant ; les Etats-unis, en revanche,
                    regroupent une forte population urbaine avec une grande émission de CO₂ par habitant.

                    Dans le 3ème graphique, on peut remarquer que la Chine et l'Inde sont les deux pays les plus
                    peuplés au monde et elles émettent peu d'émission de CO₂ par habitant en zone urbaine. Néanmoins,
                    l'émission totale de CO₂ de ces deux pays est énorme.


                    ###### Bilan
                    
                    Après l'analyse de ce jeu de données, on peut remarquer que plus un pays a de populations
                    urbaines, plus l'émission de CO₂ par personne va être grande.  De plus, comme nous l'avons
                    vu dans l'exemple de la Chine et de l'Inde, un pays peut avoir une émission de CO₂
                    totale très élevée malgré le fait que l'émission de CO₂ par habitant soit moindre du au fait que
                    la population totale soit très élevée.
                """),
                      
                html.Br(),
                dcc.Markdown("""
                    #### À propos
                    Données :

                    * [World developement indicators](https://www.kaggle.com/kaggle/world-development-indicators?select=Indicators.csv)
                    * [Countries region](https://www.kaggle.com/datasets/andreshg/countries-iso-codes-continent-flags-url?resource=download&select=countries_continents_codes_flags_url.csv)
                    * [World map](https://geojson-maps.ash.ms/)
                """)
            ],
            style = {
                'padding': '10px 50px 10px 50px',
            }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        self.app.callback(
            dash.dependencies.Output('ups-urbanpop-map', 'figure'),
            [dash.dependencies.Input('ups-crossfilter-year-slider', 'value')])(self.update_urbanpop_map)
        self.app.callback(
            dash.dependencies.Output('ups-emission-map', 'figure'),
            [dash.dependencies.Input('ups-crossfilter-year-slider', 'value')])(self.update_emission_map)
        self.app.callback(
            dash.dependencies.Output('ups-main-graph', 'figure'),
            [ dash.dependencies.Input('ups-crossfilter-which-region', 'value'),
              dash.dependencies.Input('ups-crossfilter-xaxis-type', 'value'),
              dash.dependencies.Input('ups-crossfilter-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('ups-div-country', 'children'),
            dash.dependencies.Input('ups-main-graph', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('ups-button-start-stop', 'children'),
            dash.dependencies.Input('ups-button-start-stop', 'n_clicks'),
            dash.dependencies.State('ups-button-start-stop', 'children'))(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output('ups-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('ups-button-start-stop', 'children')])(self.run_movie)
        self.app.callback(
            dash.dependencies.Output('ups-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('ups-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('ups-crossfilter-year-slider', 'value'),
             dash.dependencies.State('ups-button-start-stop', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('ups-emission-time-series', 'figure'),
            [dash.dependencies.Input('ups-main-graph', 'hoverData'),
             dash.dependencies.Input('ups-crossfilter-xaxis-type', 'value')])(self.update_emission_timeseries)
        self.app.callback(
            dash.dependencies.Output('ups-urbanpop-time-series', 'figure'),
            [dash.dependencies.Input('ups-main-graph', 'hoverData'),
             dash.dependencies.Input('ups-crossfilter-xaxis-type', 'value')])(self.update_urbanpop_timeseries)
        self.app.callback(
            dash.dependencies.Output('ups-pop-time-series', 'figure'),
            [dash.dependencies.Input('ups-main-graph', 'hoverData'),
             dash.dependencies.Input('ups-crossfilter-xaxis-type', 'value')])(self.update_pop_timeseries)

    def update_graph(self, regions, xaxis_type, year):
        dfg = self.df.loc[year]
        dfg = dfg[dfg['RegionName'].isin(regions)]
        fig = px.scatter(
            dfg, x = "Urban population (%)", y = "CO2 emissions per person (t)", 
            size = "Total population", size_max = 60,
            color = "RegionName", color_discrete_map = self.region_colors,
            hover_name = "CountryName", log_x = True
        )

        fig.update_layout(
            xaxis = dict(
                title ='Poucentage de la population résidant en zone urbaine',
                type = 'linear',
                range = (0, 105) 
            ),
            yaxis = dict(
                title = "Émissions de CO₂ par personne (en t)",
                range = (-3, 25)
            ),
            margin = {'l': 40, 'b': 30, 't': 10, 'r': 0},
            hovermode = 'closest',
            showlegend = False
        )
        return fig

    def update_urbanpop_map(self, year):
        dfg = self.df.loc[year]
        fig = px.choropleth_mapbox(dfg, geojson=self.map, 
                                locations = 'CountryName', featureidkey = 'properties.name', # join keys
                                color = 'Urban population (%)', color_continuous_scale = "Viridis",
                                mapbox_style = "carto-positron",
                                zoom = 0, center = {"lat": 47, "lon": 2},
                                opacity = 0.5, range_color = (0, 100),
                                labels = {'Urban population (%)':'Urban population (%)'}
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    
    def update_emission_map(self, year):
        dfg = self.df.loc[year]
        fig = px.choropleth_mapbox(dfg, geojson=self.map, 
                                locations = 'CountryName', featureidkey = 'properties.name', # join keys
                                color = 'CO2 emissions per person (t)',
                                mapbox_style = "carto-positron",
                                zoom = 0, center = {"lat": 47, "lon": 2},
                                opacity = 0.5, range_color = (0, 25),
                                labels = {'CO2 emissions per person (t)':'CO2 emissions per person (t)'}
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def create_time_series(self, country, what, axis_type, title):
        return {
            'data': [go.Scatter(
                x = self.years,
                y = self.df[self.df["CountryName"] == country][what],
                mode = 'lines+markers',
            )],
            'layout': {
                'height': 225,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title':title,
                          'type': 'linear' if axis_type == 'Linéaire' else 'log'},
                'xaxis': {'showgrid': False}
            }
        }

    def get_country(self, hoverData):
        if hoverData == None:
            return self.df['CountryName'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    def update_emission_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'CO2 emissions (kt)', xaxis_type, 'Émissions de CO₂ (en kt)')

    def update_urbanpop_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'Urban population', xaxis_type, "Population en zone urbaine")

    def update_pop_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'Total population', xaxis_type, 'Population totale')

    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    def run_movie(self, text):
        if text == self.START:
            return 0 
        else:
            return -1

    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ups = UrbanPolutionStats()
    ups.run(port=8055)
