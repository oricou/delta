import requests
import zipfile
from io import BytesIO
import pandas as pd
import numpy as np

def population(file):
    df = pd.read_excel(file, sheet_name=1, skiprows=2,
                       usecols=[0, 1], nrows=102,
                       names=['departement', 'population'],
                       dtype={'departement': str, 'population': np.float64})
    df.drop(df[df.departement == 'France métropolitaine'].index[0], inplace=True)
    # change population / 1000 value into population
    df['population'] = df['population'] * 1000
    df['DEP'] = df.apply(lambda row: row['departement'].split(' ')[0], axis=1)
    df['DEP_NAME'] = df.apply(lambda row: ' '.join(row['departement'].split(' ')[1:]), axis=1)
    del df['departement']
    # change mayotte code from 975 to 976
    df.at[df[df.DEP == '975'].index[0], 'DEP'] = '976'
    return df.to_pickle('./population2020.pkl')

def deces(file):
    deces2020 = pd.read_csv(file, sep=";", encoding="latin1", header=0, dtype=str)
    df = deces2020[['DEPDEC', 'LIEUDECR']].groupby(by=['DEPDEC']).count()
    df.reset_index(inplace=True)
    df.rename(columns={'DEPDEC': 'DEP', 'LIEUDECR': 'DECES'}, inplace=True)
    # get departements population
    population2020 = pd.read_pickle('population2020.pkl')
    df = pd.merge(df, population2020, on='DEP')
    df["deces pour 10000"] = (df.DECES * 10000) // df['population']
    return df.to_pickle("./deces_par_departements.pkl")

def naissances(file):
    naissances2020 = pd.read_csv(file, sep=";", encoding="latin1", header=0, dtype=str)
    df = naissances2020[["DEPNAIS", "ANAIS"]].groupby(by=["DEPNAIS"]).count()
    df.reset_index(inplace=True)
    df.rename(columns={"DEPNAIS": "DEP", "ANAIS": "NAISSANCES"}, inplace=True)
    # get departements population
    population2020 = pd.read_pickle('population2020.pkl')
    df = pd.merge(df, population2020, on='DEP')
    df["Naissances pour 10000"] = (df.NAISSANCES * 10000) // df.population
    df.to_pickle('./naissances_par_departements.pkl')


def exec_zip(url, filename, func):
    with requests.get(url) as res:
        with zipfile.ZipFile(BytesIO(res.content)) as z:
            with z.open(filename) as f:
                return func(f)

#####
#   MAIN
#####

#   POPULATION

url = 'https://www.insee.fr/fr/statistiques/fichier/4277596/T20F013.xlsx'
with requests.get(url) as res:
    population(BytesIO(res.content))


# DECES

url = 'https://www.insee.fr/fr/statistiques/fichier/5431034/etatcivil2020_dec2020_csv.zip'
exec_zip(url, 'FD_DEC_2020.csv', deces)


# NAISSANCES

url = 'https://www.insee.fr/fr/statistiques/fichier/5419785/etatcivil2020_nais2020_csv.zip'
exec_zip(url, 'nais2020.csv', naissances)


# GEOJSON used to display departements on map
url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-avec-outre-mer.geojson'
departements_geojson_file = 'departements-avec-outre-mer.geojson'
with requests.get(url) as res:
    with open(departements_geojson_file, 'wb') as file:
        file.write(BytesIO(res.content).getbuffer())