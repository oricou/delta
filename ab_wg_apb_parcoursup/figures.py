import plotly.express as px
import plotly.graph_objects as go
import json

# ######################################
# Utils functions
# ######################################

period = lambda years: (
    f"en {years[0]}"
    if years[0] == (years[1] - 1)
    else f"de {years[0]} à {years[1] - 1}"
)


def formations_list_to_french(formations):
    sentence = ""
    for i in range(len(formations)):
        if i == len(formations) - 1:
            sentence += f"et {formations[i]}"
        else:
            sentence += f"{formations[i]} "
    return sentence


# ######################################
# Functions to create figures
# ######################################


def repartition_map(raw_df, formations, years):

    df = raw_df
    title = f"Répartition géographique des vœux des étudiants {period(years)}"

    # Filter df with right years
    df = df[df["session"].isin(range(years[0], years[1]))]

    # Filter df with right formation
    if not formations[0] == "Toutes les formations":
        df = df[df["formation"].isin(formations)]
        title = f"Répartition géographique des vœux des étudiants en {formations_list_to_french(formations)} {period(years)}"

    df = (
        df[["departement", "nb etudiants"]].groupby("departement", as_index=False).sum()
    )

    departements = json.load(open("./ab_wg_apb_parcoursup/data/departements.geojson"))

    fig = px.choropleth_mapbox(
        df,
        geojson=departements,
        locations="departement",
        featureidkey="properties.nom",
        color="nb etudiants",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=4.2,
        center={"lat": 47, "lon": 2},
        opacity=0.5,
        labels={"nb etudiants": "Nombre d'étudiants"},
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig, title


def formation_details_sunburst(raw_df, formations, years):

    df = raw_df
    title = f"Nombre d'étudiants par type de diplômes {period(years)}"

    # Filter df with right years
    df = df[df["session"].isin(range(years[0], years[1]))]

    # Handle if a specific formation is selected
    if not formations[0] == "Toutes les formations":
        df = df[df["formation"].isin(formations)]
        title = f"Nombre d'étudiants par catégories en {formations_list_to_french(formations)} {period(years)}"

        df = (
            df[["formation details", "nb etudiants"]]
            .groupby("formation details", as_index=False)
            .sum()
        )

        fig = px.sunburst(df, path=["formation details"], values="nb etudiants")
        fig.update_layout(margin={"r": 6, "t": 2, "l": 6, "b": 2})

        return fig, title

    # Handle general cas when all formations are selected
    df = (
        df[["formation", "formation details", "nb etudiants"]]
        .groupby(["formation", "formation details"], as_index=False)
        .sum()
    )

    fig = px.sunburst(
        df,
        path=["formation", "formation details"],
        values="nb etudiants",
    )
    fig.update_layout(margin={"r": 6, "t": 2, "l": 6, "b": 2})

    return fig, title


def categories_years_histogram(raw_df, formations, years, scale):

    df = raw_df
    title = f"Nombre d'étudiant par année par type de diplôme {period(years)}"

    # Filter df with right years
    df = df[df["session"].isin(range(years[0], years[1]))]

    # Handle if a specific formation is selected
    if not formations[0] == "Toutes les formations":
        df = df[df["formation"].isin(formations)]
        title = f"Nombre d'étudiant par année par catégorie {formations_list_to_french(formations)} {period(years)}"

        df = (
            df[["session", "formation details", "nb etudiants"]]
            .groupby(["session", "formation details"], as_index=False)
            .sum()
        )

        fig = px.histogram(
            df,
            x="formation details",
            y="nb etudiants",
            color="session",
            barmode="group",
            height=400,
            labels={
                "formation details": "Catégorie",
                "nb etudiants": "nombre d'étudiants",
                "session": "Année",
            },
            log_y=scale,
        )

        return fig, title

    # Handle general case when all formations are selected
    df = (
        df[["session", "formation", "nb etudiants"]]
        .groupby(["session", "formation"], as_index=False)
        .sum()
    )

    fig = px.histogram(
        df,
        x="formation",
        y="nb etudiants",
        color="session",
        barmode="group",
        height=400,
        labels={
            "formation": "Type de diplômes",
            "nb etudiants": "nombre d'étudiants",
            "session": "Année",
        },
        log_y=scale,
    )

    return fig, title


def women_men_histogram(raw_df, formations, years):
    df = raw_df
    title = f"Nombre d'étudiant par année par type de diplôme {period(years)}"

    # Filter df with right years
    df = df[df["session"].isin(range(years[0], years[1]))]

    # Handle if a specific formation is selected
    if not formations[0] == "Toutes les formations":
        df = df[df["formation"].isin(formations)]
        title = f"Nombre d'étudiant par année par catégorie {formations_list_to_french(formations)} {period(years)}"

        df = (
            df[["session", "formation details", "nb etudiants"]]
            .groupby(["session", "formation details"], as_index=False)
            .sum()
        )

        df["nb garcons"] = df["nb etudiants"] - df["nb filles"]

        df.loc[df.index.repeat(df["nb filles"])]["session"]

        fig = go.Figure()
        fig.add_trace(
            go.Violin(
                x=df.loc[df.index.repeat(df["nb filles"])]["formation details"],
                y=df.loc[df.index.repeat(df["nb filles"])]["session"],
                legendgroup="Filles",
                scalegroup="Yes",
                name="Femme",
                side="negative",
                line_color="blue",
            )
        )
        fig.add_trace(
            go.Violin(
                x=df.loc[df.index.repeat(df["nb garcons"])]["formation details"],
                y=df.loc[df.index.repeat(df["nb garcons"])]["session"],
                legendgroup="Garçons",
                scalegroup="No",
                name="Homme",
                side="positive",
                line_color="orange",
            )
        )
        fig.update_traces(meanline_visible=True)
        fig.update_layout(violingap=0, violinmode="overlay")

        return fig, title

    # Handle general case when all formations are selected
    df = (
        df[["session", "formation", "nb etudiants", "nb filles"]]
        .groupby(["session", "formation"], as_index=False)
        .sum()
    )

    df["nb garcons"] = df["nb etudiants"] - df["nb filles"]

    df.loc[df.index.repeat(df["nb filles"])]["session"]

    fig = go.Figure()
    fig.add_trace(
        go.Violin(
            x=df.loc[df.index.repeat(df["nb filles"])]["formation"],
            y=df.loc[df.index.repeat(df["nb filles"])]["session"],
            legendgroup="Filles",
            scalegroup="Yes",
            name="Femme",
            side="negative",
            line_color="blue",
        )
    )
    fig.add_trace(
        go.Violin(
            x=df.loc[df.index.repeat(df["nb garcons"])]["formation"],
            y=df.loc[df.index.repeat(df["nb garcons"])]["session"],
            legendgroup="Garçons",
            scalegroup="No",
            name="Homme",
            side="positive",
            line_color="orange",
        )
    )
    fig.update_traces(meanline_visible=True)
    fig.update_layout(violingap=0, violinmode="overlay")

    return fig, title
