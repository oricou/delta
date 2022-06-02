import numpy as np
import pandas as pd
import json
import requests

try:
    from DataGathering import RiotAPIScrapper as RAS
except ImportError:
    from __LeagueOfLegendsChampionsStats.data.DataGathering import RiotAPIScrapper as RAS

def data_selector():
    print("""We are using the Riot API to scrap data from their API directly since API-KEY must not be shared and only last one day.
    You will have get one yourself to do the full data gathering process. If you wish to regenerate data with a key type 1) """)
    answer = input("(1/2)>>> ")
    if answer[0] == 1:
        return True
    elif answer[1] == 2:
        return False
    else:
        return None

def surrender_gold_diff():
    euwgames = pd.read_json("EUW1_12000_BIG_GAME_DATA.json")

    def get_surrender_data():
        surr_dt = []
        for a, b in euwgames.items():
            if type(b.info) != type({}):
                continue
            try:
                if not b.info["participants"][0]["gameEndedInSurrender"]:
                    continue
                team = [0, 0]
                bwin = []
                for i in range(10):
                    if i < 5:
                        team[0] += b.info["participants"][i]["goldEarned"]
                    else:
                        team[1] += b.info["participants"][i]["goldEarned"]

                surr_dt.append(abs(team[0] - team[1]))

            except Exception as e:
                print(e)  # Handle special gamemode like custom game with a custom amount of players

        return surr_dt

    raw_data = get_surrender_data()
    pd.DataFrame(raw_data, columns=["GoldDiff"]).to_csv("surrender_gold_diff.csv")

def reduced_games():
    euwgames = pd.read_json("EUW1_12000_BIG_GAME_DATA.json")

    def get_pers_info(data):
        name = data["championName"].lower()
        win = data["win"]
        position = data["teamPosition"]
        gtime = data["timePlayed"]
        vision = data["visionScore"]
        gold = data["goldEarned"]
        assists = data["assists"]
        kills = data["kills"]
        death = data["deaths"]
        return {"name": name,
                "win": win,
                "position": position,
                "gametime": gtime,
                "vision": vision,
                "gold": gold,
                "assists": assists,
                "kills": kills,
                "death": death}

    def get_champs_pair():
        champ_role_comp = {}
        for a, b in euwgames.items():
            if type(b.info) != type({}):
                continue
            try:
                for i in range(5):
                    curr_data = get_pers_info(b.info["participants"][i])
                    adv_data = get_pers_info(b.info["participants"][i + 5])

                    # Register current champion's data for the adversarial champion
                    if champ_role_comp.get(adv_data["name"], None) is None:
                        champ_role_comp[adv_data["name"]] = [curr_data]
                    else:
                        champ_role_comp[adv_data["name"]].append(curr_data)
                    # same thing inversed
                    if champ_role_comp.get(curr_data["name"], None) is None:
                        champ_role_comp[curr_data["name"]] = [adv_data]
                    else:
                        champ_role_comp[curr_data["name"]].append(adv_data)
            except Exception as e:
                print(e)
        return champ_role_comp

    pair_data = get_champs_pair()

    with open("reduced_12000_game_data.json", "w") as outfile:
        json.dump(pair_data, outfile)


# Automate process
def get_dataset_winrate(csv_path, *args):
    lgame = pd.read_csv(csv_path, *args)
    clean_game = lgame.drop("blue_team_win", axis=1)
    # columns = np.unique([s.split("_")[0] for s in clean_game.columns.values])

    # Get champs winrates
    blue_columns = [e for e in clean_game.columns if "_blue" in e]
    red_columns = [e for e in clean_game.columns if "_red" in e]
    champ_winrate = []
    for blue_champ, red_champ in zip(blue_columns, red_columns):
        b_localgames = lgame[lgame[blue_champ] == 1]
        b_total = b_localgames.shape[0]
        r_localgames = lgame[lgame[red_champ] == 1]
        r_total = r_localgames.shape[0]
        champ_winrate.append((b_localgames["blue_team_win"].sum() + (r_total - r_localgames["blue_team_win"].sum())) / (
                    b_total + r_total))
    return champ_winrate

def read_all_data_winrate():
    games = pd.read_csv("./Champions_games/Challenger/lol_Challenger_data.csv")
    dc = games.describe()
    pick_rate = dc.iloc[1].drop("blue_team_win")
    new_columns = [s.split("_")[0] for s in pick_rate.index.values]
    clean_pick_rate = pick_rate.groupby(new_columns).sum()

    # Get champs winrates
    blue_columns = [e for e in games.columns if "_blue" in e]
    red_columns = [e for e in games.columns if "_red" in e]
    champ_winrate = []
    for blue_champ, red_champ in zip(blue_columns, red_columns):
        b_localgames = games[games[blue_champ] == 1]
        b_total = b_localgames.shape[0]
        r_localgames = games[games[red_champ] == 1]
        r_total = r_localgames.shape[0]
        champ_winrate.append((b_localgames["blue_team_win"].sum() + (r_total - r_localgames["blue_team_win"].sum())) / (
                    b_total + r_total))

    champ_win_rate = pd.DataFrame(champ_winrate, index=clean_pick_rate.index, columns=["Challenger_WinRate"])

    champ_win_rate["Grandmaster_WinRate"] = get_dataset_winrate("./Champions_games/GrandMaster/lol_GrandMaster_data.csv")
    champ_win_rate["Master_WinRate"] = get_dataset_winrate("./Champions_games/Master/lol_Master_data.csv")
    champ_win_rate.to_csv("champ_win_rate.csv")

def main_logic():
    user_entry = data_selector()
    if user_entry is None:
        print("Please try again")
        return

    if user_entry:
        print("|!| Data gathering will take 4h with a standard access key")
        KEY = input("API KEY : ")
        riot_app = RAS.RiotAccess(KEY)
        riot_app.save_data_from_source(filter_func=lambda id: "EUW1" in id,outpath="EUW1_12000_BIG_GAME_DATA.json", max_it=12000)
   # else:
   #     res = requests.get()
   #     open("EUW1_12000_BIG_GAME_DATA.json", "wb").write(res.content)
    surrender_gold_diff()
    reduced_games()
    read_all_data_winrate()

if __name__ == "__main__":
    print("Please run get_data.py from his local folder (path are relative) /!\\")
    main_logic()

"""
source : https://www.kaggle.com/datasets/jasperan/league-of-legends-1000000-master-matches

"""