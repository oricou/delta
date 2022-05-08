from statistics import median
import sys
from unicodedata import name
import dash
import flask
from dash import dcc
from dash import html
from matplotlib.pyplot import title
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import geopandas
import json

class MapStats():

    def __init__(self, application = None):
        impacts = pd.read_csv("data/final_raw_sample_0_percent.csv", sep=",", encoding="utf-8").dropna()
        impacts['Country'] = impacts['Country'].replace(['Czech Republic'], 'Czechia')
        impacts['Country'] = impacts['Country'].replace(['United States'], 'United States of America')
        impacts[impacts.columns[4]] = np.float64(impacts[impacts.columns[4]].map(lambda x: str(x)[:-1]))
        impacts[impacts.columns[5]] = np.float64(impacts[impacts.columns[5]].map(lambda x: str(x)[:-1]))

        self.impacts = impacts

        self.world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
        self.world.columns=['pop_est', 'continent', 'Country', 'code', 'gdp_md_est', 'geometry']
        self.world['gdp_per_cap'] = self.world['gdp_md_est'] * 1000000 / self.world['pop_est']

        with open("data/countries.json") as f:
            self.countries = json.load(f)

        # Calculate means and medians values
        cur_df = impacts.copy(True)
        means = cur_df.groupby(['Year', 'Country'])[cur_df.columns[4], cur_df.columns[5]].mean()
        medians = cur_df.groupby(['Year', 'Country'])[cur_df.columns[4], cur_df.columns[5]].median()
        medians.columns = ["Median " + medians.columns[0],"Median " + medians.columns[1]]
        means.columns = ["Mean " + means.columns[0],"Mean " + means.columns[1]]

        self.means_medians_df = pd.merge(means, medians, left_index=True, right_index=True, how='outer')

        self.means_medians_df = self.means_medians_df.reset_index()

        self.means_medians_loc_df = pd.merge(self.means_medians_df, self.world, on='Country', how='outer')


        self.years = self.impacts['Year'].unique()

        tmp = self.means_medians_loc_df.copy(True).dropna()

        self.fig_gdp = px.choropleth_mapbox(tmp,
                    geojson=self.countries,#world.set_index('Country').geometry,
                    locations=tmp.Country,
                    color="gdp_per_cap",#np.log10(abs(tmp[tmp.columns[4]])),
                    color_continuous_scale='greens',
                    #projection="mercator",
                    mapbox_style="carto-positron",
                    zoom=0.3,
                    labels={'gdp_per_capita' : 'GDP per capita'})

        colorbar=dict(
                  title=f'GDP per capita', 
                  )
        self.fig_gdp.update_layout(
            coloraxis_colorbar=colorbar#dict(title='Count', tickprefix='1.e')    
        )

        self.main_layout = html.Div(children=[
            html.H3(children='Maps about the environmental costs of the companies'),

            html.H5('Map of the environmental intensity'), 

            html.Div([
                    html.Div([ dcc.Graph(id='maps-main-map'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Reference'),
                        dcc.RadioItems(
                            id='maps-which-data',
                            options=[{'label':'Revenue', 'value':'Revenue'}, 
                                    {'label':'Operating Income','value':'Operating Income'}],
                            value='Revenue',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Calculation'),
                        dcc.RadioItems(
                            id='maps-which-calculation',
                            options=[{'label':'Mean', 'value':'Mean'}, 
                                    {'label':'Median','value':'Median'}],
                            value='Median',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Year'),
                        dcc.Dropdown(
                               id='maps-which-year',
                               options=[{'label': cur_year, 'value': cur_year} for cur_year in self.years],
                               value='2018',
                        ),
                        html.Br(),
                        html.Br(),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Br(),

            html.Div([ dcc.Graph(id='maps-gdp-map', figure=self.fig_gdp), ], style={'width':'90%', }),
            
            html.Br(),
            dcc.Markdown("""
            #### Glossary
            - Revenu: All revenues from sales of the companies, equivalent to turnover.
            - Operating Income: All revenues with all operating costs substracted, equivalent to benefits.

            #### About

            * Source : [Dataset on kaggle](https://www.kaggle.com/datasets/mannmann2/corporate-environmental-impact?select=final_raw_sample_0_percent.csv)
            * [Article](https://www.hbs.edu/impact-weighted-accounts/Documents/corporate-environmental-impact.pdf)
            * (c) 2022 Julien CROS & Nicolas ROMANO
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
            dash.dependencies.Output('maps-main-map', 'figure'),
            [ dash.dependencies.Input('maps-which-data', 'value'),
              dash.dependencies.Input('maps-which-calculation', 'value'),
              dash.dependencies.Input('maps-which-year', 'value')])(self.update_graph)

   
    def update_graph(self, ref, calcul, year):

        cur_col = f'{calcul} Total Environmental Intensity ({ref})'
        
        tmp = self.means_medians_loc_df.copy(True).dropna()
        tmp = tmp.loc[tmp['Year'] == np.float(year)]

        fig_choro = px.choropleth_mapbox(tmp,
                    geojson=self.countries,
                    locations=tmp.Country,
                    title=f'Map of the {calcul} Environmental Intensity on {ref}',
                    color=np.log10(abs(tmp[cur_col])),
                    hover_name=tmp[cur_col],
                    zoom=0.3,
                    color_continuous_scale="reds",
                    mapbox_style="carto-positron",
                    range_color=(min(np.log10(abs(tmp[cur_col]))), np.log10(abs(max(tmp[cur_col])))))

        colorbar=dict(len=0.75,
                  
                  title=f'Environment Intensity', 
                  x=0.9,
                  tickvals = [-2, -1, 0, 1, 2, 2.69],
                  ticktext = ['100','10','1', '-10', '-100', '-500']
                  )
        fig_choro.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=colorbar#dict(title='Count', tickprefix='1.e')    
        )
        return fig_choro

        


    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = MapStats()
    ws.run(port=8055)
