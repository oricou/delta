import os

from dash import dcc
from dash import html

cur_path = os.path.dirname(__file__)
a_propos_path = os.path.join(cur_path, "a-propos.md")

list_colors = [
    "#0000FF",
    "#1200FF",
    "#2400FF",
    "#3500FF",
    "#4700FF",
    "#5800FF",
    "#6A00FF",
    "#7C00FF",
    "#8D00FF",
    "#9F00FF",
    "#B000FF",
    "#C200FF",
    "#D400FF",
    "#E500FF",
    "#F700FF",
    "#FF00F6",
    "#FF00E4",
    "#FF00D3",
    "#FF00C1",
    "#FF00AF",
    "#FF009E",
    "#FF008C",
    "#FF007B",
    "#FF0069",
    "#FF0057",
    "#FF0046",
    "#FF0034",
    "#FF0023",
    "#FF0011",
    "#FF0000",
]

y_axis = [
    "Nombre de circulations prévues",
    "Nombre de trains annulés",
    "Retard moyen de tous les trains au départ",
    "Retard moyen de tous les trains à l'arrivée",
    "Nombre de trains en retard à l'arrivée",
    "Nombre trains en retard > 15min",
    "Nombre trains en retard > 30min",
    "Nombre trains en retard > 60min",
]


def get_color(traffic: int, max_traffic: int):
    return list_colors[round(traffic / max_traffic * (len(list_colors) - 1))]


def make_layout() -> html.Div:
    return html.Div(
        children=[
            html.Div(
                [
                    html.H1(children="Trafic et régularité des TGV de la SNCF"),
                ],
                style={"justifyContent": "center"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Iframe(
                                id="tgv-main-graph",
                                srcDoc=None,
                                width="100%",
                                height="600",
                            ),
                            dcc.Graph(id="hist-graph"),
                        ],
                        style={"width": "90%", "display": "inline-block"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Graphique",
                                style={
                                    "display": "inline-block",
                                    "margin-right": "5px",
                                },
                            ),
                            html.I(
                                className="fas fa-question-circle",
                                title="Choisissez le type de graphique avec le type de données en abscisse.",
                            ),
                            dcc.RadioItems(
                                id="plot-switch",
                                options=["Trajet", "Gare"],
                                value="Trajet",
                                labelStyle={"display": "block"},
                            ),
                            html.Br(),
                            html.Div(
                                "Type",
                                style={
                                    "display": "inline-block",
                                    "margin-right": "5px",
                                },
                            ),
                            html.I(
                                className="fas fa-question-circle",
                                title="Données brut ou normalisée. Données non normalisables pour certaines valeurs observées.",
                            ),
                            dcc.RadioItems(
                                id="datatype-switch",
                                options=[
                                    {"label": "Brut", "value": "Brut"},
                                    {"label": "Taux (%)", "value": "Taux"},
                                ],
                                value="Brut",
                                labelStyle={"display": "block"},
                            ),
                            html.Br(),
                            html.Div("Filtre"),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.RangeSlider(
                                                id="debit-filter-type-slider",
                                                min=0,
                                                max=100000,
                                                value=[0, 100000],
                                                vertical=True,
                                            )
                                        ],
                                    ),
                                ]
                            ),
                        ],
                        style={"margin-left": "20px"},
                    ),
                ],
                style={"width": "100%", "display": "flex", "justifyContent": "center"},
            ),
            html.Div(
                [
                    dcc.Slider(
                        0,
                        4,
                        1,
                        id="tgv-year-slider",
                        marks={i: str(2018 + i) for i in range(5)},
                        value=2,
                        updatemode="drag",
                    ),
                    html.Div(
                        [
                            html.Div(
                                "Valeur Observée",
                                style={
                                    "display": "inline-block",
                                    "margin-right": "5px",
                                },
                            ),
                            html.I(
                                className="fas fa-question-circle",
                                title="Choisissez le type de données etudié en ordonée.",
                            ),
                            dcc.Dropdown(
                                id="tgv-y-axis-dropdown",
                                options=[{"label": i, "value": i} for i in y_axis],
                                value="Nombre de circulations prévues",
                            ),
                        ],
                        # style={"width": "6em", "padding": "2em 0px 0px 0px"},
                    ),
                ]
            ),
            html.Br(),
            dcc.Markdown(open(a_propos_path).read()),
        ],
        style={
            "backgroundColor": "white",
            "padding": "10px 50px 10px 50px",
        },
    )


def get_stylesheet():
    return [
        {
            "href": "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
            "rel": "stylesheet",
            "integrity": "sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
            "crossorigin": "anonymous",
        }
    ]
