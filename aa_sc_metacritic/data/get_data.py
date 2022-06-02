import pandas as pd

def get_data():
    data = pd.read_csv("vgcritics.csv")
    data = data.loc[(data.critics > 5) & (data.genre != "No info")]
    data = data.loc[data['user score'] != 'tbd']
    data['r-date'] = pd.to_datetime(data['r-date'], format='%B %d, %Y')
    
    data_sales = pd.read_csv("vgsales.csv")
    
    # Same name easier merged between both data base  
    name_corres = [("Xone", "XboxOne"), ("X360", "Xbox360"), ("XB", "Xbox"), ("PS4", "PlayStation4"), ("PS3", "PlayStation3"), ("PS2", "PlayStation2"), ("PS", "PlayStation"), ("GC", "GameCube"), ("GBA", "GameBoyAdvance"), ("N64", "Nintendo64"), ("PSV", "Playstation")]
    data_sales.rename(columns = {"Name": "name", "Platform": "platform"}, inplace = True)
    for pair in name_corres : 
        data_sales.loc[data_sales['platform'] == pair[0], 'platform'] = pair[1]

    data.to_pickle("vgcritics.pkl")
    data_sales.to_pickle("vgsales.pkl")

get_data()