import sys
import dash
import flask
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from datetime import date
import json


class PollutionFrancaise():
    # ========== Global variables of the class ==========

    # Dict of the polluants and their mesure for a easy use of them
    dict_mesures_polluants = {
        "NO": "µg-m3",
        "NO2": "µg-m3",
        "O3": "µg-m3",
        "NOX as NO2": "µg-m3",
        "PM10": "µg-m3",
        "PM2.5": "µg-m3",
        "C6H6": "µg-m3",
        "SO2": "µg-m3",
        "CO": "mg-m3"
    }

    # The whole 2021 months list
    months_list = [
        '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
        '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12'
    ]

    # The list of all our polluants
    polluants_list = [
        'PM10', 'NO', 'NO2', 'O3', 'NOX as NO2', 'PM2.5', 'C6H6', 'SO2', 'CO'
    ]

    # The list of all our france's regions
    regions_list = [
        'Grand Est', "Provence-Alpes-Côte d'Azur", 'Île-de-France',
        'Normandie', 'Hauts-de-France', 'Auvergne-Rhône-Alpes', 'Occitanie',
        'Nouvelle-Aquitaine', 'Bretagne', 'Pays de la Loire',
        'Bourgogne-Franche-Comté', 'Centre-Val de Loire', 'Guadeloupe',
        'La Réunion', 'Martinique', 'Guyane', 'Corse', 'Mayotte'
    ]

    def __init__(self, application=None):
        # Reading the file to load the data to display our map of france
        map_data = pd.read_csv("data/monthly_day_average.csv", sep=';')
        map_data = map_data.set_index("Date")
        self.map_data = map_data

        # Reading the file to load the data to display our lines for the pollution's values evolution
        line_plot_data = pd.read_csv("data/monthly_hour_average.csv", sep=';')
        line_plot_data = line_plot_data.set_index("Date")
        self.line_plot_data = line_plot_data

        # Dict used in our function to display the month slider
        slider_dict = dict(
            zip(list(range(1, 13)), sorted(set(self.months_list))))
        self.slider_dict = slider_dict

        # Loading the map to display the regions of France
        regions_map = json.load(open('data/regions.geojson'))
        self.regions_map = regions_map

        # Reading the file for the histogram plot
        df_influences_monthly = pd.read_csv("data/monthly_influences.csv",
                                            sep=';')
        self.data_histo = df_influences_monthly

        self.main_layout = html.Div(children=[
            # Title of our page
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([
                                html.H4(
                                    "Evolution des polluants contenus dans l'air en France par régions.",
                                    style={"font-weight": "bold"},
                                ),
                                # html.
                                # H5("Rendu du devoir pour le projet de PYBD dans le cadre du cursus de SCIA à EPITA par Noé Jenn-Treyer et Jules Dorbeau.",
                                #    style={"margin-top": "0px"}),
                                # html.
                                # H5("Suite au ratachement sur le projet delta, nous avons eu des problèmes de styles voci un lien ou se situe notre projet avant les fixs (figures plus grandes):",
                                #    style={"margin-top": "0px"}),
                                # dcc.Markdown("https://dash-pybd-jules-dorbeau.herokuapp.com/",
                                #    style={"margin-top": "0px"}),
                            ])
                        ],
                        className="three column",
                        id="title",
                    ),
                    # create empty div for align center
                    html.Div(className="one-third column", ),
                ],
                id="header",
                style={"margin-bottom": "25px"},
            ),

            # ===== MAP =====
            # Description of the histogram and the displayed data
            html.Div(
                [
                    html.
                    P("Sur cette carte de France, nous avons voulu représenter les moyennes journalières des polluants en fonction du polluant et de la date choisie par l'utilisateur.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                    html.
                    P("Le but est de pouvoir facilement observer les moyennes des régions françaises et leur évolution au fil des jours.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                    html.
                    P("Afin de voir la valeur précise pour une région, il suffit d'y passer sa souris.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                ],
                className="pretty_container twelwe columns",
            ),
            # Display of our map with date and polluant selection
            html.Div(
                [
                    # Div for the polluant and date selection
                    html.Div(
                        [
                            html.P('Choix de la date :',
                                   style={"font-weight": "bold"}),
                            dcc.DatePickerSingle(
                                id='single-date-picker-map',
                                min_date_allowed=date(2021, 1, 1),
                                max_date_allowed=date(2021, 12, 31),
                                initial_visible_month=date(2021, 1, 1),
                                date=date(2021, 1, 1),
                                display_format='MMM Do, YY'),
                            html.P(),
                            html.P('Choix du polluant :',
                                   style={"font-weight": "bold"}),
                            dcc.RadioItems(
                                id='radio-selection-polluant-map',
                                options=[{
                                    'label': pol,
                                    'value': pol
                                } for pol in self.polluants_list],
                                value='PM10',
                                labelStyle={'display': 'block'},
                            ),
                        ],
                        style={"margin-right": "30px"},
                        className="pretty_container three columns",
                    ),
                    # Div for our map plot
                    html.Div(
                        [
                            dcc.Graph(id='map-plot-graph'),
                        ],
                        className="pretty_container eight columns",
                    ),
                ], ),

            # ===== MULTI LINES =====
            # Description of the histogram and the displayed data
            html.Div(
                [
                    html.
                    P("Pour ce graphique représentant l'évolution des polluants sur un mois pour une région sélectionnée par l'utilisateur, nous avons voulu pouvoir représenter simplement l'évolution heure par heure des polluant que nous voulons choisir mais sans pour autant créer trop de boutons.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                    html.
                    P("Nous avons donc opté pour un graphe avec les évolutions de tout les polluants permettant ainsi de choisir quels polluants afficher ou non en cliquant sur leur dénomination sur le côté droit du graphe.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                ],
                className="pretty_container twelwe columns",
            ),

            # Slider for the multiple lines plot
            html.Div(
                [
                    html.
                    P("Sélectionnez le mois durant lequel vous souhaitez obsever l'évolution des polluants et la région.",
                      className="control_label",
                      style={
                          "text-align": "center",
                          "font-weight": "bold"
                      }),
                    dcc.Slider(1,
                               12,
                               step=None,
                               marks=self.slider_dict,
                               value=1,
                               id='slider-date-plot-line'),
                ],
                style={
                    'display': 'inline-block',
                },
                className="pretty_container twelwe columns",
            ),

            # Choices for the region and graph of the lines
            html.Div(
                [
                    # Div for the region selection
                    html.Div(
                        [
                            html.P('Choix de la région :',
                                   style={"font-weight": "bold"}),
                            dcc.RadioItems(
                                id='radio-selection-region-plot-lines',
                                options=[{
                                    'label': reg,
                                    'value': reg
                                } for reg in self.regions_list],
                                value='Grand Est',
                                labelStyle={'display': 'block'},
                            ),
                        ],
                        style={"margin-right": "30px"},
                        className="pretty_container three columns",
                    ),
                    # Div for our multi lines plot
                    html.Div(
                        [
                            dcc.Graph(id='multi-lines-plot-graph'),
                        ],
                        className="pretty_container eight columns",
                    ),
                ], ),

            # ===== HISTOGRAM =====
            # Description of the histogram and the displayed data
            html.Div(
                [
                    html.
                    P("Pour cette dernière partie, nous avons voulu compléter les informations que nous avons affichées jusque là en permettant de voir la part des influences pour chaque régions et polluants.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                    html.
                    P("Cela permet ainsi de mieux comprendre à quoi peuvent être dus des pics de certains polluants dans des régions à des moments de l'année.",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                ],
                className="pretty_container twelwe columns",
            ),

            # Slider for the multiple lines plot
            html.Div(
                [
                    html.
                    P("Sélectionnez le mois durant lequel vous souhaitez obsever les origines des polluants.",
                      className="control_label",
                      style={
                          "text-align": "center",
                          "font-weight": "bold"
                      }),
                    dcc.Slider(1,
                               12,
                               step=None,
                               marks=self.slider_dict,
                               value=1,
                               id='slider-date-histo'),
                ],
                style={
                    'display': 'inline-block',
                },
                className="pretty_container twelwe columns",
            ),

            # Display of the histogram and selection of the region and polluant
            html.Div(
                [
                    # Div for the region selection and the polluant selection
                    html.Div(
                        [
                            html.P('Choix du polluant :',
                                   style={"font-weight": "bold"}),
                            dcc.Dropdown([
                                'PM10', 'NO', 'NO2', 'O3', 'NOX as NO2',
                                'PM2.5', 'C6H6', 'SO2', 'CO'
                            ],
                                         'PM10',
                                         id='drop-polluant-histo'),
                            html.P(),
                            html.P('Choix de la région :',
                                   style={"font-weight": "bold"}),
                            dcc.Dropdown([
                                'Grand Est', "Provence-Alpes-Côte d'Azur",
                                'Île-de-France', 'Normandie',
                                'Hauts-de-France', 'Auvergne-Rhône-Alpes',
                                'Occitanie', 'Nouvelle-Aquitaine', 'Bretagne',
                                'Pays de la Loire', 'Bourgogne-Franche-Comté',
                                'Centre-Val de Loire', 'Guadeloupe',
                                'La Réunion', 'Martinique', 'Guyane', 'Corse',
                                'Mayotte'
                            ],
                                         'Grand Est',
                                         id='drop-region-histo'),
                        ],
                        style={"margin-right": "30px"},
                        className="pretty_container three columns",
                    ),
                    # Div for our histogram plot
                    html.Div(
                        [
                            dcc.Graph(id='histo-plot-graph'),
                        ],
                        className="pretty_container eight columns",
                    ),
                ], ),

            # Section for the informations about the polluants
            html.Div(
                [
                    html.H6("Informations sur les polluants",
                            style={
                                "margin-top": "0",
                                "font-weight": "bold",
                                "text-align": "center"
                            }),
                    html.P("Particules en suspension PM10 :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Les poussières se distinguent entre elles par leur taille. Les poussières dites "respirables" sont celles qui ont un diamètre aérodynamique moyen inférieur à 10 µm. On les appelle PM10. Leur taille est suffisamment faible pour rentrer dans les poumons.\n
                    Seuil d'information et de recommandation :
                    - 50 µg/m3 en moyenne journalière\n
                    Seuil d’alerte :
                    - 80 µg/m3 en moyenne journalière\n
                    Valeur limite : 
                    - 40 µg/m3 en moyenne annuelle\n
                    Objectif de qualité : 
                    - 30 µg/m3 en moyenne annuelle
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Monoxyde d’azote (NO) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Le monoxyde d’azote (NO) anthropique est formé lors des combustions à haute température (moteurs thermiques ou chaudières). Inhalé à des concentrations de 30 à 100 mg par m³ d'air, le NO provoque une vasodilatation et abaisse la pression artérielle pulmonaire.\n
                    Seuil d'information et de recommandation :
                    - 200 µg/m3 en moyenne horaire\n
                    Seuil d'alerte : 
                    - 400 µg/m3 en moyenne horaire\n
                    Objectif de qualité : 
                    - 40 µg/m3 en moyenne annuelle
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Dioxyde d'azote (NO2) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Le NO2 est un gaz irritant qui pénètre dans les plus fines ramifications des voies respiratoires. Il peut, dès 200 μg/m3, entraîner une altération de la fonction respiratoire, une hyper-réactivité bronchique chez l'asthmatique et un accroissement de la sensibilité des bronches aux infections chez l'enfant.\n
                    Seuil d'information et de recommandation :
                    - 200 µg/m3 pour la valeur moyenne sur 1 heure et 40 µg/m3 pour une moyenne annuelle\n
                    Seuil d’alerte :
                    - 400 µg/m3 pour la valeur horaire sur 3 heures consécutives
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Ozone (O3) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    L'ozone, polluant secondaire, résulte généralement de la transformation photochimique de certains polluants dans l'atmosphère (en particulier NOx et COV) sous l'effet des rayonnements ultra-violets. L'ozone pénètre facilement jusqu'aux voies respiratoires les plus fines. Il provoque de la toux et une altération, surtout chez les enfants et les asthmatiques ainsi que des irritations oculaires. Les effets sont amplifiés par l'exercice physique.\n
                    Seuil d'information et de recommandation :
                    - 50 µg/m3 en moyenne journalière et 180 µg/m3 en moyenne par heure\n
                    Seuil d’alerte :
                    - 360 µg/m3 en moyenne horaire (au seuil 3) ou 240 µg/m3 en moyenne par heure pendant 3 heures consécutives (seuil 1)\n
                    Valeur cible (protection de la santé) :
                    - 120 µg/m3 en moyenne sur 8 heures sur 3 ans à ne pas dépasser plus de 25 fois
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Oxydes d’azote (NOx) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Les Oxydes d’Azote sont simplement l’addition du NO et du NO2.
                    Valeur limite (seuil critique) :
                    - 30 µg/m3 en moyenne annuelle (protection de la végétation)\n
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Particules fines en suspension PM2,5 :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Les particules fines (< 2,5 µm, appelées PM2,5) sont principalement émises par les véhicules diesel. La taille de ces poussières leur permet de pénétrer dans les alvéoles pulmonaires et donc d'interagir fortement avec le corps humain.\n
                    Seuil d'information et de recommandation :
                    - 10 µg/m3 en moyenne annuelle\n
                    Seuil d’alerte :
                    - 25 µg/m3 en moyenne annuelle\n
                    Valeur cible :
                    - 20 µg/m3 en moyenne annuelle
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Composé organique volatil (Benzène : C6H6) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    C’est un hydrocarbure aromatique monocyclique provenant de la combustion incomplète de composés riches en carbone. Ses sources d’émission sont les processus de combustion (dont le tabagisme), le transport routier, et les activités industrielles. Les effets sont très divers : ils vont de la simple gêne olfactive à une irritation (aldéhydes), une diminution de la capacité respiratoire, jusqu'à des effets mutagènes et cancérigènes.\n
                    Valeurs limites :
                    - 5 µg/m3 en moyenne annuelle\n
                    Objectifs de qualité :
                    - 2 µg/m3 en moyenne annuelle
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Dioxyde de soufre (SO2) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Ce gaz résulte essentiellement de la combustion de matières fossiles contenant du soufre (charbon, fuel, gazole...) et de procédés industriels. C'est un gaz irritant qui agit en synergie avec d'autres substances notamment les particules en suspension. Il est associé à une altération de la fonction pulmonaire chez l'enfant et à une exacerbation des symptômes respiratoires aigus chez l'adulte (toux, gêne respiratoire). Les personnes asthmatiques y sont particulièrement sensibles.\n
                    Seuil d'information et de recommandation :
                    - 300 µg/m3 pour la valeur moyenne sur 1 heure\n
                    Seuil d’alerte :
                    - 500 µg/m3 pour la valeur horaire sur 3 heures consécutives\n
                    Valeur limite : 
                    - 20 µg/m3 pour la moyenne annuelle (protection des écosystèmes)\n
                    Objectif de qualité : 
                    - 50 µg/m3 pour la moyenne annuelle
                    """,
                                 style={"font-size": "10pt"}),
                    html.P("Monoxyde de carbone (CO) :", style={"font-weight": "bold",}),
                    dcc.Markdown("""\
                    Il provient de la combustion incomplète des combustibles et carburants. Il se fixe à la place de l'oxygène sur l'hémoglobine du sang conduisant à un manque d'oxygénation du système nerveux, du cœur, des vaisseaux sanguins. Le système nerveux central et les organes sensoriels sont les premiers affectés (céphalées, asthénies, vertiges, troubles sensoriels). Il peut engendrer l'apparition de troubles cardio-vasculaires.\n
                    Valeur limite :
                    -10 000 µg/m3 pour le maximum journalier de la moyenne glissante sur 8 heures
                    """,
                                 style={"font-size": "10pt"}),
                ],
                className="pretty_container twelwe columns",
            ),
            
            # Section for the posibles upgrades
            html.Div(
                [
                    html.H6("Améliorations possibles",
                            style={
                                "margin-top": "0",
                                "font-weight": "bold",
                                "text-align": "center"
                            }),
                    dcc.Markdown("""\
                        Jusque là, nous avons utilisé les données de l'année 2021 récupérées en temps réel et mises à disposition par le gouvernement français. 
                        Nous pourrions donc utiliser les données de début 2022 mais aussi celles des années précédentes afin de compléter les données et pouvoir couvrir une plus grande période.\n
                        De plus, pour les données de la carte de France, au lieu de faire une moyenne journalière, nous pourrions les conserver à l'état de moyenne horaire.
                        Pour l'affichage, nous pourrions ajouter un slider changeant automatiquement de valeur et parcourant ainsi les 24 heures de la 
                        date sélectionnées pour mieux montrer l'évolution du polluant au fil des heures.
                        """,
                                 style={"font-size": "10pt", "text-align": "center"}),
                ],
                className="pretty_container twelwe columns",
            ),

            # Section for the authors
            html.Div(
                [
                    html.H6("Authors",
                            style={
                                "margin-top": "0",
                                "font-weight": "bold",
                                "text-align": "center"
                            }),
                    html.
                    P("Noé Jenn-Treyer (noe.jenn-treyer@epita.fr)  et  Jules Dorbeau (jules.dorbeau@epita.fr)  - EPITA, SCIA 2023, Groupe A",
                      style={
                          "text-align": "center",
                          "font-size": "10pt"
                      }),
                ],
                className="pretty_container twelwe columns",
            ),
            
            # Section for the sources
            html.Div(
                [
                    html.H6("Sources",
                            style={
                                "margin-top": "0",
                                "font-weight": "bold",
                                "text-align": "center"
                            }),
                    dcc.Markdown("""\
                         - Site data polluants : https://ec.europa.eu/eurostat/databrowser/view/HLTH_SHA11_HF__custom_227597/bookmark/table?lang=en&bookmarkId=1530a1e6-767e-4661-9e15-0ed2f7fae0d5
                         - Lien exemple dash pour la pagination : http://www.fao.org/faostat/en/#data/FBS
                         - Lien github pour le css : https://data.opendatasoft.com/explore/dataset/european-union-countries@public/export/
                        """,
                                 style={"font-size": "10pt"}),
                ],
                className="pretty_container twelwe columns",
            ),
        ])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Callback used to update the multiple lines plot graph
        self.app.callback(
            Output(component_id='multi-lines-plot-graph',
                   component_property='figure'), [
                       Input(component_id='slider-date-plot-line',
                             component_property='value'),
                       Input(component_id='radio-selection-region-plot-lines',
                             component_property='value')
                   ])(self.update_plot_lines)

        # Callback used to update the map of France
        self.app.callback(
            Output(component_id='map-plot-graph', component_property='figure'),
            [
                Input(component_id='single-date-picker-map',
                      component_property='date'),
                Input(component_id='radio-selection-polluant-map',
                      component_property='value')
            ])(self.update_map)

        # Callback used to update the histogram of influences
        self.app.callback(
            Output(component_id='histo-plot-graph',
                   component_property='figure'), [
                       Input(component_id='slider-date-histo',
                             component_property='value'),
                       Input(component_id='drop-polluant-histo',
                             component_property='value'),
                       Input(component_id='drop-region-histo',
                             component_property='value')
                   ])(self.update_histo)

    # Function used to update the multiple lines plot graph
    def update_plot_lines(self, month, region):
        month = self.slider_dict.get(month)
        df_plot = self.line_plot_data.copy()
        df_plot = df_plot[(df_plot["Region"] == region)
                          & (df_plot.index.str.contains(month))]
        if (df_plot.empty):
            return px.line(df_plot)
        # Getting the list of the uniques polluants
        polluants_uniques = df_plot["Polluant"].unique()

        # Dropping the non numeric columns
        df_plot = df_plot.drop(columns=["Region", "Mesure"])
        df_plot.index = pd.to_datetime(df_plot.index)

        plot_df = pd.DataFrame()
        plot_df["Date"] = df_plot.index.unique()
        plot_df = plot_df.set_index("Date")

        for pol in polluants_uniques:
            # Changing the name of the columns to display the value with the polluant
            col_name = pol + " - " + self.dict_mesures_polluants.get(pol)
            plot_df[col_name] = df_plot[df_plot["Polluant"] == pol].drop(
                columns=["Polluant"])
        # Get the names of the columns that we want to display
        col_display = plot_df.columns
        # Create our figure
        fig = px.line(plot_df,
                      x=plot_df.index,
                      y=col_display,
                      title="Taux des polluants dans l'atmosphère en " +
                      region + " durant le " + month)
        return fig

    def update_map(self, date, polluant):
        df_diplay = self.map_data.copy()
        df_diplay = df_diplay[df_diplay["Polluant"] == polluant].loc[date]
        # Create and display our figure
        fig = px.choropleth_mapbox(
            df_diplay,
            geojson=self.regions_map,
            locations='Region',
            featureidkey='properties.nom',  # join keys
            color='Valeur',
            color_continuous_scale="Viridis",
            mapbox_style="carto-positron",
            zoom=4.6,
            center={
                "lat": 46.5,
                "lon": 2
            },
            opacity=0.5,
            labels={'valeur': 'Valeur du polluant'})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def update_histo(self, month, polluant, region):
        date = self.slider_dict.get(month)
        df_histo = self.data_histo.copy()
        influences_df = df_histo[(df_histo["Region"] == region)
                                 & (df_histo["Polluant"] == polluant)
                                 & (df_histo["Date"] == (date + "-01"))]

        histo_dict = {
            'Influences': ['Industrielle', 'Fond', 'Trafic'],
            'Values': [
                influences_df['Industrielle'].values[0],
                influences_df['Fond'].values[0],
                influences_df['Trafic'].values[0]
            ]
        }
        fig = px.bar(histo_dict,
                     x="Influences",
                     y="Values",
                     title="Répartition des influences de " + polluant +
                     " dans la région " + region + " le " + date + ".",
                     color="Values")
        return fig


# Calling our function
if __name__ == '__main__':
    polFr = PollutionFrancaise()
    polFr.app.run_server(port=8051)
