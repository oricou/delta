import pandas as pd
import dash
from dash import html
from dash import dcc

import plotly.express as px
import json

class Maps():
    def __init__(self, application=None):

        self.df = pd.read_pickle('data/naissances_par_dep_1970_2020.pkl')
        self.years = sorted(set(self.df.index.values))
        self.year = self.years[0]
        self.df_dict = {}

        self.departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        self.main_layout = html.Div(children=[
            html.H2(children='Cartes de France'),
            html.Br(),
            html.Div(children=[
                html.Div([dcc.Graph(id='map-selected-year'),], style={'width':'90%', }),
                html.Div(id='selected-year-slider', children=self.year),
                dcc.Slider(
                    id='map-year-slider',
                    min=self.years[0],
                    max=self.years[-1],
                    step=1,
                    value=self.years[0],
                    marks={str(year): str(year) for year in self.years[::5]},
                )
            ])
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 30px 10px 30px'
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


    def update_map(self, year):
        if year == None:
            year = self.year
        if not year in self.df_dict.keys():
            ydf = self.df.loc[self.df.index == year].reset_index(drop=True).stack()
            year_df = pd.DataFrame(ydf, columns=['naissances'])
            year_df = year_df.reset_index(1).reset_index(drop=True)
            year_df.rename(columns={'dpt':'DEP'}, inplace=True)
            self.df_dict.update({year: year_df})
        else:
            year_df = self.df_dict.get(year)

        fig = px.choropleth_mapbox(year_df, geojson=self.departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='naissances',
                                   hover_data=['naissances'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
