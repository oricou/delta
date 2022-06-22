from dash import html, dcc
from ps_ap_chessgames.src.labels import x_labels, y_labels
from ps_ap_chessgames.src.utils import drop_smallest_grp, to_int_list
from pandas.core.frame import DataFrame

white_button_style = {
    "background-color": "white",
    "border-color": "black",
    "color": "black",
    "font-weight": "bold",
    "font-size": "1em",
    "height": "3em",
    "width": "15em",
}

valid_button_style = white_button_style | {"margin-right": "30px"}

remove_button_style = {
    "background-color": "white",
    "color": "black",
    "font-weight": "bold",
    "font-size": "1em",
    "height": "1em",
    "width": "1em",
}


def make_layout(chess_games: DataFrame):
    sorted_time = chess_games.sort_values(
        "TimeControl",
        key=lambda serie: [to_int_list(format) for format in serie.str.split("+")],
    )
    grp_by_time = sorted_time.groupby("TimeControl", sort=False)
    grp_by_time = drop_smallest_grp(grp_by_time, "TimeControl")
    time_controls = list(grp_by_time.groups.keys())

    grp_by_opening = chess_games.groupby("Opening", sort=True)
    grp_by_opening = drop_smallest_grp(grp_by_opening, "Opening")
    openings = list(grp_by_opening.groups.keys())

    return html.Div(
        children=[
            html.Center(html.H2("Chess δata")),
            html.Div(id="cls_init", style={"display": "none"}),
            html.Label(
                ["Filtres:"], style={"font-weight": "bold", "text-align": "left"}
            ),
            dcc.Dropdown(options=x_labels, value=None, id="filters"),
            html.Div(
                id="filter_opts",
                children=[
                    html.Div(
                        id="slider",
                        children=[
                            html.Br(),
                            html.P(
                                "Selectionnez une tranche d'Elo:",
                                style={"font-weight": "bold"},
                            ),
                            html.Div(
                                [
                                    "Elo minimum:",
                                    dcc.Input(
                                        id="start_value",
                                        type="number",
                                        min=0,
                                        max=1000,
                                        value=0,
                                        style={
                                            "margin-left": "1%",
                                            "margin-right": "2%",
                                        },
                                        debounce=True,
                                    ),
                                    "Elo maximum:",
                                    dcc.Input(
                                        id="end_value",
                                        type="number",
                                        min=0,
                                        max=1000,
                                        value=1000,
                                        style={
                                            "margin-left": "1%",
                                        },
                                        debounce=True,
                                    ),
                                ],
                            ),
                            html.Br(),
                            dcc.RangeSlider(
                                id="fancy_slider",
                                min=0,
                                max=1000,
                                value=[0, 1000],
                            ),
                        ],
                        style={"display": "None"},
                    ),
                    html.Div(
                        id="time",
                        children=[
                            html.Br(),
                            html.Label(
                                ["Mode de jeu:"],
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.Dropdown(
                                options=time_controls,
                                value=None,
                                id="time_drop_down",
                            ),
                        ],
                        style={"display": "None"},
                    ),
                    html.Div(
                        id="opening",
                        children=[
                            html.Br(),
                            html.Label(
                                ["Ouverture:"],
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.Dropdown(
                                options=openings,
                                value=None,
                                id="opening_drop_down",
                            ),
                        ],
                        style={"display": "None"},
                    ),
                    html.Center(
                        id="filter_buttons",
                        children=[
                            html.Br(),
                            html.Button(
                                "Valider",
                                id="filter_valid",
                                disabled=True,
                                style=valid_button_style,
                            ),
                            html.Button(
                                "Annuler",
                                id="filter_cancel",
                                style=white_button_style | {"margin-left": "30px"},
                            ),
                        ],
                        style={"display": "None"},
                    ),
                ],
                style={"margin-left": "30px", "margin-right": "30px"},
            ),
            html.Br(),
            html.P(
                "Filtres actifs:",
                style={"font-weight": "bold"},
            ),
            html.Hr(style={"margin-top": "-14px"}),
            html.Br(),
            html.Div(
                html.Div(
                    children=[
                        html.Button(
                            "Elo blancs",
                            id="WhiteElo",
                            style={"margin-right": "15px", "display": "None"},
                        ),
                        html.Button(
                            "Elo noirs",
                            id="BlackElo",
                            style={"margin-right": "15px", "display": "None"},
                        ),
                        html.Button(
                            "Mode de jeu",
                            id="TimeControl",
                            style={"margin-right": "15px", "display": "None"},
                        ),
                        html.Button(
                            "Ouverture",
                            id="Opening",
                            style={"margin-right": "15px", "display": "None"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "margin-top": "-25px",
                        "margin-bottom": "-20px",
                    },
                ),
                id="active_filters",
                style={"display": "block"},
            ),
            html.Br(),
            html.Hr(),
            html.Br(),
            dcc.Graph(id="graph"),
            html.Label(["Axe X:"], style={"font-weight": "bold", "text-align": "left"}),
            dcc.Dropdown(
                options=x_labels,
                value="WhiteElo",
                id="x_drop_down",
            ),
            html.Label(["Axe Y:"], style={"font-weight": "bold", "text-align": "left"}),
            dcc.Dropdown(
                options=y_labels,
                value="WhiteWinrate",
                id="y_drop_down",
            ),
            html.Br(),
            html.H4("Extraction de données:", style={"text-decoration": "underline"}),
            html.Div(id="extracted_data"),
            html.Hr(),
            dcc.Markdown(
                """
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle.  
                Vous pouvez changez les données affichées en abscisses et ordonnées.  

                Filtres :  
                   * Ils vous permettent de ne visualiser que les éléments respectants certaines conditions.  
                   * Vous pouvez supprimer un filtre en cliquant sur celui-ci dans la section "Filtre actifs".  
                   * Lorsque vous parametrez un filtre il faut appuyer sur le bouton "Valider" 
                   pour que celui-ci prenne effet.  
                   * Les options de filtrages disponnibles changent en fonction des filtres déjà actifs 
                   (cela vous evite d'avoir aucune donné à visualiser).  

                
                Notes :
                   * Source : [Base de données de Novembre 2013 de lichess](https://database.lichess.org/).
                   * La base de donnée utilisée date de 2013 car les bases de données plus récentes 
                   sont trop lourdes (pandas ne peut pas les lire en temps raisonnable).
                """
            ),
        ],
    )
