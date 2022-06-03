import pandas as pd
import json

#Region nettoyage des données.
# Salaire
salary = pd.read_csv("./AV_AN_WAGE_15032022112411307.csv")
salary = salary[salary["SERIES"] == "USDPPP"] # On garde seulement les lignes au prix USD
salary = salary.drop(columns=["Flag Codes", "Flags", "PowerCode", "PowerCode Code", "Reference Period Code", "Temps"]) 

salary = salary.set_index("Pays")
salary_france = salary[salary.index == "France"]

# To pickle
salary.to_pickle("./salary.pkl")

# PIB
pib = pd.read_csv("./DP_LIVE_24032022132056468.csv")  # Value en millions
pib = pib.drop(columns=["Flag Codes"])
pib = pib.rename(columns={'LOCATION' : 'COUNTRY'})

# Merge salary et pib
pib_salary = salary.reset_index().merge(pib, how='inner', on=['COUNTRY', 'TIME']).set_index('Pays')
pib_salary = pib_salary.rename(columns={'Value_y' : "pib", 'Value_x' : "salary"})

# IDH
idh = pd.read_csv("./Human Development Index (HDI).csv", sep =',', encoding='latin-1', skiprows=4, header = 1)
idh = idh.loc[:, ~idh.columns.str.contains('^Unnamed')]
idh = idh.drop(columns=["HDI Rank"])
idh.columns = idh.columns.astype(str)
idh = idh.loc[:, ~idh.columns.str.contains('^1')] #On garde seulement les colonnes des années 2000+
idh = idh.drop(idh.tail(18).index)#remove les dernieres rows qui ne nous servent pas
idh['Country'] = idh['Country'].astype(str)
idh['Country'] = idh['Country'].apply(lambda x: x[1:]) # Remove le premier char invisible.
idh = idh.melt(id_vars=["Country"], var_name="Date", value_name="idh").sort_values(by = ["Country", "Date"]).reset_index(drop=True) #Avant: colonnes = dates et mtn: on les transforme en 
# Pays iso
pays_iso = pd.read_csv("./wikipedia-iso-country-codes.csv", sep =',')
pays_iso = pays_iso.drop(columns=['ISO 3166-2', 'Numeric code'])
pays_iso = pays_iso.rename(columns={"English short name lower case": "Country"})
pays_iso['Country'] = pays_iso['Country'].astype(str)

idh_iso = pd.merge(pays_iso, idh, on=['Country'])
idh_iso = idh_iso.rename(columns = {"Alpha-3 code" : "COUNTRY", "Date" : "TIME"})
idh_iso["TIME"] = idh_iso["TIME"].astype(int)  # Convert le type de TIME en int pour pouvoir le merge plu
# Merge idh et pib_salary
pib_idh_salary = pib_salary.reset_index().merge(idh_iso, how='inner', on=['COUNTRY', 'TIME']).set_index('Pays') #Pour avoir le nom des pays complet et faire le lien avec les autres dataframes
pib_idh_salary["Pays"] = pib_idh_salary.index 

# To pickle
pib_idh_salary.to_pickle("./pib_idh_salary.pkl")

# Salaire homme/femme
hf = pd.read_csv("./sdg_05_20_tabular-1.tsv", sep='\t', na_values=": ")
hf = hf.drop(columns=['2002 ', '2006 ', '2007 ', '2008 ', '2009 '])
hf['freq,unit,nace_r2,geo\TIME_PERIOD'] = hf['freq,unit,nace_r2,geo\TIME_PERIOD'].astype(str)
hf['freq,unit,nace_r2,geo\TIME_PERIOD'] = hf['freq,unit,nace_r2,geo\TIME_PERIOD'].apply(lambda x: x.split(',')[-1])
hf = hf.rename(columns = {"freq,unit,nace_r2,geo\TIME_PERIOD":"Pays"})
hf = hf.set_index("Pays")
hf = hf.apply(lambda x : x.astype(str))
hf = hf.apply(lambda x : x.apply(lambda y: y.split()[0]))
hf = hf.apply(lambda x : x.astype(float))
hf = hf.loc[hf.count(1) > hf.shape[1]/2, hf.count(0) > hf.shape[0]/2] #on supprime les lignes qui on plus de 50% de valeurs manquantes.
hf = hf.drop(index=['EU28', 'EU27_2020', 'EA19']) #inintéressant
hf = hf.fillna(method="ffill", axis=1)
hf["Alpha-2 code"] = hf.index
hf.loc["UK", "Alpha-2 code"] = "GB" #L'angleterre = GB en alpha code 2

# Merge hf et pays iso
hf = pd.merge(hf, pays_iso, how='inner', on="Alpha-2 code")
hf_melted = hf.melt(id_vars=["Country", "Alpha-2 code", "Alpha-3 code"], var_name="Date", value_name="ecart").sort_values(by = ["Country", "Date"]).reset_index(drop=True)# on met les date en ligne et plus en colonnes.

# To pickle
hf.to_pickle("./hf.pkl")
hf_melted.to_pickle("./hf_melted.pkl")