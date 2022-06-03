import dash
from dash import dcc, dash_table
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from ma_aj_netflix.data.get_data import get_data

def bound(rate, mx=1):
    if rate < 0:
        return 0
    if rate > mx:
        return mx
    return rate

class NetflixStats():
    def __init__(self, application = None):
        self.df, self.popularity_df, self.sensitivity_df = get_data('ma_aj_netflix/data/netflix_final_data.csv')

        new_sensitivity = []
        for sensitivity in self.df["sensitivity"]:
            new_sensitivity.append(bound(sensitivity + 0.05 - np.random.random() * 0.1))
        self.df["approximate sensitivity"] = new_sensitivity

        new_popularity = []
        for popularity in self.df["popularity"]:
            new_popularity.append(bound(popularity + 0.5 - np.random.random(), 100))
        self.df["approximate popularity"] = new_popularity

        self.ratings = {'TV-Y':'deepskyblue', 'TV-Y7':'mediumaquamarine', 'TV-G':'limegreen', 'TV-PG':'lawngreen', 'PG':'yellow', 'PG-13':'gold', 'TV-14':'orange', 'R':'orangered', 'TV-MA':'firebrick'}

        self.main_layout = html.Div(children=[
            html.H3(children='Popularité et degré de sensibilité sur Netflix'),

            html.Div([
                dcc.Markdown("""
                #### But de la recherche et hypothèse

                > L'un des principaux problèmes auxquels sont confrontés les réseaux sociaux est que, si rien n'est fait, les gens s'engagent de manière disproportionnée dans des contenus plus sensationnalistes et provocateurs.
                > 
                > -- Traduit en français du papier de recherche "A Blueprint for Content Governance and Enforcement” par Mark Zuckerberg, Facebook (2018)

                La recherche montre le graphe suivant :
                """),
                html.Img(src="https://cdn-5c959413f911ca0ff400aa3c.closte.com/wp-content/uploads/2018/11/46275261_10105385390905251_3643739087287877632_o.jpg", width=800),
                dcc.Markdown("""
                > Nos recherches indiquent que, quelle que soit la limite fixée pour ce qui est autorisé, lorsqu'un contenu s'en rapproche, les gens s'y intéressent davantage en moyenne, même s'ils nous disent ensuite qu'ils n'aiment pas ce contenu.
                > 
                > -- Traduit en français du papier de recherche "A Blueprint for Content Governance and Enforcement” par Mark Zuckerberg, Facebook (2018)

                **Nous cherchons à voir si c'est aussi vrai dans le cas de Netflix :   **
                

                *Y a-t-il plus d'engagements avec les contenus (films ou séries) plus les sujets abordés sont sensibles ?*
                ------
                """)
            ]),

            html.Br(),
            html.Div("""
            Le graphique est interactif. Déplacez la souris sur une bulle pour avoir les titres des films et séries.
            En utilisant les icônes en haut à droite, on peut agrandir une zone et réinitialiser.
            """),

            html.Div([
                    html.Div([ dcc.Graph(id='ns-main-graph'), ], style={'width':'80%', }),

                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.Div('Échelle en Y'),
                        dcc.RadioItems(
                            id='ns-crossfilter-yaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                            value='Log',
                            labelStyle={'display':'block'},
                        ),
                        html.Br(),
                        dcc.Checklist(
                            id='random-type',
                            options=[
                                {'label': 'Epsilon aléatoire', 'value': True},
                            ],
                            value=[True]
                        ),
                    ], style={'margin-left':'15px', 'width': '12em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),
            html.Br(),
            html.Div([
                dcc.Markdown("""
                    **Ce qu'on appelle `popularité relative`**
                    : taux d'engagement relatif aux plus populaire, c'est à dire une valeur de 15 en popularité indique que le titre a eu 15% d'engagements comparé au titre le plus populaire (100%) parmi la liste (calculé à base des tendances de recherches Google)

                    **Ce qu'on entend par `degré de sensibilité`**
                    : plus ou moins susceptible à être censuré (par la protection familiale par exemple) : nudité, violence, opinions controversées, etc.

                    **Ce qu'on désigne par `epsilon aléatoire`**
                    : plusieurs programmes pouvant avoir la même popularité et degré de sensibilité, les valeurs peuvent se confondre sur le graphique.
                    Ainsi, afin de mieux visualiser la densité, nous proposons de faire varier aléatoirement les valeurs dans un environ proche (±0.5% pour la popularité et ±5% pour le degré de sensibilité)


                    Plus les points sont hauts, plus ils sont populaires.
                    Plus les points sont vers la droites, plus ils sont sensibles.


                    *N.B: Les titres de popularité de 0% (qui forment 98% de nos données) ont été virés pour une meilleure visualisation.*
                """),
                html.Br(),
                dcc.Markdown("""
                    ###### Comment utiliser les paramètres du graphe et comment l'interpréter ?

                    Il faut se focaliser principalement sur la légende de classification d'âge. 
                    Pour pouvoir reproduire une "policy line" comme dans le graphe de Zuckerberg, c'est-à-dire créer une certaine restriction à des programmes sensibles (nudité, violence, substance, ...), essayez de retirer petit à petit les plus élévés (donc commençant par TV-MA, puis R, etc.).
                    Pour le faire, il suffit de cliquer une fois sur une classification dans la légende. Cliquer deux fois permet d'isoler la classification.

                    Remarquez au niveau de la restriction PG-13 (inclus), le graphe commence à ressembler à celui de Zuckerberg. Cependant, à part ce cas-là, ce n'est pas toujours évident.
                """)
            ]),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div('Popularité des programmes en fonction de leur degré de sensibilité regroupé par intervales (et vice-versa)', style={'font-size' : 'large'}),
                html.Div([
                    dcc.Graph(id='ns-stats-popularity-series', 
                            style={'width':'45%', 'display':'inline-block'}),
                    dcc.Graph(id='ns-stats-sensitivity-series',
                            style={'width':'45%', 'display':'inline-block', 'padding-left': '2%'}),
                    html.Div('Statistiques'),
                    dcc.RadioItems(
                        id='ns-crossfilter-which-stats',
                        options=[{'label': i[0], 'value': i[1]} for i in {'moyenne':'mean', 'médiane':'median'}.items()],
                        value='mean',
                        labelStyle={'display':'inline-block'},
                    )
                ], style={ 'display':'flex', 
                        'borderTop': 'thin lightgrey solid',
                        'borderBottom': 'thin lightgrey solid',
                        'justifyContent':'center', }),
                html.Br(),
                dcc.Markdown("""
                    La couleur rouge représente la valeur maximale, le jaune la minimale.


                    ###### Interprétation des statistiques
                    
                    On peut remarquer d'une part que les sensibilités des programmes les plus populaires sont celles entre les valeurs 0.5 et 0.6.
                    D'autre part, les programmes ayant les degrés de sensibilités les plus élevés ne sont généralement pas les plus populaires (entre 20 et 25% de popularité), néanmoins ils ont bien un engagement considérable
                    (Attention à ne pas être induit en erreur, Les programmes qui sont plus populaires que 25% ne forment qu'environ 1.4% des titres !).
                """)
            ]),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div('Les 10 programmes les plus populaires', style={'font-size' : 'large'}),
                dash_table.DataTable(self.popularity_df.to_dict("records"), style_cell={'textAlign': 'left'}),
            ]),
            html.Br(),
            html.Div([
                html.Div('Les 10 programmes les plus sensibles', style={'font-size' : 'large'}),
                dash_table.DataTable(self.sensitivity_df.to_dict("records"), style_cell={'textAlign': 'left'}),
            ]),
            html.Div([
                html.Br(),
                dcc.Markdown("""
                    ###### Interprétation des tableaux

                    Les tableaux montrent que de manière globale (donc avec accès à tous les programmes), 
                    les gens n'ont pas nécessairement tendance à s'intéresser aux programmes les plus sensibles.
                """)
            ]),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Markdown("""
                    #### Récolter les données

                    ##### Les titres Netflix
                    Nous avons récupéré les titres Netflix avec leurs données associées à partir d'un dataset sur Kaggle https://www.kaggle.com/shivamb/netflix-shows 

                    ##### Le taux d'engagement ou popularité relative

                    Concernant la popularité, une base de données contenant les informations relatives était difficile à trouver. Nous avons donc décidé d'en créer une nous-mêmes en se basant sur les données fournies par Google Trends.

                    Google Trends est une API/site de recherche de tendances qui indique la fréquence de saisie d'un terme de recherche donné dans le moteur de recherche de Google par rapport au volume de recherche total du site sur une période donnée. Google Trends peut être utilisé pour la recherche comparative de mots-clés et pour découvrir les pics de volume de recherche de mots-clés déclenchés par des événements.

                    Google Trends fournit des données relatives aux mots-clés, notamment l'indice du volume de recherche et des informations géographiques sur les utilisateurs du moteur de recherche.

                    Les informations obtenues étaient suffisantes pour nous donner une estimation du taux d'engagement avec un film ou une série donnée de Netflix.

                    N'ayant pas de chiffre concret du nombre de recherches par titre, nous avons effectué une recherche pour trouver le plus populaire de la liste grâce à la fonctionnalité de comparaison de mots-clés (5 par 5). Après l'avoir récupéré, ayant maintenant une référence, nous avons refait une passe pour obtenir les pics de volume de recherche pour chacun des titres comparés à celui-ci.

                    *N.B 1: Nous avons bien veillé à faire des recherches de "thèmes" quand cela était possible pour éviter les confusions et avoir le moins d'erreurs. Les recherches par "thèmes" permettent de mieux préciser le contexte. Par exemple, les mots-clés "Black Panther" peuvent désigner le film ou bien littéralement l'animal, on essaye donc de prendre le bon "thème" afin d'avoir des résultats plus corrects.*

                    *N.B 2 : Nous nous sommes limités aux titres sortis après 2015 étant limité par ce qui est disponible au public sur Google Trends.*


                    ##### Le degré de sensibilité

                    Concernant la sensibilité, nous nous sommes basés sur 2 indices, le premier étant la classification d'âge, présent sur le dataset original.
                    Nous convertissons le degré de sensibilité obtenu en un nombre entre 0 et 2/3.

                    Mais nous voulions aussi nous baser sur les thématiques du film. C'est pourquoi, à l'aide du titre des programmes, nous avons fait des requêtes html sur le site https://www.imdb.com/ afin de récupérer tous les mots clés correspondants.
                    Parallèlement, nous avons construit une liste de mots clés sensibles.
                    
                    Enfin, pour chaque programme, nous comptons les occurrences de mots sensibles parmi ses mots clés, afin de construire un indice entre 0 et 1/3.
                    Le degré de sensibilité est donné par la somme de ces deux indices.

                    """),
                    html.Br(),
                    dcc.Markdown("""
                    #### Analyse des résultats
                    
                    Même si nous pouvons constater que les quelques programmes les plus populaires sont pour la plupart classés grand public, avec une sensibilité moyenne (0.6 pour Avengers infinity war),
                    le nuage de points tend à montrer que les programmes sensibles occupent une bonne partie de l'espace des programmes populaires. En effet, en retirant les sensibilités les plus élévées, comme pourrait le faire un control parental,
                    l'on créé une ligne de "censure" comme dans le graphe de Zuckerberg.

                    De plus, les programmes les moins sensibles, souvent réservés à un public très jeune, sont assez peu populaires, ainsi, les programmes à sensibilité moyenne et forte se partagent les programmes populaires.
                    Mais n'oublions pas que les adultes sont surement une audience plus visée que les enfants, ce qui peut expliquer le nombre important de titres à classification d'âge élevée.

                    En conclusion, bien que la tendance n'est pas aussi visible qu'avec la courbe attendue, une majorité des programmes populaires de Netflix sont assez sensibles et susceptibles d'être censurés dans certains pays.
                    """),
                    html.Br(),
                    dcc.Markdown("""
                    #### À propos

                    * Sources : 
                        * [Dataset des contenus Netflix](https://www.kaggle.com/shivamb/netflix-shows ) sur Kaggle
                        * [Internet Movie Database](https://www.imdb.com/)
                    * 2022 Mirabelle Abdulmassih, Alexandre James
                    """)
                ]),
            ]),      
        ])
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('ns-main-graph', 'figure'),
            [ dash.dependencies.Input('ns-crossfilter-yaxis-type', 'value'),
              dash.dependencies.Input('random-type', 'value')])(self.update_graph)

        self.app.callback(
            dash.dependencies.Output('ns-stats-popularity-series', 'figure'),
            [dash.dependencies.Input('ns-crossfilter-which-stats', 'value')])(self.get_stats_of_popularity_per_sensitivity)
        self.app.callback(
            dash.dependencies.Output('ns-stats-sensitivity-series', 'figure'),
            [dash.dependencies.Input('ns-crossfilter-which-stats', 'value')])(self.get_stats_of_sensitivity_per_popularity)


    def update_graph(self, yaxis_type, random_type):
        dfr = self.df.set_index('rating')
        dfr = dfr.T[self.ratings.keys()].T.reset_index()
        fig = px.scatter(dfr,
                         title="Poularité des programmes Netflix en fonction de leur degré de sensibilité",
                         y = "popularity" if len(random_type) == 0 else "approximate popularity",
                         x = "sensitivity" if len(random_type) == 0 else "approximate sensitivity", 
                         hover_name="title", log_y=True, color="rating", color_discrete_map = self.ratings)
        fig.update_layout(
                 yaxis = dict(title='Pourcentage de popularité (relative)',
                              type= 'linear' if yaxis_type == 'Linéaire' else 'log',
                              range=(0,100) if yaxis_type == 'Linéaire' 
                                              else (np.log10(1), np.log10(100)) 
                             ),
                 xaxis = dict(title="Degré de sensibilité", range=(0,1)),
                 margin={'l': 40, 'b': 30, 't': 40, 'r': 0},
                 hovermode='closest',
                 legend=dict(
                     title_text="Classification d'âge"
                 ),
             )
        return fig

    def get_data_in_ranges(self, what, ranges):
        data_in_ranges = []

        for i in range(0, len(ranges) - 1):
            data_in_ranges.append(np.logical_and(self.df[what] >= ranges[i], self.df[what] <= ranges[i + 1]))

        return data_in_ranges

    def get_stats_of_ranges(self, data_in_ranges, ranges, stats_of):
        ranges_df = pd.DataFrame([], [f'{ranges[i]} - {ranges[i + 1]}' for i in range(len(ranges) - 1)], [f'{stats_of} mean', f'{stats_of} median'])
        for i in range(len(data_in_ranges)):
            mean = self.df[data_in_ranges[i]][stats_of].mean()
            median = self.df[data_in_ranges[i]][stats_of].median()
            ranges_df.iloc[i, 0] = mean
            ranges_df.iloc[i, 1] = median
        return ranges_df

    def get_stats_of_popularity_per_sensitivity(self, stats):
        ranges = [i/10 for i in range(0, 11)]
        sensitivity_in_ranges = self.get_data_in_ranges('sensitivity', ranges)
        popularity_stats = self.get_stats_of_ranges(sensitivity_in_ranges, ranges=ranges, stats_of='popularity')
        return self.create_stats_graph(popularity_stats, f"popularity {stats}", "Degré de sensibilité", f"Popularité ({stats})")

    def get_stats_of_sensitivity_per_popularity(self, stats):
        ranges = [i for i in range(0, 101, 5)]
        popularity_in_ranges = self.get_data_in_ranges('popularity', ranges)
        sensitivity_stats = self.get_stats_of_ranges(popularity_in_ranges, ranges=ranges, stats_of='sensitivity')
        return self.create_stats_graph(sensitivity_stats, f"sensitivity {stats}", "Pourcentage de popularité", f"Sensibilité ({stats})")

    def create_stats_graph(self, df, what, xtitle, ytitle):
        def SetColor(y):
            if(y == df[what].min()):
                if(y == df[what].max()):
                    return "gold"
                return "yellow"
            elif(y == df[what].max()):
                return "red"
            else:
                return "orange"
        return {
            'data': [
            go.Bar(
                y = df[what],
                x = df.index,
                marker = dict(
                    color = list(map(SetColor, df[what]))
                )
            )
            ],
            'layout': {
                'height': 225,
                'margin': {'l': 50, 'b': 80, 'r': 10, 't': 20},
                'yaxis': {'title':ytitle},
                'xaxis': {'title':xtitle, 'showgrid': False}
            }
        }

    def get_film(self, hoverData):
        if hoverData == None:  # init value
            return self.df['title'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def film_chosen(self, hoverData):
        return self.get_film(hoverData)

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ns = NetflixStats
    ns.run(port=8055)
