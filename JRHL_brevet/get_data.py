import urllib.request
import os

urls = ['https://data.education.gouv.fr/explore/dataset/fr-en-dnb-par-etablissement/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B']

dossier_data = "./data/"

paths = ['fr-en-dnb-par-etablissement.csv']

if __name__ == "__main__":
    if not os.path.isdir(dossier_data):
        os.mkdir(dossier_data)

    for i in range(len(paths)):
        path, url = paths[i], urls[i]
        if not os.path.isfile(dossier_data + path):
            print(f"Téléchargement {path} depuis {url}.")
            urllib.request.urlretrieve(url, dossier_data + path)
