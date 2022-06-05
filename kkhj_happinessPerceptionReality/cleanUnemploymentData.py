import pandas as pd


# Extract data, rejet useless columns and make it ready for future instructions
def get_unemployment():
    tab = pd.read_csv("kkhj_happinessPerceptionReality/data/unemployment-rate.csv").rename(columns={'Entity': 'Country', 'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'Unemployment rate %'}).set_index('Country')
    mask = (tab['Year'] >= 2012) & (tab['Year'] <= 2021)
    df = tab[mask].reset_index()
    del df['Code']
    df = df.dropna()
    return df


# Params: x - unemployment rate extracted from the dataset;
#         rate_inf - the min rate in the form;
#         rate_sup - the max rate in the form;
#         index_sup - the highest index
# Based on the form below, calculate index (out of 10)
# Unemployment rate % 0    2.5    5    7.5    10    12.5    15    17.5    20    25    100
# Happiness           10    9     8     7      6      5      4      3      2     1     0
def get_index(x, rate_inf, rate_sup, index_sup):
    return index_sup - (x - rate_inf) / (rate_sup - rate_inf)


# Params: x - unemployment rate extracted from the dataset
# Apply get_index on x dependant on its neighbors
# rule: more unemployment => less happiness
def transform_rate_to_index(x):
    # rate_index = {unemployment rate : correspondent index}
    rate_index = {0: 10,
                  2.5: 9,
                  5: 8,
                  7.5: 7,
                  10: 6,
                  12.5: 5,
                  15: 4,
                  17.5: 3,
                  20: 2,
                  25: 1,
                  100: 0}

    # if x has an already-known index
    if x in rate_index:
        return rate_index[x]
    else:
        rate_index = list(rate_index.items())
        rate_inf = 0
        rate_sup = 2.5
        index_sup = 10
        for i in range(1, len(rate_index)):
            if rate_index[i][0] < x:
                rate_inf = rate_index[i][0]
                rate_sup = rate_index[i+1][0]
                index_sup = rate_index[i][1]
            else:
                break
    res = get_index(x, rate_inf, rate_sup, index_sup)
    return res


# main function, convert unemployment rate to index (out of 10)
def unemployment_out_of_ten():
    df = get_unemployment()
    df['Unemployment rate %'] = df['Unemployment rate %'].apply(transform_rate_to_index)
    df['Year'] = df['Year'].astype(int)
    return df.rename(columns={'Unemployment rate %': 'Unemployment Index'})
