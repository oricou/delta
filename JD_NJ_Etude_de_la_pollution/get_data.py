# Python libraries 
import zipfile
import shutil
import os
import toolz
# Other libraries
import pandas as pd 

# ===== Global variables =====

# The whole 2021 months list
months_list = [
    '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
    '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12'
]

# The list of all our polluants
polluants_list = [
    'PM10', 'NO', 'NO2', 'O3', 'NOX as NO2', 'PM2.5', 'C6H6', 'SO2', 'CO'
]

# The list of all our france's regions
regions_list = [
    'Grand Est', "Provence-Alpes-Côte d'Azur", 'Île-de-France', 'Normandie',
    'Hauts-de-France', 'Auvergne-Rhône-Alpes', 'Occitanie',
    'Nouvelle-Aquitaine', 'Bretagne', 'Pays de la Loire',
    'Bourgogne-Franche-Comté', 'Centre-Val de Loire', 'Guadeloupe',
    'La Réunion', 'Martinique', 'Guyane', 'Corse', 'Mayotte'
]

# Dict of the polluants and their mesure for a easy use of them
dict_mesures_polluants = {
    "NO": "µg-m3",
    "NO2": "µg-m3",
    "O3": "µg-m3",
    "NOX as NO2": "µg-m3",
    "PM10": "µg-m3",
    "PM2.5": "µg-m3",
    "C6H6": "µg-m3",
    "SO2": "µg-m3",
    "CO": "mg-m3"
}

