import pandas as pd
import numpy as np
import logging
from urllib import request
logging.basicConfig(level=logging.INFO)
import os
import json

TGVCSVURL = "https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
TGVCSVFILE = "regularite-mensuelle-tgv-aqst.csv"
STATIONSJSONURL = "https://ressources.data.sncf.com/explore/dataset/liste-des-gares/download/?format=json&timezone=Europe/Paris&lang=fr"
STATIONSJSONFILE = "liste-des-gares.json"
STATIONSIDXJSONFILE = "stations.json"

REMAP = {
    'PARIS LYON': 'paris gare de lyon souterrain',
    'LILLE': 'lille champ de mars',
    'MONTPELLIER': 'montpellier st roch',
    'MARNE LA VALLEE': 'marne la vallée chessy',
    'STRASBOURG': 'strasbourg neudorf',
    'ANGERS SAINT LAUD': 'angers st laud',
    'SAINT ETIENNE CHATEAUCREUX': 'st étienne châteaucreux',
    'BESANCON FRANCHE COMTE TGV': 'besançon franche comté tgv',
    'VALENCE ALIXAN TGV': 'valence tgv',
    'NIMES': 'nîmes',
    'BELLEGARDE (AIN)': 'bellegarde',
    'ANGOULEME': 'angoulême',
    'NANCY': 'nancy ville',
    'CHAMBERY CHALLES LES EAUX': 'chambéry challes les eaux',
    'METZ': 'metz ville',
    'MACON LOCHE': 'mâcon loché tgv',
}
def remap(g):
    return REMAP[g] if g in REMAP else g.lower().replace('-', ' ')

def get_data():
    request.urlretrieve(TGVCSVURL, TGVCSVFILE)
    request.urlretrieve(STATIONSJSONURL, STATIONSJSONFILE)
    with open(STATIONSJSONFILE) as f:
        stations = json.load(f)
    statidx = {}
    for s in stations:
        statidx[s["fields"]["libelle"].lower().replace('-', ' ')] = s
    with open(STATIONSIDXJSONFILE, "w") as f:
        json.dump(statidx, f)
    
    df = pd.read_csv(TGVCSVFILE, sep=";")
    df.set_index('Date')
    df = df[df['Service'] == 'National']
    
    def __grr(r):
        a = r['Gare de départ']
        b = r['Gare d\'arrivée']
        return f'{a}→{b}'
    df['connid'] = df.apply(lambda r: __grr(r), axis=1)

    def _gen_geopoly(r):
        c1 = np.array(statidx[remap(r['Gare de départ'])]['fields']['geo_shape']['coordinates'])
        c2 = np.array(statidx[remap(r['Gare d\'arrivée'])]['fields']['geo_shape']['coordinates'])
        diff = np.array([0.01, 0.01])
        return {
            "type": "Polygon",
            "coordinates": np.array([[c1, c1 + diff, c2 + diff, c2, c2 - diff, c1 - diff, c1]]).tolist()
        }
    def _gen_geopolys():
        def mkf(r):
            return {
                "type": "Feature",
                "properties": {
                    "connid": r['connid'],
                },
                "geometry": _gen_geopoly(r),
            }
        feats = [mkf(r) for (i, r) in df.groupby('connid', as_index=False).first().iterrows()]
        return {
            "type": "FeatureCollection",
            "features": feats,
        }
    with open("connpolys.geojson", "w") as f:
        json.dump(_gen_geopolys(), f)
    
    df.to_pickle("df.pkl")

if __name__ == '__main__':
    get_data()
