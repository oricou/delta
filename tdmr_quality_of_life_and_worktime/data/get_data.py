import os
import glob
from matplotlib.pyplot import axis
import pandas as pd
import plotly

pd.options.plotting.backend = "plotly"

# we get the path of each and every data file
avg_worktime = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/average_worktime_eu_weekly.csv")
hapiness_feelings_frequency = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/hapiness_feelings_frequency_eu_monthly.csv")
depressive_symptoms = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/depressive_symptoms_eu.csv")
life_satistaction = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/life_satistaction_eu.csv")
life_expectancy = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/life_expectancy_eu.csv")

avg_worktime_clean = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/average_worktime_eu_weekly_clean.csv")
hapiness_feelings_frequency_clean = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/hapiness_feelings_frequency_eu_monthly_clean.csv")
depressive_symptoms_clean = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/depressive_symptoms_eu_clean.csv")
life_satistaction_clean = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/life_satistaction_eu_clean.csv")
life_expectancy_clean = os.path.join(os.getcwd(), "tdmr_quality_of_life_and_worktime/data/life_expectancy_eu_clean.csv")

# list of the countries we base our analysis on, EU27_2020 representing the average value for all european countries
featured_countries_code = ["EU27_2020","BE","BG","CZ","DK","DE","EE","IE","EL","ES","FR","HR","IT","CY","LV","LT","LU","HU","MT","NL",
                           "AT","PL","PT","RO","SI","SK","FI","SE","IS","NO","UK","RS","TR"]
featured_countries_name = ["Europe", "Belgique", "Bulgarie","Tchéquie","Danemark","Allemagne",
                           "Estonie","Irelande","Grèce","Espagne","France","Croatie","Italie",
                           "Chypre","Lettonie","Lithuanie","Luxembourg","Hongrie","Malte",
                           "Pays-Bas","Autriche","Pologne","Portugal","Roumanie","Slovénie",
                           "Slovaquie","Finlande","Suisse","Island","Norvège","Royaume-Uni",
                           "Serbie","Turquie"]

def get_avg_worktime_dataframe() -> pd.DataFrame:
    
    if (not os.path.exists(avg_worktime_clean)):
        avg_worktime_df = pd.read_csv(avg_worktime, sep=",")
        avg_worktime_df.drop(columns=["DATAFLOW","LAST UPDATE","freq","unit","OBS_FLAG"], inplace=True)

        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['nace_r2'] != "TOTAL"], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['wstatus'] != "EMP"], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['worktime'] != "TOTAL"], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['age'] != "Y20-64"], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['sex'] != "T"], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[~avg_worktime_df['geo'].isin(featured_countries_code)], inplace=True)
        avg_worktime_df.drop(avg_worktime_df.index[avg_worktime_df['TIME_PERIOD'] != 2018], inplace=True)

        avg_worktime_df["Pays"] = [featured_countries_name[featured_countries_code.index(x)] for x in avg_worktime_df['geo']]
        avg_worktime_df.drop(columns=["nace_r2","wstatus","worktime","sex","age","TIME_PERIOD"], inplace=True)
        avg_worktime_df.rename(columns={"OBS_VALUE":"Temps de travail par semaine"}, inplace=True)
        avg_worktime_df.to_csv(avg_worktime_clean)
        
    else:
        avg_worktime_df = pd.read_csv(avg_worktime_clean)
    
    return avg_worktime_df


def get_hapiness_feelings_dataframe() -> pd.DataFrame:
    
    if (not os.path.exists(hapiness_feelings_frequency_clean)):
        hapiness_feelings_frequency_df = pd.read_csv(hapiness_feelings_frequency, sep=',')
        hapiness_feelings_frequency_df.drop(columns=["DATAFLOW","LAST UPDATE","freq","unit","OBS_FLAG"], inplace=True)

        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[hapiness_feelings_frequency_df['frequenc'] == "UNK"], inplace=True)
        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[hapiness_feelings_frequency_df['sex'] != "T"], inplace=True)
        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[hapiness_feelings_frequency_df['age'] != "Y_GE16"], inplace=True)
        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[hapiness_feelings_frequency_df['isced11'] != "TOTAL"], inplace=True)
        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[hapiness_feelings_frequency_df['TIME_PERIOD'] != 2018], inplace=True)
        hapiness_feelings_frequency_df.drop(hapiness_feelings_frequency_df.index[~hapiness_feelings_frequency_df['geo'].isin(featured_countries_code)], inplace=True)

        hapiness_feelings_frequency_df.drop(columns=["isced11","sex","age","TIME_PERIOD"], inplace=True)
        hapiness_feelings_frequency_df["frequenc"].replace({"ALW": "Toujours", "MOST": "La plupart du temps", "SMT": "Parfois", "RAR": "Rarement", "NVR": "Jamais"}, inplace=True)
        hapiness_feelings_frequency_df.rename(columns={"frequenc":"Fréquence", "OBS_VALUE":"Fréquence du sentiment de bonheur (% de réponse)"}, inplace=True)
        hapiness_feelings_frequency_df.to_csv(hapiness_feelings_frequency_clean)
    
    else:
        hapiness_feelings_frequency_df = pd.read_csv(hapiness_feelings_frequency_clean)
    
    return hapiness_feelings_frequency_df


