import sys
import dash
import flask
import json
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import folium

class HautDebit():
    START = 'Start'
    STOP  = 'Stop'

    ## geojson source : https://github.com/gregoiredavid/france-geojson
    def init_region(self):
        self.data_region = pd.read_excel(self.file,
                                    sheet_name='Régions',
                                    header=4,
                                    usecols="B,F:W")
        self.geo_region = json.load(open('data/regions-version-simplifiee.geojson'))
    def init_departement(self):
        self.data_departement = pd.read_excel(self.file,
                                    sheet_name='Départements',
                                    header=4,
                                    usecols="B,G:X")
        self.geo_departement = json.load(open('data/departements-version-simplifiee.geojson'))

    # def init_commune(self):
    #     self.data_commune = pd.read_excel(self.file,
    #                                 sheet_name='Communes',
    #                                 header=4,
    #                                 usecols="B,K,R:AH")
        

    def __init__(self, application = None):
        self.data_region, self.geo_region = None, None
        self.data_departement, self.geo_departement = None, None
        # self.data_commune = None
        
        self.file = 'https://www.data.gouv.fr/fr/datasets/r/d538685a-b9cb-4a3e-b90d-ad6f0a13920b'

        self.init_region()
        self.init_departement()
        # self.init_commune()

        self.year = self.data_region.columns[2:]

        self.main_layout = html.Div(children=[
            html.H3(children='Acces au haut débit en France'),

            html.Div([
                    html.Div([ dcc.Graph(id='debit-main-map'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Échelle géographique'),
                        dcc.RadioItems(
                            id='debit-crossfilter-scale-type',
                            options=[{'label': i, 'value': i} for i in ['Rég.', 'Dép.']], # , 'Commune']],
                            value='Rég.',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Div('Type'),
                        dcc.RadioItems(
                            id='debit-crossfilter-type-type',
                            options=[{'label': i, 'value': i} for i in ['Taux', 'Brute']],
                            value='Taux',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            self.START,
                            id='debit-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                    ], style={'margin-left':'20px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='debit-crossfilter-year-slider',
                            min=0,
                            max=len(self.year) - 1,
                            step = 1,
                            value=0,
                            marks={i: self.year[i] for i in range(len(self.year))},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='debit-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les régions/départements, vous avez une infobulle. 
            
            Sources : https://www.data.gouv.fr/fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements/
            """)


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

        # # I link callbacks here since @app decorator does not work inside a class
        # # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('debit-main-map', 'figure'),
            [ dash.dependencies.Input('debit-crossfilter-scale-type', 'value'),
              dash.dependencies.Input('debit-crossfilter-type-type', 'value'),
              dash.dependencies.Input('debit-crossfilter-year-slider', 'value')])(self.update_map)
        self.app.callback(
            dash.dependencies.Output('debit-button-start-stop', 'children'),
            dash.dependencies.Input('debit-button-start-stop', 'n_clicks'),
            dash.dependencies.State('debit-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('debit-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('debit-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('debit-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('debit-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('debit-crossfilter-year-slider', 'value'),
             dash.dependencies.State('debit-button-start-stop', 'children')])(self.on_interval)

    def update_map(self, scale, type, year):
        def get_good_date(scale):
            if scale == 'Rég.':
                return self.data_region.copy(), self.geo_region, 'Nom région'
            elif scale == 'Dép.':
                return self.data_departement.copy(), self.geo_departement, 'Nom département'
            # else:
            #     return self.data_commune.copy(), json.load(open('data/communes-version-simplifiee.geojson')), 'Nom commune'

        data, goejson, keyDF = get_good_date(scale)
        data = pd.DataFrame(data)

        if type == 'Taux' :
            data[data.columns[2:]] = data[data.columns[2:]].div(data[data.columns[1]], axis=0)
            range_col = (0, 1)
        else:
            range_col = (0, data[data.columns[2:]].max().max())


        fig = px.choropleth_mapbox(data, geojson=goejson, 
                           locations=keyDF, featureidkey = 'properties.nom',
                           color=self.year[year], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.2, center = {"lat": 47, "lon": 2},
                           range_color=range_col,
                           opacity=0.5,
                           labels={self.year[year]: type})
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig

    def get_country(self, hoverData):
        if hoverData == None:  # init value
            return self.df['Country Name'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

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
            if year >= len(self.year) - 1:
                return 0
            else:
                return year + 1
        else:
            return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = HautDebit()
    ws.run(port=8055)