# Dict to change the region names
dict_regions = {
    'ZAG PARIS': "Île-de-France",
    'ZR ILE-DE-FRANCE': "Île-de-France",
    'ZAR SAINT-DENIS': "Île-de-France",
    'ZAG ORLEANS': "Centre-Val de Loire",
    'ZR CENTRE-VAL DE LOIRE': "Centre-Val de Loire",
    'ZAG TOURS': "Centre-Val de Loire",
    'ZAR CHARTRES-DREUX': "Centre-Val de Loire",
    'ZAR BLOIS': "Centre-Val de Loire",
    'ZAR DIJON': "Bourgogne-Franche-Comté",
    'ZR BOURGOGNE-FRANCHE-COMTE': "Bourgogne-Franche-Comté",
    'ZAR CHALON': "Bourgogne-Franche-Comté",
    'ZAR BESANCON': "Bourgogne-Franche-Comté",
    'ZAR BELFORT-MONTBELIARD': "Bourgogne-Franche-Comté",
    'ZAR LE-HAVRE': "Normandie",
    'ZR NORMANDIE': "Normandie",
    'ZAG ROUEN': "Normandie",
    'ZAR CAEN': "Normandie",
    'ZAR DIEPPE': "Normandie",
    'ZAG BLDV': "Hauts-de-France",
    'ZR HAUTS-DE-FRANCE': "Hauts-de-France",
    'ZAR COTE-D-OPALE': "Hauts-de-France",
    'ZAG LILLE': "Hauts-de-France",
    'ZAR CREIL': "Hauts-de-France",
    'ZAR AMIENS': "Hauts-de-France",
    'ZAR ARRAS': "Hauts-de-France",
    'ZAG METZ': "Grand Est",
    'ZR GRAND-EST': "Grand Est",
    'ZAR REIMS': "Grand Est",
    'ZAG STRASBOURG': "Grand Est",
    'ZAG NANCY': "Grand Est",
    'ZAG NANTES-SAINT-NAZAIRE': "Pays de la Loire",
    'ZR PAYS-DE-LA-LOIRE': "Pays de la Loire",
    'ZAR ANGERS-LOIRE': "Pays de la Loire",
    'ZAR LAVAL': "Pays de la Loire",
    'ZAR LE-MANS': "Pays de la Loire",
    'ZAG RENNES': "Bretagne",
    'ZAR BREST': "Bretagne",
    'ZR BRETAGNE': "Bretagne",
    'ZR NOUVELLE-AQUITAINE': "Nouvelle-Aquitaine",
    'ZAR POITIERS': "Nouvelle-Aquitaine",
    'ZAR NIORT': "Nouvelle-Aquitaine",
    'ZAG BORDEAUX': "Nouvelle-Aquitaine",
    'ZAR LIMOGES': "Nouvelle-Aquitaine",
    'ZAG POINTE-A-PITRE': "Guadeloupe",
    'ZR GUADELOUPE': "Guadeloupe",
    'ZAR FORT-DE-FRANCE': "Martinique",
    'ZR MARTINIQUE': "Martinique",
    'ZR GUYANE': "Guyane",
    'ZAR ILE-DE-CAYENNE': "Guyane",
    'ZAR VOLCAN': "La Réunion",
    'ZR LA REUNION': "La Réunion",
    'ZR MAYOTTE': "Mayotte",
    'ZAG MONTPELLIER': "Occitanie",
    'ZR OCCITANIE': "Occitanie",
    'ZAR NIMES': "Occitanie",
    'ZAR PERPIGNAN': "Occitanie",
    'ZAG TOULOUSE': "Occitanie",
    'ZAG CLERMONT-FERRAND': "Auvergne-Rhône-Alpes",
    'ZR AUVERGNE-RHONE-ALPES': "Auvergne-Rhône-Alpes",
    'ZAR MOULINS': "Auvergne-Rhône-Alpes",
    'ZAG GRENOBLE': "Auvergne-Rhône-Alpes",
    'ZAG LYON': "Auvergne-Rhône-Alpes",
    'ZAR VALLEE-DU-RHONE': "Auvergne-Rhône-Alpes",
    'ZAG SAINT-ETIENNE': "Auvergne-Rhône-Alpes",
    'ZAR PAYS-DE-SAVOIE': "Auvergne-Rhône-Alpes",
    'ZAR VALLEE-DE-L-ARVE': "Auvergne-Rhône-Alpes",
    'ZAR VALLEE-DE-LA-TARANTAISE': "Auvergne-Rhône-Alpes",
    'ZAG MARSEILLE-AIX': "Provence-Alpes-Côte d'Azur",
    'ZR PROVENCE-ALPES-COTE D?AZUR': "Provence-Alpes-Côte d'Azur",
    'ZAG TOULON': "Provence-Alpes-Côte d'Azur",
    'ZAR FREJUS-DRAGUIGNAN': "Provence-Alpes-Côte d'Azur",
    'ZAG AVIGNON': "Provence-Alpes-Côte d'Azur",
    'ZAG NICE': "Provence-Alpes-Côte d'Azur",
    'ZAR AJACCIO': "Corse",
    'ZR CORSE': "Corse",
    'ZAR BASTIA': "Corse"
}

# ===== Functions used =====

# Function used to clean the dataset
def clean_dataset(dataset):
    # Changing regions names and dropping columns
    df_to_clean = dataset.replace({"Zas": dict_regions})

    drop_columns = [
        'Organisme', 'code zas', 'code site', 'nom site',
        "type d'implantation", "type de valeur", "valeur brute",
        'taux de saisie', 'couverture temporelle', 'couverture de données',
        "Réglementaire", "validité", "code qualité", "type d'évaluation"
    ]
    df_to_clean = df_to_clean.drop(columns=drop_columns)

    # Renaming the columns
    dict_rename = {
        'Zas': 'Region',
        "type d'influence": "Influence",
        "unité de mesure": "Mesure",
        "valeur": "Valeur",
    }

    # Renaming the columns and dropping nan values
    df_to_clean = df_to_clean.rename(columns=dict_rename)
    df_to_clean = df_to_clean.dropna()

    # Changing the type to datetime
    df_to_clean["Date de fin"] = pd.to_datetime(df_to_clean["Date de fin"])
    df_to_clean["Date de début"] = pd.to_datetime(df_to_clean["Date de début"])

    # Reset index and changing the index
    df_to_clean = df_to_clean.reset_index()
    df_to_clean = df_to_clean.drop(columns=['index'])
    # df_to_clean = df_to_clean.set_index("Date de fin")
    df_to_clean = df_to_clean.sort_index()

    # Dict to change the values of the mesure to have unique types
    mesure_change = {"µg/m3": "µg-m3"}

    # Changing the values for uniformity
    df_to_clean = df_to_clean.replace({"Mesure": mesure_change})

    return df_to_clean

