import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class MoviesStats():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = pd.read_pickle('ADHD_Movies/data/movies_data.pkl')
        self.genres_colors = {'Crime':'black', 'Comedy':'Silver', 'Action':'rosybrown', 'Thriller':'firebrick',
                                 'Adventure':'darksalmon', 'Science Fiction': 'sienna', 'Animation':'sandybrown',
                                 'Family':'tan', 'Drama':'gold', 'Romance':'darkkhaki', 'Mystery':'olivedrab',
                                 'Horror':'darkgreen', 'Fantasy':'darkcyan', 'War':'deepskyblue', 'Music':'slategray',
                                 'Western':'navy', 'History':'blue', 'Documentary':'darkorchid', 'TV Movie':'plum'}
        self.french = {'Crime':'Crime', 'Comedy':'Comédie', 'Action':'Action', 'Thriller':'Thriller',
                       'Adventure':'Aventure', 'Science Fiction': 'Sci-Fi', 'Animation':'Animation',
                       'Family':'Famille', 'Drama':'Drame', 'Romance':'Romance', 'Mystery':'Mystère',
                       'Horror':'Horreur', 'Fantasy':'Fantastique', 'War':'Guerre', 'Music':'Musical',
                       'Western':'Western', 'History':'Historique', 'Documentary':'Docu', 'TV Movie':'TV Movie'}
        self.years = sorted(set(self.df.index.values))

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution de la rentabilité des films'),

            html.Div('Déplacez la souris sur une bulle pour avoir les informations du film.'),

            html.Div([
                html.Div([ dcc.Graph(id='mvs-main-graph'), ], style={'width':'90%', }),

                html.Div([
                    html
                        .Div('Genres :'),
                    dcc.Checklist(
                        id='mvs-which-genre',
                        options=[{'label': self.french[i], 'value': i} for i in sorted(self.genres_colors.keys())],
                        value=sorted(self.genres_colors.keys()),
                        labelStyle={'display':'block'},
                    ),
                    html.Br(),
                    html.Div('Échelle en X :'),
                    dcc.RadioItems(
                        id='mvs-crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                        value='Log',
                        labelStyle={'display':'block'},
                    ),
                    html.Br(),
                    html.Button(
                        self.START,
                        id='mvs-button-start-stop',
                        style={'display':'inline-block'}
                    ),
                ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
            ], style={
                'padding': '10px 50px',
                'display':'flex',
                'justifyContent':'center'
            }),

            html.Div([
                html.Div(
                    dcc.Slider(
                        id='mvs-crossfilter-year-slider',
                        min=self.years[0],
                        max=self.years[-5],
                        step = 1,
                        value=self.years[0],
                        marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display':'block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='mvs-auto-stepper',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
            ], style={
                'padding': '0px 50px',
                'width':'100%'
            }),

            html.Br(),
            dcc.Markdown("""
            Les données choisies pour l'étude sont les films populaires à la date du 28/04/2022. 
            (popularité : selon https://developers.themoviedb.org/3/getting-started/popularity) 
            
            Certaines données sont incomplètes et à ne pas prendre littéralement :
            * Les films début 1900, sûrement dû aux manques d'informations transmises depuis l'époque.
            * Les films vers 2022, souvent annoncés mais pas encore sortis.
            """),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
            #### À propos

            * Données : https://developers.themoviedb.org/
            * (c) 2022 Axel Denost / Hugo Debaye
            """),


        ], style={
            #'backgroundColor': 'rgb(240, 240, 240)',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('mvs-main-graph', 'figure'),
            [ dash.dependencies.Input('mvs-which-genre', 'value'),
              dash.dependencies.Input('mvs-crossfilter-xaxis-type', 'value'),
              dash.dependencies.Input('mvs-crossfilter-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('mvs-div-movie', 'children'),
            dash.dependencies.Input('mvs-main-graph', 'hoverData'))(self.movie_chosen)
        self.app.callback(
            dash.dependencies.Output('mvs-button-start-stop', 'children'),
            dash.dependencies.Input('mvs-button-start-stop', 'n_clicks'),
            dash.dependencies.State('mvs-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('mvs-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('mvs-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('mvs-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('mvs-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('mvs-crossfilter-year-slider', 'value'),
             dash.dependencies.State('mvs-button-start-stop', 'children')])(self.on_interval)


    def update_graph(self, genres, xaxis_type, year):
        dfg = self.df.loc[year]
        dfg = dfg[dfg['genres'].isin(genres)]
        fig = px.scatter(dfg, x = "budget", y = "revenue",
                         #title = f"{year}", cliponaxis=False,
                         size = "popularity", size_max=60,
                         color = "genres", color_discrete_map = self.genres_colors,
                         hover_name="original_title", log_x=True)
        fig.add_trace(go.Scatter(
            x=[0, 1000000000] ,
            y=[0, 1000000000],
            mode="lines",
            line=go.scatter.Line(color="red"),
            showlegend=False)
        )
        fig.update_layout(
            xaxis = dict(title='Budget du film (en $ US de 2022)',
                         type= 'linear' if xaxis_type == 'Linéaire' else 'log',
                         range=(0, 1000000000) if xaxis_type == 'Linéaire'
                         else (np.log10(50), np.log10(1000000000))
                         ),
            yaxis = dict(title="Revenus du film (en $ US de 2022)", range=(0,1000000000)),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            hovermode='closest',
            showlegend=False,
            height=700,
        )
        return fig

    def get_movie(self, hoverData):
        if hoverData == None:  # init value
            return self.df['original_title'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def movie_chosen(self, hoverData):
        return self.get_movie(hoverData)

    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
            return 0
        else:
            return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-5]:
                return self.years[0]
            else:
                for i in range (0, len(self.years)):
                    if year == self.years[i]:
                        return self.years[i + 1]
                    if year < self.years[i]:
                        return self.years[i]
        else:
            return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=False, port=port)


if __name__ == '__main__':
    ws = MoviesStats()
    ws.run(port=8055)
