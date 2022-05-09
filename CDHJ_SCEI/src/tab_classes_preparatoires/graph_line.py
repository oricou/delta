import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

STATS_LYCEE_FILE_PATH = os.path.join("data", "stats_lycees", "stats_lycees.csv")
PARIS_COORDS = (48.52, 2.19)
GRAPH_PRECISION = 1000
ROLLING_WINDOW = 100

RAYON_TERRE_KM = 6371

stats_lycees = pd.read_csv(STATS_LYCEE_FILE_PATH, index_col=[0])


def update_graph_distance_to_paris(year):

    yearly_stats = stats_lycees[stats_lycees["year"] == year]
    unique_yearly_stats = yearly_stats.drop_duplicates(subset=["etablissement"])
    distance_paris = unique_yearly_stats.apply(
        lambda row: RAYON_TERRE_KM
        * np.arccos(
            np.sin(np.radians(PARIS_COORDS[1])) * np.sin(np.radians(row["latitude"]))
            + np.cos(np.radians(PARIS_COORDS[1]))
            * np.cos(np.radians(row["latitude"]))
            * np.cos(np.radians(row["longitude"] - PARIS_COORDS[0]))
        ),
        axis=1,
    )
    min_distance, max_distance = min(distance_paris), max(distance_paris)

    pas = (max_distance - min_distance) / GRAPH_PRECISION
    x = np.arange(min_distance, max_distance, pas)
    data = pd.DataFrame(
        data={
            "Distance de Paris en Km": x,
            "Nombre de Classes Préparatoires au Km²": [
                distance_paris[distance_paris <= x_i].sum() / (np.pi * x_i**2)
                for x_i in x
            ],
        },
    )
    fig = go.Figure(
        data=px.line(
            data,
            x="Distance de Paris en Km",
            y="Nombre de Classes Préparatoires au Km²",
            title="Nombre de Classes Préparatoires au km² en fonction de la distance de Paris",
        ),
    )

    return (fig,)


def update_graph_student_distance_to_paris(year):

    yearly_stats = stats_lycees[stats_lycees["year"] == year]
    unique_yearly_stats = yearly_stats.drop_duplicates(subset=["etablissement"])
    distance_paris = unique_yearly_stats.apply(
        lambda row: RAYON_TERRE_KM
        * np.arccos(
            np.sin(np.radians(PARIS_COORDS[1])) * np.sin(np.radians(row["latitude"]))
            + np.cos(np.radians(PARIS_COORDS[1]))
            * np.cos(np.radians(row["latitude"]))
            * np.cos(np.radians(row["longitude"] - PARIS_COORDS[0]))
        ),
        axis=1,
    )

    min_distance, max_distance = min(distance_paris), max(distance_paris)

    pas = (max_distance - min_distance) / GRAPH_PRECISION
    x = np.arange(min_distance, max_distance, pas)
    data = pd.DataFrame(
        data={
            "Distance de Paris en Km": x,
            "Nombre moyen d'étudiants inscrits par Classe Préparatoire": [
                unique_yearly_stats[distance_paris <= x_i]["inscrits"].mean()
                for x_i in x
            ],
        },
    )
    fig = go.Figure(
        data=px.line(
            data,
            x="Distance de Paris en Km",
            y="Nombre moyen d'étudiants inscrits par Classe Préparatoire",
            title="Nombre moyen d'étudiants inscrits par Classe Préparatoire en fonction de la distance de Paris",
        ),
    )

    return (fig,)
