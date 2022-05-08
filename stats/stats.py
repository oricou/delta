import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly
import dateutil as du

class Stats():

    def __init__(self, application = None):
        impacts = pd.read_csv("data/final_raw_sample_0_percent.csv", sep=",", encoding="utf-8").dropna()
        impacts['Country'] = impacts['Country'].replace(['Czech Republic'], 'Czechia')
        impacts['Country'] = impacts['Country'].replace(['United States'], 'United States of America')
        impacts[impacts.columns[4]] = np.float64(impacts[impacts.columns[4]].map(lambda x: str(x)[:-1]))
        impacts[impacts.columns[5]] = np.float64(impacts[impacts.columns[5]].map(lambda x: str(x)[:-1]))

        self.impacts = impacts

        self.main_layout = html.Div(children=[
            html.H3(children='Statistics on the monetized impact of the companies on the environment.'),
            html.H5(children='Histogram'),
            html.Div([ dcc.Graph(id='stats-main-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Reference'),
                           dcc.Checklist(
                               id='stats-ref-type',
                               options=[{'label':'Revenue', 'value':'Revenue'}, 
                                        {'label':'Operating Income','value':'Operating Income'}],
                               value=['Revenue', 'Operating Income'],
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                html.Div([ html.Div('Year'),
                           dcc.Dropdown(
                               id='stats-which-year',
                               options=[{'label': cur_year, 'value': cur_year} for cur_year in impacts['Year'].unique()] + [{'label': 'None', 'value': 'None'}],
                               value='None',
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                html.Div([ html.Div('Country'),
                           dcc.Dropdown(
                               id='stats-which-country',
                               options=[{'label': cur_country, 'value': cur_country} for cur_country in impacts['Country'].unique()] + [{'label': 'None', 'value': 'None'}],
                               value='None',
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Scale on y'),
                           dcc.RadioItems(
                               id='stats-yaxis-type',
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

        self.app.callback(
                    dash.dependencies.Output('stats-main-graph', 'figure'),
                    [ dash.dependencies.Input('stats-ref-type', 'value'),
                      dash.dependencies.Input('stats-which-year', 'value'),
                      dash.dependencies.Input('stats-which-country', 'value'),
                      dash.dependencies.Input('stats-yaxis-type', 'value')])(self.update_graph)
        '''self.app.callback(
                    [ dash.dependencies.Output('nrg-which-month', 'disabled'),
                      dash.dependencies.Output('nrg-which-year', 'disabled')],
                      dash.dependencies.Input('nrg-price-type', 'value') )(self.disable_month_year)'''

    def update_graph(self, ref, year, country, yaxis_type):
        df = self.impacts.copy(True)
        if (year != 'None'):
            df = df.loc[df.Year == year]
        if (country != 'None'):
            df = df.loc[df.Country == country]

        fig = plotly.subplots.make_subplots()
        print(ref)
        for col in ref:
            fig.add_trace(go.Histogram(x=df[f'Total Environmental Intensity ({col})'], nbinsx=100,
                        name=f"Amount of entries ({col})"))
        
        if (yaxis_type == 'Logarithmic'):
            fig.update_yaxes(type="log")
        return fig

        
if __name__ == '__main__':
    stats = Stats()
    stats.app.run_server(debug=True, port=8051)
