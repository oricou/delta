import pandas as pd
import plotly as plt
import os
import glob
import dash
import plotly.express as px
import numpy as np
from dash import dcc
from dash import html
import plotly.graph_objects as go
from postbac.get_data import load_data
from plotly.subplots import make_subplots

class PostBac():


    branches = ['Ecole d\'Ingénieur', 'Ecole de Commerce', 'BTS', 'BUT', 'CPGE', 'Licence', 'EFTS', 'IFSI', 'PACES', 'PASS', 'DUT', 'Management']

    introduction = """
    Bienvenue,\n
    Dans cette étude nous allons voir l'évolution des voeux et des choix faits par des néo-bacheliers pour leurs études supérieurs entre 2016 et 2021. 
    Cette étude montrera tout d'abord l'impact que Parcousup a eu sur les voeux et les choix des étudiants par rapport à APB, puis elle regardera l'évolution globale des voeux et des choix des néo-bacheliers et les inégalités qui peuvent en découler (inégalité homme/femme, inégalité entre étudiant boursier et non-boursier).
    
    """
    
    admis = """
    On peut voir que le nombre d'admis évolue de manière constant entre 2016 et 2021. Parcousup ayant remplacé APB et 2018, on peut voir que Pacoursup a eu un effet modéré sur le nombre d'admis. On peut tout de même voir qu'il y a eu une augmentation du nombre d'admis depuis 2018 avec un pic d'admis en 2020. Ce pic est explicable par la crise du coronavirus et l'annulation des épreuves du baccalauréat remplacés par les moyennes des notes de Terminale des candidats. Cette méthode a créé un boum du nombre de bachelier et donc a influé sur le nombre d'admis. Quant au nombre grandissant d'admis il est très probable que le changement APB à Parcoursup ait créé ce changement (on ne peut en effet pas remettre en cause un boom des naissances car l'augmentation est continue pendant près de 3 ans).  
    """
    
    affectation = """
        Sur ce graphique, nous pouvons voir que le pourcentage de candidats n'ayant reçu aucune affectation a augmenté de 2% entre 2018 et 2020, moment du changement de Parcoursup. Il n'est pas impossible que cette augmentation soit liée au changement d'APB à Parcoursup. En effet, Parcousup donnait plus de liberté et de contrôle aux candidats mais en contrepartie augmentait les chances qu'un candidats n'ait aucun voeu (exemple : Un candidats qui ne souhaite que des écoles qu'il ne peut avoir car trop haut niveau).\n
        L'augmentation de ce pourcentage est aussi liée à l'augmentation des écoles hors-Parcoursup. En effet sur ce graphique on compte les candidats sans affectation comme les candidats n'ayant accepté aucun voeu, cependant cela peut être des candidats qui vont dans des écoles externes au système de Parcoursup. \n
        Le pic de l'année 2020 est explicable par l'augmentation du nombre de candidats lié à l'annulation du baccalauréat \n
        En conclusion on peut voir une légère différence entre APB et Parcoursup. Le nombre d'admis a augmenté suite à Parcoursup mais aussi le pourcentage de candidats n'ayant reçu aucune affectation et bien qu'il y ait d'autres facteurs extérieurs (l'augmentation du taux de réussite au bac, les boums de naissances), l'augmentation est continue et trop importante pour n'être expliquée que par ces facteurs.\n
    """
    
    hf = """\n
    Sur ces graphiques on peut voir des tendances s'afficher clairement :\n
    Beaucoup de fiières sont proches d'une parité homme-femme (Licence, DUT, BTS et CPGE). Ces filières étant assez généraliste il n'est pas surprenant d'y trouver une parité.\n
    Il est cependant intéressant de remarquer que dans des études plus spécialisées (école d'ingénieurs, PACES, EFTS et IFSI) que la parité est beaucoup moins existante. Il est assez difficile de trouver toutes les causes de ces disparités mais on peut citer l'éducation des étudiants, la situation actuelle des filières lors du choix. Il est possible que ces choix soient liés aux préférences de chaque sexe au vu du manque d'évolution de ces chiffres sur les 6 dernières années\n
    On peut remarquer que Parcoursup n'a eu aucun effet pour augmenter la mixité. 
    """
    
    boursier = """
    Le pourcentage de boursier est variable en fonction des années, c'est le seul graphique ici qui varie autant (le graphique sur la mixité montrait une certaine stabilité par exemple). Une partie de ces variations est liés au changement de nom et au reclassement de certaines filières. L'autre partie n'est liée à rien : les choix des candidats ne sont pas liés à leur moyen pour les filières publiques ou ne nécessitant peu d'argent, cependant, le pourcentage de boursier est constant pour les écoles onéreuses.\n
    En effet, on peut voir une tendance: les filières peu onéreuses (faculté, BTS ou DUT) sont plus privilégiées par les boursiers alors que les filières onéreuses (Ecole d'ingénieurs / de commerce ou CPGE) ne le sont pas. Cela montre une sélection évidente par les moyens financiers des candidats et donc une inégalité pure dans l'accès aux études. Inégalité que Parcoursup n'a pas su éviter.\n 
    """
    
    conclusion ="""\n\n
    En conclusion on peut voir l'impact certain de Parcoursup sur le nombre d'admis en école supérieur ainsi que le pourcentage d'étudiant n'ayant eu aucune affectation. Parcoursup a su ouvrir et donner plus de liberté aux candidats pour leur choix d'études mais en contrepartie donne plus de chance aux étudiants de n'avoir aucune affectation.\n
    On a pu voir dans cette étude que le baccalauréat est encore une épreuve qui sélectionne avant les études supérieures : l'année 2020, année sans baccalauréat classique, a fait augmenter le nombre d'admis mais aussi le pourcentage de candidat sans affectation\n
    Nos graphiques montrent aussi que des inégalités franches subsistent que Parcoursup n'a pas changés : le manque de parité entre filières en est un exemple (bien qu'il soit complexe d'arriver à un 50/50 parfait, il est difficile de comprendre pourquoi certaines filières ont un rapport 90/10) mais la plus grande inégalité est le plafond de verre que subissent les boursiers. Les écoles privées devenant bien trop cher, il est difficile pour un boursier d'y accéder et ils sont relégués à un choix bien plus restreint que les étudiants non boursiers.
    """
    dataframe = load_data()
    def __init__(self, application = None):
        self.df = PostBac.dataframe
        self.main_layout = html.Div(children=[
            html.H3(children="Evolution des voeux post bac entre 2016 et 2021"),
            html.H5(children='Thomas Chivet et Antoine Vergnaud'),
            html.Div(style={'width' : '100%', 'margin' : 'auto', 'text-align': 'justify'},
                    children=[dcc.Markdown(PostBac.introduction)],),
            html.H4(children="Nombre d'admis en fonction des années"),
            html.Div([ dcc.Graph(id='admis-hist'), ], style={'width':'100%'}),
            html.Div([ dcc.RadioItems(id='hist-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Div(style={'width' : '100%', 'margin' : 'auto', 'text-align': 'justify'},
                     children=[dcc.Markdown(PostBac.admis)],),
            
            html.H4(children="Pourcentage de candidats n'ayant reçu aucune affectation en fonction des années"),
            html.Div([ dcc.Graph(id='unaffiliated-line'), ], style={'width':'100%'}),
            
            html.Div([ dcc.RadioItems(id='line-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
                                     
            html.Div(style={'width' : '100%', 'margin' : 'auto', 'text-align': 'justify'},
                     children=[dcc.Markdown(PostBac.affectation)],),


            html.H4(children="Pourcentage d'hommes et de femmes par filière"),
            html.Div([ dcc.Graph(id='hf-pie'), ], style = {'width' : '100%', }),
            html.Div([ dcc.RadioItems(id='scatter-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),

            html.P("Fillières:"),
            dcc.Dropdown(id='years',
                         options=PostBac.branches,
                         value='BTS', 
                         clearable=False
                        ),
            html.Div(style={'width' : '100%', 'margin' : 'auto'},children=[dcc.Markdown(PostBac.hf)]),
            html.H4(children="Pourcentage de boursier par filière"),
            html.Div([ dcc.Graph(id='boursier-hist'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='scatter-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Div(style={'width' : '100%', 'margin' : 'auto', 'text-align': 'justify'},
                     children=[dcc.Markdown(PostBac.boursier)],),
            html.H4(children="Conclusion"),
            html.Div(style={'width' : '100%', 'margin' : 'auto', 'text-align': 'justify'},
                     children=[dcc.Markdown(PostBac.conclusion)],),
            dcc.Link('Sources', href='https://data.enseignementsup-recherche.gouv.fr/pages/explorer/?q=&sort=modified&refine.keyword=orientation'),
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )
        if application:
            self.app = application
        else: 
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
            

        self.app.callback(
                    dash.dependencies.Output('admis-hist', 'figure'),
                    dash.dependencies.Input('hist-opts', 'value'))(self.show_admis_hist)
        self.app.callback(
                    dash.dependencies.Output('unaffiliated-line', 'figure'),
                    dash.dependencies.Input('line-opts', 'value'))(self.show_unaffiliated_candidates)
        self.app.callback(
                    dash.dependencies.Output('boursier-hist', 'figure'),
                    dash.dependencies.Input('scatter-opts', 'value'))(self.show_boursier_hist)
        self.app.callback(
                    dash.dependencies.Output('hf-pie', 'figure'),
                    dash.dependencies.Input('years', 'value'))(self.show_branch_per_sex)
        
    
    
    def show_admis_hist(self, mean):  
        fig = px.histogram(
            self.df, 
            x = self.df['Session'],
            y = self.df['Admis'],
            color = 'Filières très agrégées',
            labels={
                 "Session": "Année",
                 "Filières très agrégées": "Filières"
                 },
            )
        fig.update_layout(bargap = 0.2, yaxis_title="Nombre d'admis")    
        return fig
        
    def show_unaffiliated_candidates(self, mean):
        data = [[2016, 761659], [2017, 852262], [2018, 812082], [2019, 937332], [2020, 985538], [2021, 965531]]
        candidatesNbDf = pd.DataFrame(data, columns = ['Session', 'Nombre de candidats'])
        fig = px.line(
                candidatesNbDf,
                x = 'Session',
                y = self.df.groupby(['Session'])['Admis'].sum() * 100 / candidatesNbDf['Nombre de candidats'].sum(),
                range_y = [9,13],
                markers=True,
                labels={
                 "y": "Pourcentage de candidats non affectés",
                 "Session" : "Année"
                 },
                )
        return fig
    
    def show_boursier_hist(self, mean):  
        df = self.df.groupby(['Session', 'Filières très agrégées'])[['Admis', 'Effectif des admis boursiers']].sum()
        fig = px.histogram(
            df,
            x = df.index.get_level_values(1),
            y = df['Effectif des admis boursiers']*100 / df['Admis'],
            range_y = [0,50],
            color = df.index.get_level_values(1),
            animation_frame=df.index.get_level_values(0),
            labels={
                 "x": "Fillière",
                 "animation_frame": "Année"
                 },
            )
        fig.update_layout(showlegend=False, yaxis_title="Pourcentage de boursier")
        return fig
        
    def show_branch_per_sex(self, branch):
        years = [2016, 2017, 2018, 2019, 2020, 2021]
        # here we want our grid to be 2 x 3
        rows = 2
        cols = 3
        
        subplot_titles = ["Mixité dans la filière " + branch + ' en ' + str(x) for x in years]

        specs = [[{'type':'domain'}] * cols] * rows
        
        fig = make_subplots(
                rows=rows,
                cols=cols,
                subplot_titles=subplot_titles,
                specs=specs)
        
        fig.update_annotations(font_size=12)
        
        for i, l in enumerate(years):
            
            SexLabels = ["Proportion d'hommes", 'Proportion de femmes','Pas de données']
            my_dict={
            'SEXE': SexLabels,
            'SOMME':[self.df.loc[(self.df['Filières très agrégées'] == branch) & (self.df['Session'] == l)]["Nombre d'hommes"].sum(),
                   self.df.loc[(self.df['Filières très agrégées'] == branch) & (self.df['Session'] == l)]["Nombre de femmes"].sum(), 1]
            }
            dataframe = pd.DataFrame(data = my_dict)
            # basic math to get col and row
            row = i // cols + 1
            col = i % (rows + 1) + 1
            # this is the dataframe for every year
            fig.add_trace(
                go.Pie(labels = dataframe['SEXE'],
                       values = dataframe["SOMME"],
                       showlegend = True,
                       textposition ='inside',
                       textinfo = 'percent'),
                 row = row,
                 col = col

            )

        fig.update_layout(title="", title_x = 0.45)
        fig.update_traces(marker = dict(colors = ['#1109B1', '#D90000', 'gray']))
        return fig

if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)

