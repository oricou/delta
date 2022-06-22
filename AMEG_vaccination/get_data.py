import requests

def save_data(url, filename):
    """
    Save data from url to filename
    """
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)


save_data('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', 'data/vaccinations.csv')
save_data('https://raw.githubusercontent.com/Timelessprod/delta/main/AMEG_vaccination/data/gdp.csv', 'data/gdp.csv')
