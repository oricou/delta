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
from __LeagueOfLegendsChampionsStats import champs_comparaison as ccom

class ChampWinRate:

    ROW_STYLE = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': "50px",'width':'500px'}

    def __get_dataframe(self):
        self.source_df = pd.read_csv("__LeagueOfLegendsChampionsStats/data/champ_win_rate.csv")
        self.source_df.rename(columns={self.source_df.columns[0]: "champ_name"}, inplace=True)
        return self.source_df.query('champ_name in '+str(self.selection))

    def __get_surrender_dataframe(self):
        surrdata = pd.read_csv("__LeagueOfLegendsChampionsStats/data/surrender_gold_diff.csv")
        return surrdata


    def __init__(self, application = None):

        self.selection = ["zoe","zyra"]

        self.current_df = self.__get_dataframe()

        self.surrender_data = self.__get_surrender_dataframe()

        self.boxfig = px.box(self.surrender_data, y="GoldDiff", points="all", title="Gold difference between teams once one team surrenders")

        self.fig = px.bar(self.current_df, x="champ_name", y=["Challenger_WinRate","Grandmaster_WinRate","Master_WinRate"], barmode="group")

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)


        self.champ_compar_layout = ccom.ChampComparaison(self.app)

        self.main_layout = html.Div(children=[
            html.H1(children="League of Legends Champions Winrates"),
            dcc.Graph(
                id='winbar',
                figure=self.fig
            ), html.Div(children=[html.Div(children=[html.H4(children="Selected Champions"+"   "*20),
                                  dcc.Dropdown(self.source_df.champ_name, multi=True, id="champ-choose",
                                               placeholder="Select one or multiple champions")], style=self.ROW_STYLE),
                                  html.Div(children=[html.H4(children="Selected Ranks"),
                                  dcc.Dropdown(["Challenger","Grandmaster","Master"],["Challenger","Grandmaster","Master"], multi=True,
                                               id="rank-choose")], style=self.ROW_STYLE),
                                  html.Div(children=[self.champ_compar_layout.main_layout], style={'display': 'inline-block', 'margin-left':"50px"}),
                                  html.H4(children="Data options"),
                                  dcc.Checklist(["Sort by best average win rate"], id="option-check-list")]),
            html.Div(children=[html.H3("Informations"),dcc.Markdown("""
League of Legends is an action strategic team game where ten players fight each other to control objectives on the game's map. Each player controls a champion and each has a different set of abilities. There are 156 champions in the game for 10 different champions at every game.

That's why it's important to reinforce our strategic insight by analyzing champions by win rates and match-up (performance of one champion against one other). To achieve that goal, we will use simple insights like the win rate ratio, the amount of gold per min (which allows champions to become stronger), the vision score (which allows players to have a better view of the game's map) and the Kill, Assists, Death ratio (representing how the player performed in killing, assisting his teams or slowing down his team).

The Player's game level has a wide range of 9 ranks in the game from the lowest Iron to the best Challenger. We will use data from the 3 best ranks Challenger, Grandmaster, and Master to get a high-level insight into champion trends in the game.
Grandmaster and Challenger data are easily influenceable because of the strict limit of player numbers that can have 
these rank at the same time.
Only 300 players can be challengers per region and 700 can be grandmasters, meaning we have overall less data
than other high-level ranks like master.

            """)]),
            html.Div(children=[dcc.Graph(id="boxplot", figure=self.boxfig)], style={'display': 'inline-block',
                    'vertical-align': 'top', 'margin-left': "50px"})
            ])

        if not application:
            self.app.layout = self.main_layout

        self.app.callback(dash.dependencies.Output("winbar", "figure"),
                          [dash.dependencies.Input("champ-choose","value"),
                          dash.dependencies.Input("rank-choose","value"),
                           dash.dependencies.Input("option-check-list","value")])(self.update_with_selection)



    def update_with_selection(self,champ_select, ranks_select, options):

        if ranks_select is not None:
            y_field = list(map(lambda string: string + "_WinRate", ranks_select))
        else:
            y_field = []
        if champ_select is not None:
            self.selection = champ_select
        self.current_df = self.source_df.query('champ_name in '+str(self.selection))
        if options is not None and len(options) > 0 and y_field != []:
            self.current_df = self.current_df.sort_values(by=y_field, ascending=False)
        return px.bar(self.current_df, x="champ_name", y=y_field, barmode="group")



if __name__ == '__main__':
    nrg = ChampWinRate()
    nrg.app.run_server(debug=True, port=8051)
