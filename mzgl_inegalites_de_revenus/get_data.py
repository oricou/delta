import pandas as pd
import os
import glob
import numpy as np
import zipfile

# Retrieve path of this script
path = os.path.dirname(__file__)
# Extract data
with zipfile.ZipFile(path + "/data.zip", "r") as myzip:
    myzip.extractall(path)

# Dictionary used to convert Country ISO code Alpha-2 and Alpha-3
iso2_to_iso3 = {
    "AE": "ARE",
    "AF": "AFG",
    "AL": "ALB",
    "AM": "ARM",
    "AO": "AGO",
    "AR": "ARG",
    "AT": "AUT",
    "AU": "AUS",
    "AZ": "AZE",
    "BA": "BIH",
    "BD": "BGD",
    "BE": "BEL",
    "BF": "BFA",
    "BG": "BGR",
    "BH": "BHR",
    "BI": "BDI",
    "BJ": "BEN",
    "BN": "BRN",
    "BO": "BOL",
    "BR": "BRA",
    "BS": "BHS",
    "BT": "BTN",
    "BW": "BWA",
    "BY": "BLR",
    "BZ": "BLZ",
    "CA": "CAN",
    "CD": "COD",
    "CF": "CAF",
    "CG": "COG",
    "CH": "CHE",
    "CI": "CIV",
    "CM": "CMR",
    "CN": "CHN",
    "CO": "COL",
    "CR": "CRI",
    "CU": "CUB",
    "CV": "CPV",
    "CY": "CYP",
    "CZ": "CZE",
    "DE": "DEU",
    "DJ": "DJI",
    "DK": "DNK",
    "DO": "DOM",
    "DZ": "DZA",
    "EC": "ECU",
    "EE": "EST",
    "EG": "EGY",
    "ER": "ERI",
    "ES": "ESP",
    "ET": "ETH",
    "FI": "FIN",
    "FR": "FRA",
    "GA": "GAB",
    "GB": "GBR",
    "GE": "GEO",
    "GH": "GHA",
    "GM": "GMB",
    "GN": "GIN",
    "GQ": "GNQ",
    "GR": "GRC",
    "GT": "GTM",
    "GW": "GNB",
    "GY": "GUY",
    "HK": "HKG",
    "HN": "HND",
    "HR": "HRV",
    "HT": "HTI",
    "HU": "HUN",
    "ID": "IDN",
    "IE": "IRL",
    "IL": "ISR",
    "IN": "IND",
    "IQ": "IRQ",
    "IR": "IRN",
    "IS": "ISL",
    "IT": "ITA",
    "JM": "JAM",
    "JO": "JOR",
    "JP": "JPN",
    "KE": "KEN",
    "KG": "KGZ",
    "KH": "KHM",
    "KM": "COM",
    "KP": "PRK",
    "KR": "KOR",
    "KW": "KWT",
    "KZ": "KAZ",
    "LA": "LAO",
    "LB": "LBN",
    "LK": "LKA",
    "LR": "LBR",
    "LS": "LSO",
    "LT": "LTU",
    "LU": "LUX",
    "LV": "LVA",
    "LY": "LBY",
    "MA": "MAR",
    "MD": "MDA",
    "ME": "MNE",
    "MG": "MDG",
    "MK": "MKD",
    "ML": "MLI",
    "MM": "MMR",
    "MN": "MNG",
    "MO": "MAC",
    "MR": "MRT",
    "MT": "MLT",
    "MU": "MUS",
    "MV": "MDV",
    "MW": "MWI",
    "MX": "MEX",
    "MY": "MYS",
    "MZ": "MOZ",
    "NE": "NER",
    "NG": "NGA",
    "NI": "NIC",
    "NL": "NLD",
    "NO": "NOR",
    "NP": "NPL",
    "NZ": "NZL",
    "OM": "OMN",
    "PA": "PAN",
    "PE": "PER",
    "PG": "PNG",
    "PH": "PHL",
    "PK": "PAK",
    "PL": "POL",
    "PS": "PSE",
    "PT": "PRT",
    "PY": "PRY",
    "QA": "QAT",
    "RO": "ROU",
    "RS": "SRB",
    "RU": "RUS",
    "RW": "RWA",
    "SA": "SAU",
    "SC": "SYC",
    "SD": "SDN",
    "SE": "SWE",
    "SG": "SGP",
    "SI": "SVN",
    "SK": "SVK",
    "SL": "SLE",
    "SN": "SEN",
    "SO": "SOM",
    "SR": "SUR",
    "SS": "SSD",
    "ST": "STP",
    "SV": "SLV",
    "SY": "SYR",
    "SZ": "SWZ",
    "TD": "TCD",
    "TG": "TGO",
    "TH": "THA",
    "TJ": "TJK",
    "TL": "TLS",
    "TM": "TKM",
    "TN": "TUN",
    "TR": "TUR",
    "TT": "TTO",
    "TW": "TWN",
    "TZ": "TZA",
    "UA": "UKR",
    "UG": "UGA",
    "US": "USA",
    "UY": "URY",
    "UZ": "UZB",
    "VE": "VEN",
    "VN": "VNM",
    "YE": "YEM",
    "ZA": "ZAF",
    "ZM": "ZMB",
    "ZW": "ZWE",
}


