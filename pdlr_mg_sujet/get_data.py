import os
import pandas as pd
from math import exp



abs_path = os.path.dirname(os.path.realpath(__file__)) + "/"

path_hapiness_report = abs_path + "data/Happiness-Report.csv"
path_countries_continents = abs_path + "data/Countries-Continents.csv"


# <--------------------IMPORT ET TRAITEMENT DU DATASET Countries-Continents-------------------->

df_cc = pd.read_csv(path_countries_continents, sep=",", encoding="UTF-8")

# Renommage des colonnes et utilisation des pays comme index (pour pouvoir utiliser df_cc["Pays"]
df_cc.set_index("Country", inplace = True)


# <----------------------IMPORT ET TRAITEMENT DU DATASET Happiness-Report---------------------->

df_hr = pd.read_csv(path_hapiness_report, sep=",", encoding="UTF-8")
df_hr.columns = ["Country", "Year", "Life ladder", "logGDP", "Social support", "Life expectancy", "Freedom of life", "Generosity", "Corruption", "Positive affect", "Negative affect"] 


# Ajoute la colonne des continent et la déplace en 2ème position
df_hr = df_hr.join(df_cc, on = "Country")
tmp = df_hr.pop("Continent")
df_hr.insert(1, "Continent", tmp)

# Convertis le log du PIB en PIB 
df_hr["GDP"] = df_hr.apply(lambda x: round(exp(x["logGDP"]),2), axis=1)
#df_hr.interpolate(method = 'linear', inplace = True)