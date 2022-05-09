import os

import requests
import zipfile
from io import BytesIO
from os.path import exists
import pandas as pd
import numpy as np

def population2020(file, pkl_name):
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
    return df.to_pickle(pkl_name)

def deces2020(file, pkl_name):
    deces2020 = pd.read_csv(file, sep=";", encoding="latin1", header=0, dtype=str)
    df = deces2020[['DEPDEC', 'LIEUDECR']].groupby(by=['DEPDEC']).count()
    df.reset_index(inplace=True)
    df.rename(columns={'DEPDEC': 'DEP', 'LIEUDECR': 'DECES'}, inplace=True)
    # get departements population
    population2020 = pd.read_pickle('population2020.pkl')
    df = pd.merge(df, population2020, on='DEP')
    df["deces pour 10000"] = (df.DECES * 1000) // df['population']
    return df.to_pickle(pkl_name)

def naissances2020(file, pkl_name):
    naissances2020 = pd.read_csv(file, sep=";", encoding="latin1", header=0, dtype=str)
    df = naissances2020[["DEPNAIS", "ANAIS"]].groupby(by=["DEPNAIS"]).count()
    df.reset_index(inplace=True)
    df.rename(columns={"DEPNAIS": "DEP", "ANAIS": "NAISSANCES"}, inplace=True)
    # get departements population
    population2020 = pd.read_pickle('population2020.pkl')
    df = pd.merge(df, population2020, on='DEP')
    df["Naissances pour 10000"] = (df.NAISSANCES * 1000) // df.population
    df.to_pickle(pkl_name)


def population(file, pkl_name):
    if exists(pkl_name):
        return False
    for date in pop_years:
        pop = pd.read_excel(file, sheet_name=f'DEP_{date}', header=[0, 1, 2], index_col=[1, 2], skiprows=8)
        pop.dropna(inplace=True)
        pop.columns = pop.columns.droplevel(2)
        pop.columns = pop.columns.droplevel(1)
        pop = pop.drop(columns='Unnamed: 0_level_0')
        pop = pop.reset_index()
        pop = pop.rename(columns={'level_0': 'DEP', 'level_1': 'DEPNAME'})
        pop = pop.drop(0)
        pop = pop.set_index('DEP').set_index('DEPNAME', append=True)
        pop = pop.astype(int)
        pop = pop.groupby(by='AGE', axis=1).sum()
        pop['Total'] = pop.sum(axis=1)
        pop['year'] = date
        pop.set_index('year', append=True, inplace=True)
        pop = pop.reorder_levels([2, 0, 1], axis='index')
        pop_to_concat.append(pop.reset_index(1).reset_index(1))
    return True

def concat_pop():
    l = []
    for y in pop_years:
        df = pd.read_pickle(f'population_dep_{y}.pkl')
        df['year'] = y
        df.set_index('year', append=True, inplace=True)
        df = df.reorder_levels([2, 0, 1], axis='index')
        l.append(df)
    df = pd.concat(l)


def naissances(file, pkl_name):
    df = pd.read_csv(file, sep=";", encoding="latin1", header=0, dtype=str, usecols=[2, 3, 4])
    df = df.loc[df.annais != 'XXXX']
    df['nombre'] = df['nombre'].astype(int)
    df['annais'] = df['annais'].astype(int)
    df['dpt'] = df['dpt'].astype(int)
    df = df.groupby(by=['annais', 'dpt']).sum()
    df = df.unstack().nombre
    df = df.loc[df.index >= 1970]
    df.to_pickle(pkl_name)


def exec_zip(url, filename, pkl_name, func):
    with requests.get(url) as res:
        with zipfile.ZipFile(BytesIO(res.content)) as z:
            with z.open(filename) as f:
                return func(f, pkl_name)


lst = np.asarray([1968, 1975, 1982, 1990, 1999, 2008, 2013, 2018])


def closest(k):
    idx = (np.abs(lst - k)).argmin()
    return lst[idx]


