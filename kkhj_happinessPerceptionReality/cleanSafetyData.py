import pandas as pd


# Param: year
# Return: dataframe with necessary columns
def extract_safety(year):
    file = "kkhj_happinessPerceptionReality/data/criminality" + str(year) + ".xlsx"
    tab = pd.read_excel(file)
    df = pd.DataFrame({'Country': tab["Country"], f"{year}": tab["Safety Index"]})
    return df


# Merge all dataframes related to safety (criminality.xlsx)
def combine_dfs():
    tab = extract_safety(2012)
    for x in range(13, 22):
        file = str(20) + str(x)
        tab = tab.join(extract_safety(file).set_index(['Country']), on='Country')
    return tab.melt(['Country'], var_name='Year', value_name='Safety Index')


# main function, set Safety Index (out of 10)
def safety_out_of_10():
    tab = combine_dfs()
    tab['Year'] = tab['Year'].astype(str).astype(int)
    tab['Safety Index'] = tab['Safety Index'].div(10)
    return tab
