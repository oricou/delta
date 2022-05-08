import pandas as pd
import numpy as np
import glob 

class GunDeathsData():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.gundeaths = self.init_gundeaths()
        self.df_agedeaths = self.init_agedeaths()
        self.df_cod = self.init_cod()
        
    def init_gundeaths(self):
        dfs = {}
        xls = pd.ExcelFile('OEJD_decesParArmeAFeu/data/gun cod.xlsx')
        cod = pd.read_excel(xls, 'Deaths', skiprows=[0])
        vals2 = cod.iloc[[0]].values.tolist()
        vals1 = cod.columns.tolist()
        vals1[5:] = vals2[0][5:]
        tmp = []
        for val in vals1:
            tmp.append(val.replace("year","an"))
        cod.columns = tmp

        cod = cod.drop(cod.index[0])


        for year in range(self.begin, self.end + 1, 1):
            dfs[year] = cod[cod['Year'] == year]
        return dfs

    def init_cod(self):
        cod = self.gundeaths[2020].copy()
        cod = cod[cod['Sex'] == 'Both sexes']
        cod = cod.head(5)
        other = cod.head(1)['Total'].sum() - cod.drop(cod.index[0])['Total'].sum()
        cod = cod.append({'Intent':'Autre', 'Total':other}, ignore_index=True)
        return cod.drop(cod.index[0])

    def init_agedeaths(self):
        dfs = {}
        for year in self.gundeaths:
            age_deaths = self.gundeaths[year].copy()
            to_rem = ['Year', 'Unnamed: 3', 'Total', 'Not Stated']
            age_deaths.drop(to_rem, inplace=True, axis=1)
            melt_df = pd.melt(age_deaths, id_vars = ['Intent', 'Sex'], value_vars = age_deaths.columns.tolist()[2:13])
            dfs[year] = melt_df
        return dfs

class GunOwnersData():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.df_wages = self.init_wages()
        self.df_gowners = self.init_gowners()
        
    def init_wages(self):
        csv = pd.read_csv("OEJD_decesParArmeAFeu/data/wages_2015_q1.csv", dtype={"FIPS": str, "Average Weekly Wages": int}, skiprows = [9, 52, 53])
        csv['text'] = csv['Area Name'] + '<br>' + \
            'Average Weekly Wages ' + csv['Average Weekly Wages'].astype('str')
        csv = csv.set_index(["Area Name"])
        return csv

    def init_gowners(self):
        xls = pd.ExcelFile('OEJD_decesParArmeAFeu/data/firearm.xlsx')
        df = pd.read_excel(xls, 'State-Level Data & Factor Score')
        df['HFR'] = df['HFR']*100
        return df

class FirearmDeathData():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.df_wages = self.init_wages()
        self.df_crimes = self.init_crimes()
        self.df_pops = self.init_population()
        self.df_indexes = self.init_indexes()
        
        
    def init_wages(self):
        df_all_wages = pd.concat([pd.read_csv(file, skiprows=[9,52,53], dtype={"FIPS": str, "Average Weekly Wages": int})[["Area Name", "Period", "One-Year Employment Gain/Loss (Percent)", "Average Weekly Wages", "On-Year Weekly Wages Gain/Loss (Percent)", "USPS"]] 
                          for file in glob.glob('OEJD_decesParArmeAFeu/data/wages/bls*')])
        df_usps = df_all_wages.set_index("Area Name")["USPS"].drop_duplicates()
        df_all_wages.Period = df_all_wages.Period.str.split("Q").str[0]
        df_all_wages = df_all_wages.set_index(["Area Name", "Period"])
        df_all_wages = df_all_wages.groupby(["Area Name", "Period"]).mean()
        df_all_wages = df_all_wages.reset_index("Period")
        
        dfs = {}
        for year in range(self.begin, self.end + 1, 1):
            csv = pd.concat([df_all_wages[df_all_wages.Period == str(year)], df_usps], axis=1)
            csv['text'] = "Etat: " + csv.index + '<br>' + \
                'Salaire moyen/semaine: ' + round(csv['Average Weekly Wages'], 1).astype('str') + " $"
            dfs[year] = csv
        return dfs
    
    def init_crimes(self):
        df_crimes = pd.read_csv("OEJD_decesParArmeAFeu/data/firearm_deaths_usafacts.csv", skiprows=range(1, 27), skipfooter=5, engine='python')
        df_crimes['Years'] = df_crimes['Years'].str.replace("(People)", "", regex=False).str.strip()
        df_crimes = df_crimes.rename(columns={"Years":"state"}).set_index("state")
        return df_crimes
    
    def init_population(self):
        dfs = {}
        columns = ["POPESTIMATE2010", "POPESTIMATE2011", "POPESTIMATE2012", "POPESTIMATE2013", "POPESTIMATE2014", "POPESTIMATE2015", "POPESTIMATE2016", "POPESTIMATE2017","POPESTIMATE2018", "POPESTIMATE2019", "POPESTIMATE2020"]
        df_pop_2010 = pd.read_csv('OEJD_decesParArmeAFeu/data/nst-est2020-popchg2010-2020.csv').set_index("NAME")[columns]
        df_pop_2010.columns = ['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
        df_pop_2010 = df_pop_2010.drop(["United States", "Northeast Region", "Midwest Region", "South Region", "West Region"])
        
        df_pop_2000 = pd.read_csv('OEJD_decesParArmeAFeu/data/st-est00int-01.csv', skiprows=3, skipfooter=8, engine='python')
        df_pop_2000 = df_pop_2000.drop([0,1,2,3,4]).drop(["Unnamed: 1", "Unnamed: 12", "Unnamed: 13"], axis=1).rename({"Unnamed: 0": "Area Name"}, axis=1)
        df_pop_2000["Area Name"] = df_pop_2000["Area Name"].str.replace(".", "", regex=False)
        df_pop_2000 = df_pop_2000.set_index("Area Name")
        df_pop_2000 = df_pop_2000[df_pop_2000.index.notnull()]
        df_pop_2000 = df_pop_2000[["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]].applymap(lambda x: x.replace(",", ""))
        df_pop_2000 = df_pop_2000.astype('int64')
        
        df_pop = pd.concat([df_pop_2000, df_pop_2010], axis=1)
        for year in range(self.begin, self.end + 1, 1):
            dfs[year] = df_pop[str(year)].rename("Population")
        return dfs
    
    def init_indexes(self):
        dfs = {}
        for year in range(self.begin, self.end + 1, 1):
            df_crime_number = self.df_crimes[str(year)].rename("CrimeNumber")
            index = pd.concat([self.df_wages[year]["USPS"], self.df_pops[year]], axis = 1).join(df_crime_number)
            index["CrimeNumber"].fillna(0,inplace=True)
            index = index.dropna()
            index["index"] = index["CrimeNumber"] / (index["Population"] / 100000)
            index['text'] = "Etat: " + index.index + '<br>' + \
                'MAF: ' + round(index['index'], 1).astype('str') + '<br>' + \
                'Nombre de crimes: ' + index['CrimeNumber'].astype('str') + '<br>' + \
                'Population: ' + index['Population'].astype('str')
            dfs[year] = index
        return dfs