from ctypes import alignment
from lib2to3.pgen2.pgen import DFAState
from matplotlib.pyplot import xlabel, ylabel
import pandas as pd
import numpy as np
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

'''
Authors: Arthur Fan; Hao Ye
Create on 06/05/2022
'''

class Eletricite():
    def __init__(self, application = None):
        # Retrieve pre-processed data 
        df_full_selected = pd.read_pickle("afhy_electricite/data/preprocessed_maingraphdata.pkl")
        df_by_year = df_full_selected.groupby(by=df_full_selected.index.year).sum()
        df_animated = pd.read_pickle("afhy_electricite/data/preprocessed_barplotdata.pkl")
        df_prix = pd.read_pickle('afhy_electricite/data/preprocessed_pricedata.pkl')

        self.df_full_selected = df_full_selected
        self.df_by_year = df_by_year
        self.df_animated = df_animated
        self.df_prix = df_prix



        self.main_layout = html.Div(children=[

            html.H1(children='Evolution de la production d\'électricité dans les différents secteurs et du prix de l\'électricité en France de 2012 à 2020'),
            html.H2(children='Graphique Intéractif'),
            # Main graph 
            html.Div([dcc.Graph(id='main_graph')]),
            html.Div([
                html.Div([
                    # Dropdown to select electricity's souscription
                    html.Div('Souscription'),
                    dcc.Dropdown(
                        [3, 6, 9, 12, 15],
                        3,
                        id='souscription_selection'
                    )
                ], style={'width': '90px', 'display': 'inline-block'}),
                html.Div([html.Div('PART'),
                    # Dropdown to select electricity price part
                    dcc.Dropdown(
                        ['PART_FIXE_HT','PART_FIXE_TTC','PART_VARIABLE_HT','PART_VARIABLE_TTC'],
                        'PART_VARIABLE_TTC',
                        id='type_selection'
                    )
                ], style={'width': '220px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                html.Div([html.Div('Affichage'),
                    # Dropdown to select the period
                    dcc.Dropdown(
                        [
                            {'label': 'Jour', 'value': 'D'},
                            {'label': 'Mois', 'value': 'M'},
                            {'label': 'An', 'value': 'Y'}],
                        'D',
                        id='period_selection'
                    )
                ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                html.Div([html.Div('Échelle de la production'),
                    # To switch the type of 1st y axis
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Linear',
                        id='yaxis1_type',
                        inline=True
                    )
                ], style={'width': '200px', 'display': 'inline-block'}),
                html.Div([html.Div('Échelle des prix'),
                    # To switch the type of 2nd y axis
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Linear',
                        id='yaxis2_type',
                        inline=True
                    )
                ], style={'width': '200px', 'display': 'inline-block'})
            ],style={
                        'padding': '10px',
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justifyContent': 'flex-start',  
                    }
            ),
            html.Br(),
            dcc.Markdown("""
                Le graphique ci-dessus est interactif. Vous pouvez afficher la production d\'électricité dans les différents filières de production en France.       
                Vous pouvez choisir une précision sur des jours, des mois ou des années.
                Vous pouvez également afficher le prix de l\'électricité en choisissant le type d'abonnement en fonction de la puissance en kWA. Et également afficher quel tarif afficher.
                Vous pouvez également cliquer sur les noms des courbes dans la légende pour afficher ou non une courbe. Double-cliquer sur un nom permet d'afficher seulement une courbe ou toute les courbes.
            """),

            html.Br(),
            html.H2(children='Production d\'électricité'),

            html.Div([
                html.Div([
                    dcc.Graph(id='pie_chart')
                ], style={'display': 'inline-block'}),
                html.Div([
                    html.Div([
                        html.Div('Année'),
                        # Dropdown to select year
                        dcc.Dropdown(
                            list(df_by_year.index),
                            2012,
                            id='year_selection'
                            )
                    ], style={'width': '90px'} ),
                    html.Div([
                        dcc.Markdown("""
                            Sur le diagramme en camembert ci-contre, vous pouvez afficher la production d'électricité en France selon l'année choisit. Vous pouvez choisir l'année avec le menu déroulant ci-dessus.  \n
                            Sur ce graphique, vous pouvez voir la production en pourcentage des diffèrentes filières dans l'année. En passant la souris sur le camembert, vous aurez plus de détails sur la filière sur laquelle votre souris pointe.  
                            Il y a également la production total d'électricité en MW affiché juste au dessus du cmembert.  
                        """),
                    ], style={'margin':"0px 0px 0px 10px"})
                ],style={'display': 'inline-block', 'margin':"20px 0px 0px 10px"})
            ],style={
                        'padding': '10px 50px',
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justifyContent': 'flex-start',  
                    }
            ),

            html.H2(children='Diagramme en bâtons de la production d\'électricité'),
            html.Div([
                html.Div([dcc.Graph(id='production_bar')]),
                html.Div([
                    html.Div([
                        # Select the start date D/M/Y
                        html.Div('Date de début'),
                        html.Div([
                            html.Div('Jour'),
                            dcc.Dropdown(
                                list(range(1, 32)),
                                1,
                                id='day_start_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                        html.Div([
                            html.Div('Mois'),
                            dcc.Dropdown(
                                list(range(1, 13)),
                                1,
                                id='month_start_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                        html.Div([
                            html.Div('Année'),
                            dcc.Dropdown(
                                list(range(2012, 2021)),
                                2012,
                                id='year_start_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"})
                    ]),
                    html.Div([
                        # Select the end date D/M/Y
                        html.Div('Date de Fin'),
                        html.Div([
                            html.Div('Jour'),
                            dcc.Dropdown(
                                list(range(1, 32)),
                                1,
                                id='day_end_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                        html.Div([
                            html.Div('Mois'),
                            dcc.Dropdown(
                                list(range(13)),
                                1,
                                id='month_end_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"}),
                        html.Div([
                            html.Div('Année'),
                            dcc.Dropdown(
                                list(range(2012, 2021)),
                                2013,
                                id='year_end_bar'
                            )
                        ], style={'width': '90px', 'display': 'inline-block', 'margin':"0px 10px 0px 10px"})
                    ]),
                ],style={
                            'padding': '10px',
                            'display': 'flex',
                            'flexDirection': 'row',
                            'justifyContent': 'flex-start',  
                        }
                )
            ]),
            html.Br(),
            dcc.Markdown("""
                Sur le graphique ci-dessus, est affiché la production d'électricité par filière sur une période donné.  
                Vous pouvez-choisir la période en renseignant le date de début et la date de la fin sur les menus déroulant. 
                Si vous renseignez une date de début postérieur à la date de fin, le graphique n'affichera rien.
                En passant la souris sur le diagramme, cela affichera plus de détails sur la filière pointé. Vous pouvez également cliquer sur la légende pour afficher ou non une fillière.  
                Et en double cliquant sur une des fillière, cela affichera juste celle-ci ou réaffichera toutes les filières.
            """),
            html.Br(),

            html.H2(children='Diagramme en bâtons animé de la production d\'électricité de 2012 à 2020'),
            html.Div([
                html.Div([html.Div('Échelle'),
                    # To switch the type of axis
                    dcc.RadioItems(
                        ['Linear', 'Log'],
                        'Linear',
                        id='animated_type_xaxis',
                        inline=True
                    )
                ], style={'width': '200px', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='animated_bargraph')])
            ]),
            html.Br(),
            dcc.Markdown("""
                Le graphique ci-dessus est animé. Vous pouvez lancer et arrêter l'animation.       
                En double cliquant sur une des fillière, cela affichera juste celle-ci ou réaffichera toutes les filières. 
                Il est également possible de choisir une échelle logarithmique.
            """),

            html.Br(),
            
            dcc.Markdown("""
                Interprétation:\n
                * Nous pouvons observer les différents pic de production d'électricité entre les saisons hivernales et estival. Avec une plus grande production en hiver. Nous pouvons notamment le remarqué avec l'oscillation de la production de nucléaire.
                * Sur quasimment tous les 25 décembre, il y a une chute de production d'électricité dans le nucléaire.  
                * Avec la fermeture de la central nucléaire de Fessenheim courant 2020, la part de production du nucléaire a baissé et celle de l'hydraulique a augmenté.  
                * En août 2018, il y a une baisse du prix de l'électricité grâce à la commission de régulation d'Énergie qui a recommandé au gouvernement Français de baisser les prix de 0.7% pour les particuliers et de 1.7% pour les professionnels.
                * Le nucléaire représente la filière de production principale d'électricité en France, devant l'hydraulique  
                \n

                Comme nous avons pu le constater, le prix de l'électricité n'est pas fortement lié à la production d'électricité. Cela est dû au fait 
                que le prix de l'électricité est établie par le gouvernement Français. L'état français régule le prix en cas de besoin. 
                Néanmoins nous pouvons remarqué qu'en France, l'électricité est essentiellement produit avec du nucléaire ce qui peut expliquer la faible prix d'électricité en France comparer aux autres pays européens.

                #### À propos

                Sources:  


                * https://www.data.gouv.fr/fr/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/  
                * https://www.rte-france.com/eco2mix/telecharger-les-indicateurs   
                * https://www.rte-france.com/ 
                * (c) 2022 Arthur Fan & Hao Ye
            """)
            ], style={
                    'backgroundColor': 'white',
                    'padding': '10px 50px 10px 50px',
                })

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        # Main graph's callback function 
        self.app.callback(
                    Output('main_graph', 'figure'),
                    Input('souscription_selection', 'value'),
                    Input('yaxis2_type', 'value'),
                    Input('yaxis1_type', 'value'),
                    Input('period_selection', 'value'),
                    Input('type_selection', 'value'))(self.update_main_graph)

        # Pie chart's callback function
        self.app.callback(
                    Output('pie_chart', 'figure'),
                    Input('year_selection', 'value'))(self.update_pie_graph)

        # Barplot's callback function
        self.app.callback(
                    Output('production_bar', 'figure'),
                    Input('day_start_bar', 'value'),
                    Input('month_start_bar', 'value'),
                    Input('year_start_bar', 'value'),
                    Input('day_end_bar', 'value'),
                    Input('month_end_bar', 'value'),
                    Input('year_end_bar', 'value'))(self.update_bar_graph)

        # Animate barplot's callback function
        self.app.callback(
            Output("animated_bargraph", "figure"),
            Input("animated_type_xaxis", "value"))(self.display_animated_graph)

    def update_main_graph(self, souscription_selection, yaxis2_type, yaxis1_type, period_selection, type_selection):
    
        # Group by the selected period 
        dff_full_selected = self.df_full_selected.copy().groupby(pd.Grouper(freq=period_selection)).sum()
        # Get the corresponded column
        dff_prix = self.df_prix[self.df_prix['P_SOUSCRITE'] == souscription_selection]
        
        # Plot a main graph 
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        # 1st yaxis
        fig_1 = px.line(dff_full_selected, render_mode="webgl")
        # 2nd yaxis
        fig_2 = px.line(dff_prix[type_selection], render_mode="webgl")
        fig_2.update_traces(yaxis="y2")
        

        subfig.add_traces(fig_1.data + fig_2.data)
        subfig.layout.xaxis.title="Date"
        subfig.layout.yaxis.title="MW"
        
        # Define the type of 1st y axis
        if yaxis1_type == 'Linear':
            subfig.layout.yaxis.type="linear"
        else:
            subfig.layout.yaxis.type="log"
        
        # Define the type of 2nd y axis
        if yaxis2_type == 'Linear':
            subfig.layout.yaxis2.type="linear"
        else:
            subfig.layout.yaxis2.type='log'
        
        # Add title
        subfig.layout.yaxis2.title="prix par MW en euros"
        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        
        return subfig
    
    def update_pie_graph(self, year_selection):

        # Get data by selected year
        dff = self.df_full_selected.groupby(by=self.df_full_selected.index.year).sum().copy()
        i = int(year_selection) - 2012
        
        traces = go.Pie( 
                    textposition="inside",
                    values = dff.iloc[i,:],
                    labels = list(self.df_full_selected.columns))


        layout = go.Layout(height = 600,
                    width  = 600, 
                    title  = 'Production totale: ' + str(int(np.sum(dff.iloc[i,:]))) + " MW en " + str(dff.index[i]),
                    autosize = False)

        # Plot the pie graph
        fig = go.Figure(data = traces, layout = layout)

        return fig

    def update_bar_graph(self, day_start_bar, month_start_bar, year_start_bar, day_end_bar, month_end_bar, year_end_bar):
        df = self.df_full_selected.copy()
        # Define the start date
        date_start = pd.to_datetime(str(year_start_bar) + '-' + str(month_start_bar) + '-' + str(day_start_bar))

        # Define the end date
        date_end = pd.to_datetime(str(year_end_bar) + '-' + str(month_end_bar) + '-' + str(day_end_bar))

        # Plot the bar graph
        fig = px.bar(df.loc[date_start: date_end].sum(), color=df.columns, text_auto='.2s')
        fig.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(
            xaxis = dict(title="Filière de production"),
            yaxis= dict(title="Production en MW")
        )

        return fig

    def display_animated_graph(self, animated_type_xaxis):
        df = self.df_animated.copy()
        # Plot the animated graph
        fig = px.bar(
            df, x='Type', y="Value", color="Type",
            title="",
            # Make animation
            animation_group="Type", animation_frame='Date')
        fig.update_layout(
            xaxis = dict(title="Filière de production"),
            yaxis= dict(title="Production en MW")
        )

        fig.update_yaxes(type="linear" if animated_type_xaxis == "Linear" else "log")
        
        return fig
        
if __name__ == '__main__':
    mpj = Eletricite()
    mpj.app.run_server(debug=True, port=8051)