# Function used to clean our dataset before saving them to month
def cleaning_and_saving_month(year_month, save_file=True) : 
    # Generating the list of the files to open to load the desired month
    month_file_list = [f[f.find(year_month):] for f in os.listdir('raw_data/pollution_data_year_2021') if f.find(year_month) != -1]
    # Creating a dictionnary of the dataframe and their name by reading them
    dict_month = { i[:i.find('.')] : pd.read_csv('raw_data/pollution_data_year_2021/FR_E2_' + i, sep=';') for i in month_file_list }
    # Cleaning each of our dataframes before creating our super DataFrame
    dict_cleaned_month = toolz.valmap(clean_dataset, dict_month)
    # Creating our super DataFrame
    df_cl_month = pd.concat(dict_cleaned_month)
    # Saving our dataframe
    if save_file :
        df_cl_month.to_csv(path_or_buf = "raw_data/month_cleaned_data/cleaned_" + year_month + ".csv", sep = ';')
    # Returning our cleaned dataframe
    return df_cl_month

# Function to load our datasets 
def dataset_load(month) :
    df_cleaned_load = pd.read_csv("raw_data/month_cleaned_data/cleaned_" + month + ".csv", sep=';')
    df_indexes_load = df_cleaned_load.set_index(['Unnamed: 0', 'Unnamed: 1'])
    df_indexes_load.index.rename(['Date', 'Index'], inplace=True)
    # Changing the type to datetime
    df_indexes_load["Date de fin"] = pd.to_datetime(df_indexes_load["Date de fin"])
    df_indexes_load["Date de début"] = pd.to_datetime(df_indexes_load["Date de début"])
    return df_indexes_load

# Function used to make month influences sum for our data
def create_month_dataframe_influences(dataframe, date):
    dataframe = dataframe.drop(
        columns=["Mesure", "Valeur", "Date de fin", "Date de début"])
    resdf = pd.DataFrame()
    for region in regions_list:
        for polluant in polluants_list:
            # Getting the serie of the counts for each possible influence
            res_count = dataframe[(dataframe["Region"] == region)
                                  & (dataframe["Polluant"] == polluant
                                     )]["Influence"].value_counts()

            # Transforming that serie in a dataframe to transpose and easily get the values
            df_tmp = pd.DataFrame(res_count).transpose()

            # Getting each value from the result (0 if not in the dataframe)
            fond_count = df_tmp["Fond"].values[
                0] if "Fond" in df_tmp.columns else 0
            industrielle_count = df_tmp["Industrielle"].values[
                0] if "Industrielle" in df_tmp.columns else 0
            trafic_count = df_tmp["Trafic"].values[
                0] if "Trafic" in df_tmp.columns else 0

            # If there is no value, then we don't need to add a new row
            if not (fond_count == 0 and industrielle_count == 0
                    and trafic_count == 0):
                # Creating our new dataframe and add the informations
                data = {
                    "Region": region,
                    "Polluant": polluant,
                    "Industrielle": industrielle_count,
                    "Fond": fond_count,
                    "Trafic": trafic_count
                }
                df_to_add = pd.DataFrame(data, index=[date])

                resdf = resdf.append(df_to_add)

    resdf.index = pd.to_datetime(resdf.index)
    return resdf

# Function used to create the monthly_influences dataframe
def save_influences_csv(save_file=True) : 
    res = pd.DataFrame()
    for month in months_list :
        print("Month : {0}".format(month))
        df_month = create_month_dataframe_influences(dataset_load(month), month)
        res = res.append(df_month)
    res.index.name = "Date"
    if (save_file) : 
        res.to_csv(path_or_buf = "data/monthly_influences.csv", sep = ';')
        res.to_csv(path_or_buf = "../data/monthly_influences.csv", sep = ';')
    return res

