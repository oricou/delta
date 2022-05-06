import os
import pandas as pd

cur_path = os.path.dirname(__file__)
regu_data_path = os.path.join(cur_path, "data", "regularite-mensuelle-tgv-aqst.csv")
gares_data_path = os.path.join(cur_path, "data", "referentiel-gares-voyageurs.csv")

def make_df():
    df = (
        pd.read_csv(regu_data_path, delimiter=";")
        .dropna(axis=1)
        .drop_duplicates()
        .drop("Service", axis=1)
    )
    coord = (
        pd.read_csv(gares_data_path, delimiter=";")
        .drop(["Date fin validité plateforme", "SOPs"], axis=1)
        .dropna()
    )

    coord["Région SNCF"] = (
        coord["Région SNCF"]
        .astype(str)
        .map(
            lambda s: "ILE DE FRANCE" if "PARIS" in s else s.replace("REGION ", "")
        )
    )
    coord["UT"] = coord["UT"].astype(str).map(lambda s: s.replace(" GARE", ""))
    coord["Intitulé fronton de gare"] = (
        coord["Intitulé fronton de gare"].astype(str).map(lambda s: s.upper())
    )

    gares = pd.DataFrame(df["Gare de départ"].unique(), columns=["Gare"])
    gares_1 = (
        pd.merge(
            gares,
            coord[["UT", "Région SNCF", "WGS 84"]],
            left_on="Gare",
            right_on="UT",
            how="left",
        )
        .drop("UT", axis=1)
        .dropna()
        .drop_duplicates()
    )
    gares_2 = (
        pd.merge(
            gares,
            coord[["Intitulé fronton de gare", "Région SNCF", "WGS 84"]],
            left_on="Gare",
            right_on="Intitulé fronton de gare",
            how="left",
        )
        .drop("Intitulé fronton de gare", axis=1)
        .dropna()
        .drop_duplicates()
    )
    gares = pd.concat([gares_1, gares_2]).drop_duplicates()

    df_coord = (
        pd.merge(
            df,
            gares,
            left_on="Gare de départ",
            right_on="Gare",
            how="left",
            suffixes=(None, "_départ"),
        )
        .drop("Gare", axis=1)
        .dropna()
        .drop_duplicates()
        .rename(
            {"WGS 84": "Coord_départ", "Région SNCF": "Région_départ"},
            axis=1,
        )
    )
    df_coord = (
        pd.merge(
            df_coord, gares, left_on="Gare d'arrivée", right_on="Gare", how="left"
        )
        .drop("Gare", axis=1)
        .dropna()
        .drop_duplicates()
        .rename(
            {"WGS 84": "Coord_arrivée", "Région SNCF": "Région_arrivée"},
            axis=1,
        )
    )

    gares["WGS 84"] = gares["WGS 84"].map(lambda x: tuple(map(float, x.split(","))))
    df_coord["Date"] = pd.to_datetime(df_coord["Date"])
    df_coord.set_index("Date", inplace=True)

    df_trajet = (
        df_coord.groupby(
            [df_coord.index.to_period("Y"), "Gare de départ", "Gare d'arrivée"]
        )
        .sum()
        .reset_index()
    )
    df_trajet = (
        pd.merge(
            df_trajet,
            gares[["Gare", "WGS 84"]],
            left_on="Gare de départ",
            right_on="Gare",
            how="left",
        )
        .drop("Gare", axis=1)
        .dropna()
        .drop_duplicates()
    )
    df_trajet.rename({"WGS 84": "Coord_départ"}, axis=1, inplace=True)
    df_trajet = (
        pd.merge(
            df_trajet,
            gares[["Gare", "WGS 84"]],
            left_on="Gare d'arrivée",
            right_on="Gare",
            how="left",
        )
        .drop("Gare", axis=1)
        .dropna()
        .drop_duplicates()
        .set_index("Date")
    )
    df_trajet.rename({"WGS 84": "Coord_arrivée"}, axis=1, inplace=True)
    
    return df_trajet, df_coord, gares
