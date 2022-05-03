import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import dateutil as du
import plotly.express as px
import plotly.graph_objs as go
from scipy import stats
from scipy import fft

class Consommation():
    def __init__(self, application = None):


        alcohol_consumption = pd.read_csv('data/gho_alcohol_consumer_past_12months.csv')
        alcohol_consumption.dropna(how='all', axis=1, inplace=True)
        alcohol_consumption = alcohol_consumption.rename(columns = {"SpatialDimValueCode": "Code"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Location": "Country"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Value": "% of alcohol drinkers"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"Dim1ValueCode": "Sex"})
        alcohol_consumption = alcohol_consumption.rename(columns = {"ParentLocationCode": "Zone"})
        pib = pd.read_csv('data/gdp-per-capita-worldbank.csv')
        pib = pib.rename(columns = {"GDP per capita, PPP (constant 2017 international $)": "GDP"})
        del pib['Entity']
        pib = pib.sort_values(by = ['Year'])

        tmp = pd.merge(alcohol_consumption, pib, on = 'Code')
        tmp = tmp.sort_values(by = ['Year'])
        self.pib = tmp[['Country', 'GDP', 'Year']]


        pib = pib.drop_duplicates(subset=['Code'], keep='last')

        alcohol_consumption = alcohol_consumption.loc[alcohol_consumption["% of alcohol drinkers"] != '.']
        alcohol_consumption = alcohol_consumption.astype({"% of alcohol drinkers" : "float64"})

        self.df = pd.merge(alcohol_consumption, pib, on = 'Code')

        self.continent_colors = {'SEAR':'gold', 'EUR':'green', 'AFR':'brown', 'WPR':'red', 
                                 'AMR':'navy', 'EMR':'purple'}
        self.french = {'SEAR':'Asie du Sud-Est', 'EUR':'Europe', 'AFR':'Afrique', 'WPR':'Pacifique Occidentale', 'AMR':'Amériques', 'EMR':'Méditérranée Orientale'}
        self.sex = {'BTSX': 'Les deux sexes', 'FMLE': 'Femmes', 'MLE': 'Hommes'}

        self.main_layout = html.Div(children=[
            html.H3(children='Consommation d\'alcool dans les pays selon le PIB'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 


            html.Div([
                    html.Div([ dcc.Graph(id='wps-main-graph'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Régions'),
                        dcc.Checklist(
                            id='wps-crossfilter-which-continent',
                            options=[{'label': self.french[i], 'value': i} for i in sorted(self.continent_colors.keys())],
                            value=sorted(self.continent_colors.keys()),
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Sexe'),
                        dcc.RadioItems(
                            id='wps-crossfilter-sex',
                            options=[{'label': self.sex[i], 'value': i} for i in self.sex.keys()],
                            value='BTSX',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Échelle en X'),
                        dcc.RadioItems(
                            id='wps-crossfilter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                            value='Log',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ], style={'margin-left':'30px', 'width': '14em', 'float':'right'}),
                ], style={
                    'padding': '40px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),     

            html.Br(),

            html.Div(id='wps-div-country'),
            html.Div([
                dcc.Graph(id='wps-income-time-series', 
                          style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='wps-consumption-barcharts',
                          style={'width':'50%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Br(),
            dcc.Markdown("""
            #### À propos
            * Sources : [Observatoire mondial de la Santé](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-consumers-past-12-months-(-))
            * (c) 2022 Vincent Courty, Luca Moorghen
            """)

        ], style={
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
            dash.dependencies.Output('wps-main-graph', 'figure'),
            [ dash.dependencies.Input('wps-crossfilter-which-continent', 'value'),
              dash.dependencies.Input('wps-crossfilter-sex', 'value'),
              dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('wps-div-country', 'children'),
            dash.dependencies.Input('wps-main-graph', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('wps-income-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graph', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_income_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-consumption-barcharts', 'figure'),
            [dash.dependencies.Input('wps-main-graph', 'hoverData')])(self.update_consumption_barcharts)


    def update_graph(self, zones, sex, xaxis_type):
        dfg = self.df[self.df['Zone'].isin(zones)]
        dfg = dfg[dfg.Sex == sex]
        fig = px.scatter(dfg, x = "GDP", y = "% of alcohol drinkers",
                         color = "Zone", color_discrete_map = self.continent_colors,
                         hover_name="Country", log_x=True)
        fig.update_layout(
                 xaxis = dict(title='Revenus net par personnes (en $ US de 2020)',
                              type= 'linear' if xaxis_type == 'Linéaire' else 'log',
                              range=(0,100000) if xaxis_type == 'Linéaire' 
                                              else (np.log10(50), np.log10(100000)) 
                             ),
                 yaxis = dict(title="Consommateurs d'alcool (en %)"),
                 margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                 hovermode='closest',
                 showlegend=False,
        )
        fig.update_traces(marker=dict(size = 0 if len(zones) == 0 else (10 if len(zones) > 3 else 20) ,
                                    line=dict(width=2, color='DarkSlateGrey')))
        return fig

    def get_country(self, hoverData):
        if hoverData == None:  # init value
            return self.df['Country'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    # graph pib vs years
    def update_income_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        dfg = self.pib.loc[self.pib['Country'] == country]
        fig = px.line(dfg, x = dfg['Year'], y = dfg['GDP'], markers=True)
        fig.update_layout(
                height= 225,
                margin= {'l': 50, 'b': 20, 'r': 10, 't': 50},
                yaxis= {'title':'PIB par personne (US $)',
                          'type': 'linear' if xaxis_type == 'Linéaire' else 'log'},
                xaxis= dict(showgrid= False,
                            title= None),
        )
        return fig
        """
        return {
            'data': [go.Scatter(
                x = dfg['Year'],
                y = dfg['GDP'],
                mode = 'lines+markers',
            )],
            'layout': {
                'height': 225,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 50},
                'yaxis': {'title':'PIB par personne (US $)',
                          'type': 'linear' if xaxis_type == 'Linéaire' else 'log'},
                'xaxis': {'showgrid': False}
            }
        }
        """

    # bar charts
    def update_consumption_barcharts(self, hoverData):
        country = self.get_country(hoverData)
        dfg = self.df.loc[self.df['Country'] == country]
        dfg = dfg.sort_values(by = ['Sex'])
        dfg = dfg.replace({'BTSX': 'Les deux sexes', 'FMLE': 'Femmes', 'MLE': 'Hommes'})
        fig = px.bar(dfg, x="Sex", y="% of alcohol drinkers", color="Sex")
        fig.update_layout(
                height = 225,
                margin={'l': 50, 'b': 20, 'r': 10, 't': 50},
                yaxis={'title':'Consommateurs d\'alcool (en %)'},
                xaxis=dict(showgrid= False,
                           title= None),
                showlegend=False,
        )
        return fig

        
if __name__ == '__main__':
    con = Consommation()
    con.app.run_server(debug=True, port=8051)