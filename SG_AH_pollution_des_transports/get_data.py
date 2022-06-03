# Here is the script to get all the data needed in our project
import pandas as pd
import re


def transform_energ_names(df, col):
    energ_name = {
        "ES ": "Essence",
        "GO ": "Gazole",
        "ES/GP ": "Essence ou Gaz de Pétrole Liquéfié",
        "GP/ES ": "Essence ou Gaz de Pétrole Liquéfié",
        "EE ": "Essence Hybride rechargeable",
        "EL ": "Electricité",
        "EH ": "Essence Hybride non rechargeable",
        "GH ": "Gazole Hybride non rechargeable",
        "ES/GN ": "Essence ou Gaz Naturel",
        "GN/ES ": "Essence ou Gaz Naturel",
        "FE ": "Superéthanol",
        "GN ": "Gaz Naturel",
        "GL ": "Gazole Hybride rechargeable",
    }
    df[col].replace(energ_name, inplace=True)
    return df


def transform_countries_names(df, col):
    countries_name = {
        "AT": "Autriche",
        "BE": "Belgique",
        "BG": "Bulgarie",
        "CH": "Suisse",
        "CY": "Chypre",
        "CZ": "République Tchèque",
        "DE": "Allemagne",
        "DK": "Danemark",
        "EE": "Estonie",
        "EL": "Grèce",
        "ES": "Espagne",
        "FI": "Finlande",
        "FR": "France",
        "HR": "Croatie",
        "HU": "Hongrie",
        "IE": "Irlande",
        "IS": "Islande",
        "IT": "Italie",
        "LI": "Liechtenstein",
        "LT": "Lituanie",
        "LU": "Luxembourg",
        "LV": "Lettonie",
        "MT": "Malte",
        "NL": "Pays-Bas",
        "NO": "Norvège",
        "PL": "Pologne",
        "PT": "Portugal",
        "RO": "Roumanie",
        "SE": "Suède",
        "SI": "Slovénie",
        "SK": "Slovaquie",
        "TR": "Turquie",
        "UK": "Royaume-Uni",
    }

    df[col].replace(countries_name, inplace=True)
    return df


def get_transport_pollution_eu():
    df = pd.read_csv(
        "SG_AH_pollution_des_transports/data/emission_de_polluant_des_transports_1990-2020.csv"
    )

    # Remove the useless columns, keeping only:
    # The data (TIME_PERIOD), The country (geo), Pollution type (airpol), the value of the pollution (OBS_VALUE)
    columns_to_keep = ["airpol", "geo", "TIME_PERIOD", "OBS_VALUE"]
    df = df[columns_to_keep]
    df = df.rename(
        columns={
            "airpol": "Type de pollution",
            "geo": "Pays",
            "TIME_PERIOD": "Année",
            "OBS_VALUE": "Taux de pollution",
        }
    )

    # Remove data for all EUROPE
    df = df[df["Pays"] != "EU27_2020"]

    # Rename geo columns with right names
    df = transform_countries_names(df, "Pays")
    return df


def get_pollution_per_vehicules_eu():
    df = pd.read_csv(
        "SG_AH_pollution_des_transports/data/moyenne_emissions_CO2_vehicules_neuf_2000-2020.csv"
    )

    # Remove the useless columns
    # Keep : geo, TIME_PERIOD, OBS_VALUE
    columns_to_keep = ["geo", "TIME_PERIOD", "OBS_VALUE"]
    df = df[columns_to_keep]
    df = df.rename(
        columns={
            "geo": "Pays",
            "TIME_PERIOD": "Année",
            "OBS_VALUE": "Taux de pollution",
        }
    )

    # Seperate data for all EUROPE
    df_all_eu = df.copy().loc[(df["Pays"] == "EU27_2020")]
    df_all_eu["Pays"].replace(
        {
            "EU27_2020": "Europe Entière",
            "EU27_2007": "Europe Entière",
            "EU28": "Europe Entière",
        },
        inplace=True,
    )
    df = df[
        (df["Pays"] != "EU27_2020")
        & (df["Pays"] != "EU27_2007")
        & (df["Pays"] != "EU28")
    ]

    # Rename geo columns with right names
    df = transform_countries_names(df, "Pays")
    return (df, df_all_eu)


def get_air_pollution_schools():
    df = pd.read_csv(
        "SG_AH_pollution_des_transports/data/ecoles-creches-idf-prepared_2012-2017.csv"
    )

    # remove useless columns
    df = df.drop(["ID", "ville", "CP", "type"], axis=1)
    df["lon"] = df["geometry"].map(
        lambda x: float(re.match("POINT\((.*) ", x)[1]))
    df["lat"] = df["geometry"].map(
        lambda x: float(re.match(".* (.*)\)", x)[1]))
    return df.drop(["geometry"], axis=1)


def get_pollution_per_vehicules_in_france():
    df = pd.read_csv(
        "SG_AH_pollution_des_transports/data/vehicules_polluant_france_2015.csv",
        sep=";",
        encoding="latin1",
    )

    # Remove the useless columns
    # Keep : geo, TIME_PERIOD, OBS_VALUE
    columns_to_keep = [
        "lib_mrq_doss",
        "hc",
        "nox",
        "hcnox",
        "ptcl",
        "co2_mixte",
        "co_typ_1",
        "hybride",
        "energ",
    ]
    df = df[columns_to_keep]
    df.columns = [
        "Marque",
        "Emission HC",
        "Emission NOx",
        "Emission HC et NOx",
        "Emission de Particules",
        "Emission CO2",
        "Emission CO type1",
        "Hybride",
        "Carburant",
    ]

    # Rename geo columns with right names
    df = transform_energ_names(df, "Carburant")
    df["Hybride"].replace(
        {"non ": "non Hybride", "oui ": "Hybride"}, inplace=True)
    return df
