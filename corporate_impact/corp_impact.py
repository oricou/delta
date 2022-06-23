from statistics import median
import sys
from unicodedata import name
import dash
import flask
import time
from dash import dcc
from dash import html
from matplotlib.pyplot import title
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import plotly
import geopandas
import json

class CorporateImpact():

    def __init__(self, application = None):

        impacts = pd.read_csv("data/final_raw_sample_0_percent.csv", sep=",", encoding="utf-8").dropna()
        impacts['Country'] = impacts['Country'].replace(['Czech Republic'], 'Czechia')
        impacts['Country'] = impacts['Country'].replace(['United States'], 'United States of America')
        impacts[impacts.columns[4]] = np.float64(impacts[impacts.columns[4]].map(lambda x: str(x)[:-1]))
        impacts[impacts.columns[5]] = np.float64(impacts[impacts.columns[5]].map(lambda x: str(x)[:-1]))

        self.impacts = impacts


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
        means = cur_df.groupby(['Year', 'Country'])[[cur_df.columns[4], cur_df.columns[5]]].mean()
        medians = cur_df.groupby(['Year', 'Country'])[[cur_df.columns[4], cur_df.columns[5]]].median()
        medians.columns = ["Median " + medians.columns[0],"Median " + medians.columns[1]]
        means.columns = ["Mean " + means.columns[0],"Mean " + means.columns[1]]

        self.means_medians_df = pd.merge(means, medians, left_index=True, right_index=True, how='outer')

        self.means_medians_df = self.means_medians_df.reset_index()

        self.means_medians_loc_df = pd.merge(self.means_medians_df, self.world, on='Country', how='outer')


        self.years = self.impacts['Year'].dropna().unique()

        self.means_medians_loc_df = self.means_medians_loc_df.dropna()

        self.fig_gdp = px.choropleth_mapbox(self.means_medians_loc_df,
                    geojson=self.countries,#world.set_index('Country').geometry,
                    locations=self.means_medians_loc_df.Country,
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

            html.H5('Map of the environmental intensity (can take some time to load!)'), 

            html.Div([
                    html.Div([ dcc.Graph(id='CR-corpimpact-main-map'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Reference'),
                        dcc.RadioItems(
                            id='CR-corpimpact-which-data',
                            options=[{'label':'Revenue', 'value':'Revenue'}, 
                                    {'label':'Operating Income','value':'Operating Income'}],
                            value='Revenue',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Calculation'),
                        dcc.RadioItems(
                            id='CR-corpimpact-which-calculation',
                            options=[{'label':'Mean', 'value':'Mean'}, 
                                    {'label':'Median','value':'Median'}],
                            value='Median',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Year'),
                        dcc.Dropdown(
                               id='CR-corpimpact-which-year',
                               options=[{'label': cur_year, 'value': cur_year} for cur_year in self.years],
                               value=2018,
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
            html.H5('Map of the GDP per capita of the different countries in the world'), 

            html.Div([ dcc.Graph(id='CR-corpimpact-gdp-map', figure=self.fig_gdp), ], style={'width':'90%', }),
            
            html.H3(children='Statistics on the monetized impact of the companies on the environment.'),
            html.H5(children='Histogram'),
            html.Div([ dcc.Graph(id='CR-corpimpact-stat-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Reference'),
                           dcc.Checklist(
                               id='CR-corpimpact-stat-ref-type',
                               options=[{'label':'Revenue', 'value':'Revenue'}, 
                                        {'label':'Operating Income','value':'Operating Income'}],
                               value=['Revenue', 'Operating Income'],
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div([ html.Div('Year'),
                           dcc.Dropdown(
                               id='CR-corpimpact-stat-which-year',
                               options=[{'label': cur_year, 'value': cur_year} for cur_year in impacts['Year'].unique()] + [{'label': 'None', 'value': 'None'}],
                               value='None',
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                html.Div([ html.Div('Country'),
                           dcc.Dropdown(
                               id='CR-corpimpact-stat-which-country',
                               options=[{'label': cur_country, 'value': cur_country} for cur_country in impacts['Country'].unique()] + [{'label': 'None', 'value': 'None'}],
                               value='None',
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Scale on y'),
                           dcc.RadioItems(
                               id='CR-corpimpact-stat-yaxis-type',
                               options=[{'label': i, 'value': i} for i in ['Linear', 'Logarithmic']],
                               value='Linear',
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

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
            dash.dependencies.Output('CR-corpimpact-main-map', 'figure'),
            [ dash.dependencies.Input('CR-corpimpact-which-data', 'value'),
              dash.dependencies.Input('CR-corpimpact-which-calculation', 'value'),
              dash.dependencies.Input('CR-corpimpact-which-year', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('CR-corpimpact-stat-graph', 'figure'),
            [ dash.dependencies.Input('CR-corpimpact-stat-ref-type', 'value'),
                dash.dependencies.Input('CR-corpimpact-stat-which-year', 'value'),
                dash.dependencies.Input('CR-corpimpact-stat-which-country', 'value'),
                dash.dependencies.Input('CR-corpimpact-stat-yaxis-type', 'value')])(self.update_graph_stats)

   
    def update_graph(self, ref, calcul, year):
        cur_col = f'{calcul} Total Environmental Intensity ({ref})'

        tmp = self.means_medians_loc_df.loc[self.means_medians_loc_df['Year'] == np.float(year)]

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

        fig_choro.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
        )   

        return fig_choro

    def update_graph_stats(self, ref, year, country, yaxis_type):
        df = self.impacts.copy(True)
        if (year != 'None'):
            df = df.loc[df.Year == year]
        if (country != 'None'):
            df = df.loc[df.Country == country]

        fig = go.Figure()
        for col in ref:
            fig.add_trace(go.Histogram(x=df[f'Total Environmental Intensity ({col})'], nbinsx=100,
                        name=f"Amount of entries ({col})"))
        
        if (yaxis_type == 'Logarithmic'):
            fig.update_yaxes(type="log")
        return fig


    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = CorporateImpact()
    ws.run(port=8055)
