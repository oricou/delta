import pandas as pd
import dash_bootstrap_components as dbc
import dash

from dash_layout import dash_app

import tab_grandes_ecoles.graph_map as graph_map
import tab_grandes_ecoles.graph_bar as graph_bar
import tab_grandes_ecoles.graph_pie as graph_pie

# ---------------------------------------------------------------------------- #
#                               TAB ARCHITECTURE                               #
# ---------------------------------------------------------------------------- #

tab_grandes_ecoles = dbc.Card(
    dbc.CardBody(
        [
            dbc.Accordion(
                [
                    # ---------------------------------------------------------------------------- #
                    #                                  FIRST PART                                  #
                    # ---------------------------------------------------------------------------- #
                    dbc.AccordionItem(
                        [
                            dash.html.H2(
                                children="Géographie des Grandes Ecoles",
                                id="grandes_ecoles_map_1_title",
                                style={"text-align": "left"},
                            ),
                            dash.html.Center(
                                dash.dcc.Loading(
                                    type="default",
                                    children=dash.html.Iframe(
                                        id="grandes_ecoles_map_1",
                                        width="50%",
                                        height="500px",
                                        srcDoc=graph_map.display_graph_map_1(),
                                    ),
                                )
                            ),
                            dash.html.Div(
                                [
                                    dbc.Button(
                                        "Afficher les commentaires",
                                        id="grandes_ecoles_button_comment_1",
                                        size="lg",
                                        color="secondary",
                                        className="me-1",
                                    ),
                                    dbc.Collapse(
                                        dbc.Card(
                                            children=[
                                                dash.dcc.Markdown(
                                                    "* On remarque qu'à l'instar des Classes Préparatoires, les Grandes Ecoles sont majoritairement regroupées dans Paris et ses alentours. Cependant, leur localisation est d'avantage dispersée et on observe nombre d'entre elles dans d'autres pays, notament la cote est des Etats-Unis."
                                                )
                                            ],
                                            color="success",
                                            outline=True,
                                        ),
                                        id="grandes_ecoles_collapse_comment_1",
                                        is_open=False,
                                    ),
                                    dash.html.Br(),
                                ],
                                className="d-grid gap-2 col-6 mx-auto",
                            ),
                        ],
                        title="Géographie des Grandes Ecoles",
                    ),
                    # ---------------------------------------------------------------------------- #
                    #                                  SECOND PART                                 #
                    # ---------------------------------------------------------------------------- #
                    dbc.AccordionItem(
                        [
                            dash.html.H2(
                                children="Offre et demande de l'éducation supérieure",
                                style={"text-align": "left"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dash.dcc.Loading(
                                            dash.dcc.Graph(
                                                id="grandes_ecoles_map_2",
                                                figure=graph_map.animate_graph_map_2(
                                                    time_col="year"
                                                ),
                                            ),
                                        ),
                                    ),
                                    dbc.Col(
                                        dash.dcc.Loading(
                                            dash.dcc.Graph(
                                                id="grandes_ecoles_map_3",
                                                figure=graph_map.animate_graph_map_3(
                                                    time_col="year"
                                                ),
                                            ),
                                        ),
                                    ),
                                ]
                            ),
                            dbc.Row(
                                dash.dcc.Loading(
                                    type="default",
                                    children=dash.dcc.Graph(
                                        id="grandes_ecoles_graph_1",
                                        figure=graph_bar.plot_inscrit_per_place(),
                                    ),
                                )
                            ),
                            dash.html.Div(
                                [
                                    dbc.Button(
                                        "Afficher les commentaires",
                                        id="grandes_ecoles_button_comment_2",
                                        size="lg",
                                        color="secondary",
                                        className="me-1",
                                    ),
                                    dbc.Collapse(
                                        dbc.Card(
                                            children=[
                                                dash.dcc.Markdown(
                                                    "* Les dispartions soudaines *(Notament 2015-2016)* et les variations imprévisibles de la taille des points *(Notament 2018-2019)* d'une année sur l'autre sur les deux premiers graphes nous laisse supposer **des données collectées de manière non homogène**."
                                                ),
                                                dash.dcc.Markdown(
                                                    "* Malgré la piètre qualité des données, on peut observer que le nombre d'étudiants inscrits a eu tendance à augmenter tandis que le nombre d'étudiants ayant intégrés semble être resté stable, ce qui laisse deviner une difficulté croissante des concours au cours des 18 dernières années."
                                                ),
                                                dash.dcc.Markdown(
                                                    "* Il est intéressant de constater que si une quantité considérable des Classes Préparatoires se trouvent à Paris, les inscriptions semblent géographiquement mieux réparties d'après la première carte. On peut ainsi supposer que certains étudiants formés dans la capitale ont préféré passer les concours sur une autre partie du territoire, éventuellement pour augmenter leurs chances. Cette constatation pourra être prises en compte lors de l'analyse des résultats aux concours par département."
                                                ),
                                                dash.dcc.Markdown(
                                                    "* Il est intéressant de constater que en ne considérant que ce rapport Nombre d'Inscriptions sur Nombre de Places_disponibles classe les Concours Communs Polytechniques en tête des concours les plus difficiles. Ce classement ne prend cependant pas en compte les intégrations excédentaires des écoles qui sont, après étude du jeu de donnée, monnaie courante."
                                                ),
                                                dash.dcc.Markdown(
                                                    "* Un graphique similaire mettant en relation le rang du dernier integré et le nombre d'inscrit aurait également pu être intéressant mais le trop grand nombre de données manquante ne nous l'a hélas pas rendu possible."
                                                ),
                                            ],
                                            color="success",
                                            outline=True,
                                        ),
                                        id="grandes_ecoles_collapse_comment_2",
                                        is_open=False,
                                    ),
                                    dash.html.Br(),
                                ],
                                className="d-grid gap-2 col-6 mx-auto",
                            ),
                        ],
                        title="Offre et demande de l'éducation supérieure",
                    ),
                    # ---------------------------------------------------------------------------- #
                    #                                  THIRD PART                                  #
                    # ---------------------------------------------------------------------------- #
                    dbc.AccordionItem(
                        [
                            dash.html.H2(
                                children="Résultats aux Concours en fonction du lieu d'apprentissage",
                                style={"text-align": "left"},
                            ),
                            dash.dcc.Dropdown(
                                id="grandes_ecoles_dropdown_pie_1",
                                options=[
                                    {"label": str(concours), "value": concours}
                                    for concours in pd.unique(
                                        graph_pie.stats_lycees["concours"]
                                    )
                                ],
                                multi=False,
                                value=graph_pie.stats_lycees["concours"].iloc[0],
                                style={"width": "40%"},
                            ),
                            dash.dcc.Loading(
                                type="default",
                                children=dash.dcc.Graph(
                                    id="grandes_ecoles_graph_pie_1",
                                    figure=graph_pie.update_pie(
                                        graph_pie.stats_lycees["concours"].iloc[0],
                                        min(graph_pie.stats_lycees["year"]),
                                    ),
                                ),
                            ),
                            dbc.Alert(
                                "Aucune donnée n'est disponible pour ce coucours sur la période sélectionnée.",
                                id="grandes_ecoles_alert_pie_1",
                                dismissable=True,
                                is_open=False,
                                color="danger",
                            ),
                            dash.dcc.Slider(
                                min(graph_pie.stats_lycees["year"]),
                                max(graph_pie.stats_lycees["year"]),
                                1,
                                marks={
                                    i: str(i)
                                    for i in range(
                                        min(graph_pie.stats_lycees["year"]),
                                        max(graph_pie.stats_lycees["year"]),
                                    )
                                },
                                value=min(graph_pie.stats_lycees["year"]),
                                id="grandes_ecoles_slide_pie_1",
                            ),
                            dash.html.Div(
                                [
                                    dbc.Button(
                                        "Afficher les commentaires",
                                        id="grandes_ecoles_button_comment_3",
                                        size="lg",
                                        color="secondary",
                                        className="me-1",
                                    ),
                                    dbc.Collapse(
                                        dbc.Card(
                                            children=[
                                                dash.dcc.Markdown(
                                                    "* La catégorie *Autres régions dont la proportion est inférieure à la moyenne* correspond à la somme des scores de ces autres régions et a vocation à éviter que les graphes ne soient surchargés*"
                                                ),
                                            ],
                                            color="success",
                                            outline=True,
                                        ),
                                        id="grandes_ecoles_collapse_comment_3",
                                        is_open=False,
                                    ),
                                    dash.html.Br(),
                                ],
                                className="d-grid gap-2 col-6 mx-auto",
                            ),
                        ],
                        title="Offre et demande de l'éducation supérieure",
                    ),
                ],
                start_collapsed=True,
            ),
        ]
    ),
    className="h-0",
)

