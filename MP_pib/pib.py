import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class Pib():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = pd.read_csv('data/internet.csv')
        self.df.set_index('Time', inplace=True)
        self.df.drop(columns=['Time Code'], inplace=True)
        self.df['internet'] = pd.to_numeric(self.df['internet'],errors='coerce')
        self.df['pib'] = pd.to_numeric(self.df['pib'],errors='coerce')
        self.df['population'] = pd.to_numeric(self.df['population'],errors='coerce')

        self.years = sorted(set(self.df.index.values))

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution de l\'accès à Internet vs le PIB par habitant par pays'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 

            html.Div([
                    html.Div([ dcc.Graph(id='pib-main-graph'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Continents'),
                        dcc.Dropdown(self.df['Country Name'].unique(), ['France'],id="pib-choose-country", multi=True),
                        html.Br(),
                        html.Div('Échelle en X'),
                        dcc.RadioItems(
                            id='pib-crossfilter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                            value='Log',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            self.START,
                            id='pib-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                    html.Div([ dcc.Graph(id='pib-map-graph'), ], style={'width':'90%', }),

                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            

            html.Div([
                html.Div(
                    dcc.Slider(
                            id='pib-crossfilter-year-slider',
                            min=self.years[0],
                            max=self.years[-1],
                            step = 1,
                            value=self.years[0],
                            marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='pib-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Br(),
            html.Div(id='pib-div-country'),

            html.Div([
                dcc.Graph(id='pib-income-time-series', 
                          style={'width':'33%', 'display':'inline-block'}),
                dcc.Graph(id='pib-internet-time-series',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='pop-time-series',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Br(),
            dcc.Markdown("""

            Vous pouvez observer sur ce graphique la corrélation entre l'usage d'Internet dans un pays et le PIB par habitant.
            
            Il est aussi possible d'observer la progression du PIB par habitant pour le pays que vous sélectionnez. L'évolution de
            cette donnée est un bon indicateur du développement du pays. C'est un moyen fiable de savoir si le pays suit un essor fort
            ou non.

            Par exemple, on constate que des pays comme le Brésil subissent une forte diminution de leur PIB par habitant au cours des
            dernières années. Néanmoins, le pourcentage d'individus utilisant Internet dans le pays suit une forte progression. On peut
            imaginer que le coût des télécommunications et de l'accès à Internet a baissé ce qui n'a pas impacté le développement de ces
            technologies dans ce pays.

            Une carte du monde est aussi disponible pour observer plus facilement l'accès à Internet dans certains pays.

            #### Sources

            * Données : [Banque mondiale](https://databank.worldbank.org/Internet-Usage---GDP---Population/id/3e53c41e)
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
            dash.dependencies.Output('pib-main-graph', 'figure'),
            [ dash.dependencies.Input('pib-choose-country', 'value'),
              dash.dependencies.Input('pib-crossfilter-xaxis-type', 'value'),
              dash.dependencies.Input('pib-crossfilter-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('pib-map-graph', 'figure'),
            [ dash.dependencies.Input('pib-choose-country', 'value'),
              dash.dependencies.Input('pib-crossfilter-year-slider', 'value')])(self.update_map_graph)
        self.app.callback(
            dash.dependencies.Output('pib-div-country', 'children'),
            dash.dependencies.Input('pib-main-graph', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('pib-button-start-stop', 'children'),
            dash.dependencies.Input('pib-button-start-stop', 'n_clicks'),
            dash.dependencies.State('pib-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('pib-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('pib-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('pib-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('pib-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('pib-crossfilter-year-slider', 'value'),
             dash.dependencies.State('pib-button-start-stop', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('pib-income-time-series', 'figure'),
            [dash.dependencies.Input('pib-main-graph', 'hoverData'),
             dash.dependencies.Input('pib-crossfilter-xaxis-type', 'value')])(self.update_income_timeseries)
        self.app.callback(
            dash.dependencies.Output('pib-internet-time-series', 'figure'),
            [dash.dependencies.Input('pib-main-graph', 'hoverData'),
             dash.dependencies.Input('pib-crossfilter-xaxis-type', 'value')])(self.update_internet_timeseries)
        self.app.callback(
            dash.dependencies.Output('pop-time-series', 'figure'),
            [dash.dependencies.Input('pib-main-graph', 'hoverData'),
             dash.dependencies.Input('pib-crossfilter-xaxis-type', 'value')])(self.update_pop_timeseries)


    def update_graph(self, country, xaxis_type, year):
        dfg = self.df.loc[year]

        if country == None:
            country = ['France']

        dfg = dfg[dfg['Country Name'].isin(country)]

        fig = px.scatter(dfg, x = "pib", y = "internet",
                         #title = f"{year}", cliponaxis=False,
                         size = "population", size_max=60,
                         hover_name="Country Name", log_x=True)
        fig.update_layout(
                 xaxis = dict(title='PIB par habitant (en $ US de 2020)',
                              type= 'linear' if xaxis_type == 'Linéaire' else 'log',
                              range=(0,200000) if xaxis_type == 'Linéaire' 
                                              else (np.log10(50), np.log10(200000)) 
                             ),
                 yaxis = dict(title="Pourcentage de personnes ayant accès à Internet", range=(0,100)),
                 margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                 hovermode='closest',
                 showlegend=False,
             )
        return fig

    def update_map_graph(self, country, year):
        dfg = self.df.loc[year]

        if country == None:
            country = ['France']

        dfg = dfg[dfg['Country Name'].isin(country)]

        figure = px.scatter_geo(dfg, locations="Country Code",
                     hover_name="Country Name", size="internet",
                     projection="natural earth")

        return figure

    def create_time_series(self, country, what, axis_type, title):
        return {
            'data': [go.Scatter(
                x = self.years,
                y = self.df[self.df["Country Name"] == country][what],
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
        if hoverData == None:  # init value
            return "France"
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    def update_income_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'pib', xaxis_type, 'PIB par personne (US $)')

    def update_internet_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'internet', xaxis_type, "Pourcentage de personnes ayant accès à Internet par pays")

    def update_pop_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'population', xaxis_type, 'Population')

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
    pinter = Pib()
    pinter.run(port=8055)
