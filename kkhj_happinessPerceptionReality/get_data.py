from kkhj_happinessPerceptionReality.missingValues import get_all_datasets
from kkhj_happinessPerceptionReality.cleanEducationLevelData import *
import pycountry_convert as pc


# Get all data by merging all datasets into one
def get_data():
    # Extract datasets by completing missing values
    data = get_all_datasets()
    datasets = {'safety': data[1], 'unemployment': data[4],
                'socialContribution': data[3], 'gdpPerCapita': data[2],
                'realHappiness': data[0]}

    # TODO find better dataset for educationLevel/literacy and append line below to dict datasets
    # 'educationLevel': education_out_of_10()

    # Merge all datasets
    df = datasets['safety']
    for count, key in enumerate(datasets):
        if count == 0:
            continue
        df = pd.merge(datasets[key], df, on=["Country", "Year"])

    df.rename(columns={'Value': 'General Happiness Index'}, inplace=True)
    return add_continents(df.set_index('Year'))


# Associate continents to each country
def add_continents(datasets):
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe'
    }

    datasets['Country_code'] = datasets['Country'].apply(
        lambda x: pc.country_name_to_country_alpha2(x, cn_name_format="default"))
    datasets['Continent'] = datasets['Country_code'].apply(
        lambda x: continents[pc.country_alpha2_to_continent_code(x)])
    datasets.drop("Country_code", inplace=True, axis=1)
    return datasets
