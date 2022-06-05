import pandas as pd
import numpy as np

# Function create to filter all the database having the same form
def filter_df(df):
    df.drop(columns = ['ANAIS1', 'DEPNAIS1', 'INDNAT1', 'ETAMAT1', 'ANAIS2', 'DEPNAIS2', 'INDNAT2','ETAMAT2',
                       'JSEMAINE', 'DEPDOM', 'TUDOM', 'TUCOM', 'NBENFCOM'], axis=1, inplace=True)
    
# Function to apply to the value of a dataFrame to change their type
def convert(i):
    return int(i)     
    
# Read data    
mar_14 = pd.read_csv("data_mariages_2014.csv", sep=',', low_memory=False)
mar_15 = pd.read_csv("data_mariages_2015.csv", sep=',', low_memory=False)
mar_16 = pd.read_csv("data_mariages_2016.csv", sep=',', low_memory=False)
mar_17 = pd.read_csv("data_mariages_2017.csv", sep=',', low_memory=False)
mar_18 = pd.read_csv("data_mariages_2018.csv", sep=',', low_memory=False)
mar_19 = pd.read_csv("data_mariages_2019.csv", sep=',', low_memory=False)
mar_20 = pd.read_csv("data_mariages_2020.csv", sep=',', low_memory=False)

mar = pd.read_excel('mariages par mois.xls', skiprows = {0,1, 2, 3, 5, 6},
                    usecols = { 'Ensemble des mariages de l\'année', 'Mois du mariage', 'Janvier',
                               'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre',
                               'Octobre', 'Novembre', 'Décembre'}, skipfooter = 1, dtype=int)
mar = mar.rename(columns={"Mois du mariage": "AMAR"})
        
pacs = pd.read_excel('ensemble des pacs.xlsx', skiprows = {0,1, 2, 4},
                     usecols = {0, 4,5,6}, skipfooter = 16)
pacs = pacs.rename(columns={'Unnamed: 0' : 'AMAR'})

# Filter data
filter_df(mar_14)
filter_df(mar_15)
filter_df(mar_16)
filter_df(mar_17)
filter_df(mar_18)
filter_df(mar_19)
filter_df(mar_20)

# Read file to recover all the French departments
deps = pd.read_excel('departements-francais.xls',
                             usecols = {'NOM', 'NUMÉRO'}, skipfooter = 7)
deps.rename(columns={'NUMÉRO' : 'DEPARTEMENT'}, inplace = True)

# Creation of the database for the histogram starting in 2014
df = pd.concat([mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20])
df.to_csv('mariage_pour_tous.csv')

# Creation of the database for the map
HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
graph = pd.DataFrame(HH.groupby('AMAR').size(), columns = ['Homme_Homme'])
FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
graph = graph.assign(Femme_Femme = FF.groupby('AMAR').size())
HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
graph = graph.assign(Homme_Femme = HF.groupby('AMAR').size())
graph = graph.assign(TOTAL = df.groupby('AMAR').size().astype(int))
        
map_f = graph.copy().drop(["Homme_Homme", "Femme_Femme", "Homme_Femme", "TOTAL"], axis=1)
dep_list = df.groupby("DEPMAR").size().index.tolist()

# Add the data for each department into the database
c = 0
for idx in dep_list:
    col = df[(df['DEPMAR'] == idx)]
    map_f.insert(c, idx,col.groupby('AMAR').size())
    c += 1
map_f = map_f.transpose()
map_f.reset_index(drop = True, inplace = True)
map_f = pd.concat([map_f, deps], axis=1)
# Formatting of the department number on the map
for i in range (0,10):
    map_f.loc[map_f.DEPARTEMENT == i, "DEPARTEMENT"] = "0%i" % i
    
map_f.to_csv('mariage_par_departement.csv')

# Creation of the data base for the graph and histogram before 2014 
# (fusion of different database depending of the years described in the database)
graph = graph.reset_index()
graph['AMAR'] = graph['AMAR'].apply(convert)    
tmp = graph.merge(pacs)
tmp2= pacs.merge(mar)

mar = mar.drop(mar[mar.AMAR > 1998].index)

df = pd.concat([tmp, mar, tmp2], axis=0)
df = df.sort_values(by=['AMAR'])
df['TOTAL'] = df['TOTAL'].fillna(0)
df['Ensemble des mariages de l\'année'] = df['Ensemble des mariages de l\'année'].fillna(0)
df['Total mariage'] = df['TOTAL'] + df['Ensemble des mariages de l\'année']     

df.to_csv('mariage_depuis_1946.csv')
