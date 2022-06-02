from gc import get_count
import sys

from requests import NullHandler
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from os.path import exists
from TA_MG_SpotifyMusicPopularity.data.get_data import get_data

class Spotify():

    def init_characteristics(self):
        df = pd.read_csv('TA_MG_SpotifyMusicPopularity/data/SpotifyFeatures.csv')
        df = df.rename(columns={'artist_name':'artist', 'track_name':'title'})
        df = df.drop(columns=['Unnamed: 0'])
        self.musics = df

        dfmean = df.drop(columns=['artist', 'title', 'track_id', 'key', 'mode', 'time_signature'])
        dfmean = dfmean.groupby(['genre']).mean()
        self.characteristics = dfmean
        self.genres = dfmean.index

        dftopten = pd.DataFrame(columns=df.columns)
        for genre in dfmean.index:
            topten = df[df.genre == genre].iloc[np.argpartition(df[df.genre == genre].popularity, -10)[-10:]]
            dftopten = pd.concat([dftopten, topten])
        dftopten = dftopten.drop(columns=['artist', 'title', 'track_id', 'key', 'mode', 'time_signature'])
        dftopten = dftopten.groupby(['genre']).mean()
        self.topten = dftopten

        count = []
        for genre in dfmean.index:
            count.append(np.sum(df.genre == genre))
        self.count = count

    def __init__(self, application = None):
        if not(exists("./TA_MG_SpotifyMusicPopularity/data/SpotifyFeatures.csv") and exists("./TA_MG_SpotifyMusicPopularity/data/charts.csv")):
            get_data()
        
        self.french = {'popularity':'popularité', 'acousticness':'acousticité', 'danceability':'dansabilité', 'duration_ms':'durée en ms',
        'energy':'énergie', 'instrumentalness':'instrumentalité', 'liveness':'vivacité', 'loudness':'intensité sonore', 'speechiness':'quantité de paroles',
        'tempo':'tempo', 'valence':'valence'}

        self.init_characteristics()

        self.main_layout = html.Div(children=[
            html.H3(children='Caractéristiques de la popularité d\'une musique sur Spotify'),
            html.Div([
                html.Div([ dcc.Graph(id='charac-main-graph'), ], style={'width':'85%'}),
                
                html.Div([
                    html.Div([
                        html.Div('Caractéristique axe x :'),
                        dcc.RadioItems(
                            id='x-charac',
                            options=[{'label':self.french[self.characteristics.columns[i]], 'value':i} for i in range(len(self.characteristics.columns))],
                            value=2,
                            labelStyle={'display':'block'},
                            ),
                        html.Br(),
                        html.Div('Moyenne par genre sur le top :'),
                        dcc.RadioItems(
                            id='topten',
                            options=[{'label':'~ 10 000', 'value':False},
                                     {'label':'10', 'value':True}],
                            value=False,
                            labelStyle={'display':'block'},
                            )
                        ], style={'margin-left':'30px', 'margin-top':'100px','width': '10em', 'float':'right'} )
                    ])      
                ], style={
                    'padding-right': '30px', 
                    'display':'flex'
                }),
            
            html.Div('Cliquez sur une bulle pour avoir le diagramme polaire du genre ci-dessous.'),
            html.Br(),
            html.Div([ 
                    html.Div('Échelle'),
                    dcc.RadioItems(
                        id='log',
                        options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                        value='Linéaire',
                        labelStyle={'display':'block'},
                        )
                    ]),
            html.Br(),
            html.Br(),
            html.Div([
                dcc.Graph(id='genre-charac', 
                          style={'width':'50%'}),
            ]),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
                #### Notes :
                    
                La popularité d'un genre est un pourcentage. Celle d'une musique correspond à son nombre d'écoutes par rapport au nombre d'écoutes de la musique la plus écoutée.
                Ainsi, la valeur utilisée correspond à la moyenne des popularités des musiques d'un genre
                
                Les autres caractéristiques du graphique sont définies à cette adresse : [Caractéristiques audio d'une musique](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
                """),
            html.Br(),
            dcc.Markdown("""
                #### À propos

                * Sources : 
                    * [Caractéristiques et popularité des musiques de Spotify](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) sur kaggle.com
                    * [Informations complémentaires sur la popularité, la date, ou la région](https://www.kaggle.com/datasets/dhruvildave/spotify-charts) sur kaggle.com
                * (c) 2022 Thibaut Ambrosino, Melvin Gidel
                """)
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('charac-main-graph', 'figure'),
                    dash.dependencies.Input('x-charac', 'value'),
                    dash.dependencies.Input('log', 'value'),
                    dash.dependencies.Input('topten', 'value')
                    )(self.update_graph)
        self.app.callback(
                    dash.dependencies.Output('genre-charac', 'figure'),
                    dash.dependencies.Input('charac-main-graph', 'clickData'))(self.update_genre_graph)

    def update_graph(self, x_carac, log, topten):
        df,size = (self.characteristics,self.count) if not(topten) else (self.topten,[10 for _ in self.genres])

        log = log == 'Log'
        fig = px.scatter(df, x=df.columns[x_carac], y='popularity', color=df.index, hover_name=df.index, log_x=log,
                        title="Popularité des genres en fonction de certaines caractéristiques",
                        labels={
                            'popularity': 'popularité',
                            df.columns[x_carac]: self.french[df.columns[x_carac]]
                        },
                        size=size,
                        height=750,
                    )
        return fig

    def get_iris_fig(self, genre):
        dfmean = self.musics
        dfmean = dfmean.drop(columns=['artist', 'title', 'track_id', 'key', 'mode', 'time_signature'])
        genre_df = dfmean.where(dfmean['genre'] == genre).dropna().groupby(['genre']).mean()
        
        features=[genre_df['popularity'],genre_df['acousticness'],genre_df['danceability'],genre_df['energy'],genre_df['instrumentalness'],genre_df['speechiness'],
                genre_df['valence'],genre_df['liveness'],genre_df['loudness']]
        ranges=[100.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -60.0]

        for index in range(len(ranges)):
            features[index] = round(features[index]/ranges[index], 3)

        list = []

        for i in range(len(features)):
            list.append(features[i].values[0])

        theta = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness', 'valence', 'liveness', 'loudness']
        fig = go.Figure(data=go.Scatterpolar(
            r = list,
            theta = [self.french[i] for i in theta],
            fill = 'toself'
            ))

        fig.update_layout(
            polar=dict(
            radialaxis=dict(
                visible=True,range=[0,1.0]
            ),
            ),
            showlegend=False,
            title = 'Diagramme polaire des caractéristiques du genre "' + str(genre) + '"',
            title_x=0.5
        )

        return fig

    def get_genre(self, clickData):
        if clickData == None:  # init value
            return self.genres[np.random.randint(len(self.genres))]
        return clickData['points'][0]['hovertext']

    def update_genre_graph(self, clickData):
        genre = self.get_genre(clickData)
        fig = self.get_iris_fig(genre)
        return fig

if __name__ == '__main__':
    spo = Spotify()
    spo.app.run_server(debug=True, port=8051)