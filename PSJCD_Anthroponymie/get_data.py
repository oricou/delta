import pandas as pd
import numpy as np
import json
import geopandas as gpd
from urllib.request import urlopen

def to_str(n):
    try:
        return "0" + str(n) if n < 10 else str(n)
    except:
        return n

def get_nomsParDpt():
    url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    dpts_json = json.loads(urlopen(url).read())
    gdf = gpd.GeoDataFrame.from_features(dpts_json["features"])
    df_name = gdf.drop(columns=['geometry']).set_index("code")
    name_map = df_name.to_dict()['nom']

    df = pd.read_csv('PSJCD_Anthroponymie/data/nomsParDpt.txt', sep='\t', lineterminator='\n')

    df["DEP"] = df["DEP"].map(to_str)
    df.rename(columns={"NOM": "Nom", "DEP": "Dpt", "_1991_2000\r": "_1991_2000"}, inplace=True)
    dpt_arr = np.unique(df.Dpt.to_numpy(dtype=str))
    df = df[[dep in dpt_arr[:-6] for dep in df['Dpt']]]
    dpt_names = df.Dpt.map(name_map)
    df.insert(2, "Nom_Dpt", dpt_names)
    df.columns = df.columns.str.replace(r'^_', '')

    return dpts_json, df
