import pandas as pd
import numpy as np
import plotly.express as px 
import dash
from dash import Dash, html, dcc


class Metacritic():
    def __init__(self, application=None): 
        self.data = pd.read_pickle("aa_sc_metacritic/data/vgcritics.pkl")
        self.data_sales = pd.read_pickle("aa_sc_metacritic/data/vgsales.pkl")
        
        genre_list = ["Action", "Adventure", "Arcade", "Sports", "Fighting", "Open-World", "Role-Playing", "RPG", "Platformer", "Fantasy", "Shooter", "Simulation", "Racing", "Survival"]
        fig_plat = self.update_graph_plateforme(2007)
        fig_evolution_per_year = self.create_evolution_year()
        fig_evolution_per_month = self.create_evolution_month()
        fig_note_evolution = self.platform_evolution_note(None)
        fig_sales_evolution = self.platform_evolution_sales(None)
        fig_diff_evolution = self.platform_difference_evolution(None)
    

        self.main_layout = layout = html.Div(children=[
            
            html.Div([
                 dcc.Markdown("""
                            ## Analyse des notes Metacritic
                            Metacritic est un agrégateur de note qui prend les notes publiés sur chaque jeux par les plus gros sites parlant de jeu vidéo à travers le monde. Cet outil est aujourd'hui la référence dans le domaine et est souvent utilisé comme étalon pour connaître la qualité d'un jeu. 
                            
                            Il est aussi possible pour les utilisateurs de notés les jeux permettant de facilement comparer l'avis des joueurs par rapport à l'avis des critiques.
                            
                            ### Objectif
                            L'objectif est de voir la divergence entre les notes des joueurs et des critiques et de comparer la qualité moyenne des jeux par console. La visualiation des données par année permet aussi de mettre en avant l'emergence et la "mort" commerciale des consoles.
                            
                            Nous pouvons aussi vérifier si la rumeur disant que les jeux sont de mieux en mieux notés avec le temps est vrai.
                            """),
            ], style={
                            'borderBottom': 'lightgrey solid',
                            'padding': '0px 50px', 
                            'width':'100%'
                        }),
            html.Br(),
            
            html.Div([
                
                dcc.Markdown("""
                            *Déplacez la souris sur une bulle pour avoir les graphiques de la plateforme de jeu en bas.*
                            """),
                    
                        dcc.Graph(
                            id='platform-graph',
                            figure=fig_plat
                        ),
                        html.Div(
                            dcc.Slider(
                                    id='wps-crossfilter-year-slider',
                                    min=1995,
                                    max=2020,
                                    step = 1,
                                    value=2007,
                                    marks={str(year): str(year) for year in [i for i in range(1995,2020)]},
                            ),
                            style={'display':'inline-block', 'width':"90%"}
                        ),
                        
                        html.Br(),

                        html.Div([
                            dcc.Graph(id='wps-note-evolution', 
                                      figure=fig_note_evolution,
                                    style={'width':'33%', 'display':'inline-block'}),
                            dcc.Graph(id='wps-sales-evolution',
                                      figure=fig_sales_evolution,
                                    style={'width':'33%', 'display':'inline-block', 'padding-left': '0%'}),
                            dcc.Graph(id='wps-diff-evolution',
                                      figure=fig_diff_evolution,
                                    style={'width':'33%', 'display':'inline-block', 'padding-left': '0%'}),
                        ], style={ 'display':'flex', 
                                'borderTop': 'thin lightgrey solid',
                                'borderBottom': 'thin lightgrey solid',
                                'justifyContent':'center', }),
            
                        dcc.Markdown("""
                        ### Explications
                        On peut observer un fort désaccord entre les joueurs et les critiques pour certaines consoles. Parfois les critiques sont plus généreux (cas de la XboxOne et PS4) parfois ce sont les joueurs (Wii).
                        
                        La Wii (2006-2011) par exemple est selon la critique la consoles ayant les plus mauvais jeux alors que selon les joueurs elle se classe au même niveau, parfois même mieux que d'autres consoles. Plusieurs raisons peuvent expliquer cette écart :

                        - La Wii est une console ayant des mauvaises performances graphiques par rapport à ses concurents de l'époque. Or, les critiques prennent souvent la qualité visuel fortement en compte.
                        - La Wii propose de nombreux jeux ayant une cible familiale. Les critiques jouent souvent seul ou au moins dans un contexte de travail ce qui influence l'expérience qu'ils vont vivre et l'avis qu'ils auront des jeux.

                         """),
                        ], style={
                            'padding': '0px 50px', 
                            'width':'100%'
                        }),
            

            html.Div([
                        html.Div(
                            dcc.Graph(
                                id='evolution-year-graph',
                                figure=fig_evolution_per_year
                            ),    
                            style={'display':'inline-block', 'width':"50%"}
                        ),
                        html.Div(
                            dcc.Graph(
                                id='evolution-month-grapth',
                                figure=fig_evolution_per_month
                            ),    
                            style={'display':'inline-block', 'width':"50%"}
                        ),
                        dcc.Markdown("""
                         ### Explications
                        Contrairement a la croyance populaire les notes des meilleurs jeux n'augmentent pas d'année en année c'est même l'inverse, on peut observer une descente progressive.          
                        On peut voir que la période de l'année ayant les meilleurs jeux est en novembre. C'est à ce moment là que sorte beaucoup de très grosses productions pour profiter des ventes de noël. A l'inverse l'été est une période creuse où sorte en moyenne moins de très bons jeux. 
                    """),
                        html.Br(),
                        dcc.Markdown("""
                        #### À propos

                        * Metacritic : https://www.metacritic.com/
                        * Origine des données : [Deep contractor on Kaggle](https://www.kaggle.com/datasets/deepcontractor/top-video-games-19952021-metacritic)
                        * *Les données de ventes utilisés s'arrêtent à l'année 2016. Données de vente indisponibles pour la Nintendo Switch et la Playstation Vita*
                        """),
                        ], style={
                            'borderTop': 'lightgrey solid',
                            'padding': '0px 50px', 
                            'width':'100%'
                        }),
            
        ])
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
            
        self.app.callback(
            dash.dependencies.Output('platform-graph', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(self.update_graph_plateforme)
        
        self.app.callback(
            dash.dependencies.Output('wps-note-evolution', 'figure'),
            [dash.dependencies.Input('platform-graph', 'hoverData')])(self.platform_evolution_note)
        self.app.callback(
            dash.dependencies.Output('wps-sales-evolution', 'figure'),
            [dash.dependencies.Input('platform-graph', 'hoverData')])(self.platform_evolution_sales)
        self.app.callback(
            dash.dependencies.Output('wps-diff-evolution', 'figure'),
            [dash.dependencies.Input('platform-graph', 'hoverData')])(self.platform_difference_evolution)

    def update_graph_plateforme(self, year):
        data = self.data
        yearTarget = year
        platform_list = ["PC", "XboxOne", "Xbox360", "Xbox", "PlayStation4", "PlayStation3", "PlayStation2", "PlayStation", "Switch", "WiiU", "Wii", "GameCube", "Nintendo64", "Dreamcast", "3DS", "DS", "GameBoyAdvance", "PlayStationVita", "PSP"]
        data_annual = data.loc[data["r-date"].dt.year == yearTarget]

        def score(row, targetPlatform) : 
            if targetPlatform == row.platform :
                return row.score
            
        def user_score(row, targetPlatform) :
            if targetPlatform == row.platform :
                if row[4] != "tbd" : 
                    return float(row[4])

        data_platform = pd.DataFrame()
        previousMeanScore = 0
        data_platform = []
        for tg in platform_list : 
            meanScore = data_annual.apply(score, targetPlatform = tg, axis='columns').mean()
            if pd.isna(meanScore) : 
                continue
            meanUserScore = data_annual.apply(user_score, targetPlatform = tg, axis='columns').mean()
            numberInPlatform = data_annual.platform.map(lambda g: g == tg).value_counts().loc[True]
            data_tmp = pd.DataFrame({'platform' : tg, 'Score moyen des utilisateurs' : meanScore, 'Score moyen des critiques': meanUserScore, 'nb_games' : numberInPlatform}, index=["A"])
            data_platform.append(data_tmp)
        data_platform = pd.concat(data_platform) 

        platform_colors = {'PC':'silver',"XboxOne":"greenyellow", "Xbox360":"chartreuse", "Xbox":"lime", "PlayStation4":"navy", "PlayStation3":"blue", "PlayStation2":"dodgerblue", "PlayStation":"cyan", "Switch":"red", "WiiU":"firebrick", "Wii":"lightcoral", "GameCube":"salmon", "Nintendo64":"darkred", "Dreamcast":"sandybrown", "3DS":"#B05500", "DS":"#FF7B00", "GameBoyAdvance":"#F3ED36", "PlayStationVita":"#C9C40E", "PSP":"gold"}

        fig = px.scatter(data_platform, x='Score moyen des utilisateurs', y='Score moyen des critiques', color="platform", hover_name="platform",
                        color_discrete_map=platform_colors, title="Score moyen par plateforme sur Metacritic en " + str(yearTarget),
                        size='nb_games', size_max=50)
        fig.update_layout(yaxis_range=[6, 9])
        fig.update_layout(xaxis_range=[60,90])
        return fig
        
    def update_graph_genre(self, year) : 
        yearTarget = year
        data = self.data
        data_annual = data.loc[data["r-date"].dt.year == yearTarget]
        
        def score(row, targetGenre) : 
            if targetGenre in row.genre :
                return row.score
            
        def user_score(row, targetGenre) :
            if targetGenre in row.genre :
                if row[4] != "tbd" : 
                    return float(row[4])

        data_gs = pd.DataFrame()
        for tg in genre_list : 
            meanScore = data_annual.apply(score, targetGenre = tg, axis='columns').mean()
            meanUserScore = data_annual.apply(user_score, targetGenre = tg, axis='columns').mean()
            numberInGenre = data_annual.genre.map(lambda g: tg in g).value_counts().loc[True]
            data_tmp = pd.DataFrame({'genre' : tg, 'Score moyen des critiques' : meanUserScore, 'Score moyen des utilisateurs': meanScore, 'nb_games' : numberInGenre}, index=["A"])
            data_gs = data_gs.append(data_tmp)

        genre_colors = {'Action':'gold', 'Adventure':'green', 'Arcade':'brown', 'Sports':'navy', 'Fighting':'#FF0004', 'Open-World':'#00FF16', 'Role-Playing':'#FFB300', 'RPG':'#FAB900', 'Platformer':'#00FCCD', 'Fantasy':'#FC00AB', 'Shooter':'#A33E02', 'Simulation':'#1F8714', 'Racing':'#9B9B9B', 'Survival':'#825C02'}

        fig = px.scatter(data_gs, x='Score moyen des utilisateurs', y='Score moyen des critiques', color="genre", hover_name="genre",
                        color_discrete_map=genre_colors, title="Score moyen par genre sur Metacritic en " + str(yearTarget),
                        size='nb_games', size_max=50)
        return fig
    
    def create_evolution_year(self) : 
        data = self.data
        data_mean = data.groupby(data['r-date'].dt.year).head(50)
        del data_mean['users']
        del data_mean['critics']

        evolution_per_year = data_mean.groupby(data['r-date'].dt.year).mean()

        fig_evolution_per_year = px.line(evolution_per_year, title="Moyenne des 50 meilleurs jeux par année", labels={
                            "value": "Score moyen",
                            "r-date": "Année",
                        },)
        return fig_evolution_per_year

    def create_evolution_month(self) : 
        data = self.data
        data_mean = data.groupby(data['r-date'].dt.month).head(50)
        del data_mean['users']
        del data_mean['critics']
        evolution_per_month = data_mean.groupby(data['r-date'].dt.month).mean()

        fig_evolution_per_month = px.line(evolution_per_month, title="Moyenne des 50 meilleurs jeux par mois de l'année", labels={
                            "value": "Score moyen",
                            "r-date": "Mois",
                        },)
        return fig_evolution_per_month
    
    def get_platform(self, hoverdata) : 
        if hoverdata == None :
            return "Wii"
        return hoverdata['points'][0]['hovertext']
    
    def platform_evolution_sales(self, hoverdata) : 
        platform = self.get_platform(hoverdata)
        data = self.data
    
        data_platform = self.data_sales.loc[self.data_sales["platform"] == platform]
        data_mean = data_platform.groupby(data_platform['Year']).sum()

        evolution_per_year = data_mean
        fig = px.bar(evolution_per_year, y="Global_Sales", title="Ventes cumulés des jeux sorties pendant une année sur " + platform, labels={
                         "Global_Sales": "Ventes mondiales (en millions)",
                         "Year": "Année",
                     },)
        return fig
    
    def platform_evolution_note(self, hoverdata) : 
        platform = self.get_platform(hoverdata)
        data = self.data
        data_platform = data.loc[data["platform"] == platform]
        data_mean = data_platform.groupby(data['r-date'].dt.year).mean()

        evolution_per_year = data_mean
        fig = px.line(evolution_per_year, y="score", title="Evolution des notes des jeux sorties sur " + platform, labels={
                         "score": "Score moyen",
                         "r-date": "Année",
                     },)
        return fig
    
    def platform_difference_evolution(self, hoverdata) : 
        platform = self.get_platform(hoverdata)
        data_platform = self.data.loc[self.data["platform"] == platform].copy()
        data_platform['user score'] = data_platform['user score'].astype(float)
        data_diff_scores = data_platform.groupby(self.data['r-date'].dt.year).mean()
        data_diff_scores['diff'] = data_diff_scores['score'] - (data_diff_scores['user score'] * 10)
        fig = px.bar(data_diff_scores, y="diff", title="Différences entre critiques et joueurs pour des jeux sorties sur " + platform, labels={
                                "diff": "Différence entre notes des critiques et des joueurs",
                                "r-date": "Année",
                            },)
        return fig
    
if __name__ == '__main__':
    mpj = Metacritic()
    mpj.app.run_server(debug=True, port=8051)
