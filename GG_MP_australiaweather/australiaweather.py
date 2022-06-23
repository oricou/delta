import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import os


class australiaWeather():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        os.getcwd()
        df = pd.read_csv('GG_MP_australiaweather/data/stations_mesures.csv', sep=' ', names=['ID', 'lat','long','info','from','to'])
        df = df.drop(columns=['lat','long','info'])
        df = df.groupby('ID', as_index =False).agg({'from' : 'min', 'to' : 'max'})#.sort_values(by=['from','to'], ascending=True)
        
        self.stations_mesures = df
        
        self.number = len(df.index) - 150

        self.data_inv = pd.read_pickle('GG_MP_australiaweather/data/data_inventory.pkl')
        
        self.data_colors = {'PRCP':'darkblue', 'DAPR':'red', 'DWPR':'green', 'MDPR':'brown', 'TMAX':'navy', 'TMIN':'crimson', 'DATX':'magenta', 'MDTX':'cyan', 'DATN':'purple', 'MDTN':'gray', 'TAVG':'coral'}
        self.data = {'PRCP':'Precipitation', 'DAPR':'DAPR', 'DWPR':'DWPR', 'MDPR':'MDPR', 'TMAX':'Temperature maximum', 'TMIN':'Temperature minimum', 'DATX':'DATX', 'MDTX':'MDTX', 'DATN':'DATN', 'MDTN':'MDTN', 'TAVG':'Temperature moyenne'}

        self.mesures_by_stations = pd.read_pickle('GG_MP_australiaweather/data/mesures_by_stations.csv')
        self.price = pd.read_pickle('GG_MP_australiaweather/data/prices.pkl')
        self.geo_json='GG_MP_australiaweather/data/geo_datas/states.geojson'
        self.years = self.mesures_by_stations["date"].unique()
        self.y_start = self.years.min()
        self.y_end = self.years[:-2]
        
        self.main_layout = html.Div(children=[
            html.H3(children='Précipitations et marchés de l\'eau en australie'),

            html.Div([
                    html.Div([ dcc.Graph(id='sls-main-graph'), ], style={'width':'90%', }),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),
            html.Div([
                html.Div([
                    html.Button(
                            self.START,
                            id='sls-button-start-stop', 
                            style={'display':'inline-block'}
                        ),
                    html.Br(),
                    dcc.Slider(
                            id='sls-crossfilter-number-slider',
                            min=0,
                            max=self.number,
                            step = 150,
                            value= (self.number + self.number % 2) / 2,
                            marks={str(number): str(number) for number in range(0, self.number, 1000)},
                    ),
                    html.Div('Déplacez la souris pour choisir le numéro de la station. Celà affichera également les 150 suivantes'),
                ],style={'display':'inline-block', 'width':"90%"}),
                dcc.Interval(            # fire a callback periodically
                    id='sls-auto-stepper',
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
            
Depuis 2008, le gouvernement australien a décidé d'ouvrir le marché de l'eau en transformant ce bien en produit financier.
Nous avons décidé de nous interesser aux interaction entre ce marché et les précipitation.
En effet, l'australie étant un immense pays, le prix de l'eau et les précipitation varient beaucoup selon la localisation. 
Pour commencer, nous avons due determiner la fesabilité de cette étude : les donnés nessécaires etaient-elles disponibles ? Il se trouve que depuis toujours le stress hydrique est présent en australie ce qui à rendu les études météorologiques indispensable.  Les stations sont nombreuses cependant leur durée d'activité varie fortement. 
Le graphique suivant nous montre la durée de vie des différentes stations.

            """),
           html.Br(),
           html.Div([
                    html.Div([ dcc.Graph(id='sws-main-graph'), ], style={'width':'80%', }),

                    html.Div([
                        html.Div('Type de donnée'),
                        dcc.Checklist(
                            id='sws-crossfilter-which-data',
                            options=[{'label': self.data[i], 'value': i} for i in sorted(self.data_colors.keys())],
                            value=sorted(self.data_colors.keys()),
                        )
                    ], style={'margin-left':'15px', 'width': '12em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
        
            html.Br(),
            dcc.Markdown("""
                * DAPR = Number of days included in the multiday precipiation 
                * DWPR = Number of days with non-zero precipitation included in multiday precipitation total (MDPR)
                * MDPR = Multiday precipitation total
                * DATX = Number of days included in the multiday maximum temperature
                * MDTX = Multiday maximum temperature
                * DATN = Number of days included in the multiday minimum temperature
                * MDTN = Multiday minimum temperature
                
Comme constaté précédement, le nombre de station est élevé. Cependant chacune n'effectue pas les mêmes mesures. Nous avons voulu vérifier que la mesure qui nous interesse (les précipitations) était assez représenté.
Nous disposons donc de nombreuses mesures pour étudier les précipitations et les phénomènes météorologiques. Le nombre de stations ainsi que leurs activités sont montrés dans les graphiques suivants.
            """),
           html.Br(),
            html.Div('Dans la carte suivante, chaque point représente une station de mesure, sa couleur représente le total de précipitation enregistré durant le mois.'), 
            html.Div([dcc.Graph(figure=self.plotEvolutionMap()),], style={'width':'90%', }),
            html.Div([dcc.Graph(figure=self.plotPrices()),], style={'width':'100%', }),

            html.Br(),
            
            html.Br(),
            dcc.Markdown("""
On peut constater sur ces cartes que les disparités sont grandes : il pleut beaucoup au sud ouest et au nord est de ce pays. On peut constater que dans les zones peu pluvieuses le prix du ML d'eau est beacoup plus élevé. Ces cartes montrent donc que les précipitations garantissent un prix de l'eau bas. On peut cependant remettre en question la corrélation entre ces 2 cartes, en effet beaucoup d'autre éléments entrent en jeu dans ces variation. Ainsi, ce n'est pas forcement parce que les précipitations sont faibles que le prix de l'eau est élevé.
Pour cette étude nous avons utilisé les bases de donnés suivantes :
https://www1.ncdc.noaa.gov/ (National Climatic Data Center - USA) qui recense toutes les mesures de stations météorologiques à travers de monde. 
http://www.bom.gov.au/ (Bureau of meteorologie - AUS) qui recense beaucoup de donnés liés aux problématiques climatique en australie. 

(c) 2022 Martin Poulard
(c) 2022 Grégoire Gally
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

        self.app.callback(
            dash.dependencies.Output('sls-main-graph', 'figure'),
            [ dash.dependencies.Input('sls-crossfilter-number-slider', 'value')])(self.dash_plotStationLifeSpan)
        self.app.callback(
            dash.dependencies.Output('sls-button-start-stop', 'children'),
            dash.dependencies.Input('sls-button-start-stop', 'n_clicks'),
            dash.dependencies.State('sls-button-start-stop', 'children'))(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output('sls-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('sls-button-start-stop', 'children')])(self.run_movie)
        self.app.callback(
            dash.dependencies.Output('sls-crossfilter-number-slider', 'value'),
            dash.dependencies.Input('sls-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('sls-crossfilter-number-slider', 'value'),
             dash.dependencies.State('sls-button-start-stop', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('sws-main-graph', 'figure'),
            [ dash.dependencies.Input('sws-crossfilter-which-data', 'value')])(self.update_graph)
        

    def dash_plotStationLifeSpan(self, num_stations):
        df = self.stations_mesures
        if (num_stations + 150 >= len(df.index)):
            num_stations = 0
        df_plot = df.copy() if num_stations == None else df[num_stations:num_stations + 149].copy()
        df_plot['timespan'] = df['to']-df['from']
        df_plot = df_plot.sort_values(by='timespan', ascending=True)
        fig = px.bar(df_plot, x='ID', y='timespan', base = 'from',  barmode = 'group',
                     labels = {'ID':'Stations','timespan':'Years of existence'}, title = "Stations' lifespans",
                     range_x=(0,df_plot.shape[0]),opacity=1) 
        fig.update_traces(marker_color='green')
        fig.update_xaxes(ticktext=[], tickvals=[])
        fig.update_layout(yaxis_range=[min(df_plot['from'])*0.99, max(df_plot['to']*1.01)])
        fig.update_xaxes(constrain='range')
        fig.update_traces(hovertemplate ='<b>ID</b>: %{x}'+'<br>from : %{base}'+'<br>to : %{y}')

        return fig

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
    def on_interval(self, n_intervals, number, text):
        if text == self.STOP:  # then we are running
            if number + 150 >= self.number:
                return 0
            else:
                return number + 150
        else:
            return number  # nothing changes

    def update_graph(self, datatype):
        column = ['year', 'number']
        column = column + datatype
        dfg = self.data_inv[column]
        fig = px.bar(dfg, x = 'year', y = dfg.columns[2:], title = "Number of measure depending the year")
        
        return fig

    def plotPrices(self):
        '''
        Plots the territories' water price evoluting by month
        '''

        fig = (px.choropleth(self.price,
                    geojson=self.geo_json,
                    locations=self.price['dest_state'],
                    featureidkey="properties.STATE_NAME",
                    color="price_per_ML",
                    animation_frame='date_of_approval',
                    projection="mercator",
                    range_color=[0,500]))

        fig.update_geos(fitbounds="locations", visible=True)
        return fig

    def plotEvolutionMap(self):
        '''
        Plots the map of all the stations and their precipitation evoluting by month
        '''
        fig = (px.scatter_mapbox(self.mesures_by_stations, lat='lat', lon='long',
        hover_name="ID",
        animation_group="ID",
        animation_frame="date",
        color='value',
        range_color = [0,6000],
        zoom=3, height=500))
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    
    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)
    
        
if __name__ == '__main__':
    ws = WorldStats()
    ws.run(port=8055)