import dash
from matplotlib.pyplot import legend, title
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash import dcc, html
from .data.get_data import extract_data

class Inequalities():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = extract_data()
        self.color = {'Gauche': 'indianred', 'Centre': 'goldenrod', 'Droite': 'darkcyan'}
        self.years = self.df.year.unique()
        self.offset = 0.025

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des inégalités par parti politique en Europe depuis les années 2000', style={'font-weight': 'bold'}),

            html.Div("L'indice (ou coefficient) de Gini est un indicateur synthétique permettant de rendre compte du niveau d'inégalité pour une variable et sur une population donnée."),
            html.Div("Il varie entre 0 (égalité parfaite) et 1 (inégalité extrême). Entre 0 et 1, l'inégalité est d'autant plus forte que l'indice de Gini est élevé."),
            html.Br(),

            html.Div('(Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.)'),
            html.Br(),

            html.Div([
                    html.Div([
                        # Properly display the main graph title
                        html.H6('Evolution du coefficient de Gini et des partis politiques en Europe',
                                style={
                                    'font-weight': 'bold',
                                    'display':'flex',
                                    'justifyContent':'center',
                                    'font-size':'22px'
                                }
                        ),

                        # Display the main graph
                        dcc.Graph(id='ine_gini-main-graph'),

                        # Set the year slider
                        html.Div(
                            dcc.Slider(
                                    id='ine_gini-crossfilter-year-slider',
                                    step = 1,
                                    min=self.years[0],
                                    max=self.years[-1],
                                    value=self.years[0],
                                    marks={str(year): str(year) for year in self.years[::3]},
                            ), style={'width': '100%'}),

                        # fire a callback periodically
                        dcc.Interval( 
                            id='ine_gini-auto-stepper',
                            interval=750,
                            max_intervals = -1,
                            n_intervals = 0
                        ),
                    ]),
                    
                    html.Div([
                        # Manage spacing
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        # Display the checklist element
                        html.Div('Orientations Politiques', style={'font-weight': 'bold'}),
                        dcc.Checklist(
                            id='ine_gini-crossfilter-which-party',
                            options=[{'label': ' ' + i, 'value': i} for i in sorted(self.color.keys())],
                            value=sorted(self.color.keys()),
                        ),

                        # Manage spacing
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        # Display dropdown element
                        html.Div('Paramètre Politique', style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='ine_gini-which-parameter',
                            value='gouvernement',
                            clearable=False,
                            options=[{'label': 'gouvernement', 'value': 'gouvernement'},
                                     {'label': 'parlement', 'value': 'parlement'}],
                            style={'width': '102%'},
                        ),

                        # Manage spacing
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        # Display the stop button for the year slider
                        html.Div(html.Button(self.START, id='ine_gini-button-start-stop'))
                    ], style={'margin-left':'90px'}), 

                    html.Div([
                        # Manage spacing
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        # Display the political orientation legend for the main graph
                        html.Span(style={'height': '19px', 'width': '19px', 'border-radius': '50%', 'display': 'inline-block', "background-color": self.color['Centre']}),
                        html.Br(),
                        html.Span(style={'height': '19px', 'width': '19px', 'border-radius': '50%', 'display': 'inline-block', "background-color": self.color['Droite']}),
                        html.Br(),
                        html.Span(style={'height': '19px', 'width': '19px', 'border-radius': '50%', 'display': 'inline-block', "background-color": self.color['Gauche']}),
                    ]),
                ], style={
                    'display':'flex',
                    'justifyContent':'center',
                    'borderTop': 'thin lightgrey solid',
                }),

            # Display the selected country
            html.Br(),
            html.Div(id='ine_gini-div-country', style={'font-size': '20px', 'borderBottom': 'thin lightgrey solid'}),
            html.Br(),

            # Display the two linked subgraphs
            html.Div([
                    dcc.Graph(id='ine_gini-gini-evolution', style={'width':'50%', 'display':'inline-block'}),
                    dcc.Graph(id='ine_gini-mean-gini-per-party', style={'width':'50%', 'display':'inline-block'}),
                ], style={ 'display':'flex', 
                           'borderBottom': 'thin lightgrey solid',
                           'align-content':'center' }),

            dcc.Markdown('''
            ### Analyse:
            Notre projet essaye de mettre en relation l'orientation politique et l'inégalité en utilisant le coefficient de gini. Cependant, ce coefficient connait quelques biais qui peuvent empêcher une analyse statistique fine. En effet, comme la moyenne, un même coefficient peut venir de plusieurs répartitions différentes.

            ###### Résultats:
              * Tout d'abord, il est bon de noter que le parlement et le gouvernement sont dans la majorité des cas de la même orientation politique.
              * On peut aussi remarquer que la crise économique a beaucoup influencé la valeur du coefficient de gini. Ce dernier baissant en Europe car la répartition des richesses est devenu plus égalitaire bien que la majorité population ait perdu de l'argent.
              * Il ne semble pas avoir de corrélation entre l'orientation politique et la baisse du coefficient de gini.

            ###### Critiques:
              * Le data-set détaillant l'orientation politique, bien que très utile n'a pas énormément de sens en lui-même. En effet, deux partis de gauche sont différents, ne se correspondent pas vraiment entre pays et change en fonction du temps. Pour réduire cela nous avons décidé de travailler que depuis 2000.
              * Les conséquences (positives ou négatives) d'un parti ne peuvent se mesurer qu'avec un certains décalage, le temps que les lois entre en vigueur et aient un effet sur le coefficient de gini.
            ''', style={'borderBottom': 'thin lightgrey solid', 'borderTop': 'thin lightgrey solid'}),

            # Display the "A propos" section
            dcc.Markdown("""
            ### À propos

                * Dans le cadre d'un projet de Python pour le Big Data (PYBD), encadré par Olivier Ricou à l'EPITA
                * [Version Plotly](https://plotly.com/python/v3/gapminder-example/)
                * Données : - [World Inequality Database](https://wid.world/fr/donnees/)
                            - [Comparative Political Data Set](https://www.cpds-data.org/index.php/data)
                * (c) 2022 Philippe Aymard, Alexandre Rulleau
            """),
        ], style={'padding': '10px 50px 10px 50px'})

        # application should have its own layout and use self.main_layout as a page or in a component
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        # Main graph callback
        self.app.callback(
            dash.dependencies.Output('ine_gini-main-graph', 'figure'),
            [dash.dependencies.Input('ine_gini-crossfilter-which-party', 'value'),
            dash.dependencies.Input('ine_gini-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('ine_gini-which-parameter', 'value')])(self.update_graph)

        # Stop button callback
        self.app.callback(
            dash.dependencies.Output('ine_gini-button-start-stop', 'children'),
            dash.dependencies.Input('ine_gini-button-start-stop', 'n_clicks'),
            dash.dependencies.State('ine_gini-button-start-stop', 'children'))(self.button_on_click)

        # Year slider callback
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('ine_gini-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('ine_gini-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('ine_gini-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('ine_gini-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('ine_gini-crossfilter-year-slider', 'value'),
             dash.dependencies.State('ine_gini-button-start-stop', 'children')])(self.on_interval)

        # Callback to handle the selected callback
        self.app.callback(
            dash.dependencies.Output('ine_gini-div-country', 'children'),
            dash.dependencies.Input('ine_gini-main-graph', 'hoverData'))(self.get_country)

        # Callback for the two subgraphs
        self.app.callback(
            dash.dependencies.Output('ine_gini-gini-evolution', 'figure'),
            [dash.dependencies.Input('ine_gini-main-graph', 'hoverData'),
            dash.dependencies.Input('ine_gini-which-parameter', 'value')])(self.update_gini_evolution)
        self.app.callback(
            dash.dependencies.Output('ine_gini-mean-gini-per-party', 'figure'),
            [dash.dependencies.Input('ine_gini-main-graph', 'hoverData'),
            dash.dependencies.Input('ine_gini-which-parameter', 'value')])(self.update_mean_gini_per_party)

    def update_graph(self, parties, year, parameter):
        # Use input parameters
        dfg = self.df[self.df.year == year]
        dfg = dfg[dfg[f'Orientation politique du {parameter}'].isin(parties)]

        # Handle the case were no political orientation is selected
        if dfg.empty:
            fig = go.Figure(go.Scattergeo())
        else:
            fig = px.scatter_geo(dfg, locations="iso", hover_name="country",
                                 hover_data={'gini': True, 'gini_display': False, 'iso': False},
                                 size="gini_display", color=f'Orientation politique du {parameter}',
                                 color_discrete_map=self.color, opacity=0.95)

        # Update graph display
        fig.update_geos(
            resolution=50,
            showcoastlines=True, coastlinecolor="RebeccaPurple",
            showland=True, landcolor="MediumSeaGreen",
            showocean=True, oceancolor="LightSkyBlue",
            scope='europe', projection_type='natural earth',
        )

        fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        return fig

    def update_gini_evolution(self, hover_data, parameter):
        # Use input parameters
        country = self.get_country(hover_data)
        dfg = self.df[self.df.country == country]

        # Create the figure
        fig = go.Figure()
        for index, row in dfg.reset_index().iterrows():
            previous_gini = dfg.iloc[[0]].gini if index == 0 else dfg.iloc[[index - 1]].gini
            previous_year = 2000 if index == 0 else dfg.iloc[[index - 1]].year
            party = row[f'Orientation politique du {parameter}']

            fig.add_trace(go.Scatter(x=[int(previous_year), row.year],
                                     y=[float(previous_gini), row.gini],
                                     fill='tozeroy', fillcolor=self.color[party],
                                     line_color=self.color[party], text=party))

        # Update graph display
        fig.update_layout(
            title="<b>Courbe d'évolution du coefficient de Gini selon l'année, coloré en fonction des partis",
            title_x=0.0,
            margin={"r":110,"t":60,"l":30,"b":80},
            hovermode='closest',
            showlegend=False,
            xaxis_title=dict(text="Années"),
            yaxis_title=dict(text="Coefficient de Gini"),
            yaxis_range=[dfg['gini'].min() - self.offset,
                         dfg['gini'].max() + self.offset],
        )
        
        return fig
    
    def update_mean_gini_per_party(self, hover_data, parameter):
        # Use inputs parameter
        country = self.get_country(hover_data)
        dfg = self.df[self.df.country == country]
        dfg = dfg.groupby(f'Orientation politique du {parameter}')['gini'].mean().to_frame(name='moyenne').reset_index()
        
        # Create the figure
        fig = px.bar(dfg, x=f'Orientation politique du {parameter}', y='moyenne',
                     color=f'Orientation politique du {parameter}', color_discrete_map=self.color)

        # Update graph display
        fig.update_layout(
            title='<b>Coefficient de Gini moyen par orientation politique',
            title_x=0.5,
            hovermode='closest',
            showlegend=True,
            legend={'title': 'Orientations Politiques'},
            xaxis_title=dict(text="Orientations politiques"),
            yaxis_title=dict(text="Coefficient de Gini (en moyenne)"),
            yaxis_range=[dfg['moyenne'].min() - self.offset,
                         dfg['moyenne'].max() + self.offset],
        )
        return fig

    # Get the selected country
    def get_country(self, hover_data):
        if hover_data == None: # init value
            return self.df['country'].iloc[np.random.randint(len(self.df))]
        return hover_data['points'][0]['hovertext']

    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:
            return 0 
        return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-1]:
                return self.years[0]
            return year + 1
        return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ineq = Inequalities()
    ineq.run(port=8055)