def get_depressive_symptoms_dataframe() -> pd.DataFrame:
    
    if (not os.path.exists(depressive_symptoms_clean)):
        depressive_symptoms_df = pd.read_csv(depressive_symptoms, sep=',')
        depressive_symptoms_df.drop(columns=["DATAFLOW","LAST UPDATE","freq","unit","OBS_FLAG"], inplace=True)

        depressive_symptoms_df.drop(depressive_symptoms_df.index[depressive_symptoms_df['isced11'] != "TOTAL"], inplace=True)
        depressive_symptoms_df.drop(depressive_symptoms_df.index[depressive_symptoms_df['sex'] != "T"], inplace=True)
        depressive_symptoms_df.drop(depressive_symptoms_df.index[depressive_symptoms_df['age'] != "TOTAL"], inplace=True)
        depressive_symptoms_df.drop(depressive_symptoms_df.index[depressive_symptoms_df['hlth_pb'] != "DPR"], inplace=True)
        depressive_symptoms_df.drop(depressive_symptoms_df.index[depressive_symptoms_df['TIME_PERIOD'] != 2019], inplace=True)
        depressive_symptoms_df.drop(depressive_symptoms_df.index[~depressive_symptoms_df['geo'].isin(featured_countries_code)], inplace=True)

        depressive_symptoms_df.set_index("geo", inplace=True)
        depressive_symptoms_df.drop(columns=["isced11","sex","age","TIME_PERIOD","hlth_pb"], inplace=True)
        depressive_symptoms_df.rename(columns={"OBS_VALUE":"Part de symptomes dépressifs (%)"}, inplace=True)
        depressive_symptoms_df.to_csv(depressive_symptoms_clean)
        
    else:
        depressive_symptoms_df = pd.read_csv(depressive_symptoms_clean)
    
    return depressive_symptoms_df


def get_life_satistaction_dataframe() -> pd.DataFrame:
    
    if (not os.path.exists(life_satistaction_clean)):
        life_satistaction_df = pd.read_csv(life_satistaction, sep=',')
        life_satistaction_df.drop(columns=["DATAFLOW","LAST UPDATE","freq","unit","OBS_FLAG"], inplace=True)

        life_satistaction_df.drop(life_satistaction_df.index[life_satistaction_df['isced11'] != "TOTAL"], inplace=True)
        life_satistaction_df.drop(life_satistaction_df.index[life_satistaction_df['sex'] != "T"], inplace=True)
        life_satistaction_df.drop(life_satistaction_df.index[life_satistaction_df['age'] != "Y_GE16"], inplace=True)
        life_satistaction_df.drop(life_satistaction_df.index[life_satistaction_df['indic_wb'] != "LIFESAT"], inplace=True)
        life_satistaction_df.drop(life_satistaction_df.index[life_satistaction_df['TIME_PERIOD'] != 2018], inplace=True)
        life_satistaction_df.drop(life_satistaction_df.index[~life_satistaction_df['geo'].isin(featured_countries_code)], inplace=True)

        life_satistaction_df.set_index("geo", inplace=True)
        life_satistaction_df.drop(columns=["isced11","sex","age","TIME_PERIOD","indic_wb"], inplace=True)
        life_satistaction_df.rename(columns={"OBS_VALUE":"Note de satisfaction dans la vie (/10)"}, inplace=True)
        life_satistaction_df.to_csv(life_satistaction_clean)
        
    else:
        life_satistaction_df = pd.read_csv(life_satistaction_clean)
    
    return life_satistaction_df


def get_life_expectancy_dataframe() -> pd.DataFrame:
    
    if (not os.path.exists(life_expectancy_clean)):
        life_expectancy_df = pd.read_csv(life_expectancy, sep=',')
        life_expectancy_df.drop(columns=["DATAFLOW","LAST UPDATE","freq","unit","OBS_FLAG"], inplace=True)

        life_expectancy_df.drop(life_expectancy_df.index[life_expectancy_df['sex'] != "T"], inplace=True)
        life_expectancy_df.drop(life_expectancy_df.index[life_expectancy_df['age'] != "Y_LT1"], inplace=True)
        life_expectancy_df.drop(life_expectancy_df.index[life_expectancy_df['TIME_PERIOD'] != 2018], inplace=True)
        life_expectancy_df.drop(life_expectancy_df.index[~life_expectancy_df['geo'].isin(featured_countries_code)], inplace=True)

        life_expectancy_df.set_index("geo", inplace=True)
        life_expectancy_df.drop(columns=["sex","age","TIME_PERIOD"], inplace=True)
        life_expectancy_df.rename(columns={"OBS_VALUE":"Espérance de vie"}, inplace=True)
        life_expectancy_df.to_csv(life_expectancy_clean)
        
    else:
        life_expectancy_df = pd.read_csv(life_expectancy_clean)
    
    return life_expectancy_df


def get_complete_dataframes():
    avg_worktime_df = get_avg_worktime_dataframe()
    hapiness_feelings_frequency_df = get_hapiness_feelings_dataframe()
    depressive_symptoms_df = get_depressive_symptoms_dataframe()
    life_satistaction_df = get_life_satistaction_dataframe()
    life_expectancy_df = get_life_expectancy_dataframe()
    return [pd.concat([avg_worktime_df.set_index("geo"), depressive_symptoms_df.set_index("geo"), life_satistaction_df.set_index("geo"), life_expectancy_df.set_index("geo")], axis=1), pd.merge(avg_worktime_df, hapiness_feelings_frequency_df, on="geo")]
