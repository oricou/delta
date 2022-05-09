from enum import unique
import folium
import pandas as pd
import plotly.express as px
import os

STATS_LYCEE_FILE_PATH = os.path.join("data", "stats_lycees", "stats_lycees.csv")

stats_lycees = pd.read_csv(STATS_LYCEE_FILE_PATH, index_col=[0])

france = folium.Map(location=[46, 2], zoom_start=6)


def update_graph_map_1(year):
    global france

    yearly_stats = stats_lycees[stats_lycees["year"] == year]
    unique_yearly_stats = yearly_stats.drop_duplicates(subset=["etablissement"])
    unique_yearly_stats = unique_yearly_stats[unique_yearly_stats["inscrits"] > 0]

    for _, lycee, latitude, longitude in (
        unique_yearly_stats[["etablissement", "latitude", "longitude"]]
        .dropna()
        .itertuples()
    ):
        old_stats = stats_lycees[stats_lycees["longitude"] == longitude][
            stats_lycees["latitude"] == latitude
        ]
        if old_stats[old_stats["year"] < year][old_stats["inscrits"] > 0].empty:
            folium.Marker(
                (longitude, latitude), popup=lycee, icon=folium.Icon(color="red")
            ).add_to(france)
        else:
            folium.Marker(
                (longitude, latitude), popup=lycee, icon=folium.Icon(color="blue")
            ).add_to(france)

    return (
        france.get_root().render(),
        "Géographie des classes préparatoires en {}".format(year),
    )


def update_graph_map_2(year):
    yearly_stats = stats_lycees[stats_lycees["year"] == year]

    yearly_stats["Pourcentage de filles inscrites"] = (
        yearly_stats["dont filles"] / yearly_stats["inscrits"]
    )

    unique_yearly_stats = yearly_stats.groupby("etablissement").agg(
        {
            "Pourcentage de filles inscrites": "mean",
            "inscrits": "sum",
            "longitude": "max",
            "latitude": "max",
        }
    )
    unique_yearly_stats["Pourcentage de filles inscrites"] = 100 * unique_yearly_stats[
        "Pourcentage de filles inscrites"
    ].round(2)

    unique_yearly_stats.drop_duplicates(subset=["latitude", "longitude"], inplace=True)

    fig = px.density_mapbox(
        unique_yearly_stats,
        lat="longitude",
        lon="latitude",
        z="Pourcentage de filles inscrites",
        radius=30,
        center=dict(lat=46, lon=2),
        zoom=4,
        mapbox_style="carto-darkmatter",
        height=800,
        title="Propotion de filles inscrites en {} par Classe Préparatoire".format(
            year
        ),
        hover_name=unique_yearly_stats.index,
        hover_data=["Pourcentage de filles inscrites", "inscrits"],
        color_continuous_scale=px.colors.diverging.Picnic,
        color_continuous_midpoint=unique_yearly_stats[
            "Pourcentage de filles inscrites"
        ].mean(),
    )

    return (fig,)
