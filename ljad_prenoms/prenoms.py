import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

from get_data import * 

class Prenoms():
    xls = pd.ExcelFile('data/irsoceds2013_T102.xls')

    def __init__(self, application=None):
        self.dpt = ["0" + str(i) for i in range(10)] + [str(i) for i in range(10,96)] + ["971", "972", "973", "974"]

        self.prenoms = get_prenoms()
        self.population = get_populations()
        self.departements = get_france_geojson()
        self.chomage = get_chomage()
        
        self.secteurs = {
            secteur : pd.read_excel(Prenoms.xls, secteur).iloc[1,0].split('-')[1]
            if len(secteur) > 6
            else pd.read_excel(Prenoms.xls, secteur).iloc[1,0][7:]
            for secteur in Prenoms.xls.sheet_names
        }
        self.secteurs_t = {key: val for key, val in self.secteurs.items() if key.startswith('T ')}
        self.secteurs_h = {key: val for key, val in self.secteurs.items() if key.startswith('TH')}
        self.secteurs_f = {key: val for key, val in self.secteurs.items() if key.startswith('TF')}

        self.sect_dict = {
            0: self.secteurs_t,
            1: self.secteurs_h,
            2: self.secteurs_f,
        }
        self.sect_default_value = {
            0: 'T - T',
            1: 'TH - T',
            2: 'TF - T',
        }

        self.years = np.arange(1994, 2013)
        
        self.main_layout = html.Div(children=[
            html.H3(children='Informations prénoms - emplois / départements'),
            html.Div([
                         html.Div([ dcc.Graph(id='map'), ],
                                  style={'height':'100%','width':'58%', 'display': 'inline-block'}),
                         html.Div([ dcc.Graph(id='graph'), ],
                                  style={'height': '100%','width':'32%', 'display': 'inline-block'}),
                     ],style={
                         'backgroundColor': 'gray',
                         # 'display': 'flex', 'justify-content': 'space-between',
                         'height': '60em','width': '100%',
                     }),
            html.Div([
                html.Div([ html.Div('Type de cartes'),
                           dcc.RadioItems(
                               id='map-type',
                               options=[{'label':'Prénoms', 'value':0}, 
                                        {'label':'Chomage','value':1},
                                        {'label':'Emploi','value':2}],
                               value=0,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div([ dcc.Input(
                                 id='name',
                                 type='text',
                                 placeholder='',
                                 debounce=True,
                                 value='GUILLAUME'
                             ), ], style={'width':'9em', }),
                html.Div([ html.Div('Annee ref.'),
                           dcc.Dropdown(
                               id='year',
                               options=[{'label': i, 'value': i} for i in self.years],
                               value=2000,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Sheet'),
                           dcc.Dropdown(
                               id='secteurs',
                               options=[{'label': secteurs, 'value': sheet}
                                     for sheet, secteurs in self.secteurs_t.items()],
                               value='T - T', # première feuille, 'Tous secteurs'
                           ),
                         ], style={'width': '25em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                html.Div([ html.Div('Sexe'),
                           dcc.RadioItems(
                               id='sexe',
                               options=[{'label':'Tous', 'value':0}, 
                                        {'label':'Homme','value':1},
                                        {'label':'Femme','value':2}],
                               value=0,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
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


        self.app.callback(
                [dash.dependencies.Output('map', 'figure'),
                dash.dependencies.Output('graph', 'figure'),],
                [dash.dependencies.Input('map-type', 'value'),
                dash.dependencies.Input('name', 'value'),
                dash.dependencies.Input('year', 'value'),
                dash.dependencies.Input('secteurs', 'value'),
            ])(self.update_graph)

        self.app.callback(
            [dash.dependencies.Output('secteurs', 'options'),
             dash.dependencies.Output('secteurs', 'value')],
            [dash.dependencies.Input('sexe', 'value')]
        )(self.update_secteurs)

        # self.app.callback(
        #         dash.dependencies.Output('graph', 'figure'),
        #         [dash.dependencies.Input('name', 'value')
        #         ,])(self.plot_name_occurence_france)
        
    def update_secteurs(self, sexe):
        options = [{'label': secteurs, 'value': sheet}
                for sheet, secteurs in self.sect_dict[sexe].items()]
        value = self.sect_default_value[sexe]
        return options, value

    def update_occ_name_year(self, name, year):
        if name == None or year == None:
            return
        df = get_occ_name_year(self.prenoms, name, year).set_index("dpt").reindex(self.dpt, fill_value=0).reset_index()
        fig = px.choropleth_mapbox(df, geojson=self.departements, locations='dpt', color='nombre',
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, max(1, df.nombre.max())),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'departement', 'nombre':'occurence'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def plot_name_occurence_france(self, name):
        occurences = self.prenoms[self.prenoms.preusuel == name].drop(columns='sexe')
        occurences = occurences.groupby('annais').sum().reset_index()
        fig = px.line(occurences, y='nombre', x='annais',
                      markers=True,
                      labels={"nombre":f"occurences des {name}", "annais": "années"})
        return fig

    def plot_name_occurence_departement(self, name, departement):
        occurences = self.prenoms[self.prenoms.preusuel == name].drop(columns='sexe')
        fig = px.scatter(occurences[occurences.dpt == departement], y='nombre', x='annais', labels={"nombre":f"occurences des {name}", "annais": "années"})
        return fig
    
    def update_chomage_year(self, year):
        fig = px.choropleth_mapbox(self.chomage, geojson=self.departements, locations='dpt', color=year,
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, 16),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'departement', year:'chomage'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
    
    def plot_emploi_sheet_year(self, sheet, year):
        df = read_sheet(Prenoms.xls, sheet).loc[:,['dpt', year]]
        fig = px.choropleth_mapbox(df, geojson=self.departements, locations='dpt', color=year,
                               featureidkey='properties.code',
                               color_continuous_scale="Amp",
                               range_color=(0, max(1, df[year].max())),
                               mapbox_style="carto-positron",
                               zoom=5, center = {"lat": 47, "lon": 2},
                               opacity=0.5,
                               labels={'dpt':'departement', year:'emploi'}
                              )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    def update_graph(self, map_type, name, year, sheet):
        name = name.lower()
        if map_type == 0:
            return self.update_occ_name_year(name, year), self.plot_name_occurence_france(name)
        elif map_type == 1:
            return self.update_chomage_year(year), self.plot_name_occurence_france(name)
        else:
            return self.plot_emploi_sheet_year(sheet, year), self.plot_name_occurence_france(name)

if __name__ == '__main__':
    nrg = Prenoms()
    nrg.app.run_server(debug=True, port=8051)
