import pandas as pd

path_hapiness_report = "data/Happiness-Report.csv"
path_countries_continents = "data/Countries-Continents.csv"


# <----------------------IMPORT ET TRAITEMENT DU DATASET Happiness-Report---------------------->

df_hr = pd.read_csv(path_hapiness_report, sep=",", encoding="UTF-8")

# Renommage des colonnes
df_hr_col_en = ["Country name","year","Life Ladder","Log GDP per capita",
              "Social support","Healthy life expectancy at birth","Freedom to make life choices",
              "Generosity","Perceptions of corruption,Positive affect","Negative affect"]
df_hr_col_fr = ["Pays","Année","Echelle de vie","log PIB par habitant","Support social",
              "Espérance de vie","Liberté de vivre","Générosité","Perception de la corruption",
              "Effets positifs","Effets négatifs"]
df_hr.columns = df_hr_col_fr
## df_hr.interpolate(method = 'linear', inplace = True)

# <--------------------IMPORT ET TRAITEMENT DU DATASET Countries-Continents-------------------->

df_cc = pd.read_csv(path_countries_continents, sep=",", encoding="UTF-8")

# Renommage des colonnes et utilisation des pays comme index (pour pouvoir utiliser df_cc["Pays"]
df_cc_col_en = ["Continents", "Countries"]
df_cc_col_fr = ["Continent", "Pays"]
df_cc.columns = df_cc_col_fr
df_cc.set_index("Pays", inplace = True)