# ---------------------------------------------------------------------------- #
#                               CALLBACK SECTION                               #
# ---------------------------------------------------------------------------- #


@dash_app.callback(
    dash.Output("grandes_ecoles_graph_pie_1", "figure"),
    dash.Output("grandes_ecoles_alert_pie_1", "is_open"),
    dash.Input("grandes_ecoles_dropdown_pie_1", "value"),
    dash.Input("grandes_ecoles_slide_pie_1", "value"),
)
def update_pie(concours, year):
    return graph_pie.update_pie(concours, year)


@dash_app.callback(
    dash.Output("grandes_ecoles_collapse_comment_1", "is_open"),
    [dash.Input("grandes_ecoles_button_comment_1", "n_clicks")],
    [dash.State("grandes_ecoles_collapse_comment_1", "is_open")],
)
def show_comment_1(n, is_open):
    if n:
        return not is_open
    return is_open


@dash_app.callback(
    dash.Output("grandes_ecoles_collapse_comment_2", "is_open"),
    [dash.Input("grandes_ecoles_button_comment_2", "n_clicks")],
    [dash.State("grandes_ecoles_collapse_comment_2", "is_open")],
)
def show_comment_2(n, is_open):
    if n:
        return not is_open
    return is_open


@dash_app.callback(
    dash.Output("grandes_ecoles_collapse_comment_3", "is_open"),
    [dash.Input("grandes_ecoles_button_comment_3", "n_clicks")],
    [dash.State("grandes_ecoles_collapse_comment_3", "is_open")],
)
def show_comment_3(n, is_open):
    if n:
        return not is_open
    return is_open
