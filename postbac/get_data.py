import numpy as np
import pandas as pd
import os
import glob


list_column = ['Session', 'Admis', 'Filières très agrégées', 'Effectif total des candidatures', 'Filières très agrégées', 'Effectif des admis boursiers', 'Nombre d\'hommes', 'Nombre de femmes'] 

def remove_useless_column(df):

    df = df.loc[:, df.columns.intersection(list_column)]
    return df
    
def open_and_concat_df():
    
    path = os.path.join(os.getcwd(), 'postbac/data/*.csv')
    files = glob.glob(path)
    return pd.concat((pd.read_csv(i, sep = ';') for i in files))
    
def remove_NaNs_and_unknown(dataframe):

    lenD = len(dataframe.columns)
    for i in range (lenD):
        dataframe.iloc[:, i] = dataframe.iloc[:, i].replace('inconnu', '0')
        dataframe.iloc[:, i] = dataframe.iloc[:, i].replace(np.nan, 0)
        try:
            dataframe.iloc[:, i] = dataframe.iloc[:, i].astype('int64')
        except:
            dataframe.iloc[:, i] = dataframe.iloc[:, i].replace(0, '')
    return dataframe

def rename_columns(dataframe): 
    
    dataframe.rename(columns = {'Effectif total des candidats ayant accepté la proposition de l’établissement (admis)' : 'Candidats admis parcoursup'}, inplace = True)
    dataframe.rename(columns = {'Effectif total des candidats admis' : 'Admis'}, inplace = True)
    dataframe.rename(columns = {'Effectif total des candidats' : 'Effectif total des candidatures'}, inplace = True)
    dataframe.rename(columns = {'Effectif total des candidats admis, dont filles' : 'Nombre de femmes'}, inplace = True)
    return dataframe
    
def fuse_similar_columns(dataframe):

    dataframe['Admis'] += dataframe['Candidats admis parcoursup']
    dataframe['Filière de formation'] +=  dataframe['Filières de formations']
    dataframe['Filières très agrégées'] += dataframe['Filière de formation très agrégée']
    dataframe['Effectif total des candidatures'] += dataframe['Effectif total des candidats pour une formation']
    dataframe['Effectif des admis boursiers'] += dataframe['Dont effectif des admis boursiers néo bacheliers']
    dataframe['Nombre de femmes'] += dataframe['Dont effectif des candidates admises']
    return dataframe
    
def load_data():

    dataframe = open_and_concat_df()
    dataframe = rename_columns(dataframe)
    dataframe = remove_NaNs_and_unknown(dataframe)
    dataframe = fuse_similar_columns(dataframe)


    # This line is to normalize the data of the apb 'fillières très agrégées' column which is made of a number and an underscore (e.g '1_BTS') 
    dataframe['Filières très agrégées'] = dataframe['Filières très agrégées'].str.replace('\d_', '', regex=True)

    # Those lines are used to put similar study branches under the same name 
    dataframe.loc[dataframe['Filières très agrégées'] == 'Ingénieur', 'Filières très agrégées'] = "Ecole d'Ingénieur"
    dataframe.loc[dataframe['Filières très agrégées'] == 'Autre', 'Filières très agrégées'] = 'Autre formation'


    dataframe["Nombre d'hommes"] = dataframe['Admis'].copy()
    dataframe["Nombre d'hommes"] -= dataframe['Nombre de femmes']
    
    dataframe = remove_useless_column(dataframe)
    return dataframe