# Function used to make daily average for our data
def day_average_data(dataset, do_display=False):
    # Final dataframe (we append for each day)
    res = pd.DataFrame()

    for polluant in polluants_list:
        for region in regions_list:
            df_polluant_region = dataset[(dataset["Region"] == region) & (dataset["Polluant"] == polluant)]
            # Checking if the dataframe for this region and polluant is empty or not
            if not df_polluant_region.empty :
                # Keeping the mesure for the result dataset
                unite_mesure = df_polluant_region["Mesure"].unique()[0]
                
                # Doing the mean of the polluant for this region and day
                mean_df_day_res = df_polluant_region.groupby(pd.Grouper(freq='D')).mean()

                # Adding the missing columns
                mean_df_day_res["Polluant"] = polluant
                mean_df_day_res["Region"] = region
                mean_df_day_res["Mesure"] = unite_mesure
                
                # Display the informations if we want to
                if do_display : 
                    print("Region : {0} | Polluant : {1} | Mesure : {2}".format(region, polluant, unite_mesure))
                    print(mean_df_day_res)
                    
                res = res.append(mean_df_day_res)
    res = res.sort_index()
    return res

# Function used to create the monthly_day_average dataframe
def create_and_save_df_average_days(save_file = True) :
    res = pd.DataFrame()
    for month in months_list : 
        print("Month : {0}".format(month))
        month_df = dataset_load(month)
        month_df = month_df.reset_index()
        month_df = month_df.drop(columns=["Date", "Index", "Date de fin"]).set_index("Date de début")
        df_day_average = day_average_data(month_df)
        df_day_average.index = df_day_average.index.rename("Date")
        res = res.append(df_day_average)
    if save_file : 
        res.to_csv(path_or_buf = "data/monthly_day_average.csv", sep = ';')
        res.to_csv(path_or_buf = "../data/monthly_day_average.csv", sep = ';')
    return res

# Function used to make hourly average for our data
def hour_average_data(dataset, do_display=False):
    # Final dataframe (we append for each day)
    res = pd.DataFrame()

    for polluant in polluants_list:
        for region in regions_list:
            df_polluant_region = dataset[(dataset["Region"] == region) & (dataset["Polluant"] == polluant)]
            # Checking if the dataframe for this region and polluant is empty or not
            if not df_polluant_region.empty :
                # Keeping the mesure for the result dataset
                unite_mesure = df_polluant_region["Mesure"].unique()[0]
                
                # Doing the mean of the polluant for this region and day
                mean_df_day_res = df_polluant_region.groupby(pd.Grouper(freq='H')).mean()

                # Adding the missing columns
                mean_df_day_res["Polluant"] = polluant
                mean_df_day_res["Region"] = region
                mean_df_day_res["Mesure"] = unite_mesure
                
                # Display the informations if we want to
                if do_display : 
                    print("Region : {0} | Polluant : {1} | Mesure : {2}".format(region, polluant, unite_mesure))
                    print(mean_df_day_res)
                    
                res = res.append(mean_df_day_res)
    res = res.sort_index()
    return res

# Function used to create the monthly_hour_average dataframe
def create_and_save_df_average_hours(save_file = True) :
    res = pd.DataFrame()
    for month in months_list :
        print("Month : {0}".format(month))
        month_df = dataset_load(month)
        month_df = month_df.reset_index()
        month_df = month_df.drop(columns=["Date", "Index", "Date de fin"]).set_index("Date de début")
        df_hour_average = hour_average_data(month_df)
        df_hour_average.index = df_hour_average.index.rename("Date")
        res = res.append(df_hour_average)
    if save_file : 
        res.to_csv(path_or_buf = "data/monthly_hour_average.csv", sep = ';')
        res.to_csv(path_or_buf = "../data/monthly_hour_average.csv", sep = ';')
    return res

