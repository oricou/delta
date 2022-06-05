
import pandas as pd
import dateutil
import glob

'''
Authors: Arthur Fan; Hao Ye
Create on 06/05/2022
'''

# Function to preprocess data
def clean_data(df):
    # remove odd rows
    df = df.iloc[::2]
    # Replace non defined data by 0
    df = df.replace('ND', 0)
    # String to numeric 
    df.iloc[:,5:36].apply(pd.to_numeric)
    
    # groupby date
    df = df.groupby(pd.Grouper(key='Date')).sum()
    df.reset_index(inplace=True)
    
    return df

# Retrieve all data needed from data/  
df = pd.concat({dateutil.parser.parse(f.split('RTE-')[1].split('csv')[0]):clean_data(pd.read_csv(f, delimiter=";", low_memory=False)) for f in glob.glob('RTE-*')})
# Sort dataframe 
df.sort_index(inplace=True)
df.reset_index(drop=True, inplace=True)

df_full = df.copy()

# Transform column Date to datetime type
df_full['Date'] = pd.to_datetime(df_full['Date'], format='%d/%m/%Y')
# Set Date column to index
df_full.set_index('Date', inplace=True)
# Rename columns 
df_full.rename(columns={'NuclÈaire': 'Nuclèaire',
                   'BioÈnergies': 'Bioénergies'}, inplace=True)
# Select all columns needed for the analysis 
selection = ['Fioul', 'Charbon', 'Nuclèaire', 'Eolien', 'Solaire', 'Hydraulique', 'Bioénergies']
df_full_selected = df_full[selection]

# Save the dataframe into pickle file 
df_full_selected.to_pickle("preprocessed_maingraphdata.pkl")

# Group datas by month
df_animated = df_full_selected.groupby(pd.Grouper(freq='M')).sum().copy()
df_animated.reset_index(inplace=True)
# Group and sum datas by type of production
df_animated = df_animated.melt(id_vars="Date", var_name="Type", value_name="Value")
# Sort dataframe by index 
df_animated.sort_index(inplace=True)
# Transform Data column to string type
df_animated['Date'] = df_animated['Date'].apply(lambda x: str(x))
# Save the dataframe into pickle file 
df_animated.to_pickle("preprocessed_barplotdata.pkl")

df_prix = pd.read_csv('TRV_electricite_2012-2022.csv', delimiter=';', decimal=',')
# Clean data
df_prix.drop(columns=['Unnamed: 7', 'DATE_FIN'], inplace=True)
# Transform column DATE_DEBUT to datetime type
df_prix['DATE_DEBUT'] = pd.to_datetime(df_prix['DATE_DEBUT'], format='%d/%m/%Y')
# Set DATE_DEBUT column to index 
df_prix.set_index('DATE_DEBUT', inplace=True)
# Multiply by 1000 to correspond the price of 1 million watt of electricity
df_prix[['PART_FIXE_HT','PART_FIXE_TTC','PART_VARIABLE_HT','PART_VARIABLE_TTC']] = df_prix[['PART_FIXE_HT','PART_FIXE_TTC','PART_VARIABLE_HT','PART_VARIABLE_TTC']] * 1000
# Save the dataframe into pickle file 
df_prix.to_pickle("preprocessed_pricedata.pkl")
