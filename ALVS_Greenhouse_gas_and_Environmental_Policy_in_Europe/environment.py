import sys
import dash
import flask
from dash import dcc
from dash import html
from .get_data import get_cleaned_data
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class EuropeanEnvironmentStudies():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = get_cleaned_data()
        self.years = sorted(set(self.df.Time.values))
        self.pays = list(self.df.Pays.unique())
        self.main_layout = html.Div(children=[
            html.H3(children='Politique environnementale et émission de gaz à effet de serre'),

            html.Div('Les graphiques suivant ont pour objectif de montrer l\'évolution des émissions de gaz à effet de serre selon les politiques \
                environnementales menées en Europe depuis 1995.'),

            html.Div('La comparaison se base notamment sur les pourcentages respectifs du PIB de chaque pays européen utilisé pour l\'environnement et sur leurs \
                    recettes fiscales, soit l\'argent récolté par les différentes taxes environnementales. \
                    La quantité de gaz à effet de serre est exprimée en Tonnes par Habitant ou avec l\'indice I90, qui a pour base 100=1990.'),

            html.Br(),

            dcc.Markdown("""
            Pour le graphique ci-dessous :
            - Les axes X et Y représentent la politique environnementale, avec respectivement le pourcentage du PIB utilisé et le pourcentage des taxes environnementales.
            - La taille des bulles et leur couleur représentent la quantité d'émission de gaz à effet de serre, l'unité est modifiable dans la légende. 
            """),
            html.Br(),
            html.H5(id='wps-graph-title'),
            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques des informations du pays en bas.'), 
            html.Div([
                    html.Div([ dcc.Graph(id='wps-main-graph-our'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Pays'),
                        html.Div([
                        dcc.Checklist(
                            id='wps-crossfilter-which-pays',
                            options=[{'label': self.pays[i], 'value': self.pays[i]} for i in range(len(self.pays))],
                            value=sorted(self.pays),
                            labelStyle={'display':'block'},
                        )], style={'maxHeight':'300px', 'overflow':'scroll','width':'10em'}),
                        html.Br(),
                        html.Div('Unité'),
                        dcc.RadioItems(
                            id='wps-crossfilter-unit-type',
                            options=[{'label': i, 'value': i} for i in ['T_HAB', 'I90']],
                            value='T_HAB',
                            labelStyle={'display':'block'},
                        ),
                        
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            self.START,
                            id='wps-button-start-stop-our', 
                            style={'display':'inline-block'}
                        ),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='wps-crossfilter-year-slider-our',
                            min=self.years[0],
                            max=self.years[-1],
                            step = 1,
                            value=self.years[0],
                            marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='wps-auto-stepper-our',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            
            html.Br(),
            html.Div("Les différents graphiques ci-dessous nous permettent de mieux comprendre l'évolution des données en prenant un pays en particulier."),
            html.Div("On voit donc l'évolution des émissions de gaz à effet de serre, le poucentage du PIB investi et le pourcentage des taxes environnementales."),

            html.Br(),
            html.H5(id='wps-div-country-our'),

            html.Div([
                dcc.Graph(id='wps-income-time-series-our', 
                          style={'width':'33%', 'display':'inline-block'}),
                dcc.Graph(id='wps-fertility-time-series-our',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='wps-pop-time-series-our',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            
            html.Br(),
            dcc.Markdown("""
            #### Analyse
            Notre hypothèse de départ était d'observer une corrélation franche entre les investissement 
            et les émissions de gaz à effet de serre d'un pays.  
            A partir de 2009, nous observons légèrement cette corrélation sur le graphique, avec des pays
            polluant moins et dépensant plus en haut à droite du graphique, et des pays polluant plus et
            dépensant moins en bas à gauche.
            Cependant, cette observation reste peu concluante, car certains pays dépensent peu et polluent peu.  
            On peut penser que d'autres facteurs rentrent en jeu, notamment la population d'un pays,
            la croissance de la demande énergétique, le type de production énergétique...
            
            #### À propos
            ##### Sources
            * [Dépenses nationales pour la protection de l’environnement](https://ec.europa.eu/eurostat/databrowser/view/ten00135/default/table?lang=fr)
            * [Émissions de gaz à effet de serre par secteur source (source: AEE)](https://ec.europa.eu/eurostat/databrowser/view/sdg_13_10/default/table?lang=fr)
            ##### Auteurs
            * (c) 2022 Alexandre Lemonnier & Victor Simonin
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

        # I link callbacks here since @app decorator does not work inside a clasaphiques ci-dessous nous permettent de mieux comprendre l'évolution des données en prenant un pays en particulier."),
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('wps-main-graph-our', 'figure'),
            [ dash.dependencies.Input('wps-crossfilter-which-pays', 'value'),
              dash.dependencies.Input('wps-crossfilter-unit-type', 'value'),
              dash.dependencies.Input('wps-crossfilter-year-slider-our', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('wps-div-country-our', 'children'),
            dash.dependencies.Input('wps-main-graph-our', 'hoverData'))(self.timeseries_title)
        self.app.callback(
            dash.dependencies.Output('wps-graph-title', 'children'),
            dash.dependencies.Input('wps-crossfilter-year-slider-our', 'value'))(self.graph_title)
        self.app.callback(
            dash.dependencies.Output('wps-button-start-stop-our', 'children'),
            dash.dependencies.Input('wps-button-start-stop-our', 'n_clicks'),
            dash.dependencies.State('wps-button-start-stop-our', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('wps-auto-stepper-our', 'max_interval'),
            [dash.dependencies.Input('wps-button-start-stop-our', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('wps-crossfilter-year-slider-our', 'value'),
            dash.dependencies.Input('wps-auto-stepper-our', 'n_intervals'),
            [dash.dependencies.State('wps-crossfilter-year-slider-our', 'value'),
             dash.dependencies.State('wps-button-start-stop-our', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('wps-income-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-unit-type', 'value')])(self.update_income_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-fertility-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData')])(self.update_fertility_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-pop-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData')])(self.update_pop_timeseries)

    def update_graph(self, pays, unit_type, year):
        dfg = self.df[self.df.Time == year]
        dfg = dfg[dfg['Pays'].isin(pays)]
        fig = px.scatter(dfg, x = "PIB", y = "TAXES", 
                         #title = f"{year}", cliponaxis=False,
                         size = unit_type, size_max=40, 
                         color = unit_type, 
                         hover_name="Pays")
        fig.update_layout(
                 xaxis = dict(title='Pourcentage du PIB utilisé pour l\'environnement',
                              type= 'linear',
                              range=(0,6)  
                             ),
                 yaxis = dict(title="Pourcentage des taxes pour l'environnement", range=(0,17)),
                 margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                 hovermode='closest',
                 showlegend=False,
             )
        return fig

    def create_time_series(self, country, what, y_label):
        return {
            'data': [go.Scatter(
                x = self.years,
                y = self.df[self.df["Pays"] == country][what],
                mode = 'lines+markers',
            )],
            'layout': {
                'height': 260,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title':y_label,
                          'type': 'linear'},
                'xaxis': {'showgrid': False}
            }
        }


    def get_country(self, hoverData):
        if hoverData == None:  # init value
            return self.df['Pays'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def timeseries_title(self, hoverData):
        return f"Evolution des données informatives pour le pays suivant : {self.get_country(hoverData)}"
    
    def graph_title(self, slider_value):
         return f"Évolution des émissions de gaz à effet de serre et politiques environnementales en Europe en {slider_value}"

    # graph incomes vs years
    def update_income_timeseries(self, hoverData, unit_type):
        country = self.get_country(hoverData)
        if unit_type == "T_HAB":
            return self.create_time_series(country, 'T_HAB','Tonnes par habitants')
        return self.create_time_series(country, "I90", "Indice 1990 = 100")

    # graph children vs years
    def update_fertility_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'PIB', "PIB investi (en %)")

    # graph population vs years
    def update_pop_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'TAXES', 'Taxes environnementale (en %)')

       # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
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

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = EuropeanEnvironmentStudies()
    ws.run(port=8055)

