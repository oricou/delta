import numpy as np               # bibliothèque qui ajoute les tables
import pandas as pd              # bibliothèque qui ajoute les tableaux (tableurs)
import matplotlib.pyplot as plt  # bibliothèque graphique pour tracer des courbes

import json
import plotly.express as px


def get_prenoms():
    prenoms_raw = pd.read_csv("ljad_prenoms/data/dpt2020.csv", sep=";", encoding="utf-8")
    no_name = prenoms_raw[prenoms_raw.preusuel == "_PRENOMS_RARES"]
    prenoms = prenoms_raw.drop(index = no_name.index)
    
    no_date = prenoms[prenoms.annais == "XXXX"]
    prenoms = prenoms.drop(index = no_date.index)
    # Supprimer les cas non daté suffisent a supprimer les cas sans départements
    prenoms.annais = prenoms.annais.astype(int)
    prenoms.preusuel = prenoms.preusuel.str.lower()
    prenoms.dpt = prenoms.dpt.astype(int)
    return prenoms

def get_populations():
    population_raw = pd.read_excel('ljad_prenoms/data/base-pop-historiques-1876-2019.xlsx', header=5)
    population_raw_ = population_raw.drop(columns=["CODGEO", "REG"])
    return population_raw_.groupby("DEP").sum()

def get_france_geojson():
    with open("ljad_prenoms/data/departements.geojson") as response:
        departements = json.load(response)
    
    for departement in departements["features"]:
        code = departement["properties"]["code"]
        departement["properties"]["code"] = code[1] if code[0] == '0' else code

    return departements

def get_occ_name_year(df, name, year):
    df_year = df[df.annais == year]
    return df_year[df_year.preusuel == name].groupby("dpt").sum().drop(columns=["sexe", "annais"]).reset_index()

# récupère le pourcentage de chomage par département par années.
def get_chomage():
    # Drop region and useless rows
    to_drop = [0, 1, 2, 11, 16, 20, 23, 30, 34, 39, 42, 47,
        50, 55, 61, 66, 71, 77, 86, 90, 99, 104, 110, 118, 119, 120]
    chomage_raw = pd.read_excel('ljad_prenoms/data/irsoceds2013_T302.xls', header=2).drop(index=to_drop)
    chomage_raw.DATE = chomage_raw.DATE.str[:2] # works only because no DOM TOM
    chomage_raw.iat[-1,0] = "20"
    chomage_raw.DATE = chomage_raw.DATE.astype(int)
    chomage_raw = chomage_raw.rename(columns={"DATE": "dpt"})
    chomage_raw = chomage_raw.set_index("dpt")
    chomage_raw.columns = chomage_raw.columns.astype(int)
    return chomage_raw.reset_index()

def read_sheet(xls, sheet):    
    to_drop = [0, 1, 2, 11, 16, 20, 23, 30, 34, 39, 42, 47,
        50, 55, 61, 66, 71, 77, 86, 90, 99, 104, 110, 118, 119, 120]
    emploi_raw = pd.read_excel(xls, sheet, header=4).drop(index=to_drop)
    emploi_raw.DATE = emploi_raw.DATE.str[:2]
    emploi_raw = emploi_raw.rename(columns={"DATE": "dpt"})
    emploi_raw.iat[-1,0] = "20"
    emploi_raw.dpt = emploi_raw.dpt.astype(int)
    emploi_raw.set_index("dpt", inplace=True)
    emploi_raw.columns = emploi_raw.columns.str[6:10].astype(int)
    return emploi_raw

def read_all_sheet_emploi(xls) -> pd.DataFrame:
    dfs = []
    for name in xls.sheet_names[48:]:
        df = read_sheet(xls, name)
        
        gender, code = name.split(' - ')
        gender_code = 1 if gender == 'TH' else 2
        
        df = pd.concat([
            df[s].to_frame().assign(annee=s)
            .set_index('annee', append=True)
            .rename(columns={s:'nombre'})
        for s in df])
        
        df['sexe'] = gender_code
        df['categorie'] = code
        df.set_index(['sexe', 'categorie'], append=True, inplace=True)
        dfs.append(df.reorder_levels(['sexe', 'dpt', 'annee', 'categorie']))

    return pd.concat(dfs).sort_index()
