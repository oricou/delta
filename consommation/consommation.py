import dash
import flask
from dash import dcc
from dash import html
import dateutil as du
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from .get_data_consommation import load_df


class Consommation():
    def __init__(self, application = None):


        self.df  = load_df()

        self.continent_colors = {'SEAR':'gold', 'EUR':'green', 'AFR':'brown', 'WPR':'red', 
                                 'AMR':'navy', 'EMR':'purple'}

        self.french = {'SEAR':'Asie du Sud-Est', 'EUR':'Europe', 'AFR':'Afrique', 'WPR':'Pacifique Occidentale',
                       'AMR':'Amériques', 'EMR':'Méditérranée Orientale'}

        self.sex = {'BTSX': 'Les deux sexes', 'FMLE': 'Femmes', 'MLE': 'Hommes'}

        self.main_layout = html.Div(children=[
            html.H3(children='Consommation d\'alcool dans les pays selon le PIB'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 


            html.Div([
                    html.Div([ dcc.Graph(id='con-main-graph'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Régions'),
                        dcc.Checklist(
                            id='con-crossfilter-which-region',
                            options=[{'label': self.french[i], 'value': i} for i in sorted(self.continent_colors.keys())],
                            value=sorted(self.continent_colors.keys()),
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Sexe'),
                        dcc.RadioItems(
                            id='con-crossfilter-sex',
                            options=[{'label': self.sex[i], 'value': i} for i in self.sex.keys()],
                            value='BTSX',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        html.Div('Échelle en X'),
                        dcc.RadioItems(
                            id='con-crossfilter-xaxis-type',
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
                    'padding': '0px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),     

            html.Br(),

            html.Div(id='con-div-country'),
            html.Div([
                dcc.Graph(id='con-income-time-series', 
                          style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='con-consumption-barcharts',
                          style={'width':'50%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Br(),
            dcc.Markdown("""
            Chaque point du graphique représente un pays. Vous pouvez passer votre souris sur un point afin d'avoir plus d'informations sur un pays.

            Notes :
            * On remarque globalement une corrélation entre la richesse et la consommation d'alcool mais il existe surtout une homogénéité au sein des régions.
            * En effet, certains pays du Moyen-Orient comme l'Arabie Saoudite ou les Emirats Arabes Unis sont particulièrement riches mais leur population consomme très peu d'alcool probablement pour des raisons religieuses.
            * Les pays les plus fervents d'alcool sont les pays européens, pays qui sont aussi les plus riches et les plus stables tandis que les pays africains dépassent rarement les 50% de la population consommant de l'alcool.
            * Les hommes consomment plus d'alcool que les femmes partout.
            * Enfin, certains pays ont des données à prendre avec des pincettes comme le Vietnam qui semble afficher un pourcentage surréaliste.
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
            dash.dependencies.Output('con-main-graph', 'figure'),
            [ dash.dependencies.Input('con-crossfilter-which-region', 'value'),
              dash.dependencies.Input('con-crossfilter-sex', 'value'),
              dash.dependencies.Input('con-crossfilter-xaxis-type', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('con-div-country', 'children'),
            dash.dependencies.Input('con-main-graph', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('con-income-time-series', 'figure'),
            [dash.dependencies.Input('con-main-graph', 'hoverData'),
             dash.dependencies.Input('con-crossfilter-xaxis-type', 'value')])(self.update_income_timeseries)
        self.app.callback(
            dash.dependencies.Output('con-consumption-barcharts', 'figure'),
            [dash.dependencies.Input('con-main-graph', 'hoverData')])(self.update_consumption_barcharts)


    def update_graph(self, regions, sex, xaxis_type):
        # Keeping only the regions selected in the checkbox
        dfg = self.df[self.df['region'].isin(regions)]

        # Keeping rows with selected sex
        dfg = dfg[dfg.sexe == sex]

        # Keeping the most recent year
        dfg = dfg.drop_duplicates(subset=['pays'], keep='last')

        fig = px.scatter(dfg, x = "pib", y = "pourcentage",
                         color = "region", color_discrete_map = self.continent_colors,
                         hover_name="pays", log_x=True)
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
        fig.update_traces(marker=dict(size = 0 if len(regions) == 0 else (10 if len(regions) > 3 else 20) ,
                                    line=dict(width=2, color='DarkSlateGrey')))
        return fig

    def get_country(self, hoverData):
        if hoverData == None:  # init value
            return self.df['pays'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    # graph pib vs years
    def update_income_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        dfg = self.df.loc[self.df['pays'] == country]
        fig = px.line(dfg, x = dfg['annee'], y = dfg['pib'], markers=True)
        fig.update_layout(
                height= 225,
                margin= {'l': 50, 'b': 20, 'r': 10, 't': 50},
                yaxis= {'title':'PIB par personne (US $)',
                          'type': 'linear' if xaxis_type == 'Linéaire' else 'log'},
                xaxis= dict(showgrid= False,
                            title= None),
        )
        return fig

    # bar charts
    def update_consumption_barcharts(self, hoverData):
        country = self.get_country(hoverData)
        dfg = self.df.loc[self.df['pays'] == country]
        dfg = dfg.drop_duplicates(subset=['sexe'], keep='last')
        dfg = dfg.sort_values(by = ['sexe'])
        dfg = dfg.replace({'BTSX': 'Les deux sexes', 'FMLE': 'Femmes', 'MLE': 'Hommes'})
        fig = px.bar(dfg, x="sexe", y="pourcentage", color="sexe")
        fig.update_layout(
                height = 225,
                margin={'l': 50, 'b': 20, 'r': 10, 't': 50},
                yaxis={'title':'Consommateurs d\'alcool (en %)'},
                xaxis=dict(showgrid= False,
                           title= None),
                showlegend=False,
        )
        fig.update_traces(width=0.5)
        return fig

        
if __name__ == '__main__':
    con = Consommation()
    con.app.run_server(debug=True, port=8051)
