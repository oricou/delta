import pandas as pd
import re
import pathlib
import requests

def read_excel_sheets(xls_path):
    """Read all sheets of an Excel workbook and return a single DataFrame"""
    print(f'Loading {xls_path} into pandas')
    xl = pd.ExcelFile(xls_path)
    df = list()
    for idx, name in enumerate(xl.sheet_names):
        # print(f'Reading sheet #{idx}: {name}')

        sheet = xl.parse(name,
                         index_col=[0],
                         skiprows=[96, 97, 99, 100],
                         usecols=lambda x : x != 'Index').T
        sheet.index = sheet.index.map(lambda x: pd.to_datetime(x + '_1', format="_%Y_%m_%d"))
        sheet['Département'] = name

        df.append(sheet)
    return pd.concat(df)

def main():
    data_dir = pathlib.Path('data')
    if not data_dir.is_dir():
        data_dir.mkdir()

    url = "https://www.data.gouv.fr/api/1/datasets/chiffres-departementaux-mensuels-relatifs-aux-crimes-et-delits-enregistres-par-les-services-de-police-et-de-gendarmerie-depuis-janvier-1996/"
    crimes_resources = requests.get(url).json()

    prog = re.compile(".*\.xlsx")
    filenames = {
                    d['title']:d['url']
                    for d in crimes_resources['resources']
                    if prog.match(d['title'])
                }


    dfs = {}
    for k, v in filenames.items():
        name_db = f'{v[-7:-5]}_db'
        if pathlib.Path(f'data/{name_db}.pkl').is_file():
            dfs[name_db] = pd.read_pickle(f'data/{name_db}.pkl')
        else:
            if not pathlib.Path('data/' + k).is_file():
                with open('data/' + k, 'wb') as file:
                    file.write(requests.get(v).content)
            dfs[name_db] = read_excel_sheets('data/' + k)
            dfs[name_db].to_pickle(f'data/{name_db}.pkl')

if __name__ == "__main__":
    main()
