import os
import pandas as pd


def getDataFramFromPos(path, i):
    filename = 'pop' + str(i) + '.csv'
    df = pd.read_csv(os.path.join(path, filename), usecols=['Regions', 'Total'], encoding='UTF-8')
    return df.rename(columns={'Total': str(i)})


def getPopFromData(path):
    result = getDataFramFromPos(path, 2000)
    for i in range(2001, 2023):
        df = getDataFramFromPos(path, i)
        result = result.join(df[str(i)])
    return result


def extractTaxesDataFrameFromFiles(fileName):
    df = pd.read_csv(fileName, delimiter=';', encoding='UTF-8')
    tmp = pd.DataFrame().assign(Taxes=df['Impots'])
    return tmp


def getTaxesDataFrames(dirName):
    fileName = os.path.join(dirName, 'impots2000.csv')
    year = 2000
    df = pd.read_csv(fileName, delimiter=';', usecols=['Regions', 'Impots'], encoding='UTF-8')
    df = df.rename(columns={'Impots': year})
    for year in range(2001, 2012):
        fileName = os.path.join(dirName, 'impots' + str(year) + '.csv')
        df = df.assign(year=extractTaxesDataFrameFromFiles(fileName))
        df = df.rename(columns={'year': year})
    return df


def extractSalaryDataFrameFromFiles(fileName):
    df = pd.read_csv(fileName, delimiter=';', encoding='UTF-8')
    tmp = pd.DataFrame().assign(Taxes=df['Salaire'])
    return tmp


def getSalarysFromDataFrames(dirName):
    fileName = os.path.join(dirName, 'impots2000.csv')
    year = 2000
    df = pd.read_csv(fileName, delimiter=';', usecols=['Regions', 'Salaire'], encoding='UTF-8')
    df = df.rename(columns={'Impots': year})
    for year in range(2001, 2012):
        fileName = os.path.join(dirName, 'impots' + str(year) + '.csv')
        df = df.assign(year=extractSalaryDataFrameFromFiles(fileName))
        df = df.rename(columns={'year': year})
    return df


def treatment_data_histo():
    df_hist = pd.read_csv('donnes_brut/populations/population_year_regions.csv', sep=';', encoding='iso-8859-1')
    df_hist["year"] = df_hist["year"].astype(int)
    df_hist["total"] = df_hist["total"].astype(int)
    df_hist["men"] = df_hist["men"].astype(int)
    df_hist["women"] = df_hist["women"].astype(int)
    return df_hist


if __name__ == '__main__':
    treatment_data_histo().to_csv('data/data_histo_population.csv')
    print(getPopFromData('donnes_brut/populations/'))
    print(getTaxesDataFrames('donnes_brut/taxes/'))
    print(getSalarysFromDataFrames('donnes_brut/taxes/'))
