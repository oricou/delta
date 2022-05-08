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
import json

infl2 = pd.read_csv('movie_data_analysis/data/inflation.csv')
def us_convert(before, now, value):
	bef_cpi = infl2[infl2.year == before].cpi.values[0]
	now_cpi = infl2[infl2.year == now].cpi.values[0]
	perc = (now_cpi - bef_cpi) / bef_cpi * 100
	return value * (1 + perc / 100)


def convert_genres(s):
	l = json.loads(s.replace('\'', '"'))
	ret = []
	for d in l:
		ret.append(d['name'])
	return ret

class MovieProduction():

    def __init__(self, application = None):
        
        df = pd.read_csv('movie_data_analysis/evolution_production/data/production.csv')

        # Convert genres dicts into lists
        df.genres = df.genres.apply(convert_genres)
        
        # Remove lines where budget is missing
        df = df[~(df.budget == 0)]
        
        # Drop years to filter out
        df = df[~(df.release_year.astype(int) > 2015)]

        # Expand the genres lists
        df = df.explode('genres')

        # Reorganise
        df.set_index('release_year', inplace=True)
        df.sort_index(inplace=True)
        # Sum or mean
        df = df.groupby(['genres', 'release_year']).agg({'budget':'sum'})

        # Save genres and years for later
        self.genres = df.reset_index().genres.unique()
        self.years = df.reset_index().release_year.unique()

        # Build the actual dataframe for budgets
        self.bdg_sums = pd.DataFrame(index=self.genres, columns=[self.years])
        # Now each genre is a column
        self.bdg_sums = self.bdg_sums.T

        # Fill the dataframe with the bugdets
        for index in df.index:
            cat, year = index
            # print(cat, year)
            # print(inputs_by_genres.loc[index])
            self.bdg_sums.at[year, cat] = df.loc[index]

        # Reorganise index
        self.bdg_sums.index = pd.Index([i[0] for i in self.bdg_sums.index.to_flat_index()])
        # Fill missing values
        # self.bdg_sums = self.bdg_sums.fillna(method='ffill')
        self.bdg_sums.sort_index(inplace=True)


        self.main_layout = html.Div(children=[
            html.H3(children='Evolution du budget de production par genre par année'),
            html.Div([ dcc.Graph(id='bgr-main-graph'), ], style={'width':'100%', }),
            html.Div([
                # html.Div([ html.Div('Prix'),
                #            dcc.RadioItems(
                #                id='bgr-price-type',
                #                options=[{'label':'Absolu', 'value':0}, 
                #                         {'label':'Équivalent J','value':1},
                #                         {'label':'Relatif : 1 en ','value':2}],
                #                value=1,
                #                labelStyle={'display':'block'},
                #            )
                #          ], style={'width': '9em'} ),
                # html.Div([ html.Div('Mois ref.'),
                #            dcc.Dropdown(
                #                id='bgr-which-month',
                #                options=[{'label': i, 'value': Energies.mois[i]} for i in Energies.mois],
                #                value=1,
                #                disabled=True,
                #            ),
                        #  ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
                # html.Div([ html.Div('Annee ref.'),
                #            dcc.Dropdown(
                #                id='bgr-which-year',
                #                options=[{'label': i, 'value': i} for i in self.years],
                #                value=2000,
                #                disabled=True,
                #            ),
                #          ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
                # html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Échelle en y'),
                           dcc.RadioItems(
                               id='bgr-yaxis-type',
                               options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                               value='Linéaire',
                               labelStyle={'display':'block'},
                           ),
                           html.Div('Prendre en compte l\'inflation'),
                            dcc.Checklist(
                                id='bgr-inflation-bool',
                                options = [
                                    {'label' : 'Inflation', 'value': True}
                                    ],
                            ),
                         ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                        dcc.Markdown("""
                        #### À propos
                        * Données : [Kaggle / TMdB](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
                        * (c) 2022 Adrien Huet et Charlie Brosse
                        """),
                    
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
                    dash.dependencies.Output('bgr-main-graph', 'figure'),
                    [ 
                        # dash.dependencies.Input('bgr-price-type', 'value'),
                    #   dash.dependencies.Input('bgr-which-month', 'value'),
                    #   dash.dependencies.Input('bgr-which-year', 'value'),
                    dash.dependencies.Input('bgr-inflation-bool', 'value'),
                      dash.dependencies.Input('bgr-yaxis-type', 'value')]
                      )(self.update_graph)
        # self.app.callback(
        #             [ dash.dependencies.Output('bgr-which-month', 'disabled'),
        #               dash.dependencies.Output('bgr-which-year', 'disabled')],
        #               dash.dependencies.Input('bgr-price-type', 'value') )(self.disable_month_year)
    

    def update_graph(self, inflation, xaxis_type):
        if not inflation:
            df = self.bdg_sums
        else:
            # filter out years not registered in the inflation csv
            df = self.bdg_sums[self.bdg_sums.index >= 1913]
            df = df.apply(lambda ser : pd.Series([us_convert(before, 2021, val) for before, val in zip(ser.index, ser.values)], ser.index))

        fig = px.line(df[df.columns[0]], template='plotly_white')

        for c in df.columns[1:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
        
        fig.update_layout(
            xaxis = dict(title='Année',),
            yaxis = dict(title="Budget total par genre",
                type= 'linear' if xaxis_type == 'Linéaire' else 'log'
            ),

         margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
         hovermode='closest',
         showlegend=True,
         )
        return fig

if __name__ == '__main__':
    mvP = MovieProduction()
    mvP.app.run_server(debug=True, port=8051)

