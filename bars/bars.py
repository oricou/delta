import dash
from dash import dcc
from dash import html
import plotly.express as px
import json

from bars.get_data_bars import *

data_bars = init_data_bars()
data_revenus = init_data_revenus()
barNumber = init_barNumber()
departements = json.load(open('./bars/data/departements-version-simplifiee.geojson'))
data_bars_revenus = init_data_bars_revenus(data_bars, data_revenus)


class Bars():

    def __init__(self, application=None):

        nbBar_revenu_byCp = init_nbBar_revenu_byCp(data_bars_revenus)
        data_bars_revenus_unique = data_bars_revenus.iloc[:, :6].drop_duplicates().merge(
            nbBar_revenu_byCp[['Postal code', 'Revenu fiscal de référence par foyer fiscal']], on=['Postal code'],
            how='inner')
        fig_dep_1 = px.choropleth_mapbox(barNumber, geojson=departements,
                                         locations='Département', featureidkey='properties.code',  # join keys
                                         color='Nombre de bars',
                                         color_continuous_scale=px.colors.sequential.turbid,
                                         mapbox_style="carto-positron",
                                         range_color=(0, 1000),
                                         zoom=4.5, center={"lat": 47, "lon": 2},
                                         opacity=0.75,
                                         labels={'prix': 'Nombre de bars'}
                                         )
        fig_dep_1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig_dep_2 = px.choropleth_mapbox(barNumber.sort_values(by='Nombre de bars'), geojson=departements,
                                         locations='Département', featureidkey='properties.code',  # join keys
                                         color='Nombre de bars', color_continuous_scale=px.colors.sequential.turbid,
                                         mapbox_style="carto-positron",
                                         range_color=(0, 1000),
                                         zoom=3.8, center={"lat": 47, "lon": 2},
                                         opacity=0.75,
                                         animation_frame='Nombre de bars',
                                         labels={'prix': 'Nombre de bars'}
                                         )
        fig_dep_2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig_concentration1 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                               color_continuous_scale=px.colors.sequential.Plasma,
                                               zoom=4.5, center={"lat": 47, "lon": 2},
                                               mapbox_style="stamen-terrain", )

        fig_concentration1.update_layout(mapbox_style="carto-darkmatter")
        fig_concentration1.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        fig_concentration2 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                               animation_frame='Département',
                                               zoom=3.8, center={"lat": 47, "lon": 2},
                                               mapbox_style="stamen-terrain", )

        fig_concentration2.update_layout(mapbox_style="carto-darkmatter")
        fig_concentration2.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        fig_conc_revnFisc = px.density_mapbox(data_bars_revenus_unique, lat='Latitude', lon='Longitude',
                                              z='Revenu fiscal de référence par foyer fiscal', radius=5,
                                              color_continuous_scale=px.colors.carto.Temps,
                                              zoom=4.5, center={"lat": 47, "lon": 2},
                                              mapbox_style="stamen-terrain", )

        fig_conc_revnFisc.update_layout(mapbox_style="carto-darkmatter")
        fig_conc_revnFisc.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        code_postaux_geo = json.load(open('./bars/data/contours-codes-postaux.geojson'))
        tmp = nbBar_revenu_byCp.drop('Revenu fiscal de référence par foyer fiscal', axis=1)
        tmp['Revenu par foyer fiscal'] = nbBar_revenu_byCp['Revenu fiscal de référence par foyer fiscal'].round(
            decimals=1)

        fig_CP = px.choropleth_mapbox(tmp, geojson=code_postaux_geo,
                                      locations='Postal code', featureidkey='properties.codePostal',  # join keys
                                      color='Nombre de bars', color_continuous_scale=px.colors.carto.Redor,
                                      mapbox_style="carto-positron",
                                      hover_data=['Revenu par foyer fiscal'],
                                      range_color=(0, 150),
                                      zoom=10, center={"lat": 48.857381, "lon": 2.34453},
                                      opacity=0.75,
                                      labels={'prix': 'Nombre de bars'}
                                      )
        fig_CP.update_layout(mapbox_style="carto-darkmatter", margin={"r": 0, "t": 0, "l": 0, "b": 0})

        mean_by_bar_number = init_mean_by_bar_number(nbBar_revenu_byCp)
        fig_blue_1 = px.histogram(data_frame=mean_by_bar_number, x='Revenu fiscal de référence par foyer fiscal',
                                  y='Nombre de bars')

        if application:
            self.main_layout = html.Div(children=[
                html.H3(children='Répartition des bars en France'),
                dcc.Markdown("""
                    Les bars font partie intégrante de la vie des français.
                Après le boulot, pour fêter un évènement ou encore pour sortir entre amis, on y passe tous un jour.

                Leur répartition en France n'est pas homogène, en effet des régions en habritent plus que d'autres.
                Est-ce justifié par le taux de concentration du nombre d'habitant ? Des catégories sociales des habitants? Ou bien simplement d'être breton ?

                Nous avons essayé ici de prendre les paramètres géographiques de ces régions afin d'émettre des hypothèses quant à leur répartition en France.

                    """),
                html.Div(
                    [dcc.Graph(id='fig_department', figure=fig_dep_1)], style={'width': '100%', }),
                html.Br(),
                dcc.Markdown(""" Sur ce graphique nous pouvons observer le taux de bars par département.
                        Nous remarquons que dans des régions comme la Bretagne, le Nord-Pas-de-Calais ou encore l'Ile de France, e nombre de bars est plus élévé que la moyenne. 
                        On peut également remarquer que les bars sont relativement présent dans les zones touristiques : les départements proches de la côte possèdent plus de bars que dans les zones centrales de la France. On pourra vérifier l'impact de la côte sur le nombre de bars à l'aide du graphique suivant."""),
                html.Div(
                    [dcc.Graph(id='sond_t2', figure=fig_dep_2)], style={'width': '100%', }),
                html.Br(),
                dcc.Markdown("""On peut ici voir, en cliquant sur le bouton "Play", le classement des départements contenant le moins de bar aux départements en contenant le plus. On peut aussi s'amuser à voir les départements contenant un nombre de bar particulier en manipulant le curseur.
"""),
                html.Div(
                    [
                        dcc.Graph(id='fig_concentration', figure=fig_concentration1),
                        dcc.RadioItems(
                            id='radio_concentration',
                            options=[{'label': 'Concentration des bars en France', 'value': 'graph1'},
                                     {'label': 'Concentration des bars en France par département', 'value': 'graph2'}],
                            value='graph1',
                            labelStyle={'display': 'block'}),
                    ], style={'width': '100%', }),
                dcc.Markdown(
                    """On voit très clairement ici que les bars se concentrent principalement dans la capitales et sur les littoraux"""),
                html.Br(),
                html.Br(),
                html.Div(
                    [dcc.Graph(id='sond_t2', figure=fig_conc_revnFisc)], style={'width': '100%', }),
                dcc.Markdown("""On voit sur ce graphique que les campagnes sont assez effacées quand on prend en compte le revenu fiscal de référence. On voit donc deux choses : 
                * La plus part des campagnes n'ont pas assez de bars par rapport à la hauteur du revenus fiscal de référence. 
                * Les villes sont quant à elles beaucoup plus marquées car la concentration de bars y est plus importante et les revenus fiscaux plus élevés"""),
                html.Br(),
                html.Div(
                    [dcc.Graph(id='sond_t2', figure=fig_CP)], style={'width': '100%', }),
                html.Br(),
                dcc.Markdown(
                    """Nous avons là un zoom sur Paris et ses arrondissements. On voit la concentration de bars dans chacun de ces codes postaux, on peut voir le revenu fiscal de référence par code postale en passant la souris dessus. On peut dézoomer pour voir la subdivision entière de la france en code postal et ainsi constater la concentration des bars en fonction des catégories sociales et des quartiers plutôt défavorisés"""),
                html.Div(
                    [
                        html.Label('Bars en fonction du revenu '),
                        dcc.Graph(id='fig_blue', figure=fig_blue_1),
                        dcc.RadioItems(
                            id='radio_blue',
                            options=[
                                {'label': 'Bar plot', 'value': 'graph1'},
                                {'label': 'Scatter plot 1', 'value': 'graph2'},
                                {'label': 'Scatter plot 2', 'value': 'graph3'},
                                {'label': 'Scatter plot 3', 'value': 'graph5'},
                                {'label': 'Scatter plot 4', 'value': 'graph6'},
                                {'label': 'Line plot logarithm', 'value': 'graph7'},
                            ],
                            value='graph1',
                            labelStyle={'display': 'inline'}),
                    ], style={'width': '100%', }),
                html.Br(),
                dcc.Markdown(
                    """Sur le graphe 3 on voit que globalement la plus part des villes/codes postaux possèdent moins de 20 bars. On voit également que dans les villes à fort et faible revenus fiscaux, dans les extremums, la quantité de bars n'excède pas la centaine de bars."""),
                dcc.Markdown(
                    """Nous voyons sur ce premier graphe qu'un grand nombre de bars se trouve dans les endroits avec un revenus fiscal de référence assez faible."""),
                dcc.Markdown(
                    """Nous voyons sur ce dernier graphe que le nombre de bars est assez faible dans les extremums et que la plus part des endroits avec beaucoup de bars se trouvent dans les endroits avec un revenu fiscal de référence compris entre 20 et 40 ce qui appuie les résultats du barplot."""),
                html.Br(),
                html.Br(),

                dcc.Markdown("""
            En conclusion, nous avons vu que le taux de bars dépendait de :
            * Nombre d'habitants (logique, plus il y a d'habitants plus il y a de bars)
            * Par conséquent du département (là où il y a plus ou moins d'habitants)
            Nous avons aussi cherché à voir si la classe sociale de la population avait un impact sur leur nombre.
            Nous en avons déduit que les communes aux plus petits revenus étaient celles qui possédaient le plus de bars.
            """)
            ], style={
                'backgroundColor': 'white',
                'padding': '10px 50px 10px 50px',
            }
            )
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(dash.dependencies.Output('fig_concentration', 'figure'),
                          [dash.dependencies.Input('radio_concentration', 'value')])(self.update_graph_concentration)

        self.app.callback(dash.dependencies.Output('fig_blue', 'figure'),
                          [dash.dependencies.Input('radio_blue', 'value')])(self.update_graph_blue)

    def update_graph_concentration(self, value):
        if value == 'graph1':
            fig_concentration1 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département',
                                                   radius=4.3,
                                                   color_continuous_scale=px.colors.sequential.Plasma,
                                                   zoom=4.5, center={"lat": 47, "lon": 2},
                                                   mapbox_style="stamen-terrain", )
            fig_concentration1.update_layout(mapbox_style="carto-darkmatter")
            fig_concentration1.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            return fig_concentration1
        else:
            fig_concentration2 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département',
                                                   radius=4.3,
                                                   animation_frame='Département',
                                                   zoom=3.8, center={"lat": 47, "lon": 2},
                                                   mapbox_style="stamen-terrain", )
            fig_concentration2.update_layout(mapbox_style="carto-darkmatter")
            fig_concentration2.update_layout(margin=dict(b=0, t=0, l=0, r=0))
            return fig_concentration2

    def update_graph_blue(self, value):
        nbBar_revenu_byCp = init_nbBar_revenu_byCp(data_bars_revenus)
        mean_by_bar_number = init_mean_by_bar_number(nbBar_revenu_byCp)
        nbBar_revenu_byCp = data_bars_revenus.groupby('Nom')[
            'Revenu fiscal de référence par foyer fiscal'].mean().reset_index()

        if value == 'graph1':
            fig_blue_1 = px.histogram(data_frame=mean_by_bar_number, x='Revenu fiscal de référence par foyer fiscal',
                                      y='Nombre de bars')
            return fig_blue_1
        elif value == 'graph2':
            fig_blue_2 = px.scatter(data_frame=mean_by_bar_number, y='Revenu fiscal de référence par foyer fiscal',
                                    x=mean_by_bar_number['Nombre de bars'], log_y=True)
            return fig_blue_2
        elif value == 'graph3':
            fig_blue_3 = px.line(mean_by_bar_number, x="Nombre de bars",
                                 y="Revenu fiscal de référence par foyer fiscal",
                                 title='Revenu fiscal de référence moyen en fonction du nombre de bars dans une commune',
                                 labels={
                                     "Revenu fiscal de référence par foyer fiscal": "Revenu fiscal de référence moyen",
                                 })
            return fig_blue_3
        elif value == 'graph5':
            fig_blue_5 = px.scatter(data_frame=nbBar_revenu_byCp, x='Revenu fiscal de référence par foyer fiscal',
                                    y=nbBar_revenu_byCp.index, log_y=True, labels={
                    "index": "Bar n°"})
            return fig_blue_5
        elif value == 'graph6':
            fig_blue_7 = px.scatter(data_frame=nbBar_revenu_byCp, y='Revenu fiscal de référence par foyer fiscal',
                                    x=nbBar_revenu_byCp.index, labels={
                    "index": "Bar n°",
                    "Revenu fiscal de référence par foyer fiscal": "Revenu fiscal de référence moyen",

                }, )
            fig_blue_7.update_xaxes(tickformat="0")
            return fig_blue_7
        else:
            fig_blue_6 = px.line(x=np.arange(len(nbBar_revenu_byCp)),
                                 y=np.sort(nbBar_revenu_byCp['Revenu fiscal de référence par foyer fiscal']),
                                 log_y=True,
                                 title='Revenu fiscal de référence des %d bars' % len(nbBar_revenu_byCp), labels={
                    "y": "Revenu fiscal de référence par foyer fiscal"})
            fig_blue_6.update_xaxes(tickformat="0")
            return fig_blue_6


if __name__ == '__main__':
    bars = Bars()
    bars.app.run_server(debug=True, port=8051)
