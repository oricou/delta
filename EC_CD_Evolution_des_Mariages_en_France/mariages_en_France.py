import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import json
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from scipy import stats
from scipy import fft

class Mariage():
    # State for the button
    START = 'Start'
    STOP  = 'Stop'
    
    def __init__(self, application = None):
        def convert(i):
            return int(i)
        
        
        # List of month name to update the histogram to display month name and not their number
        self.L = ['janv', 'fev', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'sept', 'oct','nov','dec']    
        self.dep = '01'
        
        # Data loading and variable declarations
        self.table = pd.read_csv('EC_CD_Evolution_des_Mariages_en_France/data/mariage_pour_tous.csv').drop(columns=['Unnamed: 0'])
        self.histo_1946 = pd.read_csv('EC_CD_Evolution_des_Mariages_en_France/data/mariage_depuis_1946.csv').drop(columns=['Unnamed: 0'])
        
        # Copy the data before modification to use them to create the graph (line)
        self.df = self.histo_1946.copy()

        self.histo_1946 = self.histo_1946.drop(self.histo_1946.iloc[:,1:9], axis=1)
        
        # Selection of the data for the year 1946 (histogram)
        line = self.histo_1946.iloc[[0]]
        
        self.year = 1946
        
        # Initialisation of the different figures used on the html page
        self.map_f = pd.read_csv('EC_CD_Evolution_des_Mariages_en_France/data/mariage_par_departement.csv').drop(columns=['Unnamed: 0'])
                
        self.departements = json.load(open('EC_CD_Evolution_des_Mariages_en_France/data/departements-version-simplifiee.geojson'))
        
        self.fig = px.line(self.df, x='AMAR', y=['Homme_Homme', 'Femme_Femme', 'Homme_Femme', 'Pacs de personnes de sexe différent', 'Pacs de personnes de même sexe', 'Ensemble des Pacs', 'Total mariage'])

        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations=self.map_f.DEPARTEMENT,
                           hover_name = self.map_f.NOM,
                           featureidkey = 'properties.code', 
                           color='2014', range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        self.fig_histo = px.histogram(line, x='AMAR', y=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
                                                         'Septembre', 'Octobre', 'Novembre', 'Décembre'], barmode='group')
        self.fig.update_layout(
            title = 'Mariages et Pacs en France depuis 1946',
            xaxis = dict(title = 'Année de l\'Union'),
            yaxis = dict(title = 'Nombre d\'Union'), 
            legend = dict(title = 'Type d\'Union')
        )
        self.fig_histo.update_layout(
            title = 'Mariages en %s' % (self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = ''), 
            legend = dict(title = 'Nombre de mariages') 
        )
         
        # Initialisation of the html page
        self.main_layout = html.Div(children=[
            html.H3(children='Mariages en France'),
            html.Div([
                dcc.Graph(
                    id='mdf-map-graph',
                    figure=self.fig_map,
                    style={'width':'40%', }),
                dcc.Graph(
                    id='mdf-main-graph',
                    figure=self.fig,
                    style={'width':'60%', 'display':'inline-block'}),
                ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Div([
                    dcc.Slider(id='mdf-crossfilter-year-slider',
                        min=1946,
                        max=2020,
                        step=1,
                        value=1946,
                        marks={str(year): str(year) for year in range(1945, 2021, 5)},),
                    dcc.Interval(
                        id='mdf-auto-stepper',
                        interval=1000,
                        max_intervals = -1,
                        n_intervals = 0
                        ),
                        ], style={
                            'padding': '0px 50px', 
                            'width':'90%'
                        }),
            html.Button(
                self.START,
                id='mdf-button-start-stop', 
                style={'display':'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='mdf-histo-graph',
                    figure=self.fig_histo
                    , style={'width':'100%', })
                    ]),
                        html.Br(),
            dcc.Markdown(
                """
                La carte devient interactive à partir de 2014. En cliquant sur un département, l'histogramme affichera les données sur le département sélectionné. 
                Notes :
                       * 1945 : Fin de la IIe guerre mondiale (explosion de mariages)
                       * 15 novembre 1999 : Création des PACS
                       * 17 mai 2013 : Mariage pour tous
                       * HH : Mariage Homme-Homme
                       * FF : Mariage Femme-Femme
                       * HF : Mariage Homme-Femme
            #### À propos
            * Sources : https://www.insee.fr/fr/statistiques
            * (c) 2022 Elodine Coquelet & Calliopee Desenfans
            """)
            ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        # Callback to update the map and histogram
        self.app.callback(
            dash.dependencies.Output('mdf-map-graph', 'figure'),
            dash.dependencies.Output('mdf-histo-graph', 'figure'),
            dash.dependencies.Input('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('mdf-map-graph', 'clickData'))(self.update_graph)
        # Change the status of the button (START or STOP)
        self.app.callback(
            dash.dependencies.Output('mdf-button-start-stop', 'children'),
            dash.dependencies.Input('mdf-button-start-stop', 'n_clicks'),
            dash.dependencies.State('mdf-button-start-stop', 'children'))(self.change_button)
        # Update automatically the slider when the animation is not stop
        self.app.callback(
            dash.dependencies.Output('mdf-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('mdf-button-start-stop', 'children')])(self.run_movie)
        # Update the variables depending on the value of the slider. Triggered by the previous callback
        self.app.callback(
            dash.dependencies.Output('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('mdf-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.State('mdf-button-start-stop', 'children')])(self.on_interval)

    # Update the map and make it visible in 2014 (opacity=opa)    
    def update_map(self):
        opa = 0 if self.year < 2014 else 0.5
        year = self.year if self.year > 2013 else 2014
        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations= self.map_f.DEPARTEMENT,
                           hover_name = self.map_f.NOM,
                           featureidkey = 'properties.code', 
                           color=str(year), range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=opa,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    # Update the histogram depending of the year
    def update_histo(self):
        # Display a histogram of the number of mariage by month during the year
        if self.year < 2014:
            line = self.histo_1946.iloc[[self.year - 1946]]
            self.fig_histo = px.histogram(line, x='AMAR', y=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
                                                             'Septembre', 'Octobre', 'Novembre', 'Décembre'], barmode='group')
            self.fig_histo.update_layout(
                title = 'Mariages en %s' % (self.year),
                xaxis = dict(title = ''),
                yaxis = dict(title = 'Nombre de mariages'), 
                legend = dict(title = 'Mois de mariage') 
            )
            return
        
        # Display the number of mariages and their type (HH, FF ou HF) by month for a department during the year
        df = self.table[self.table['AMAR'] == self.year]
        df = df[df['DEPMAR'] == self.dep]
        
        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph = pd.DataFrame(HH.groupby('MMAR').size(), columns = ['HH'])
        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph = graph.assign(FF = FF.groupby('MMAR').size())
        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph = graph.assign(HF = HF.groupby('MMAR').size())
        
        graph = graph.reset_index()
        graph = self.check_months(graph)
        graph = graph.sort_values(by=['MMAR'])
        graph['MMAR'] =  graph['MMAR'].apply(self.update_month)
        # Eliminate all NaN of the Table
        graph = graph.fillna(0)
        
        self.fig_histo = px.histogram(graph, x = 'MMAR', y = ['HH', 'FF', 'HF'], barmode='group')
        
        self.fig_histo.update_layout(
            title = 'Mariage et divorce %s en %s' % (self.dep_name(), self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage') 
        )
    
    # Trigger the update of the map and the histogram
    def update_graph(self, year, clickData):
        ctx = dash.callback_context
        button_id =""
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
        # Check if the user moved the slider  
        if button_id == 'mdf-crossfilter-year-slider':
            self.year = year
            self.update_map()
        # Check if the user click on the map to select a department
        if button_id == 'mdf-map-graph':
            self.dep = str(clickData['points'][0]['location'])
        self.update_histo()
        
        return self.fig_map, self.fig_histo
    
    def str_update(self, s):
        if s == 'FM':
            return 'MF'
        return s
        
    # Replace the months numbers by their name
    def update_month(self, s):
        return self.L[int(s) - 1]
    
    # Add to the data the month without any mariages
    def check_months(self, graph):
        col = graph['MMAR'].unique()
        idx = len(col)
    
        for i in range(1, 13):
            if i < 10:
                s = "0" + str(i)
            else:
                s = str(i)
            if i not in col :
                # The value '0.0001' allows the month to appear on the histogram
                graph.loc[idx] = (int(s), 0,0, 0.0001)
                idx += 1
        return graph
    
    # Return the name of the department based on its number
    def dep_name(self):
            return self.map_f[self.map_f['DEPARTEMENT'] == self.dep].iloc[0,7]
    
    # Update the state of the button
    def change_button(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START
    
    # Launch and stop the animation
    def run_movie(self, text):
        if text == self.START:
            return 0 
        else:
            return -1
    
    # Update the variable to create the animation
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:
            if self.year < 2014:
                self.year += 1
                return self.year
            if self.dep == '19':
                self.dep = '2A'
            elif self.dep == '2A':
                self.dep = '2B'
            elif self.dep == '2B':
                self.dep = '21'
            elif self.dep == '95':
                self.dep = '01'
                if year == 2020:
                    self.year = 1946
                else:
                    self.year += 1
            else:
                tmp = int(self.dep) + 1
                self.dep = str(tmp) if tmp > 9 else "0" + str(tmp)
                
        return self.year 

if __name__ == '__main__':
    mdf = Mariage()
    mdf.app.run_server(debug=True, port=8051)
