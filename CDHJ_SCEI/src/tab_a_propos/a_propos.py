import dash_bootstrap_components as dbc
import dash


class Tab_a_propos:
    def __init__(self, dash_app):
        self.app = dash_app

        # ---------------------------------------------------------------------------- #
        #                                COPYRIGHT CARD                                #
        # ---------------------------------------------------------------------------- #
        card_1_content = [
            dash.html.H5("Auteurs", className="card-title"),
            dash.dcc.Markdown(
                """Cette présentation dynamique des statistiques d'intégration des Grandes Ecoles a été réalisée dans le cadre du cours **Python pour le Big Data** d'**Olivier RICOU** à l'**Epita** en **2022** par :
                        
                            > - Henri JAMET : <henri.jamet@epita.fr>
                            > - Corentin DUCHÊNE : <corentin.duchene@epita.fr>
                            """,
                className="card-text",
            ),
        ]

        # ---------------------------------------------------------------------------- #
        #                                 SOURCES CARD                                 #
        # ---------------------------------------------------------------------------- #
        card_2_content = [
            dash.html.H5("Source de données", className="card-title"),
            dash.dcc.Markdown(
                "Les données utilisées proviennent majoritairement du site **SCEI** responsable de l'inscription aux concours des Grandes Ecoles (https://www.scei-concours.fr/statistiques.php)."
            ),
            dash.dcc.Markdown(
                """Les données *géographiques* proviennent quant à elles des bibliothèques et bases de données suivantes:
                        
                        > - Folium (https://python-visualization.github.io/folium/)
                        > - MapBox (https://account.mapbox.com/auth/signup/)
                        > - GeoCode ("https://api-adresse.data.gouv.fr/search/")
                        > - OpenStreetMap (https://www.openstreetmap.org/copyright)""",
                className="card-text",
            ),
        ]

        # ---------------------------------------------------------------------------- #
        #                                DISCLAIMER CARD                               #
        # ---------------------------------------------------------------------------- #
        card_3_content = [
            dash.html.H5("Données manquantes et aberrantes", className="card-title"),
            dash.dcc.Markdown(
                "> *Les données récupérées sur **SCEI** se sont révélées considérablement lacunaires et parfois vraisemblablement absurdes. Si nous avons tenté au maximum de supprimer les données aberrantes, notre filtrage est victime d'un biais subjectif selon ce que nous avons considéré comme vraisemblable. Par ailleurs, l'absence de données pour certains établissements ou certaines années a également pu amener à une représentation biaisée des données.*"
            ),
            dash.html.H5(
                "Choix des données affichées et de leur type de représentation",
                className="card-title",
            ),
            dash.dcc.Markdown(
                "> *Si nous avons fait de notre mieux pour ne porter aucun jugement sur les données que nous avons étudié, le choix des graphes et des statistiques utilisées est porteur d'une certaine subjectivité. L'utilisation de toutes les données que nous avions à disposition n'étant pas toujours pertinente, il convient également de rappeler que les données affichées ici ne sont qu'un extrait des données originales choisi arbitrairement.*"
            ),
        ]

        self.layout = dash.html.Div(
            [
                dash.html.Div(children=card_1_content),
                dash.html.Div(children=card_2_content),
                dash.html.Div(children=card_3_content),
            ],
        )
