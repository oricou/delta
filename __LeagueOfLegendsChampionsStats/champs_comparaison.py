import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
import json

class ChampComparaison:

    ROW_STYLE = {'display': 'inline-block', 'vertical-align': 'top'}
    CHAMP_COLUMNS = ["winrate","visionPerMin","goldPerMin","kills","assists","deaths"]

    def __get_dataframe(self):
        with open('__LeagueOfLegendsChampionsStats/data/reduced_12000_game_data.json') as json_file:
            self.source_df = json.load(json_file)

    def extract_matchup_data(self, champ1, champ2):
        ch1_data = list(filter(lambda game: game["name"] == champ1, self.source_df[champ2]))
        ch1_size = len(ch1_data)
        ch2_data = list(filter(lambda game: game["name"] == champ2, self.source_df[champ1]))
        ch2_size = len(ch2_data)

        if ch1_size == 0 or ch2_size == 0:
            return None, None

        ch1_res = {"winrate": 0, "visionPerMin": 0, "goldPerMin": 0, "kills": 0, "assists": 0, "deaths": 0}
        ch2_res = {"winrate": 0, "visionPerMin": 0, "goldPerMin": 0, "kills": 0, "assists": 0, "deaths": 0}
        # Average our data
        for dico in ch1_data:
            ch1_res["winrate"] += int(dico["win"])
            ch1_res["visionPerMin"] += dico["vision"] / (dico["gametime"] / 60)
            ch1_res["goldPerMin"] += dico["gold"] / (dico["gametime"] / 60)
            ch1_res["kills"] += dico["kills"]
            ch1_res["assists"] += dico["assists"]
            ch1_res["deaths"] += dico["death"]

        for dico in ch2_data:
            ch2_res["winrate"] += int(dico["win"])
            ch2_res["visionPerMin"] += dico["vision"] / (dico["gametime"] / 60)
            ch2_res["goldPerMin"] += dico["gold"] / (dico["gametime"] / 60)
            ch2_res["kills"] += dico["kills"]
            ch2_res["assists"] += dico["assists"]
            ch2_res["deaths"] += dico["death"]

        ch1_res["winrate"] = round(ch1_res["winrate"] / ch1_size, 2)
        ch1_res["visionPerMin"] = round(ch1_res["visionPerMin"] / ch1_size, 2)
        ch1_res["goldPerMin"] = round(ch1_res["goldPerMin"] / ch1_size, 2)
        ch1_res["kills"] = round(ch1_res["kills"] / ch1_size, 2)
        ch1_res["assists"] = round(ch1_res["assists"] / ch1_size, 2)
        ch1_res["deaths"] = round(ch1_res["deaths"] / ch1_size, 2)

        ch2_res["winrate"] = round(ch2_res["winrate"] / ch2_size, 2)
        ch2_res["visionPerMin"] = round(ch2_res["visionPerMin"] / ch2_size, 2)
        ch2_res["goldPerMin"] = round(ch2_res["goldPerMin"] / ch2_size, 2)
        ch2_res["kills"] = round(ch2_res["kills"] / ch2_size, 2)
        ch2_res["assists"] = round(ch2_res["assists"] / ch2_size, 2)
        ch2_res["deaths"] = round(ch2_res["deaths"] / ch2_size, 2)

        return pd.DataFrame.from_dict(ch1_res,orient="index"), pd.DataFrame.from_dict(ch2_res,orient="index")


    def __init__(self, application = None):

        self.__get_dataframe()

        self.champ1 = "rakan"
        self.champ2 = "nami"

        c1,c2 = self.extract_matchup_data("rakan","nami")
        c1_color_table = ["#01FF70" if c1.loc[self.CHAMP_COLUMNS[i]][0] > c2.loc[self.CHAMP_COLUMNS[i]][0] else
                          "#FF4136" if c1.loc[self.CHAMP_COLUMNS[i]][0] < c2.loc[self.CHAMP_COLUMNS[i]][0] else "#7FDBFF" for i in range(6)]
        c2_color_table = ["#01FF70" if c1_color_table[i] == "#FF4136" else "#FF4136" if c1_color_table[i] != "#7FDBFF" else "#7FDBFF" for i in range(6)]

        arranged_c1 = [{"0":key, "1":item} for key,item in c1.to_dict()[0].items()]
        arranged_c2 = [{"0": key, "1": item} for key, item in c2.to_dict()[0].items()]
        self.main_layout = html.Div(children=[html.Div([html.H2("Champion 1"),
                                                        dcc.Dropdown(list(self.source_df.keys()), self.champ1, id="choose-c1"),
                                                        dash.dash_table.DataTable(arranged_c1, id="table1",
                                                        style_data_conditional=[
                                                            {
                                                                'if': {
                                                                    'column_id': '1',
                                                                    'row_index': i
                                                                },
                                                                'backgroundColor': c1_color_table[i]

                                                            } for i in range(6)
                                                        ])], style=self.ROW_STYLE),
                                     html.Div([html.H2("Champion 2"),
                                               dcc.Dropdown(list(self.source_df.keys()), self.champ2, id="choose-c2"),
                                               dash.dash_table.DataTable(arranged_c2, id="table2",
                                                         style_data_conditional=[
                                                             {
                                                                 'if': {
                                                                     'column_id': '1',
                                                                     'row_index': i
                                                                 },
                                                                 'backgroundColor': c2_color_table[i]

                                                             } for i in range(6)
                                                         ]
                                                         )], style=self.ROW_STYLE)])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(dash.dependencies.Output("table1", "data"),
                          [dash.dependencies.Input("choose-c1", "value"),
                           dash.dependencies.Input("choose-c2", "value")])(self.table_one_update)

        self.app.callback(dash.dependencies.Output("table2", "data"),
                          [dash.dependencies.Input("choose-c1", "value"),
                           dash.dependencies.Input("choose-c2", "value")])(self.table_two_update)

        self.app.callback(dash.dependencies.Output("choose-c2","options"),
                          dash.dependencies.Input("choose-c1","value"))(self.update_champ_pool)

        self.app.callback([dash.dependencies.Output("table1","style_data_conditional"),
                          dash.dependencies.Output("table2","style_data_conditional")],
                          [dash.dependencies.Input("choose-c1", "value"),
                           dash.dependencies.Input("choose-c2", "value")])(self.update_table1_style)

    def table_one_update(self, choosed_champ1, choosed_champ2):

        if choosed_champ1 is None or choosed_champ2 is None:
            return []

        self.champ1 = choosed_champ1
        self.champ2 = choosed_champ2
        c1,c2 = self.extract_matchup_data(self.champ1,self.champ2)

        if c1 is None or c2 is None:
            return []

        c1_color_table = ["#01FF70" if c1.loc[self.CHAMP_COLUMNS[i]][0] > c2.loc[self.CHAMP_COLUMNS[i]][0] else
                          "#FF4136" if c1.loc[self.CHAMP_COLUMNS[i]][0] < c2.loc[self.CHAMP_COLUMNS[i]][0] else "#7FDBFF" for i in range(6)]
        c2_color_table = ["#01FF70" if c1_color_table[i] == "#FF4136" else "#FF4136" if c1_color_table[i] != "#7FDBFF" else "#7FDBFF" for i in range(6)]
        arranged_c1 = [{"0":key, "1":item} for key,item in c1.to_dict()[0].items()]
        return arranged_c1

    def table_two_update(self, choosed_champ1, choosed_champ2):

        if choosed_champ1 is None or choosed_champ2 is None:
            return []

        self.champ1 = choosed_champ1
        self.champ2 = choosed_champ2
        c1,c2 = self.extract_matchup_data(self.champ1,self.champ2)

        if c1 is None or c2 is None:
            return []

        c1_color_table = ["#01FF70" if c1.loc[self.CHAMP_COLUMNS[i]][0] > c2.loc[self.CHAMP_COLUMNS[i]][0] else
                          "#FF4136" if c1.loc[self.CHAMP_COLUMNS[i]][0] < c2.loc[self.CHAMP_COLUMNS[i]][0] else "#7FDBFF" for i in range(6)]
        c2_color_table = ["#01FF70" if c1_color_table[i] == "#FF4136" else "#FF4136" if c1_color_table[i] != "#7FDBFF" else "#7FDBFF" for i in range(6)]
        arranged_c2 = [{"0": key, "1": item} for key, item in c2.to_dict()[0].items()]
        return arranged_c2

    def update_champ_pool(self, choosed_champ1):

        if choosed_champ1 is None:
            choosed_champ1 = "rakan"

        ch1_data = list(map(lambda dico:dico["name"], self.source_df[choosed_champ1]))
        return ch1_data

    def update_table1_style(self, choosed_champ1, choosed_champ2):
        c1, c2 = self.extract_matchup_data(choosed_champ1, choosed_champ2)
        c1_color_table = ["#01FF70" if c1.loc[self.CHAMP_COLUMNS[i]][0] > c2.loc[self.CHAMP_COLUMNS[i]][0] else
                          "#FF4136" if c1.loc[self.CHAMP_COLUMNS[i]][0] < c2.loc[self.CHAMP_COLUMNS[i]][
                              0] else "#7FDBFF" for i in range(6)]
        c2_color_table = [
            "#01FF70" if c1_color_table[i] == "#FF4136" else "#FF4136" if c1_color_table[i] != "#7FDBFF" else "#7FDBFF"
            for i in range(6)]
        return [
                {
                    'if': {
                        'column_id': '1',
                        'row_index': i
                    },
                    'backgroundColor': c1_color_table[i]

                } for i in range(6)
            ],[
                 {
                     'if': {
                         'column_id': '1',
                         'row_index': i
                     },
                     'backgroundColor': c2_color_table[i]

                 } for i in range(6)
             ]







if __name__ == '__main__':
    nrg = ChampComparaison()
    nrg.app.run_server(debug=True, port=8051)
