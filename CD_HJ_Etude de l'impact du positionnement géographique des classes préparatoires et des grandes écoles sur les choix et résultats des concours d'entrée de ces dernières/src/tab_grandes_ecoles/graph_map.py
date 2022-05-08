import folium
import pandas as pd
import os
import plotly.express as px
import numpy as np

STATS_ECOLES = os.path.join("data", "ecole.csv")
STATS_GENERALES = os.path.join("data", "stats_generales", "stats_generales.csv")

stats_ecoles = pd.read_csv(STATS_ECOLES, index_col=[0])
stats_generales = stats_generales = pd.read_csv(STATS_GENERALES, index_col=[0])

france = folium.Map(location=[46, 2], zoom_start=6)


def display_graph_map_1():
    global france

    for _, ecole, latitude, longitude in (
        stats_ecoles[["ecole", "longitude", "latitude"]]
        .drop_duplicates(subset=["ecole"])
        .dropna()
        .itertuples()
    ):
        folium.Marker(
            (longitude, latitude), popup=ecole, icon=folium.Icon(color="blue")
        ).add_to(france)

    return france.get_root().render()


schools_stats = (
    stats_generales[
        ["year", "ecole", "latitude", "longitude", "inscrits_nb", "integres_nb"]
    ]
    .drop(
        stats_generales.dropna()[
            stats_generales.ecole.str.startswith("¥").dropna()
        ].index
    )
    .dropna()
)


def animate_graph_map_2(time_col):
    fig = px.scatter_mapbox(
        schools_stats,
        lat="latitude",
        lon="longitude",
        hover_name="ecole",
        size="inscrits_nb",
        animation_frame=time_col,
        mapbox_style="carto-positron",
        category_orders={time_col: list(np.sort(schools_stats[time_col].unique()))},
        zoom=5,
        title="Evolution du nombre d'étudiants inscrits par grandes écoles",
        height=1000,
    )
    return fig


def animate_graph_map_3(time_col):
    fig = px.scatter_mapbox(
        schools_stats,
        lat="latitude",
        lon="longitude",
        hover_name="ecole",
        size="integres_nb",
        animation_frame=time_col,
        mapbox_style="carto-positron",
        category_orders={time_col: list(np.sort(schools_stats[time_col].unique()))},
        zoom=5,
        title="Evolution du nombre d'étudiants intégrés par grandes écoles",
        height=1000,
    )
    return fig