def create_pop():
    df2 = pd.read_pickle('naissances_par_dep_1970_2020.pkl')
    df_pop = pd.read_pickle('population_dep_1968_2018.pkl')

    folder = 'population_birth_rate'
    if not exists(folder):
        os.mkdir(folder)

    for year in df2.index.values:
        if exists(f'{folder}/{year}.pkl'):
            continue
        pyear = closest(year)
        pop = df_pop.loc[pyear].copy()
        # prepare pop for merge
        pop = pop[['Total', 'DEP', 'DEPNAME']].reset_index()
        # change '2A' and '2B' dep (for Corse) to 20
        pop.loc[pop.DEP == '2A', 'DEP'] = 20
        pop.loc[pop.DEP == '2B', 'DEP'] = 20
        pop.DEP = pop.DEP.astype(int)
        # Give 2A and 2B population the value of their sum
        corse_total = pop.loc[pop.DEP == 20].groupby(by='DEP').sum().Total.values[0]
        pop.loc[pop.DEP == 20, 'Total'] = corse_total

        # get df of 1 year
        dfn = pd.DataFrame(df2.loc[df2.index == year].reset_index(drop=True).stack(), columns=['naissances'])
        dfn = dfn.reset_index(1).reset_index(drop=True)
        dfn.rename(columns={'dpt': 'DEP'}, inplace=True)
        # merge
        dfm = pd.merge(dfn, pop, on='DEP')
        dfm['tx_nat_p_1000'] = dfm['naissances'] * 1000 / pd.Series(dfm['Total'], dtype=float)
        dfm['DEP'] = dfm.DEP.astype(object)
        dfm.loc[dfm.index < 9, 'DEP'] = dfm.loc[dfm.index < 9, 'DEP'].apply(lambda x: f'0{x}')
        dfm.loc[dfm.DEPNAME == 'Corse-du-Sud', 'DEP'] = '2A'
        dfm.loc[dfm.DEPNAME == 'Haute-Corse', 'DEP'] = '2B'
        dfm.to_pickle(f'{folder}/{year}.pkl')



#####
#   MAIN
#####

#   POPULATION

# 2020
pkl = 'population2020.pkl'
if not exists(pkl):
    url = 'https://www.insee.fr/fr/statistiques/fichier/4277596/T20F013.xlsx'
    with requests.get(url) as res:
        population2020(BytesIO(res.content), pkl)

# from 1970 to 2020
pop_to_concat = []
pop_years = [1968, 1975, 1982, 1990, 1999, 2008, 2013, 2018]
pkl = 'population_dep_1968_2018.pkl'
file = 'pop-sexe-age-quinquennal6818.xls'
url = 'https://www.insee.fr/fr/statistiques/fichier/1893204/pop-sexe-age-quinquennal6817.zip'
if exec_zip(url, file, pkl, population):
    pd.concat(pop_to_concat).to_pickle(pkl)

# DECES

# 2020
pkl = 'deces_par_departements2020.pkl'
if not exists(pkl):
    url = 'https://www.insee.fr/fr/statistiques/fichier/5431034/etatcivil2020_dec2020_csv.zip'
    exec_zip(url, 'FD_DEC_2020.csv', pkl, deces2020)


# NAISSANCES

# 2020
pkl = 'naissances_par_departements2020.pkl'
if not exists(pkl):
    url = 'https://www.insee.fr/fr/statistiques/fichier/5419785/etatcivil2020_nais2020_csv.zip'
    exec_zip(url, 'nais2020.csv', pkl, naissances2020)

# from 1970 to 2020
pkl = 'naissances_par_dep_1970_2020.pkl'
if not exists(pkl):
    url = 'https://www.insee.fr/fr/statistiques/fichier/2540004/dpt2020_csv.zip'
    exec_zip(url, 'dpt2020.csv', pkl, naissances)


# GEOJSON used to display departements on map
departements_geojson_file = 'departements-avec-outre-mer.geojson'
if not exists(departements_geojson_file):
    url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-avec-outre-mer.geojson'
    with requests.get(url) as res:
        with open(departements_geojson_file, 'wb') as file:
            file.write(BytesIO(res.content).getbuffer())

create_pop()