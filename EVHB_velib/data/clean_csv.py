# After fetching, we had a lot of junk data, so we removed / renamed columns accordingly
# We had a lot of processing to find where this coordinate (bike station) is located (which district)

from os import sep
import threading
import plotly.graph_objects as go
import json
import glob
import os
import pandas as pd
from shapely.geometry import Point, Polygon

with open('data/canton.json') as f:
    geojson_france = json.load(f)


def clean_csv(path):
    clean = path.replace('data/velib/', 'data/velib/clean_')
    good = path.replace('data/velib/', 'data/velib/good_')

    db_velib = pd.read_csv(path,
                           dtype={"Identifiant station": str},
                           sep=';')

    db_velib.drop("Code INSEE communes équipées", axis=1, inplace=True)
    db_velib.rename(columns={
        "Identifiant station": "id",
        "Nom station": "station",
        "Station en fonctionnement": "working",
        "Capacité de la station": "capacity",
        "Nombre bornettes libres": "avail. station",
        "Nombre total vélos disponibles": "avail. bike",
        "Vélos mécaniques disponibles": "mech. bike",
        "Vélos électriques disponibles": "elec. bike",
        "Borne de paiement disponible": "atm",
        "Retour vélib possible": "bike return",
        "Actualisation de la donnée": "data actualization",
        "Coordonnées géographiques": "geo",
        "Nom communes équipées": "commune"
    }, inplace=True)

    db_velib["working"] = db_velib["working"] == "OUI"
    db_velib["atm"] = db_velib["atm"] == "OUI"
    db_velib["bike return"] = db_velib["bike return"] == "OUI"

    def contains(geojson, point_str):
        try:
            a, b = point_str.split(',')
            a, b = float(a), float(b)
        except:
            return ""

        point = Point(a, b)
        for c in geojson["features"]:
            if c["geometry"]["type"] == "MultiPolygon":
                continue

            tmp = list(map(lambda x: (x[1], x[0]),
                           c["geometry"]["coordinates"][0]))
            polygon = Polygon(tmp)
            if polygon.contains(point):
                return c["id"]
        return ""

    db_velib["arrond"] = db_velib["geo"].apply(
        lambda x: contains(geojson_france, x))

    interesting_columns = db_velib[["arrond", "avail. bike"]]
    interesting = interesting_columns.groupby(by="arrond").sum().reset_index()

    db_velib.to_csv(clean, sep=";", index=False, index_label=False)
    interesting.to_csv(good, sep=";", index=False, index_label=False)


files = glob.glob('data/velib/[0-9]*')


def chunks(l, chunks_nb=16):
    n = int(len(l) / chunks_nb)
    for i in range(0, len(l), n):
        yield l[i:i + n]


def work(files):
    for path in files:
        clean = path.replace('data/velib/', 'data/velib/clean_')
        good = path.replace('data/velib/', 'data/velib/good_')

        if os.path.isfile(clean) and os.path.isfile(good):
            continue

        print(path)
        clean_csv(path)
        print("OK")


threads = []
for i, chunk in enumerate(chunks(files, 16)):
    threads.append(threading.Thread(target=work, args=(chunk,)))

for i in range(16):
    threads[i].start()

for i in range(16):
    threads[i].join()
