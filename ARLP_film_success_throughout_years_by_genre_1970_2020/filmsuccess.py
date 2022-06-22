import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from .data.get_data import extract_data
import numpy as np

#fig = px.scatter(df, x="year", y="gross", size=np.exp(df["total_score"]), size_max=60, hover_name="name", hover_data=["genre"], color=df.genre[df.genre.apply(lambda x: len(x) > 0)].apply(lambda x: x[0]))

class FilmSuccess():

    def __init__(self, application = None):
        df = extract_data()
        df.rename(columns={"total_score": "user_rating"}, inplace=True)
        
        self.app = dash.Dash(__name__)
    
        colors = { 'Horror' : 'red', 'Mystery' : 'pink', 'Thriller' : 'black',
              'Crime' : 'purple', 'Drama' : 'darkviolet', 'Comedy' : 'indigo',
              'Sci-Fi' : 'blue', 'Music' : 'light blue', 'Action' : 'cyan',
              'Biography' : 'teal', 'History' : 'olive', 'War' : 'light green',
              'Fantasy' : 'lime', 'Romance' : 'yellow', 'Western' : 'moccasin',
              'Family' : 'orange', 'Animation' : 'darkorange',
              'Adventure' : 'brown', 'Musical' : 'grey', 'Sport' : 'darksalmon',}

        fig2_df = pd.DataFrame()
        exploded_df = df.explode("genre")
        genres = exploded_df.genre.unique()
        for genre in genres:
          _df = exploded_df[exploded_df['genre'] == genre]
          _df = _df.groupby('year').mean()
          _df["genre"] = genre
          fig2_df = pd.concat([fig2_df, _df])
        fig2_df = fig2_df.reset_index()

        self.main_layout = html.Div(children = [
                                          html.H3('Succès des films américains par genre'),
                                          html.Div("Déplacez votre souris sur le graphique et cliquez sur un point de la courbe pour obtenir des informations additionnels dans le second graphique. Vous pouvez aussi masquer des genres en cliquant dessus dans la légende. N'hésitez pas à zoomer pour voir le graphique plus en détail. Vous pouvez choisir sur la gauche les donnée représentées en ordonné."),

                                          html.Div(children = [
                                            html.Div([dcc.RadioItems(
                                                id='y_axis',
                                                options=[{'label': i, 'value': i} for i in fig2_df[["profit", "user_rating", "votes"]].columns],
                                                value=fig2_df[["profit", "user_rating", "votes"]].columns[0],
                                                labelStyle={'display':'block'}
                                              )], style={'display':'flex', 'align-items':'center', 'width':'10%'}),
                                            html.Div([dcc.Graph(id="fig2")], style={'width':'90%'})
                                          ], style={'display':'flex'}),
                                          
                                          html.Div("Déplacez votre souris sur les bulles pour obtenir des informations additionnels. Le graphique ci-dessous affiche les 5 films avec le plus haut profit pour l'année et le genre sélectionné ainsi que les 5 films avec le profit le plus faible afin de voir quels films ont eut le plus d'impact durant l'année. La taille des bulles correspond aux notes des spectateurs."),
                                          html.Div([dcc.Graph(id="fig3")]),
                                          dcc.Markdown("""
                        #### À propos
                        
                        Le scrapper est disponible dans les fichiers sources. Un notebook est aussi trouvable dans le code source avec davantage de graphiques et analyses.
                        
                        * Sources : 
                           * [Imdb](https://www.imdb.com/)
                           * [RottenTomatoes](https://www.rottentomatoes.com/)
                        * (c) 2022 Louis Prenleloup - Axel Ribon
                        """)
                                        ])
                                        
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        @self.app.callback(
            dash.dependencies.Output('fig2', 'figure'),
            dash.dependencies.Input('y_axis', 'value'))
        def update_fig2(y_value):
          fig = px.line(fig2_df, x="year", y=y_value, color="genre", color_discrete_map=colors, hover_data=["genre"])
          return fig

        @self.app.callback(
            dash.dependencies.Output('fig3', 'figure'),
            dash.dependencies.Input('fig2', 'clickData'))
        def update_fig3(clickData):
          if clickData == None:
            year = 2015
            genre = genres.tolist()[0]
          else:
            year = clickData['points'][0]['x']
            genre = clickData['points'][0]['customdata'][0]

          fig3_df = exploded_df[exploded_df.year == year]
          fig3_df = fig3_df[fig3_df.genre == genre]
          fig3_df.drop(fig3_df[fig3_df.profit.isna()].index, inplace=True)
          fig3_df = fig3_df.sort_values(by='profit')
          fig3_df = pd.concat([fig3_df.head(5), fig3_df.tail(5)])

          return px.scatter(fig3_df, x="name", y="profit", title="{} {}".format(year, genre), color="genre", color_discrete_map=colors, size=np.exp(fig3_df.user_rating), size_max=60, hover_data={"user_rating": True, "votes": True})


    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    filmsuc = FilmSuccess()
    filmsuc.run(port=8055)
