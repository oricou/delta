import pandas as pd

def color_party(left, mid, right):
    values = [left, mid, right]
    parties = ['Gauche', 'Centre', 'Droite']
    return parties[values.index(max(values))]

def extract_data():
    country_name_fr = [
        'Autriche', 'Belgique', 'Bulgarie', 'Croatie', 'Chypre', 'République tchèque', 'Danemark', 'Estonie',
        'Finlande', 'France', 'Allemagne', 'Grèce', 'Hongrie', 'Irlande', 'Italie', 'Lettonie', 'Lituanie',
        'Luxembourg', 'Malte', 'Pays-Bas', 'Pologne', 'Portugal', 'Roumanie', 'Slovaquie', 'Slovénie', 'Espagne',
        'Suède', 'Royaume-Uni'
    ]
    columns = ['eu', 'year', 'country', 'iso', 'gov_right1', 'gov_cent1', 'gov_left1', 'gov_right3', 'gov_cent3', 'gov_left3']
    
    df1 = pd.read_excel('./ARPA_inequality_per_political_party/data/politique_mondiale.xlsx', usecols=columns, skipfooter=1, dtype={'year': int}).query('(eu == 1) & (year >= 2000)')
    df1 = df1.replace(df1['country'].unique().tolist(), country_name_fr)
    df1['Orientation politique du gouvernement'] = df1.apply(lambda x: color_party(x['gov_left1'], x['gov_cent1'], x['gov_right1']), axis=1)
    df1["Orientation politique du parlement"] = df1.apply(lambda x: color_party(x['gov_left3'], x['gov_cent3'], x['gov_right3']), axis=1)

    df2 = pd.read_excel('./ARPA_inequality_per_political_party/data/inegalite_europe.xlsx', header=None, names=['country', 'def', 'pall', 'year', 'gini'], usecols=['country', 'year', 'gini'])
    df2['gini_display'] = df2['gini'] ** 6 # A displayable gini coefficient

    pd.merge(df1, df2).to_pickle("./ARPA_inequality_per_political_party/data/inequalities.pkl")

if __name__ == '__main__':
    # Our base datas cannot be downloaded from code, so we added them manually as they were not to heavy.
    # It implies that "data/inegalite_europe.xlsx" and "data/politique_mondiale.xlsx" should be present for the code to work.
    extract_data()
