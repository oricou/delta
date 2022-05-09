import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

STATS_ECOLES = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ecole.csv")
STATS_GENERALES = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "stats_generales",
    "stats_generales.csv",
)

stats_ecoles = pd.read_csv(STATS_ECOLES, index_col=[0])
stats_generales = stats_generales = pd.read_csv(STATS_GENERALES, index_col=[0])


def plot_inscrit_per_place():
    data = stats_generales.reset_index(drop=True)
    data["Inscriptions par place"] = (
        data["inscrits_nb"]
        / data["places"].str.extract(r".*([\d.]+).*").astype(float).squeeze()
    )
    data["Inscriptions par place"].replace([np.inf, -np.inf], np.nan, inplace=True)
    graph_df = (
        data.loc[data["Inscriptions par place"].dropna().index][
            ["filiere", "banque", "ecole", "Inscriptions par place"]
        ]
        .sort_values(by="Inscriptions par place", ascending=False)
        .groupby("banque")
        .mean()
        .sort_values(by="Inscriptions par place", ascending=False)
    )
    graph_df

    fig = px.bar(
        graph_df,
        y="Inscriptions par place",
        x=graph_df.index,
        text_auto=".2s",
        title="Etudiants inscrits par places disponibles pour chacune des banques",
    )
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    return fig
