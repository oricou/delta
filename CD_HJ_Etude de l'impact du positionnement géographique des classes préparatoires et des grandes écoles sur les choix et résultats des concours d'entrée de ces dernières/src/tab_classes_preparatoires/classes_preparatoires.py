import dash_bootstrap_components as dbc
import dash
import os

from dash_layout import dash_app

import tab_classes_preparatoires.graph_map as graph_map
import tab_classes_preparatoires.graph_line as graph_line

# ---------------------------------------------------------------------------- #
#                           TAB ARCHITECTURE SECTION                           #
# ---------------------------------------------------------------------------- #

tab_classes_preparatoires = dbc.Card(
    dbc.CardBody(
        [
            # ---------------------------------------------------------------------------- #
            #                                  FIRST PART                                  #
            # ---------------------------------------------------------------------------- #
            dash.html.H2(
                children="Géographie des classes préparatoires en {}".format(
                    graph_map.stats_lycees.year.min()
                ),
                id="classes_preparatoires_map_1_title",
                style={"text-align": "left"},
            ),
            dash.html.Center(
                dash.dcc.Loading(
                    type="default",
                    children=dash.html.Iframe(
                        id="classes_preparatoires_map_1",
                        width="50%",
                        height="500px",
                    ),
                ),
            ),
            dash.dcc.Dropdown(
                id="classes_preparatoires_dropdown_map_1",
                options=[
                    {"label": str(year), "value": year}
                    for year in range(
                        graph_map.stats_lycees.year.min(),
                        graph_map.stats_lycees.year.max() + 1,
                    )
                ],
                multi=False,
                value=graph_map.stats_lycees.year.min(),
                style={"width": "40%"},
            ),
            dbc.Alert(
                "Sur la carte ci-dessus, les lycées ayant pour la première fois cette année formé des élèves participant aux concours sont indiquées en rouge.",
                color="primary",
            ),
            dash.html.Div(
                [
                    dbc.Button(
                        "Afficher les commentaires",
                        id="classes_preparatoires_button_comment_1",
                        size="lg",
                        color="secondary",
                        className="me-1",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            children=[
                                dash.dcc.Markdown(
                                    "* On remarque que le nombre de Classes Préparatoires n'a cessé de croitre au cours des 18 dernières années."
                                ),
                                dash.dcc.Markdown(
                                    "* On peut noter que si Paris profite d'une impressionnante densité de Classes Préparatoires, les autres grandes villes n'en sont pas autant surchargées."
                                ),
                                dash.dcc.Markdown(
                                    "* On identifie sans peine la *diagonale du vide*, zone géographique qui découpe la France du sud-ouest au nord-est et dont les Classes Préparatoires semblent singulièrement absentes."
                                ),
                            ],
                            color="success",
                            outline=True,
                        ),
                        id="classes_preparatoires_collapse_comment_1",
                        is_open=False,
                    ),
                    dash.html.Br(),
                ],
                className="d-grid gap-2 col-6 mx-auto",
            ),
            # ---------------------------------------------------------------------------- #
            #                                  SECOND PART                                 #
            # ---------------------------------------------------------------------------- #
            dash.html.H2(
                children="Accès à la formation en fonction du lieu",
                style={"text-align": "left"},
            ),
            dash.html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dash.dcc.Loading(
                                    type="default",
                                    children=dash.dcc.Graph(
                                        id="classes_preparatoires_graph_1", figure={}
                                    ),
                                )
                            ),
                            dbc.Col(
                                dash.dcc.Loading(
                                    type="default",
                                    children=dash.dcc.Graph(
                                        id="classes_preparatoires_graph_2", figure={}
                                    ),
                                )
                            ),
                        ]
                    ),
                ]
            ),
            dash.html.Div(
                [
                    dbc.Button(
                        "Afficher les commentaires",
                        id="classes_preparatoires_button_comment_2",
                        size="lg",
                        color="secondary",
                        className="me-1",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            children=[
                                dash.dcc.Markdown(
                                    "* Paris se trouvant à envrion 700km de sa plus lointaine frontière terrestre, il est cohérent de remarquer la décroissance du nombre de Classes Préparatoires au km² à partir de cette distance."
                                ),
                                dash.dcc.Markdown(
                                    "* On remarque que quelle que soit l'année, Paris profite du plus grand nombre de Classes Préparatoires au km², mais aussi du plus grand nombre d'élèves par établissement, ce qui peut nuire à la qualité de l'apprentissage."
                                ),
                                dash.dcc.Markdown(
                                    "* On note une décroissance générale du nombre d'élève par établissement à mesure que l'on s'éloigne de la capitale."
                                ),
                            ],
                            color="success",
                            outline=True,
                        ),
                        id="classes_preparatoires_collapse_comment_2",
                        is_open=False,
                    ),
                    dash.html.Br(),
                ],
                className="d-grid gap-2 col-6 mx-auto",
            ),
            # ---------------------------------------------------------------------------- #
            #                                  THIRD PART                                  #
            # ---------------------------------------------------------------------------- #
            dash.html.H2(
                children="L'accès à la formation en fontion du sexe",
                style={"text-align": "left"},
            ),
            dash.html.Center(
                dash.html.Div(
                    dash.dcc.Loading(
                        type="default",
                        children=dash.dcc.Graph(
                            id="classes_preparatoires_map_2", figure={}
                        ),
                    )
                ),
            ),
            dbc.Alert(
                "Sur la carte ci-dessus, la taille des points et leur impact sur la densité de coloration correspond à la proportion de filles inscrites par Classe Préparatoires. La couleur neutre (Le blanc) correspond a des Classes Préparatoires dont la proportion de filles inscrites est dans la moyenne.",
                color="primary",
            ),
            dash.html.Div(
                [
                    dbc.Button(
                        "Afficher les commentaires",
                        id="classes_preparatoires_button_comment_3",
                        size="lg",
                        color="secondary",
                        className="me-1",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            children=[
                                dash.dcc.Markdown(
                                    "* La couleur blanche correspondant à des Classes Préparatoires dont la proportion de filles inscrites est dans la moyenne, on peut constater que cette proportion n'a que modérement évolué au cours de 18 dernières années, passant d'environ **19% en 2004** à **23% en 2019**"
                                ),
                                dash.dcc.Markdown(
                                    "* Cette carte confirme également nos premières observation quant à la répartitions des Classes Préparatoires sur le territoire : En réinitialisant le niveau de zoom, on observe une densité nettement supérieure au niveau de **Paris** tandis qu'on distingue à peine les plus grandes villes, **Marseille, Lyon, Nancy ou Lille.**"
                                ),
                            ],
                            color="success",
                            outline=True,
                        ),
                        id="classes_preparatoires_collapse_comment_3",
                        is_open=False,
                    ),
                    dash.html.Br(),
                ],
                className="d-grid gap-2 col-6 mx-auto",
            ),
        ]
    ),
    className="h-0",
)

