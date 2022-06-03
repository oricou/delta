# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
from .data.get_data import *
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Stats():
    
    def __init__(self, application=None):
            
        self.energies = energies
        self.gazes = gazes
        
        self.ratio_fig = px.line(ratio_polution_energie.T)
        self.ratio_fig.update_layout(title = "Ratio de l'émission de gaz par rapport à l'électricité produite",
                      xaxis = dict( title = "Année"),
                      yaxis = dict( title = "GWh électricité pour 1000 tonnes de gaz à effet de serre"))
        
        self.layout = html.Div(children=[
            
            html.H2(children="Taux d'émission de gaz à effet de serres, en fonction de la production et du type d'électricité, en Europe"),
    
            dcc.Markdown("Sélectionner le type de production électrique :"),
            
            html.Div([
                dcc.Dropdown(list(energies.keys()),
                             value='Total', id='dropdown-which-energy', clearable=False)
            ], style={'display': 'inline-block', 'width': '25%', 'border': '2px green solid'}),         
            
            html.Div([dcc.Graph(id='energy_production')]),
            
            html.Div([
                dcc.Dropdown(list(camembert['2000'].index),
                            value='France', id='dropdown-which-country', clearable=False),
                
                dcc.Dropdown(list(camembert.keys()),
                             value='2000', id='dropdown-which-year', clearable=False)
            ], style={'width': '25%', 'border': '2px green solid'}),              
            
            html.Div([dcc.Graph(id='energy_pie')]),
            
            dcc.Markdown("Sélectionner le secteur d'émission de gaz à effet de serre :"),
            
            html.Div([
                dcc.Dropdown(list(gazes.keys()),
                             value='Total', id='dropdown-which-sector', clearable=False)
            ], style={'display': 'inline-block', 'width': '25%', 'border': '2px green solid'}),
            
            html.Div([dcc.Graph(id='gaz_emission')]),
            
            html.Div([dcc.Graph(figure=self.ratio_fig)]),
            
            html.H2(children="À propos"),
            dcc.Markdown("Sources :"),
            dcc.Link('Emission de gaz à effet de serre par secteur en Europe', href='https://ec.europa.eu/eurostat/databrowser/view/ENV_AIR_GGE__custom_2662782/default/table?lang=fr'),
            html.Br(),
            dcc.Link("Production brute d'électricité par type d'énergie en Europe", href='https://ec.europa.eu/eurostat/databrowser/view/NRG_IND_PEH__custom_2403953/default/table?lang=fr'),
            
            html.H5(children="(c) Maxime Brouillard, Romain Brand")
        ])
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.layout        
        
        
        self.app.callback(
            dash.dependencies.Output('energy_production', 'figure'),
            [ dash.dependencies.Input('dropdown-which-energy', 'value')])(self.update_graph_energy)  
        
        self.app.callback(
            dash.dependencies.Output('gaz_emission', 'figure'),
            [ dash.dependencies.Input('dropdown-which-sector', 'value')])(self.update_graph_gaz)
        
        self.app.callback(
            dash.dependencies.Output('energy_pie', 'figure'),
            [ dash.dependencies.Input('dropdown-which-country', 'value'),
              dash.dependencies.Input('dropdown-which-year', 'value')])(self.update_pie_energy)
        
    def update_graph_energy(self, energy):
        
        fig = px.line(self.energies[energy].T)
        fig.update_layout(title = "Production d'électricité en Europe",
                          xaxis = dict( title = "Année"),
                          yaxis = dict( title = "Energie éléctrique en GWh"))
        return fig
    
    def update_graph_gaz(self, sector):
        
        fig = px.line(self.gazes[sector].T)
        fig.update_layout(title = "Taux d'émission de gaz à effet de serre en Europe",
                          xaxis = dict( title = "Année"),
                          yaxis = dict( title = "Emission de gaz à effet de serre en Mille tonne"))
        return fig
    
    def update_pie_energy(self, country, year):
        
        traces = [go.Pie(textposition="inside",
                 labels = camembert[year].loc[country].drop('Total').index,
                 values = camembert[year].loc[country].drop('Total'))]

        fig = go.Figure(data = traces)
        
        return fig
        
    def run(self, debug=True, port=8051):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port) # 0.0.0.0 is needed for Docker

if __name__ == '__main__':
    ws = Stats()
    ws.run()
