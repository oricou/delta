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

def get_colors(traffic: int, max_traffic: int):
    return list_colors[round(traffic/max_traffic * (len(list_colors)-1))]

def make_layout() -> html.Div:
    return html.Div(
            children=[
                html.H3(children="Régularité des Grandes Lignes de TGV de la SNCF"),
                html.Div(
                    [
                        html.Iframe(
                            id="tgv-main-graph", srcDoc=None, width="100%", height="600"
                        ),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Div(
                    [
                        dcc.Slider(
                            0,
                            4,
                            1,
                            id="year-slider",
                            marks={i: str(i) for i in range(4)},
                            value=2,
                            updatemode='drag'
                        )
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