# ---------------------------------------------------------------------------- #
#                               CALLBACK SECTION                               #
# ---------------------------------------------------------------------------- #


@dash_app.callback(
    [
        dash.Output(
            component_id="classes_preparatoires_map_1", component_property="srcDoc"
        ),
        dash.Output(
            component_id="classes_preparatoires_map_1_title",
            component_property="children",
        ),
    ],
    [
        dash.Input(
            component_id="classes_preparatoires_dropdown_map_1",
            component_property="value",
        )
    ],
)
def update_map(year):
    return graph_map.update_graph_map_1(year)


@dash_app.callback(
    [
        dash.Output(
            component_id="classes_preparatoires_graph_1", component_property="figure"
        ),
    ],
    [
        dash.Input(
            component_id="classes_preparatoires_dropdown_map_1",
            component_property="value",
        )
    ],
)
def update_graph_distance_to_paris(year):
    return graph_line.update_graph_distance_to_paris(year)


@dash_app.callback(
    [
        dash.Output(
            component_id="classes_preparatoires_graph_2", component_property="figure"
        ),
    ],
    [
        dash.Input(
            component_id="classes_preparatoires_dropdown_map_1",
            component_property="value",
        )
    ],
)
def update_graph_distance_to_paris_2(year):
    return graph_line.update_graph_student_distance_to_paris(year)


@dash_app.callback(
    [
        dash.Output(
            component_id="classes_preparatoires_map_2", component_property="figure"
        ),
    ],
    [
        dash.Input(
            component_id="classes_preparatoires_dropdown_map_1",
            component_property="value",
        )
    ],
)
def update_graph_distance_to_paris_2(year):
    return graph_map.update_graph_map_2(year)


@dash_app.callback(
    dash.Output("classes_preparatoires_collapse_comment_1", "is_open"),
    [dash.Input("classes_preparatoires_button_comment_1", "n_clicks")],
    [dash.State("classes_preparatoires_collapse_comment_1", "is_open")],
)
def show_comment_1(n, is_open):
    if n:
        return not is_open
    return is_open


@dash_app.callback(
    dash.Output("classes_preparatoires_collapse_comment_2", "is_open"),
    [dash.Input("classes_preparatoires_button_comment_2", "n_clicks")],
    [dash.State("classes_preparatoires_collapse_comment_2", "is_open")],
)
def show_comment_2(n, is_open):
    if n:
        return not is_open
    return is_open


@dash_app.callback(
    dash.Output("classes_preparatoires_collapse_comment_3", "is_open"),
    [dash.Input("classes_preparatoires_button_comment_3", "n_clicks")],
    [dash.State("classes_preparatoires_collapse_comment_3", "is_open")],
)
def show_comment_3(n, is_open):
    if n:
        return not is_open
    return is_open