def get_inegalities_df(countries_df):
    """
    Read every csv files of the World Inegalities Database, load it into one dataframe
    """
    df = pd.concat(
        [
            pd.read_csv(filename, index_col=False, sep=";")
            for filename in glob.glob("".join([path, "/data/wid_data/WID_data_*.csv"]))
        ]
    )
    df = df.loc[df["year"] >= 1995]
    df = (
        df.drop(["pop", "age", "variable"], axis=1)
        .set_index(["country", "percentile", "year"])
        .rename_axis(["alpha2", "Percentile", "Year"], axis=0)
        .sort_index()
    )
    return (
        df.join(countries_df, sort=False)
        .reset_index()
        .set_index(["alpha3", "Percentile", "Year"])
        .sort_index()
    )


def get_corruption_df():
    """
    Read corruption perception dataset, load it into one dataframe
    """
    list_dataframe = []
    for filename in os.listdir("".join([path, "/data/Corruption_perceptions_index/"])):
        year = filename[4:8]
        tmp_df = (
            pd.read_csv(
                "".join([path, "/data/Corruption_perceptions_index/", filename]),
                sep=",",
                index_col=False,
            )
            .filter(["ISO", "Rank", "Score"], axis=1)
            .rename(columns={"Score": "score"})
        )
        tmp_df["Year"] = year
        # Update CPI (Corruption Perceptions Index) score before 2012
        if year < "2012":
            tmp_df.score = tmp_df.score.astype("float64").apply(lambda x: x * 10)
        list_dataframe.append(tmp_df)
    return (
        pd.concat(list_dataframe, axis=0)
        .astype({"Year": "int64"})
        .set_index(["ISO", "Year"])
        .rename_axis(["alpha3", "Year"], axis=0)
        .rename(columns={"Score": "score"})
        .sort_index()
    )


def get_democratie_index_df():
    """
    Read democracy dataset, load it into one dataframe
    """
    df = pd.read_csv("".join([path, "/data/Democracy_Indices.csv"]))
    df.geo = df.geo.str.upper()
    return (
        df.set_index(["geo", "time"])
        .rename_axis(["alpha3", "Year"], axis=0)
        .filter(["Democracy index (EIU)"])
        .rename(columns={"Democracy index (EIU)": "score"})
        .sort_index()
    )


def get_countries_df():
    """
    Read countries dataset, load it into one dataframe
    """
    df = (
        pd.read_csv(
            "".join([path, "/data/wid_data/WID_countries.csv"]),
            sep=";",
            index_col=False,
        )
        .drop(["region2", "titlename"], axis=1)
        .replace(
            {
                "Africa": "Afrique",
                "Asia": "Asie",
                "Oceania": "Océanie",
                "Americas": "Amérique",
            }
        )
        .rename(columns={"shortname": "Country_Name"})
    )
    df["alpha3"] = df["alpha2"].map(iso2_to_iso3)
    return df.set_index(["alpha2"]).dropna().sort_index()


def get_population_df():
    """
    Read population dataset, load it into one dataframe
    """
    return (
        pd.read_csv("".join([path, "/data/Population/data.csv"]))
        .set_index(["alpha3"])
        .drop(["Country Name", "Series Name", "Series Code"], axis=1)
        .drop([str(year) for year in range(1970, 1995)], axis=1)
        .replace("..", 0)
        .sort_index()
    )


def get_gdp_df():
    """
    Read Gross domestic product per capita dataset, load it into one dataframe
    """
    gdp_df = (
        pd.read_csv("".join([path, "/data/GDP/data.csv"]))
        .drop(["Series Code", "Country Name"], axis=1)
        .set_index(["alpha3", "Series Name"])
        .replace("..", np.nan)
        .sort_index()
    )
    gdp_df = gdp_df.loc[(slice(None), "GDP per capita (current US$)", slice(None))]
    return gdp_df.loc[
        :,
        [str(year) for year in range(1995, 2021)],
    ].sort_index()
