import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from .get_data import *
import json


class Pollution():
    def __init__(self, application=None):
        # Retrieving the date needed
        self.pollution_eu = get_transport_pollution_eu()
        self.pollution_vehicules_eu = get_pollution_per_vehicules_eu()
        self.pollution_vehicules_france = get_pollution_per_vehicules_in_france()
        self.pollution_schools_idf = get_air_pollution_schools()

        # complementary data needed for the graphs
        self.years_school = [x for x in range(2012, 2018)]
        self.years = [x for x in range(1990, 2020)]
        self.countries = [
            "Allemagne",
            "Autriche",
            "Belgique",
            "Bulgarie",
            "Chypre",
            "Croatie",
            "Danemark",
            "Espagne",
            "Estonie",
            "Finlande",
            "France",
            "Grèce",
            "Hongrie",
            "Irlande",
            "Islande",
            "Italie",
            "Lettonie",
            "Lituanie",
            "Luxembourg",
            "Malte",
            "Norvège",
            "Pays-Bas",
            "Pologne",
            "Portugal",
            "Roumanie",
            "Royaume-Uni",
            "République Tchèque",
            "Slovaquie",
            "Slovénie",
            "Suède",
        ]

        self.main_layout = html.Div(
            children=[
                html.H1(children="Pollution des Transports à différentes échelles", style={
                        "color": "darkred", "text-decoration": "underline"}),
                html.H2(
                    children="1. Étude de la pollution des transports en Europe"),
                html.H4(
                    children="Pollution des Transports en Europe de 1990 à 2020"),
                html.Div(
                    [
                        dcc.Graph(id="pol-main-europe-graph"),
                    ],
                    style={"width": "100%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Type de Pollution", style={
                                         "font-weight": "bold"}),
                                dcc.RadioItems(
                                    id="pol-europe-type",
                                    options=[
                                        {"label": "Oxyde d'azote", "value": "NOX"},
                                        {
                                            "label": "Composés organiques volatils autre que le méthane",
                                            "value": "NMVOC",
                                        },
                                        {
                                            "label": "Particules < 10 nanomètres",
                                            "value": "PM10",
                                        },
                                    ],
                                    value="NOX",
                                    labelStyle={"display": "block"},
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Button(
                            "Start",
                            id="pol-button-start-stop",
                            style={"display": "inline-block"},
                        ),
                        html.Div(),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            dcc.Slider(
                                id="pol-europe-year-slider",
                                min=1990,
                                max=2020,
                                step=1,
                                value=1990,
                                marks={
                                    str(year): str(year) for year in self.years[::2]
                                },
                            ),
                            style={"display": "inline-block", "width": "90%"},
                        ),
                        dcc.Interval(  # fire a callback periodically
                            id="pol-auto-stepper",
                            interval=1500,  # in milliseconds
                            max_intervals=-1,  # start running
                            n_intervals=0,
                        ),
                    ],
                    style={"padding": "0px 50px", "width": "100%"},
                ),
                dcc.Markdown(
                    """
                    Cette carte est intéractive. Pour visualiser la pollution d'une
                    certaine temporalité appuyez sur le button stop et glissez le curseur
                    le long de l'axe pour changer l'année observée.
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """
                    Cette carte nous permet d'observer les différents niveaux de
                    pollution par pays entre 1990 et 2020. Ces pourcentages étant calculés
                    par rapport aux données de l'année 2000, cela nous permet de savoir si
                    les émissions des différents gaz polluants, à une année choisie, sont
                    considérablement différentes par rapport à l'année de référence. On 
                    peut par exemple observer que la Lettonie rejette énormément d'oxyde
                    d'azote et de composés organiques volatils autre que le méthane. Dans
                    l'Europe de l'Est, on voit qu'à partir de 2006 la pollution en
                    particules augmente beaucoup. En revanche la pollution en composés 
                    organiques autre que le méthane a beaucoup diminué sur toute la temporalité
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """
                    Maintenant qu'on a observé la pollution des transports en général et
                    autre que le C02, nous allons nous concentrer sur les véhicules neufs
                    afin d'estimer quel pays contribue le plus à la pollution en CO2 en
                    Europe.
                    """, style={'text-align': 'justify'}
                ),
                html.Br(),
                html.H4(
                    children="Émission de CO2 des véhicules neufs entre 2000 et 2020 en Europe"
                ),
                html.Div([dcc.Graph(id="pol-europe-cars-graph")]),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Choix de visualisation",
                                         style={"font-weight": "bold"}),
                                dcc.RadioItems(
                                    id="pol-all-europe-choice",
                                    options=[
                                        {
                                            "label": "Un pays par rapport à toute l'Europe",
                                            "value": "mean",
                                        },
                                        {
                                            "label": "Tous les pays",
                                            "value": "all_countries",
                                        },
                                    ],
                                    value="all_countries",
                                    labelStyle={"display": "block"},
                                ),
                            ],
                            style={"width": "20em"},
                        ),
                        html.Div(
                            [
                                html.Div("Pays", style={
                                         "font-weight": "bold"}),
                                dcc.Dropdown(
                                    id="pol-which-country",
                                    options=[
                                        {"label": i, "value": i} for i in self.countries
                                    ],
                                    value="France",
                                    disabled=True,
                                ),
                            ],
                            style={"width": "15em",
                                   "padding": "2em 0px 0px 0px"},
                        ),
                        html.Div(style={"width": "2em"}),
                    ],
                    style={
                        "padding": "25px 60px",
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "flex-start",
                    },
                ),
                dcc.Markdown(
                    """Avec cette représentation il est possible de comparer un seul pays
                    avec la moyenne de la consommation de toute l'Europe en choisissant
                    le pays souhaité avec le menu déroulant.
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """La Suède émettait énormément de CO2 dans les années 2000 et s'est
                    ensuite réduit pour faire parti des pays les moins polluant d'Europes.
                    Les Pays-Bas reste majoritèrement ceux qui sont les moins pollueurs
                    parmis tout les pays d'Europe. La France quant à elle reste toujours
                    très en dessous de la moyenne européene et est plutôt stable dans le
                    temps.
                    Mais comparer aux Pays-Bas sur les dernières années la France reste
                    plus pollueuse.
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """
                    Dans la suite nous allons nous concentrer sur la France pour voir
                    comment elle contribue à la pollution européenne, et après voir quel
                    impact cela a sur la vie des français et plus particulièrement sur
                    les écoles et crèches de l'Île-de-France.                    
                    """, style={'text-align': 'justify'}
                ),
                html.Br(),
                html.H2(
                    children="2. Étude de la pollution des transports en France"),
                html.H4(
                    children="Éjection de différents gaz en fonction de la marque en France en 2015"
                ),
                html.Div(
                    [
                        dcc.Graph(id="pol-main-graph"),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Type de gaz", style={
                                         "font-weight": "bold"}),
                                dcc.RadioItems(
                                    id="pol-type-gaz",
                                    options=[
                                        {"label": "Oxyde d'azote", "value": "NOx"},
                                        {
                                            "label": "Hydrocarbure et Oxyde d'azote",
                                            "value": "HC et NOx",
                                        },
                                        {"label": "Hydrocarbure", "value": "HC"},
                                        {
                                            "label": "Particules fine",
                                            "value": "Particules",
                                        },
                                        {"label": "CO2", "value": "CO2"},
                                        {"label": "CO type1", "value": "CO type1"},
                                    ],
                                    value="NOx",
                                    labelStyle={"display": "block"},
                                    #'Hybride', 'Carburant',
                                ),
                            ],
                            style={"width": "16em"},
                        ),
                        html.Div(
                            [
                                html.Div("Catégorie", style={
                                         "font-weight": "bold"}),
                                dcc.RadioItems(
                                    id="pol-choice",
                                    options=[
                                        {"label": "Marque", "value": "Marque"},
                                        {
                                            "label": "Hybride",
                                            "value": "Hybride",
                                        },
                                        {"label": "Carburant",
                                            "value": "Carburant"},
                                    ],
                                    value="Marque",
                                    labelStyle={"display": "block"},
                                ),
                            ],
                            style={"width": "9em",
                                   "padding": "0px 0px 0px 10em"},
                        ),
                    ],
                    style={
                        "padding": "10px 50px",
                        "display": "flex",
                        "flexDirection": "row",
                        "justifyContent": "flex-start",
                    },
                ),
                dcc.Markdown(
                    """
                    Le graphique représente la moyenne des émissions des véhicules
                    circulant en France selon les informations données par les
                    constructeurs. Sur celui-ci, il est posssible de trier les données
                    en fonction des différentes émissions des véhicules ainsi que de
                    leur types ou de leur marques.
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """
                    Pour certaines émissions, il manque des valeurs leurs donnant la
                    moyenne de 0. Cela peut aussi venir de leur non émission avec les
                    voitures électriques par example. Ces valeurs sont donc mise tout
                    à la fin pour informer le lecteur d'un potentiel problème.
                    """, style={'text-align': 'justify'}
                ),
                html.Br(),
                html.H4(
                    children="Pollution aérienne des écoles et crêches en Île de France entre 2012 et 2017"
                ),
                html.Div([dcc.Graph(id="pol-school-graph")]),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Type de Pollution", style={
                                         "font-weight": "bold"}),
                                dcc.RadioItems(
                                    id="pol-idf-type",
                                    options=[
                                        {"label": "Particules < 10 nanomètres",
                                            "value": "PM10"},
                                        {"label": "Particules < 2.5 nanomètres",
                                            "value": "PM25"},
                                        {"label": "Dioxyde d'azote", "value": "NO2"},
                                    ],
                                    value="NO2",
                                    labelStyle={"display": "block"},
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Button(
                            "Start",
                            id="pol-idf-button-start-stop",
                            style={"display": "inline-block"},
                        ),
                        html.Div(),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            dcc.Slider(
                                id="pol-idf-year-slider",
                                min=2012,
                                max=2017,
                                step=1,
                                value=2012,
                                marks={
                                    str(year): str(year) for year in self.years_school
                                },
                            ),
                            style={"display": "inline-block", "width": "90%"},
                        ),
                        dcc.Interval(  # fire a callback periodically
                            id="pol-idf-auto-stepper",
                            interval=1500,  # in milliseconds
                            max_intervals=-1,  # start running
                            n_intervals=0,
                        ),
                    ],
                    style={"padding": "0px 50px", "width": "100%"},
                ),
                dcc.Markdown(
                    """
                    La carte permet de visualiser la pollution aérienne au abords de chaque école. Il 
                    est possible de choisir le type de pollution et de suivre son évolution au fil des ans.
                    """, style={'text-align': 'justify'}
                ),

                dcc.Markdown(
                    """
                    Cette représentation prend comme valeur centrale l'objectif de qualité donné par l'OMS
                    ce qui explique pourquoi certaines échelles vont en dessous de 0 lorsque
                    les valeurs maximales deviennent trop élevées.
                    """, style={'text-align': 'justify'}
                ),
                dcc.Markdown(
                    """
                    On observe que la pollution est très élevée dans beaucoup des écoles et crèches
                    près du centre de Paris. On peut aussi noter que l'objectif de qualité de l'air
                    n'est pas atteint pour beaucoup d'établissements surtout pour les particules de moins
                    de 2.5 nanomètres.
                    """, style={'text-align': 'justify'}
                ),
                html.Br(),
                html.H2(children="À propos"),
                dcc.Markdown(
                    """
                    * Sources :
                        * [Emissions de polluants des transports en Europe](https://ec.europa.eu/eurostat/databrowser/view/t2020_rk300/default/table?lang=fr)
                        * [Emissions de CO2 et de polluants des véhicules commercialisés en France] (https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/)
                        * [Base de données de la pollution aérienne aux abords des écoles et crèches d’Île-de-France] (https://www.data.gouv.fr/fr/datasets/base-de-donnees-de-la-pollution-aerienne-aux-abords-des-ecoles-et-creches-dile-de-france/)
                        * [Moyenne des émissions de CO2 par kilomètre provenant de véhicules particuliers neufs (source: AEE, DG CLIMA)] (https://ec.europa.eu/eurostat/databrowser/view/sdg_12_30/default/table?lang=fr)
                        * [Norme de Qualité de l'air] (https://www.ecologie.gouv.fr/sites/default/files/01_Tableau-Normes-Seuils%20r%C3%A9glementaires.pdf)
                    * (c) 2022 Sarah Gutierez et Adrien Houpert
                        """
                ),
            ],
            style={
                "backgroundColor": "white",
                "padding": "10px 50px 10px 50px",
            },
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # European Pollution graph
        self.app.callback(
            dash.dependencies.Output("pol-main-europe-graph", "figure"),
            [
                dash.dependencies.Input("pol-europe-type", "value"),
                dash.dependencies.Input("pol-europe-year-slider", "value"),
            ],
        )(self.update_graph_poll_eu)

        # Button start/stop for europe map
        self.app.callback(
            dash.dependencies.Output("pol-button-start-stop", "children"),
            dash.dependencies.Input("pol-button-start-stop", "n_clicks"),
            dash.dependencies.State("pol-button-start-stop", "children"),
        )(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output("pol-auto-stepper", "max_interval"),
            [dash.dependencies.Input("pol-button-start-stop", "children")],
        )(self.run_time)
        self.app.callback(
            dash.dependencies.Output("pol-europe-year-slider", "value"),
            dash.dependencies.Input("pol-auto-stepper", "n_intervals"),
            [
                dash.dependencies.State("pol-europe-year-slider", "value"),
                dash.dependencies.State("pol-button-start-stop", "children"),
            ],
        )(self.on_interval)

        self.app.callback(
            dash.dependencies.Output("pol-idf-button-start-stop", "children"),
            dash.dependencies.Input("pol-idf-button-start-stop", "n_clicks"),
            dash.dependencies.State("pol-idf-button-start-stop", "children"),
        )(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output("pol-idf-auto-stepper", "max_interval"),
            [dash.dependencies.Input("pol-idf-button-start-stop", "children")],
        )(self.run_time)
        self.app.callback(
            dash.dependencies.Output("pol-idf-year-slider", "value"),
            dash.dependencies.Input("pol-idf-auto-stepper", "n_intervals"),
            [
                dash.dependencies.State("pol-idf-year-slider", "value"),
                dash.dependencies.State(
                    "pol-idf-button-start-stop", "children"),
            ],
        )(self.on_interval_idf)

        # Callbacks for vehicules in EU
        self.app.callback(
            dash.dependencies.Output("pol-europe-cars-graph", "figure"),
            [
                dash.dependencies.Input("pol-all-europe-choice", "value"),
                dash.dependencies.Input("pol-which-country", "value"),
            ],
        )(self.update_graph_europe_vehicules)

        self.app.callback(
            [
                dash.dependencies.Output("pol-which-country", "disabled"),
            ],
            dash.dependencies.Input("pol-all-europe-choice", "value"),
        )(self.disable_choice_country)

        # Callbacks for vehicules graph in France
        self.app.callback(
            dash.dependencies.Output("pol-main-graph", "figure"),
            [
                dash.dependencies.Input("pol-type-gaz", "value"),
                dash.dependencies.Input("pol-choice", "value"),
            ],
        )(self.update_graph_vehicules)

        # Callbacks for schools graph of France
        self.app.callback(
            dash.dependencies.Output("pol-school-graph", "figure"),
            [
                dash.dependencies.Input("pol-idf-year-slider", "value"),
                dash.dependencies.Input("pol-idf-type", "value"),
            ],
        )(self.update_graph_schools)

    # Update function for the study of Europe vehicules
    def update_graph_europe_vehicules(self, all_europe="all_countries", country="France"):
        df, mean_eu = self.pollution_vehicules_eu

        if all_europe == "mean":
            df = df.loc[df["Pays"] == country]
            # For all Europe we have data starting at 2007
            min_year = 2007

            # BUT for certain countries the analysis starts later
            if df["Année"].min() > 2007:
                min_year = df["Année"].min()
                mean_eu = mean_eu.loc[mean_eu["Année"] >= min_year]

            mean_eu = pd.concat(
                [mean_eu, df.loc[df["Année"] >= min_year]], ignore_index=True
            )
            fig = px.line(
                mean_eu,
                x="Année",
                y="Taux de pollution",
                color="Pays",
                title=f"Comparaison entre la moyenne des émissions de CO2 pour toute l'Europe et en {country}",
            )
            return fig

        return px.line(
            df,
            x="Année",
            y="Taux de pollution",
            color="Pays",
            title="Moyenne des émissions de CO2 pour chacun des pays d'Europe",
            labels={"Taux de pollution": f"Taux de Pollution en g/km"},
        )

    # Update function for the study of France vehicules
    def update_graph_vehicules(self, name, axis):
        col = f"Emission {name}"
        agg = (
            self.pollution_vehicules_france.copy()[[axis, col]]
            .groupby([axis])
            .mean()
            .reset_index()
            .sort_values(by=[col, axis])
            # .replace(np.NaN,0)
        )

        title = f"par {axis.lower()}" if axis != 'Hybride' else f"{axis.lower()}"
        fig = px.bar(
            agg,
            y=col,
            x=axis,
            title=f"Moyenne d'{col} pour les modèles {title}",
            color_discrete_sequence=["purple"] * len(agg),
        )
        fig.update_traces(
            textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
        )
        return fig

    # Update function for the European map of pollution
    def update_graph_poll_eu(self, name="NMVOC", year=1990):
        dfg = self.pollution_eu
        dfg = dfg.loc[dfg["Type de pollution"] == name]
        dfg = dfg.loc[dfg["Année"] == year]

        countries = json.load(
            open("SG_AH_pollution_des_transports/data/europe_geoson.json")
        )

        fig = px.choropleth_mapbox(
            dfg,
            geojson=countries,
            locations="Pays",
            featureidkey="properties.name",  # join keys
            color="Taux de pollution",
            color_continuous_scale="jet",
            mapbox_style="carto-positron",
            zoom=2.5,
            center={"lat": 53, "lon": 3},
            opacity=0.7,
            labels={"Taux de pollution": f"Poucentage de pollution de {name}"},
            range_color=[50, 300],
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def update_graph_schools(self, year=2012, name_seuil="PM25"):
        dfg = self.pollution_schools_idf
        col = f"{name_seuil}_{year}"
        title = "mg/m3 de " + name_seuil
        dfg = dfg.rename(columns={col: title})
        num = 40 if name_seuil == "NO2" else 30 if name_seuil == "PM10" else 10
        fig = px.scatter_mapbox(
            dfg,
            lat=dfg.lat,
            lon=dfg.lon,
            hover_name="nom",
            color=title,
            color_continuous_scale=px.colors.cyclical.IceFire,
            size=title,
            size_max=15,
            color_continuous_midpoint=num,
        )
        fig.update_layout(mapbox_style="stamen-terrain")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    # start and stop the time
    def button_on_click(self, n_clicks, text):
        if text == "Start":
            return "Stop"
        else:
            return "Start"

    def run_time(self, text):
        if text == "Start":
            return 0
        else:
            return -1

    # intervals for years
    def on_interval(self, n_intervals, year, text):
        if text == "Stop":  # we run
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year

    def on_interval_idf(self, n_intervals, year, text):
        if text == "Stop":  # we run
            if year == self.years_school[-1]:
                return self.years_school[0]
            else:
                return year + 1
        else:
            return year

    # Enables of disables the poll for countries
    def disable_choice_country(self, info):
        return (info != "mean",)


if __name__ == "__main__":
    pol = Pollution()
    pol.app.run_server(debug=True, port=8051)
