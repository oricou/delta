import requests
import pandas as pd
import time
import json

class RiotAccess:

    RIOT_API_KEY = ""
    EU_RIOT_MATCH_ENDPOINT = "https://europe.api.riotgames.com/lol/match/v5/matches/"
    ASIA_RIOT_MATCH_ENDPOINT="https://asia.api.riotgames.com/lol/match/v5/matches/"
    NA_RIOT_MATCH_ENDPOINT="https://americas.api.riotgames.com/lol/match/v5/matches/"
    MATCH_ID_PATH = "MatchesID/games.csv"

    END_POINT_MATCH = {"BR1":NA_RIOT_MATCH_ENDPOINT,
                       "LA1":NA_RIOT_MATCH_ENDPOINT,
                       "EUN1":EU_RIOT_MATCH_ENDPOINT,
                       "EUW1":EU_RIOT_MATCH_ENDPOINT,
                       "LA2":NA_RIOT_MATCH_ENDPOINT,
                       "NA1":NA_RIOT_MATCH_ENDPOINT,
                       "TR1":ASIA_RIOT_MATCH_ENDPOINT,
                       "KR":ASIA_RIOT_MATCH_ENDPOINT,
                       "JP1":ASIA_RIOT_MATCH_ENDPOINT,
                       "OC1":NA_RIOT_MATCH_ENDPOINT,
                       "RU":EU_RIOT_MATCH_ENDPOINT}



    REQUEST_SLEEP_TIME = 1.2

    def __init__(self, API_KEY=None):
        if API_KEY is not None:
            self.RIOT_API_KEY = API_KEY
        self.headers = {"X-Riot-Token": self.RIOT_API_KEY}

    def update_api_key(self, newkey):
        self.RIOT_API_KEY = newkey
        self.headers = {"X-Riot-Token": self.RIOT_API_KEY}

    def get_match_id_info(self, matchID):
        """
        :param matchID: ID of a league of legends match
        :return: a json of what everything that happened during that game
        """
        endpoint = self.END_POINT_MATCH[matchID.split("_")[0]]
        try:
            req = requests.get(endpoint+matchID, headers=self.headers)
            return req.json()
        except Exception as e:
            print("[ERROR] get_match_id_info : ", str(e))
            return None

    def save_data_from_source(self, start_id=0,max_id=None,outpath="out_data.json", filter_func=None,max_it=-1):
        """
        :param start_id: start reading data from this line number
        :param max_id: stop reading data from this line number
        :param outpath: save location of all matches into a big json file
        :return:
        """
        try:
            id_file = pd.read_csv(self.MATCH_ID_PATH)
        except:
            print("Couldn't access to the MATCH_ID file. Please check MATCH_ID_PATH is correct /!\\")
            return

        jsonout = {}
        it = 0

        for k,ID in enumerate(id_file['MATCH_ID']):
            if k < start_id or (filter_func is not None and not filter_func(ID)):
                continue
            elif (max_id is not None and k > max_id) or it > max_it:
                break
            data = self.get_match_id_info(ID)
            if data is not None:
                jsonout[ID] = data

            it += 1
            # WAITING TIME BETWEEN REQUESTS
            time.sleep(self.REQUEST_SLEEP_TIME)

        with open(outpath, 'w') as f:
            json.dump(jsonout, f)





if __name__ == "__main__": #For debug purposes only
    riot_app = RiotAccess()
    riot_app.save_data_from_source(filter_func=lambda id: "EUW1" in id, outpath="MatchesID/EUW1_12000_BIG_GAME_DATA.json", max_it=12000)
    #print(riot_app.get_match_id_info("RU_343155688"))
