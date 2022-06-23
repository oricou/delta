import os
import pandas as pd

# URL for downloading the dataset
url = "https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-principaux-diplomes-et-formations" \
      "-prepares-etablissements-publics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header" \
      "=true&csv_separator=%3B "


# Declare the relevant columns
relevant_columns = ["Niveau dans le diplôme",
                    "Année universitaire",
                    "Regroupement de diplômes",
                    "Cycle universitaire (cursus LMD)",
                    "Type d'établissement",
                    "Grande discipline",
                    "Secteur disciplinaire",
                    "Nombre d'étudiants inscrits (inscriptions principales) hors doubles inscriptions CPGE",
                    "Dont femmes"]

# We need low_memory=False as some columns have mixed types and require it, sep=";" as the website specifies it
data = pd.read_csv(url, low_memory=False, sep=";", usecols=relevant_columns)

# Remove rows with no students
data = data[data["Nombre d\'étudiants inscrits (inscriptions principales) hors doubles inscriptions CPGE"] != 0]

# Rename the column to shorten the name & clarify the study
data = data.rename(columns={
    "Nombre d'étudiants inscrits (inscriptions principales) hors doubles inscriptions CPGE": "Nombre d'étudiants"}
)

# declare file location
filename = os.getcwd() + "/data/formations.csv"

# create data if missing
os.makedirs(os.path.dirname(filename), exist_ok=True)

# write
data.to_csv(filename, index=False)
