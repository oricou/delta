import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


class Radar_Accidents():
    def __init__(self, application=None):
        self.df_radars = pd.read_pickle("data/lptr_radars.pkl")
        self.df_accidents = pd.read_pickle("data/lptr_accidents.pkl")
        self.dep_counts = pd.read_pickle("data/lptr_radar_accidents_dep.pkl")

        self.main_layout = html.Div(children=[
            html.H2('Impact des radars sur les accidents de la route en France'),
            dcc.Graph(id='sm-dep-counts'),
            dcc.Markdown("""
                Il n'y a manifestement pas d'impact significatif de la quantité de radar sur le nombre d'accidents
            """),
            html.Br(),
            html.P("Choix de la période :"),
            dcc.Slider(2005, 2018, 1,
                    value=2005,
                    id="range-slider",
                    marks={x:str(x) for x in range(2005,2019)}
            ),
            html.Div(children=[
                html.Div([
                    html.H4('Localisation des radars'),
                    dcc.Graph(id="scatter-mapbox-radars"),
                ]),
                html.Div([
                    html.H4('Localisation des accidents'),
                    dcc.Graph(id="scatter-mapbox-accidents"),
                ])
            ], style={'display':'flex'}),
            html.Div([
                html.H4('Sources :'),
                html.A('accidents', href="https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/",style={'margin':'2px'}),
                html.A('radars', href="https://www.data.gouv.fr/en/datasets/radars-automatiques/",style={'margin':'2px'})
            ]),
            html.Div('Auteurs : Lucas Pinot, Timothée Ribes  © 2022 ')

            ]) # end main layout

        if application:
            self.app = application
        else:
            self.app = Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output("scatter-mapbox-radars", "figure"),
            Input("range-slider", "value")) (self.update_bar_chart)

        self.app.callback(
            Output("scatter-mapbox-accidents", "figure"),
            Input("range-slider", "value")) (self.update_loc_accidents)
        self.app.callback(
            Output("sm-dep-counts", "figure"),
            Input("range-slider", "value")
        ) (self.update_graph)

    def update_loc_accidents(self, slider_range):
        # le masque pour afficher seulement les radars installés à l'année indiquée par le slider
        # (y compris les années d'avant)
        mask = self.df_accidents['an'] == slider_range

        # la fonction d'affichage du graphique avec ses paramètres.
        fig = px.scatter_mapbox(self.df_accidents[mask],
                                lat="lat", lon="long",
                                hover_name='adr', color_discrete_sequence=["blue"],
                                zoom=3.75, height=425, width=425, center={'lat':46,'lon':2})

        # fonction pour afficher la map.
        fig.update_layout(mapbox_style="open-street-map")
        return fig

    def update_bar_chart(self, slider_range):
        # le masque pour afficher seulement les radars installés à l'année indiquée par le slider
        # (y compris les années d'avant)
        mask = self.df_radars['an'] <= slider_range

        # la fonction d'affichage du graphique avec ses paramètres.
        fig = px.scatter_mapbox(self.df_radars[mask],
                                lat="lat", lon="long",
                                hover_name='emplacement', color_discrete_sequence=["blue"],
                                zoom=3.75, height=425, width=425, center={'lat':46,'lon':2})

        # fonction pour afficher la map.
        fig.update_layout(mapbox_style="open-street-map")
        return fig

    def update_graph(self, slider_range):
        #dfg = self.df.loc[year]
        #dfg = dfg[dfg['region'].isin(regions)]
        mask = self.dep_counts['an'] <= slider_range
        fig = px.scatter(self.dep_counts[mask], x = "nb de radars", y = "nb d'accidents", 
                         #title = f"{year}", cliponaxis=False,
                         #size = "population", size_max=60, 
                         #color = "region", color_discrete_map = self.continent_colors,
                         hover_name="dep"
        )
        return fig


if __name__ == '__main__':
    rd_acc = Radar_Accidents()
    rd_acc.app.run_server(debug=True, port=8051)
