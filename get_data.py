import pandas as pd
import json
import plotly.express as px
import numpy as np
from IPython.display import Image
import pickle

def getJoinCity():
    tmp = df.copy()
    tmp = tmp.groupby(['Commune'])['Commune'].count().reset_index(name='Nombre de catastrophe')

    dfJoinCity = tmp.join(dfCity.set_index('name'), on='Commune')
    dfJoinCity = dfJoinCity.dropna()

    dfJoinCity['Nombre de catastrophe log'] = np.log10(dfJoinCity['Nombre de catastrophe'])
    return dfJoinCity

def getJoinRegion(dfJoinCity):
    dfJoinRegion = dfJoinCity.copy()
    dfJoinRegion = dfJoinRegion.groupby(['department_code'])['Nombre de catastrophe'].sum().reset_index()
    return dfJoinRegion

def getJoinMonth(dfJoin):
    tmp = dfJoin.copy()
    
    tmp['Nombre de catastrophe'] = 1
    
    tmp['date'] = tmp["debut"].dt.strftime('%m')
    tmp['date'] = pd.to_datetime(tmp['date'],format='%m')

    per = tmp.date.dt.to_period("M")
    g = tmp.groupby(per)
    g = g.sum().reset_index()


    g['Mois'] = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
    
    return g

def sumByYear(df):
    lst = []
    
    for e in range(1982, 2015):
        lst.append(df[pd.DatetimeIndex(df['debut']).year == e])

    return pd.DataFrame({"Année": range(1982, 2015), "Nombre de catastrophe": [len(e) for e in lst]})

df = pd.read_excel('data/Arretes_de_catastrophe_naturelles.xlsx')
df['debut'] = pd.to_datetime(df['Date début'],format='%Y%m%d')
df['fin'] = pd.to_datetime(df['Date fin'],format='%Y%m%d')

dfCity = pd.read_csv('./data/cities.csv')
dfCity = dfCity[dfCity['department_code'] <= "95"]

dfJoinCity = getJoinCity()
dfJoinRegion = getJoinRegion(dfJoinCity)
dfJoinMonth = getJoinMonth(df)
dfByYear = sumByYear(df)

data = []
data.append(dfJoinCity)
data.append(dfJoinRegion)
data.append(dfJoinMonth)
data.append(dfByYear)

file = open('data/save_data', 'wb')
pickle.dump(data, file)
file.close()
