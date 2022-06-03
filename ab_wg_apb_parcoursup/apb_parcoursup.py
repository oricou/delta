import dash
from dash import dcc
from dash import html
from .data.get_data import get_data, about_md, documentation_lexique
from .figures import (
    repartition_map,
    formation_details_sunburst,
    categories_years_histogram,
    women_men_histogram,
)


class APB_PARCOURSUP:
    def __init__(self, application=None):
        # Import data
        self.df = get_data()

        # Dash layout
        self.main_layout = html.Div(
            className="app-body",
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="twelve columns",
                            children=[
                                html.Div(
                                    style={"float": "left"},
                                    children=[
                                        html.H1(
                                            "Évolution des voeux Parcoursup/APB depuis 2016"
                                        ),
                                        html.H4("Project de Python pour le Big Data"),
                                        dcc.Markdown(
                                            """Disponible aussi sur [https://pybd-project.herokuapp.com/](https://pybd-project.herokuapp.com/)"""
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                dcc.Tabs(
                    id="tab",
                    children=[
                        dcc.Tab(
                            label="Présentation des données",
                            children=[
                                # Control panel
                                html.Div(
                                    className="row",
                                    id="control-panel",
                                    style={
                                        "position": "sticky",
                                        "top": 10,
                                        "width": "100%",
                                        "zIndex": 12000,
                                    },
                                    children=[
                                        html.Div(
                                            className="six columns pretty_container",
                                            children=[
                                                html.Label("Choisissez une période"),
                                                dcc.RangeSlider(
                                                    2016,
                                                    2021,
                                                    1,
                                                    id="years",
                                                    value=[2016, 2021],
                                                    marks={
                                                        i: str(i)
                                                        for i in range(2016, 2022)
                                                    },
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="six columns pretty_container",
                                            children=[
                                                html.Label("Choisissez une formation"),
                                                html.Div(
                                                    [
                                                        dcc.Dropdown(
                                                            id="formations",
                                                            placeholder="Choisissez une formation",
                                                            options=[
                                                                {
                                                                    "label": "Toutes les formations",
                                                                    "value": "Toutes les formations",
                                                                },
                                                                {
                                                                    "label": "Autre formation",
                                                                    "value": "Autre formation",
                                                                },
                                                                {
                                                                    "label": "BTS",
                                                                    "value": "BTS",
                                                                },
                                                                {
                                                                    "label": "CPGE",
                                                                    "value": "CPGE",
                                                                },
                                                                {
                                                                    "label": "DUT / BUT",
                                                                    "value": "DUT",
                                                                },
                                                                {
                                                                    "label": "EFTS",
                                                                    "value": "EFTS",
                                                                },
                                                                {
                                                                    "label": "Ecole d'Ingénieur",
                                                                    "value": "Ecole d'Ingénieur",
                                                                },
                                                                {
                                                                    "label": "Ecole de Commerce",
                                                                    "value": "Ecole de Commerce",
                                                                },
                                                                {
                                                                    "label": "IFSI",
                                                                    "value": "IFSI",
                                                                },
                                                                {
                                                                    "label": "Licence",
                                                                    "value": "Licence",
                                                                },
                                                                {
                                                                    "label": "Management",
                                                                    "value": "Management",
                                                                },
                                                                {
                                                                    "label": "PACES / PASS / Licence L.AS",
                                                                    "value": "PACES",
                                                                },
                                                            ],
                                                            value="Toutes les formations",
                                                            multi=False,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="eight columns pretty_container",
                                            children=[
                                                html.Label(
                                                    id="france_map_title",
                                                    children="Nombre d'étudiants par type de diplômes de 2016 à 2021",
                                                ),
                                                dcc.Graph(
                                                    id="france_map",
                                                    figure=repartition_map(
                                                        self.df,
                                                        ["Toutes les formations"],
                                                        [2016, 2022],
                                                    )[0],
                                                    config={
                                                        "modeBarButtonsToRemove": [
                                                            "lasso2d",
                                                            "select2d",
                                                        ]
                                                    },
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="four columns pretty_container",
                                            children=[
                                                html.Label(
                                                    id="formation_details_title",
                                                    children="Répartition géographique des vœux des étudiants de 2016 à 2021",
                                                ),
                                                dcc.Graph(
                                                    id="formation_details_figure",
                                                    figure=formation_details_sunburst(
                                                        self.df,
                                                        ["Toutes les formations"],
                                                        [2016, 2022],
                                                    )[0],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="three columns pretty_container",
                                            children=[
                                                html.Label(
                                                    "Sélectionnez une échelle pour l'axe des ordonnées"
                                                ),
                                                html.Br(),
                                                dcc.RadioItems(
                                                    options=[
                                                        {
                                                            "label": "Décimal",
                                                            "value": False,
                                                        },
                                                        {
                                                            "label": "Logarithmique",
                                                            "value": True,
                                                        },
                                                    ],
                                                    value=False,
                                                    id="histogram_scale",
                                                ),
                                                html.Hr(),
                                                dcc.Checklist(
                                                    id="women_men_enable",
                                                    options=[
                                                        {
                                                            "label": " Afficher la répartition homme/femme (Cela peut prendre quelques minutes)",
                                                            "value": True,
                                                        }
                                                    ],
                                                    value=[],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="nine columns pretty_container",
                                            children=[
                                                html.Label(
                                                    id="category_year_title",
                                                    children="Nombre d'étudiant par année par type de diplôme de 2016 à 2021",
                                                ),
                                                dcc.Graph(
                                                    id="category_year_histogram",
                                                    figure=categories_years_histogram(
                                                        self.df,
                                                        ["Toutes les formations"],
                                                        [2016, 2022],
                                                        False,
                                                    )[0],
                                                    config={
                                                        "modeBarButtonsToRemove": [
                                                            "lasso2d",
                                                            "select2d",
                                                        ]
                                                    },
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="Documentation et lexique",
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="fix columns pretty_container",
                                            children=[
                                                dcc.Markdown(
                                                    children=documentation_lexique
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Hr(),
                dcc.Markdown(children=about_md),
            ],
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Callbacks

        self.app.callback(
            [
                dash.dependencies.Output("france_map", "figure"),
                dash.dependencies.Output("france_map_title", "children"),
                dash.dependencies.Output("formation_details_figure", "figure"),
                dash.dependencies.Output("formation_details_title", "children"),
            ],
            [
                dash.dependencies.Input("years", "value"),
                dash.dependencies.Input("formations", "value"),
            ],
        )(self.update_map_sunburst)

        self.app.callback(
            [
                dash.dependencies.Output("category_year_histogram", "figure"),
                dash.dependencies.Output("category_year_title", "children"),
            ],
            [
                dash.dependencies.Input("years", "value"),
                dash.dependencies.Input("formations", "value"),
                dash.dependencies.Input("histogram_scale", "value"),
                dash.dependencies.Input("women_men_enable", "value"),
            ],
        )(self.update_histogram)

    def update_map_sunburst(self, years, formations):
        # Enable to chose only one year
        years[1] += 1

        # Handle formation group
        if formations == "PACES":
            formations = ["PACES", "PASS", "LicenceLas"]
        elif formations == "DUT":
            formations = ["DUT", "BUT"]
        else:
            formations = [formations]

        france_map, france_map_title = repartition_map(self.df, formations, years)

        formation_details_figure, formation_details_title = formation_details_sunburst(
            self.df, formations, years
        )

        return [
            france_map,
            france_map_title,
            formation_details_figure,
            formation_details_title,
        ]

    def update_histogram(self, years, formations, histogram_scale, women_men_enable):
        # Enable to chose only one year
        years[1] += 1

        # Handle formation group
        if formations == "PACES":
            formations = ["PACES", "PASS", "LicenceLas"]
        elif formations == "DUT":
            formations = ["DUT", "BUT"]
        else:
            formations = [formations]

        if women_men_enable and women_men_enable[0]:
            category_year_histogram, category_year_title = women_men_histogram(
                self.df, formations, years
            )
        else:
            category_year_histogram, category_year_title = categories_years_histogram(
                self.df, formations, years, histogram_scale
            )

        return [category_year_histogram, category_year_title]


if __name__ == "__main__":
    project = APB_PARCOURSUP()
    project.app.run_server(debug=True, port=8051)
