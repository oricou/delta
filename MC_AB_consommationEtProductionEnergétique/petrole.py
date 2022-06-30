import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
import plotly.express as px
import json
import math

from MC_AB_consommationEtProductionEnergétique.get_data import get_data
from MC_AB_consommationEtProductionEnergétique.get_data import get_by_year
from MC_AB_consommationEtProductionEnergétique.get_data import list_years
from MC_AB_consommationEtProductionEnergétique.get_data import list_countries
from MC_AB_consommationEtProductionEnergétique.get_data import country_code


class Petrole():
    def __init__(self, application=None):

        self.prod, self.cons, self.export, self.impor = get_data()
   
        self.years = list_years(self.impor)

        self.partners = [item for item in self.impor["partner"].unique() if item == item]
        self.countries = [item for item in self.impor["geo"].unique() if item == item]

        with open("MC_AB_consommationEtProductionEnergétique/data/europe.geo.json", "r", encoding="utf-8") as f: # https://geojson-maps.ash.ms/
            self.europe = json.load(f)

        for i in self.europe["features"]:
            fips = i["properties"]["iso_a2"]
            i["id"] = fips
        
        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""
            # Independance Européene face au Pétrole comme énergie fossile
            
            Ici nous pouvons voir les statistiques entre 1990 et 2020 sur les exportations, importations, consommations et productions de prétrole en Europe.
            Les Importations peuvent venir de pays hors Europe.
            
            Plus bas, il est possible de voir une carte qui montre l'excedent, positif ou négatif, de pétrole pour chaque pays d'Europe chaque année.
            Un excedent négatif signifie que le pays tourne sur ses réserves, positif qu'il stock des barils.
            
            Enfin, il est possible de simuler à une certaine année un pays qui met fin à ses exportations de pétrole, et donc de voir si il passe dans le vert, et si il fait passer des autres dans le rouge.
            
            Il est possible de s'aider des dernier graphes montrant qui sont les gros importateurs de pétrole en Europe, et pour chaque pays, d'où vient son approvisionnement."""),
            html.Div([ html.Div('Année ref.'),
                          dcc.Slider(0, len(self.years) -1, 1,
                               id='pet-year',
                               marks={i: str(self.years[i]) for i in range(len(self.years))},
                               value=len(self.years) // 2
                           ),
                           html.Div('Selectionner les pays dont on souhaite stopper les exportations'),
                           dcc.Dropdown(
                               id='pet-excluded-countries',
                               options=[{"label":country_code[i], "value": i} for i in self.partners],
                               value=[],
                               multi=True
                           ),
                           html.P('L\' unité de "OBS_VALUE" est en milliers de tonnes de pétrole par an.'),
                         ], style={'position': 'sticky', 'top': 0, 'zIndex': 1, 'backgroundColor': 'white', 'width': '100%', 'padding':'4em 0px 0px 0px'}), # bas D haut G
            html.Div([
                html.Div([
                    html.H2('Differentes cartes informatives sur le pétrole en Europe:'),
                    dcc.RadioItems(id='pet-graph-choose',
                            options=['Importations', 'Exportations', 'Consommations', 'Productions'],
                            value='Importations',
                            inline=True,
                            labelStyle={'font-size': '2em'} ),
                    html.Div([ dcc.Graph(id='pet-graph'), ], style={'width': '100em' })])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.H2('Excedent de pétrole par pays, calculé par :'),
                    html.H4('Exc = production + importation - exportation - consommation '),
                    html.P('Ici nous pouvons voir la balance totale de pétrole de chaque pays européen à une certaine année.'),
                    html.P('Si un pays est dans le rouge, il perd plus de pétrole qu\'il a et donc tourne sur ses réserves.'),
                    html.Div([ dcc.Graph(id='pet-rel-graph'), ], style={'width': '100em' })])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.H2('Les 10 plus gros exportateurs de pétrole:'),
                    html.Div([ dcc.Graph(id='pet-big-import-graph'), ], style={'width': '100em' })])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                    html.H2('Selectionner le pays dont on souhaite voir d\'où viennent les importations'),
                        dcc.Dropdown(
                            id='pet-specific-importation-of-country',
                            options=[{"label":country_code[i], "value": i} for i in self.countries],
                            value='FR'
                           ),
                    html.Div([ dcc.Graph(id='pet-specific-import-graph'), ], style={'width': '100em' })
            ], style={})
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
                    dash.dependencies.Output('pet-graph', 'figure'),
                    [dash.dependencies.Input('pet-year', 'value'),
                    dash.dependencies.Input('pet-excluded-countries', 'value'),
                    dash.dependencies.Input('pet-graph-choose', 'value')])(self.update_graph_pet)
        self.app.callback(
                    dash.dependencies.Output('pet-rel-graph', 'figure'),
                    [dash.dependencies.Input('pet-year', 'value'),
                    dash.dependencies.Input('pet-excluded-countries', 'value')])(self.update_graph_reliability)
        self.app.callback(
                    dash.dependencies.Output('pet-big-import-graph', 'figure'),
                    [dash.dependencies.Input('pet-year', 'value'),
                    dash.dependencies.Input('pet-excluded-countries', 'value')])(self.update_biggest_importators)
        self.app.callback(
                    dash.dependencies.Output('pet-specific-import-graph', 'figure'),
                    [dash.dependencies.Input('pet-year', 'value'),
                    dash.dependencies.Input('pet-excluded-countries', 'value'),
                    dash.dependencies.Input('pet-specific-importation-of-country', 'value')])(self.update_importators)
    

    def update_graph_import(self, year):
        year = self.years[year]
        df = self.impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()

        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_export(self, year, excluded_countries):
        year = self.years[year]
        df = self.export[~self.export.geo.isin(excluded_countries)]
        df = df[self.export.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_cons(self, year):
        year = self.years[year]
        df = self.cons[self.cons.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig
    
    def update_graph_prod(self, year):
        year = self.years[year]
        df = self.prod[self.prod.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_pet(self, year, excluded_countries, graph_choose):
        if graph_choose == "Importations":
            return self.update_graph_import(year)
        if graph_choose == "Exportations":
            return self.update_graph_export(year, excluded_countries)
        if graph_choose == "Consommations":
            return self.update_graph_cons(year)

        return self.update_graph_prod(year)

    def update_graph_reliability(self, year, excluded_countries):
        year = self.years[year]
        #cons = self.cons[~self.cons.geo.isin(excluded_countries)]
        cons = self.cons[self.cons.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        #prod = self.prod[~self.prod.geo.isin(excluded_countries)]
        prod = self.prod[self.prod.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        #export = self.export[~self.export.geo.isin(excluded_countries)]
        export = self.export[self.export.TIME_PERIOD == year]
        export.loc[export.geo.isin(excluded_countries), "OBS_VALUE"] = 0
        export = export.groupby("geo")["OBS_VALUE"].sum()

        #impor = self.impor[~self.impor.geo.isin(excluded_countries)]
        impor = self.impor[~self.impor.partner.isin(excluded_countries)]
        impor = impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        df = prod + impor - export - cons
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="RdYlGn",
                                range_color=(-1, 1),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_biggest_importators(self, year, excluded_countries):
        year = self.years[year]
        df = self.impor[~self.impor.partner.isin(excluded_countries)]
        df = df[df.TIME_PERIOD == year].groupby("partner")["OBS_VALUE"].sum()
        df = df.reset_index()
        df = df[df.OBS_VALUE != 0]
        df.sort_values(by=['OBS_VALUE'], inplace=True,
        ascending=False)
        df = df.nlargest(n = 10, columns = ['OBS_VALUE'])

        df['partner'] = df['partner'].apply(lambda x: country_code[x])
        fig = px.bar(df, x="partner", y="OBS_VALUE")

        return fig

    def update_importators(self, year, excluded_countries, country):
        year = self.years[year]
        df = self.impor[~self.impor.partner.isin(excluded_countries)]
        df = df[df.TIME_PERIOD == year][df.geo == country].groupby("partner")["OBS_VALUE"].sum()
        df = df.reset_index()
        df = df[df.OBS_VALUE != 0]
        df.sort_values(by=['OBS_VALUE'], inplace=True, ascending=False)
        df = df.nlargest(n = 10, columns = ['OBS_VALUE'])
        df['partner'] = df['partner'].apply(lambda x: country_code[x])
        fig = px.bar(df, x="partner", y="OBS_VALUE")

        return fig

    



if __name__ == '__main__':
    ind = Petrole()
    ind.app.run_server(debug=True, port=8051)