# Function used to unzip our data
def unzip_data(): 
    if not 'pollution_data_year_2021' in os.listdir("raw_data") : 
        zipList = os.listdir("raw_data")
        try: 
            os.mkdir("raw_data/pollution_data_year_2021") 
        except OSError : 
            pass
        for compressedData in zipList : 
            with zipfile.ZipFile('raw_data/' + compressedData, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                zipObj.extractall('raw_data/pollution_data_year_2021/')
                # Done !

# Check if the files exists and delete them if its the case to avoid conflicts
def clean_files() : 
    # Try creating a folder for the monthly data
    try: 
        os.mkdir("raw_data/month_cleaned_data") 
    except OSError : 
        pass
    
    # If we already have file in our data folder, 
    # Then we delete it to avoid conflicts : 
    if len(os.listdir("data")) == 4 : 
        if "monthly_day_average.csv" in os.listdir("data") : 
            os.remove("data/monthly_day_average.csv")
        if "monthly_hour_average.csv" in os.listdir("data") : 
            os.remove("data/monthly_hour_average.csv")
        if "monthly_influences.csv" in os.listdir("data") : 
            os.remove("data/monthly_influences.csv")
    # Remove from source data for delta project
    if "monthly_day_average.csv" in os.listdir("../data") : 
        os.remove("../data/monthly_day_average.csv")
    if "monthly_hour_average.csv" in os.listdir("../data") : 
        os.remove("../data/monthly_hour_average.csv")
    if "monthly_influences.csv" in os.listdir("../data") : 
        os.remove("../data/monthly_influences.csv")

# Function to delete the files that we don't use anymore
def delete_raw_and_temporary_files() :
    print("Starting deleting raw data...")
    if os.path.isdir('raw_data/pollution_data_year_2021'):
        # remove directory and all its content
        shutil.rmtree('raw_data/pollution_data_year_2021')
    else:
        raise ValueError("Path {} is not a file or dir.".format('raw_data/pollution_data_year_2021'))
    print("Deleting raw data done !\n")
    
    print("Starting deleting monthly data files...")
    if os.path.isdir('raw_data/month_cleaned_data'):
        # remove directory and all its content
        shutil.rmtree('raw_data/month_cleaned_data')
    else:
        raise ValueError("Path {} is not a file or dir.".format('raw_data/month_cleaned_data'))
    print("Monthly data files deleted !\n")

# Function used to load the monthly_day_average dataframe
def load_day_average() : 
    return pd.read_csv("data/monthly_day_average.csv")

# Function used to load the monthly_hour_average dataframe
def load_hour_average() : 
    return pd.read_csv("data/monthly_hour_average.csv")

# Function used to load the monthly_influences dataframe
def load_influences() : 
    return pd.read_csv("data/monthly_influences.csv")

def main() : 
    # Unzip the data
    print("Starting to unzip the data and clean data to avoid conflicts...")
    unzip_data()
    clean_files()
    print("Done !\n")
    
    # Loop to save all of our monthly files
    print("Starting cleaning and saving of the months...")
    for month in months_list : 
        # Prevent from override
        cleaning_and_saving_month(month, save_file=True)
        print("Month done : {}".format(month))
    print("Cleaning and saving of the month done !\n")
    
    print("Starting creating and saving the dataframe of the months influences...")
    save_influences_csv(save_file=True)
    print("Creating and saving the dataframe of the months influences done !\n")

    print("Starting creating and saving the dataframe of the daily average values for each region...")
    create_and_save_df_average_days(save_file=True)
    print("Creating and saving the dataframe of the daily average values for each region done !\n")
    
    print("Starting creating and saving the dataframe of the hourly average values for each region...")
    create_and_save_df_average_hours(save_file=True)
    print("Creating and saving the dataframe of the hourly average values for each region done !\n")
    
    # Removing all the raw and temporaty data to as we don't need it anymore
    print("Starting removing unused files...")
    delete_raw_and_temporary_files()
    print("Unused files removed !\n")
  

if __name__ == '__main__':
    main()