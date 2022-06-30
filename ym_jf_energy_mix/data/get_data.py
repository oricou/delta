# must be run from file root (python3 get_data.py)

# if it doesn't work just download the file from the website at
# https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption
# rename it to World_Energy_Consumption.csv (note the underscores)
# place it in data/ and ym_jf_energy_mix/data/

import requests
import shutil

URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

a = requests.get(URL)

open('World_Energy_Consumption.csv', 'wb').write(a.content)
shutil.copyfile("./World_Energy_Consumption.csv", "../../data/World_Energy_Consumption.csv")