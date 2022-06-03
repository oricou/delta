import requests
import os
import pandas as pd

url_lieux = [
        {"lieux_2015.csv" : "https://www.data.gouv.fr/fr/datasets/r/31db21ef-4328-4c5e-bf3d-66a8fe82e6a2"},
        {"lieux_2016.csv" : "https://www.data.gouv.fr/fr/datasets/r/08b77510-39c4-4761-bf02-19457264790f"},
        {"lieux_2017.csv" : "https://www.data.gouv.fr/fr/datasets/r/9b76a7b6-3eef-4864-b2da-1834417e305c"},
        {"lieux_2018.csv" : "https://www.data.gouv.fr/fr/datasets/r/d9d65ca1-16a3-4ea3-b7c8-2412c92b69d9"},
        {"lieux_2019.csv" : "https://www.data.gouv.fr/fr/datasets/r/2ad65965-36a1-4452-9c08-61a6c874e3e6"},
        {"lieux_2020.csv" : "https://www.data.gouv.fr/fr/datasets/r/e85c41f7-d4ea-4faf-877f-ab69a620ce21"}
      ]

url_carac = [
        {"caracteristiques_2020.csv" : "https://www.data.gouv.fr/fr/datasets/r/07a88205-83c1-4123-a993-cba5331e8ae0"},
        {"caracteristiques_2019.csv" : "https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a"},
        {"caracteristiques_2018.csv" : "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405"},
        {"caracteristiques_2017.csv" : "https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354"},
        {"caracteristiques_2016.csv" : "https://www.data.gouv.fr/fr/datasets/r/96aadc9f-0b55-4e9a-a70e-c627ed97e6f7"},
        {"caracteristiques_2015.csv" : "https://www.data.gouv.fr/fr/datasets/r/185fbdc7-d4c5-4522-888e-ac9550718f71"}
        ]

try:
    os.mkdir("Lieux")
    os.mkdir("Caracteristiques")
except FileExistsError:
    pass

for item in url_lieux:
    for name, link in item.items():
        response = requests.get(link)
        open("Lieux/" + name, "wb").write(response.content)

for item in url_carac:
    for name, link in item.items():
        response = requests.get(link)
        open("Caracteristiques/" + name, "wb").write(response.content)

solver = {'voie' : 'O'}
df_2015 = pd.read_csv("Lieux/lieux_2015.csv")
df_2016 = pd.read_csv("Lieux/lieux_2016.csv", dtype=solver)
df_2017 = pd.read_csv("Lieux/lieux_2017.csv", dtype=solver)
df_2018 = pd.read_csv("Lieux/lieux_2018.csv", dtype=solver)
df_2019 = pd.read_csv("Lieux/lieux_2019.csv", sep=";")
df_2020 = pd.read_csv("Lieux/lieux_2020.csv", sep=";")
a = pd.read_csv("Caracteristiques/caracteristiques_2015.csv", encoding="latin-1")
b = pd.read_csv("Caracteristiques/caracteristiques_2016.csv", encoding="latin-1")
c = pd.read_csv("Caracteristiques/caracteristiques_2017.csv", encoding="latin-1")
d = pd.read_csv("Caracteristiques/caracteristiques_2018.csv", encoding="latin-1")
e = pd.read_csv("Caracteristiques/caracteristiques_2019.csv", sep=";")
f = pd.read_csv("Caracteristiques/caracteristiques_2020.csv", sep=";")
df_lieux = pd.concat([df_2015, df_2016, df_2017, df_2018, df_2019, df_2020])
df_carac = pd.concat([a, b, c, d, e, f])

df_final = df_lieux.merge(df_carac, on="Num_Acc", how="left",)
column_list = ["catr", "prof", "surf", "col","atm", "int", "lum", "plan", "mois", "an"]
df_final = df_final[column_list]
for column in df_final:
    df_final = df_final.loc[df_final[column] >= 0]
dates = {15 : 2015,
         16 : 2016,
         17 : 2017,
         18 : 2018}
    
for a,b in dates.items():
    df_final['an'].mask(df_final['an'] == a, b, inplace=True)    

df_final.to_csv("final_df.csv")
