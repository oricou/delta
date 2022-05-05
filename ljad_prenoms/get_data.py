import numpy as np               # bibliothèque qui ajoute les tables
import pandas as pd              # bibliothèque qui ajoute les tableaux (tableurs)
import matplotlib.pyplot as plt  # bibliothèque graphique pour tracer des courbes

import json
import plotly.express as px


def get_prenoms():
    prenoms_raw = pd.read_csv("data/dpt2020.csv", sep=";", encoding="utf-8")
    no_name = prenoms_raw[prenoms_raw.preusuel == "_PRENOMS_RARES"]
    prenoms = prenoms_raw.drop(index = no_name.index)
    
    no_date = prenoms[prenoms.annais == "XXXX"]
    prenoms = prenoms.drop(index = no_date.index)
    # Supprimer les cas non daté suffisent a supprimer les cas sans départements
    prenoms.annais = prenoms.annais.astype(int)
    prenoms.preusuel = prenoms.preusuel.str.lower()
    return prenoms

def get_populations():
    population_raw = pd.read_excel('data/base-pop-historiques-1876-2019.xlsx', header=5)
    population_raw_ = population_raw.drop(columns=["CODGEO", "REG"])
    return population_raw_.groupby("DEP").sum()

def get_france_geojson():
    with open("data/departements.geojson") as response:
        departements = json.load(response)
    return departements

def get_occ_name_year(df, name, year):
    df_year = df[df.annais == year]
    return df_year[df_year.preusuel == name].groupby("dpt").sum().drop(columns=["sexe", "annais"]).reset_index()

# récupère le pourcentage de chomage par département par années.
def get_chomage():
    # Drop region and useless rows
    to_drop = [0, 1, 2, 11, 16, 20, 23, 30, 34, 39, 42, 47,
        50, 55, 61, 66, 71, 77, 86, 90, 99, 104, 110, 120]
    chomage_raw = pd.read_excel('data/irsoceds2013_T302.xls', header=2).drop(index=to_drop)
    chomage_raw.DATE = chomage_raw.DATE.str[:2] # works only because no DOM TOM
    chomage_raw = chomage_raw.rename(columns={"DATE": "dpt"})
    chomage_raw = chomage_raw.set_index("dpt")
    chomage_raw.columns = chomage_raw.columns.astype(int)
    return chomage_raw.reset_index()

def read_sheet(xls, sheet):    
    to_drop = [0, 1, 2, 11, 16, 20, 23, 30, 34, 39, 42, 47,
        50, 55, 61, 66, 71, 77, 86, 90, 99, 104, 110, 120]
    emploi_raw = pd.read_excel(xls, sheet, header=4).drop(index=to_drop)
    emploi_raw.DATE = emploi_raw.DATE.str[:2]
    emploi_raw = emploi_raw.rename(columns={"DATE": "dpt"}).set_index("dpt")
    emploi_raw.columns = emploi_raw.columns.str[6:10].astype(int)
    return emploi_raw.reset_index()

def get_secteurs(xls):
    secteurs = {
        secteur : pd.read_excel(Prenoms.xls, secteur).iloc[1,0].split('-')[1]
        if len(secteur) > 6
        else pd.read_excel(Prenoms.xls, secteur).iloc[1,0][7:]
        for secteur in Prenoms.xls.sheet_names
    }
