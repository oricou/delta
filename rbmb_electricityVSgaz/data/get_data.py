
import pandas as pd
import numpy as np

def get_data_energies_from_EC_Europa_EU(filename="rbmb_electricityVSgaz/data/nrg_ind_peh.xlsx"):
    """
    Prend en entrée le path vers un fichier excel contenant les données et renvois un dictionnaire ayant pour clés
    les différents types d'énergies du fichier excel et contenant les dataframes associées.
    """
    
    xls = pd.ExcelFile(filename)

    energies = {}

    en_tot = pd.read_excel(xls, 'Feuille 1', skiprows = range(0,11))
    energies["Total"] = en_tot

    carburant_comb = pd.read_excel(xls, 'Feuille 2', skiprows = range(0,11))
    energies["Carburant Combustibles"] = carburant_comb

    hydraulique = pd.read_excel(xls, 'Feuille 3', skiprows = range(0,11))
    energies["Hydraulique"] = hydraulique

    energie_hydraulique_pompage = pd.read_excel(xls, 'Feuille 4', skiprows = range(0,11))
    energies["Hydraulique Pompage"] = energie_hydraulique_pompage

    geothermie = pd.read_excel(xls, 'Feuille 5', skiprows = range(0,11))
    energies["Géothermique"] = geothermie

    eolien = pd.read_excel(xls, 'Feuille 6', skiprows = range(0,11))
    energies["Éolien"] = eolien

    solaire = pd.read_excel(xls, 'Feuille 7', skiprows = range(0,11))
    energies["Solaire"] = solaire

    energie_hydrocinétique_houlomotrice_marémotrice = pd.read_excel(xls, 'Feuille 8', skiprows = range(0,11))
    energies["Hydrocinétique, houlomotrice et marémotrice"] = energie_hydrocinétique_houlomotrice_marémotrice

    nucleaire = pd.read_excel(xls, 'Feuille 9', skiprows = range(0,11))
    energies["Nucleaire"] = nucleaire

    for i in energies:
        energies[i] = energies[i].drop(0)
    
    for i in energies:
        energies[i].index = range(0, len(energies[i].index))
        energies[i] = energies[i][:43]
        energies[i].rename(columns={'TIME':'Pays'}, inplace=True)
        energies[i] = energies[i].set_index('Pays')
    
        for e in energies[i]:
            energies[i].loc[energies[i][e] == ':', e] = 0
            energies[i].replace(np.nan, 0)
        
        energies[i] = energies[i].apply(pd.to_numeric)
        
    return energies

def get_data_gaz_from_EC_Europa_EU(filename="rbmb_electricityVSgaz/data/env_air_gge.xlsx"):
    """
    Prend en entrée le path vers un fichier excel contenant les données et renvois un dictionnaire ayant pour clés
    les différents types d'énergies du fichier excel et contenant les dataframes associées.
    """
    
    xls = pd.ExcelFile(filename)

    energies = {}

    en_tot = pd.read_excel(xls, 'Feuille 1', skiprows = range(0,9))
    energies["Total"] = en_tot

    energie = pd.read_excel(xls, 'Feuille 2', skiprows = range(0,9))
    energies["Production énergétique"] = energie

    Combustion_de_combustibles_approche_sectorielle = pd.read_excel(xls, 'Feuille 3', skiprows = range(0,9))
    energies["Combustion combustibles (approche sectorielle)"] = Combustion_de_combustibles_approche_sectorielle

    Combustibles_emissions_fugitives = pd.read_excel(xls, 'Feuille 4', skiprows = range(0,9))
    energies["Combustion combustibles (émission fugitives)"] = Combustibles_emissions_fugitives

    Transport = pd.read_excel(xls, 'Feuille 5', skiprows = range(0,9))
    energies["Transport"] = Transport

    Processus_industriels_et_utilisations_de_produits = pd.read_excel(xls, 'Feuille 6', skiprows = range(0,9))
    energies["Industrie"] = Processus_industriels_et_utilisations_de_produits

    Agriculture = pd.read_excel(xls, 'Feuille 7', skiprows = range(0,9))
    energies["Agriculture"] = Agriculture

    Utilisation_des_sols = pd.read_excel(xls, 'Feuille 8', skiprows = range(0,9))

    Gestion_des_déchets = pd.read_excel(xls, 'Feuille 9', skiprows = range(0,9))
    energies["Traitement déchets"] = Gestion_des_déchets
    
    Autres_secteurs = pd.read_excel(xls, 'Feuille 10', skiprows = range(0,9))
    energies["Autre"] = Autres_secteurs
    
    CO2_indirect = pd.read_excel(xls, 'Feuille 11', skiprows = range(0,9))
    energies["CO2 Indirect"] = CO2_indirect

    for i in energies:
        energies[i] = energies[i].drop(0)
    
    for i in energies:
        energies[i].index = range(0, len(energies[i].index))
        energies[i] = energies[i][:35]
        
        energies[i].rename(columns={'TIME':'Pays'}, inplace=True)
        energies[i] = energies[i].set_index('Pays')
        energies[i] = energies[i].loc[:, ~energies[i].columns.str.contains("Unnamed")]

        for e in energies[i]:
            energies[i].loc[energies[i][e] == ':', e] = 0
            energies[i].replace(np.nan, 0)
        
        energies[i] = energies[i].apply(pd.to_numeric)

    return energies

energies = get_data_energies_from_EC_Europa_EU()
gazes = get_data_gaz_from_EC_Europa_EU()

for key in gazes:
    gazes[key] = gazes[key].drop(['1985', '1986', '1987', '1988', '1989'], axis=1)
    
for key in energies:
    energies[key] = energies[key].drop(['2020'], axis=1)
    
index = energies["Total"].index
new_index = gazes["Total"].index.intersection(index)

for key in energies:
    energies[key] = energies[key].loc[new_index, :]
    
for key in gazes:
    gazes[key] = gazes[key].loc[new_index, :]
    
ratio_polution_energie = energies["Total"]/gazes["Total"]

camembert_électricités = {}
camembert_gaz = {}

pays = energies["Total"].index

for key in energies:
    if key != "Total":
        camembert_électricités[key] = energies[key]/energies["Total"]
    
        camembert_électricités[key].replace(np.nan, 0)
    
for key in gazes:
    if key != "Total":
        camembert_gaz[key] = gazes[key]/gazes["Total"]
    
        camembert_gaz[key].replace(np.nan, 0)

index = []
for e in energies:
    index.append(e)

keys = energies["Total"].columns
dico = {}

L = []
L_col_eq = []

for e in energies:
    L = []
    for col in energies[e]:
        L.append(energies[e][col].values)
    
    L_col_eq.append((e,L))

loop = len(L_col_eq[0][1])
L_n = []

for j in range(loop):
    for i in range(len(L_col_eq)):
        dico[L_col_eq[i][0]] = L_col_eq[i][1][j]
        
    L_n.append(pd.DataFrame(dico))

camembert = {}

for i in range(len(keys)):
    L_n[i].index = pays
    camembert[keys[i]] = L_n[i]
