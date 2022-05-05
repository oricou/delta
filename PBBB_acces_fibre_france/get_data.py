import urllib.request
import os

urls = ['https://www.data.gouv.fr/fr/datasets/r/d538685a-b9cb-4a3e-b90d-ad6f0a13920b',
        'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson',
        'https://www.arcep.fr/fileadmin/reprise/dossiers/fibre/liste-gestion-identifiants-prefixe-ligne-fibre-2.xlsx']

dossier_data = "./PBBB_acces_fibre_france/data/"
paths = ['2021t4-obs-hd-thd-deploiement.xlsx',
        'departements.geojson',
        'operator-id.xlsx']

if __name__ == "__main__":
    if not os.path.isdir(dossier_data):
        os.mkdir(dossier_data)

    for i in range(len(paths)):
        path, url = paths[i], urls[i]
        if not os.path.isfile(dossier_data + path):
            print(f"Téléchargement {path} depuis {url}.")
            urllib.request.urlretrieve(url, dossier_data + path)