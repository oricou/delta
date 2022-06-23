import pandas as pd  # DataFrame
from dash import dcc, html, Input, Output, dash  # App
import plotly.express as px
import os  # Path management


class Formations:

    def __init__(self, application=None):

        self.main_layout = None
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Initial data, used for graph 3 (scatter)
        self.df = pd.read_csv(os.getcwd() + "/fwgp_formations/data/formations.csv", low_memory=False)

        # Data for graph 1 (sunburst)
        self.cursus_data = self.df.groupby(["Année universitaire",
                                            "Secteur disciplinaire",
                                            "Grande discipline"]).sum()
        self.cursus_data["Proportion Femmes"] = self.cursus_data["Dont femmes"] / \
                                                self.cursus_data["Nombre d\'étudiants"]
        self.cursus_data.reset_index([1, 2], inplace=True)

        # Data for graph 2 (treemap). Similar to graph  but grouping by differs.
        self.year_data = self.df.copy()
        self.year_data = self.year_data.groupby(["Année universitaire",
                                                 "Niveau dans le diplôme",
                                                 "Regroupement de diplômes",
                                                 "Grande discipline"]).sum()
        self.year_data["Proportion Femmes"] = self.year_data["Dont femmes"] / \
                                              self.year_data["Nombre d\'étudiants"]
        self.year_data.reset_index([1, 2, 3], inplace=True)

        # List of values used for sliders / dropdown
        self.years = self.df["Année universitaire"].unique().tolist()
        self.years.sort()
        self.scatter_levels = ["Niveau dans le diplôme", "Grande discipline", "Regroupement de diplômes"]

        # Main layout
        self.main_layout = html.Div(children=[html.Div(children=[
            # Title
            html.H1("Parité H/F dans les formations du supérieur Français, de 2006 à 2020"),
            # Introduction
            html.Div(children=[
                html.H6("Motivation :"),
                html.H6("Les lois se multiplient pour pousser la parité au sein des entreprises, et plus "
                        "particulièrement dans les professions de cadre supérieurs, et dans les instances "
                        "dirigeantes."),
                html.H6("Le gouvernement a notamment publié dans un communiqué de presse du 12 avril 2019, "
                        "un plan en 5 étapes, dont la première est d'améliorer \"L’orientation professionnelle des "
                        "jeunes femmes dès l’école, et la façon dont on peut les amener vers les formations "
                        "techniques et les carrières industrielles\"."),

                html.A("(source)", href="https://www.entreprises.gouv.fr/files/files/enjeux/mixite/communique-conseil"
                                        "-mixite-egalite-professionnelle-industrie.pdf"),
                html.H6("Cette page a pour but d'essayer de visualiser la parité H/F dans les études supérieures, "
                        "à différentes échelles, et au cours des années."),
                html.Br()]),
        ]),

            # First part, sunburst
            html.Div(children=[
                html.H4("Visualisation selon la grande discipline et niveau dans le diplôme"),
                dcc.Markdown("*Les deux figures sont interactives, cliquer sur un secteur d'un graphe le fera occuper "
                             "l'intégralité de l'espace alloué à la figure.*"),
                dcc.Markdown(
                    '*Utilisez le slider pour sélectionner l\'année scolaire*'
                ),
                dcc.Slider(id="year", min=0, max=len(self.years) - 1, value=0, step=1,
                           marks=dict(enumerate(self.years))),
                dcc.Graph(id="sunburst",
                          style={'display': 'inline-block', 'height': 720, 'width': 1280}),
                dcc.Graph(id="treemap",
                          style={'display': 'inline-block', 'width': 1280}),
                html.Br(),
                html.H6("Ces graphes permettent de visualiser la parité au sein des formations (représentée "
                        "par la couleur), en même temps que l'effectif relatif de la formation en question ("
                        "représenté par la taille des blocs). On voit que la parité n'est pas homogène au sein "
                        "des différents blocs, et que la parité générale elle-même est toujours au dessus de "
                        "50% en faveur des femmes. Mises à part les grandes disciplines de STAPS et de "
                        "Sciences et sciences de l'ingénieur, où les hommes sont majoritaires, les femmes sont "
                        "plus représentées que leurs homologues masculins.")
            ], style={'display': 'inline-block'}),

            # Second part, scatter
            html.Div(children=[
                html.H4("Évolution de la parité H/F en fonction de différents niveaux académiques au cours du temps"),
                html.Div(children=[
                    dcc.Graph(id="scatter",
                              style={'display': 'inline-block', 'width': 1280}),
                    dcc.Dropdown(self.scatter_levels, self.scatter_levels[0], id='level_selection'),
                    dcc.Markdown("*Utilisez le slider pour choisir parmi les différentes échelles*")],
                    style={'display': 'inline-block'}),
                dcc.Markdown("*Note : Une courbe part de 0 dans les premières années, dû à une absence de "
                             "données dans le jeu de donnée original jusqu'à une certaine année.*"),
                html.H6("Les graphiques par Grande discipline / Regroupement de diplômes sont très peu expressifs, "
                        "on voit une faible croissance au fil du temps de la proportions de femmes dans les études, "
                        "généralement aux alentours de 10%, sauf pour un top 3 (catégorie regroupement de diplômes) "
                        "occupé par :"),
                html.H6("-Les CPGE (principalement grâce aux formations de Lettres & Commerce), qui culminent à plus de"
                        " 81%, après une croissance de presque 25%."),
                html.H6("-Les Formations de santé, presque 72% avec une croissance de 16%"),
                html.H6("-Les HDR (habilitation à diriger des recherches), avec une croissance de 25% pour un taux de "
                        "40%"),
                html.Br(),
                html.H6("Les tendances selon le Niveau dans le diplôme sont beaucoup plus intéressantes, aussi nous y "
                        "retrouvons un phénomène de déphasage entre les différentes années, qui est logique étant "
                        "donné que les proportions auront tendances à se retrouver d'une année à l'autre dans le "
                        "niveau supérieur, au fur et à mesure que les étudiants passent les années."),
                html.H6("On remarque une montée progressive des premiers niveau depuis les années 2016 et plus, "
                        "qui se répercute progressivement dans les niveaux supérieurs par le même phénomène de "
                        "déphasage. Les études supérieures ne sont donc pas délaissées par les femmes, elles y sont "
                        "même en globalité dominantes (l'échelle du graphique est totalement au dessus de la valeur "
                        "seuil de 0.5)."),
                html.H6("Ces chiffres, associés aux différentes lois clés d'instauration d'égalité dans les "
                        "entreprises, telles que la loi Zimmermann-Copé de 2011 et la loi Rixain de décembre 2021, "
                        "laissent présager une montée en nombre des femmes dans les instances de direction des "
                        "entreprises des secteurs de la santé, du commerce et du droit, mais qui se montre encore "
                        "difficile pour les secteurs industriels ainsi que STAPS, qui sont à 37.5% et 32.7% de femmes "
                        "dans leurs formations respectives, en progression malgré tout."),
                html.H6(children=[html.A("Loi Rixain",
                                         href="https://travail-emploi.gouv.fr/actualites/l-actualite-du-ministere"
                                              "/article/la-loi-rixain-accelerer-la-participation-des-femmes-a-la-vie"
                                              "-economique-et"),
                                  html.A(" Loi Zimmermann-Copé",
                                         href="https://www.legifrance.gouv.fr/loda/id/JORFTEXT000023487662/")])
            ]),
            # About
            html.Div(children=[
                html.H4("À propos"),
                html.A("Source données : data enseignement sup-recherche (Gouvernement)",
                       href="https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-principaux" +
                            "-diplomes-et-formations-prepares-etablissements-publics/information/"),
                html.H6("Auteurs : Félix Wirth / Gaëtan Pusel")]),
        ])

        # Callback for the scatter, requiring column name to use it in new graph :
        @application.callback(
            Output('scatter', 'figure'),
            Input('level_selection', 'value')
        )
        def update_scatter(level):
            # Fetch required data
            scatter_data = self.df[["Année universitaire", level, "Nombre d'étudiants", "Dont femmes"]].copy()
            scatter_data["Année universitaire"] = scatter_data[["Année universitaire"]].applymap(
                lambda x: x.split('-')[0]
            )
            scatter_data["Année universitaire"] = pd.to_datetime(scatter_data["Année universitaire"])

            # Group by
            scatter_data = scatter_data.groupby(["Année universitaire", level]).sum()
            scatter_data["Proportion Femmes"] = scatter_data["Dont femmes"] / scatter_data["Nombre d'étudiants"]

            # Remote the unused data to fit the graph input format. NA are replaced by 0 to avoid errors. This case is
            # explained in markdown after the graph
            scatter_data = scatter_data.drop(columns=["Nombre d'étudiants", "Dont femmes"]).unstack(level).fillna(0)
            scatter_data = scatter_data["Proportion Femmes"]

            # Compute scatter
            fig = px.scatter(scatter_data,
                             trendline="rolling",
                             trendline_options=dict(window=1),
                             title="Tendance de parité H/F selon différentes échelles au cours des années",
                             hover_name=level
                             )
            # Remove raw points as we only want to keep the trending line for each different type of data
            fig.data = [t for t in fig.data if t.mode == "lines"]
            fig.update_traces(showlegend=True)
            return fig

        # Callback for the sunburst, using the year from slider :
        @application.callback(
            Output("sunburst", "figure"),
            Input("year", "value"))
        def update_sunburst(year):
            # Compute graph according to the selected year
            fig = px.sunburst(self.cursus_data.loc[self.years[year]],
                              path=[px.Constant("Formations"), "Grande discipline", "Secteur disciplinaire"],
                              values="Nombre d'étudiants",
                              color="Proportion Femmes",
                              color_continuous_scale='bluered',
                              range_color=[0.2, 0.9])
            return fig

        # Callback for treemap, using year as well
        @application.callback(
            Output("treemap", "figure"),
            Input("year", "value"))
        def update_treemap(year):
            # Compute graph according to the selected year
            fig = px.treemap(self.year_data.loc[self.years[year]],
                             path=[px.Constant("Formations"),
                                   "Niveau dans le diplôme",
                                   "Regroupement de diplômes",
                                   "Grande discipline"],
                             values="Nombre d'étudiants",
                             color="Proportion Femmes",
                             color_continuous_scale='bluered',
                             range_color=[0.2, 0.9])
            fig.update_coloraxes(showscale=False)
            return fig
