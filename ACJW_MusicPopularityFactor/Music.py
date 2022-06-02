import pandas as pd
import plotly.express as px
import ast
import dash
from dash import dcc
from dash import html
import json


class Song:
    def __init__(self, application=None):
        if application == None:
            self.root = ""
        else:
            self.root = "./ACJW_MusicPopularityFactor/"

        self.songs = pd.read_pickle(self.root + "data/songs.pkl")
        self.df = pd.read_pickle(self.root + "data/df.pkl")
        self.artists = pd.read_pickle(self.root + "data/artists.pkl")
        self.Tracks = pd.read_pickle(self.root + "data/Tracks.pkl")
        self.songs_pays = pd.read_pickle(self.root + "data/songs_pays.pkl")
        self.head_country = pd.read_pickle(self.root + "data/head_country.pkl")
        self.songpopularity = pd.read_pickle(self.root + "data/songpopularity.pkl")

        self.mymap = json.load(open(self.root + "custom.geo_1.json"))

        self.main_layout = html.Div(
            children=[
                dcc.Markdown(
                    """
            ## Facteurs de popularité des musiques
            """
                ),
                html.H3(children="POPULARITE DES GENRES AU FIL DES ANNEES"),
                html.Div(
                    [
                        dcc.Graph(id="barplot"),
                        dcc.Dropdown(
                            [
                                "AOTY Critic Score",
                                "AOTY User Score",
                                "Metacritic Critic Score",
                                "Metacritic User Score",
                            ],
                            "AOTY Critic Score",
                            id="barplot_y",
                        ),
                        dcc.Dropdown(
                            sorted(
                                self.df["Release Year"].unique().tolist(),
                                reverse=True,
                            ),
                            2018,
                            id="barplot_year",
                        ),
                        dcc.Dropdown([5, 10, 20, 50], 10, id="barplot_n"),
                    ]
                ),
                dcc.Markdown(
                    """
            Le graphique est interactif. En passant la souris sur des parties du graphe des infobulles sur le genre et la critique apparaissent.
            Les differentes notations, années et nombres de genres affichés peuvent être modifier avec les  menus deroulants ci-dessus.
            - AOTY: Album of the year, album de l'année
            - MetaCritic : Site Américain qui collecte des notes de divers sujets de la Pop culture
            """
                ),
                html.H3(children="POPULARITE DES ARTISTES"),
                html.Div([dcc.Graph(id="corrplot", figure=self.createcorrplot())]),
                dcc.Markdown(
                    """
             Ce graphique présente la corrélation entre la popularité d'une musique avec le nombre de personnes suivant son interprète sur Spotify.\n
            Le graphique est interactif, en passant la souris sur des points, des infobulles apparaisent pour afficher le genre , l'artiste et le Titre de son album.\n
            Cliquez sur des points de la légende pour retirer des genres
            
            On peut remarquer une relation entre le nombre de followers et la popularité de son album.
            """
                ),
                html.Div(
                    children=[
                        html.H3(children="POPULARITE PAR PAYS"),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="map",
                                    figure=self.createMap(),
                                    style={"padding": "100px"},
                                ),
                                dcc.Markdown(
                                    """
                                    Cette carte présente le genre le plus populaire par pays.\n
                                    Elle est intéractive, en passant la souris sur un pays, une infobulle apparait montrant le titre le plus populaire dans ce pays.\n
                                    La sélection d'un pays sur cette carte modifie le graphe ci-dessous
                                    """
                                ),
                                dcc.Graph(id="pieChart"),
                                dcc.Markdown(
                                    """
                                    Ce graphique représente les genre les plus populaires du pays selectionné sur la carte précedente.\n
                                    Il est possible de retirer des genres en cliquant sur la légende
                                    """
                                ),
                            ]
                        ),
                    ]
                ),
                dcc.Markdown(
                    """
                   #### À propos

                   * Données : 
                       - [Spotify Dataset 1921-2020, 600k+ Tracks](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks)
                       - [Contemporary album ratings and reviews](https://www.kaggle.com/datasets/kauvinlucas/30000-albums-aggregated-review-ratings)
                       - [Top 50 Spotify songs BY EACH COUNTRY](https://www.kaggle.com/datasets/leonardopena/top-50-spotify-songs-by-each-country)
                   * (c) 2022 Alexandre Castello & Jacky Wu
               """
                ),
            ],
            style={"margin": "50px", "backgroundColor": "white"},
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        self.app.callback(
            dash.dependencies.Output("barplot", "figure"),
            [
                dash.dependencies.Input("barplot_y", "value"),
                dash.dependencies.Input("barplot_year", "value"),
                dash.dependencies.Input("barplot_n", "value"),
            ],
        )(self.createbarplot)

        self.app.callback(
            dash.dependencies.Output("pieChart", "figure"),
            [dash.dependencies.Input("map", "clickData")],
        )(self.getCountry)

    def createbarplot(self, y, year, n):
        x = "Genre"

        Review_2015 = (
            self.df[self.df["Release Year"] == year]
            .groupby(x)
            .mean()
            .sort_values(by=[y, x], ascending=False)
            .head(n)
        )

        return px.bar(
            Review_2015,
            y=y,
            title=f"Best {x} by {y} in {year}",
            log_y=True,
            height=800,
            width=1100,
        )

    def createcorrplot(self):
        return px.scatter(
            self.artists.head(5000),
            x="popularity",
            y="followers",
            color="Genre",
            hover_name="artists",
            hover_data=["Title", "Label"],
        )

    def createMap(self):
        fig = px.choropleth_mapbox(
            self.head_country,
            geojson=self.mymap,
            locations="Country",
            featureidkey="properties.name",
            color="index",
            color_continuous_scale="HSV",
            hover_name="name",
            hover_data=["artists", "Album"],
            mapbox_style="carto-positron",
            zoom=1,
            center={"lat": 0, "lon": 0},
            opacity=0.5,
            labels={"Genre le plus écouté sur Spotify selon des pays en 2020"},
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_coloraxes(showscale=False)
        return fig

    def createPie(self, choice_country):
        country = self.songpopularity[self.songpopularity["Country"] == choice_country]
        # piechart
        l = []
        for c in list(country.genres):
            l.extend(c)

        piedata = pd.DataFrame(data=l, columns=["occ"])
        piedata = pd.DataFrame(piedata.groupby("occ")["occ"].count())

        fig = px.pie(
            piedata,
            values="occ",
            names=piedata.index,
            hover_name=piedata.index,
            color_discrete_sequence=px.colors.sequential.Plasma,
            title=f"Best genres in {choice_country}",
            height=700,
            width=900,
        )
        fig.update_traces(textinfo="percent+label")
        fig.update_layout(title={'font': {'size': 35}})
        return fig

    def getCountry(self, clickData):
        if clickData == None:
            return self.createPie("France")
        print(clickData)
        return self.createPie(clickData["points"][0]["location"])

    def run_server(self, debug=False, port=8050):
        self.app.run_server(debug=debug, port=port, use_reloader=False)


if __name__ == "__main__":
    song = Song()
    song.app.run_server(debug=True, port=8051, use_reloader=False)
