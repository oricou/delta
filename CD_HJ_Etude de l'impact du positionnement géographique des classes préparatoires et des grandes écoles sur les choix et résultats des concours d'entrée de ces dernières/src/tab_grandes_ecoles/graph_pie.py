import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pgeocode

STATS_LYCEE_FILE_PATH = os.path.join("data", "stats_lycees", "stats_lycees.csv")

stats_lycees = pd.read_csv(STATS_LYCEE_FILE_PATH, index_col=[0])


def update_pie(concours, year):
    data = stats_lycees[stats_lycees["year"] == year]
    data = data[data["concours"] == concours]

    if len(data) == 0:
        return (
            {},
            True,
        )

    data = data.groupby("postalcode").agg(
        {"inscrits": "median", "admissibles": "median", "integres": "median"}
    )

    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
        subplot_titles=["Inscrits", "Admissibles", "Intégrés"],
    )
    nomination = pgeocode.Nominatim("fr")
    for i, category in enumerate(["inscrits", "admissibles", "integres"]):
        category_data = data[[category]]
        category_data["postalcode"] = category_data.index.to_series()
        category_data["region"] = category_data["postalcode"].apply(
            lambda x: nomination.query_postal_code(
                str(int(x) * 1000)
                if len(str(int(x))) >= 2
                else "0" + str(int(x) * 1000)
            )
        )["state_name"]
        category_data.loc[
            category_data[category] < category_data[category].mean(), "region"
        ] = "Autres regions dont la proportion est inférieure à la moyenne".format(
            category
        )
        group_category_data = (
            category_data.groupby("region").sum()[category].sort_values()
        )
        pull_list = [0 for i in range(len(group_category_data))]
        if (
            group_category_data.index[-1]
            == "Autres régions dont la proportion est inférieure à la moyenne"
        ):
            pull_list[-2] = 0.2
        else:
            pull_list[-1] = 0.2
        fig.add_trace(
            go.Pie(
                labels=group_category_data.index.to_list(),
                values=group_category_data.to_list(),
                pull=pull_list,
                name=category,
            ),
            row=1,
            col=i + 1,
        )

    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="Proportion de l'origine des candidats au concours {} en {}".format(
            concours, year
        ),
    )
    return fig, False
