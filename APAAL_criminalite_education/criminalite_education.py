import dash
from dash import dcc
from dash import html
import pickle


class Criminalite_Education:
    def __init__(self, application=None):

        # Education

        with open('APAAL_criminalite_education/data/fig_education.pickle', 'rb') as handle:
            fig_education = pickle.load(handle)

        # Crimes

        with open('APAAL_criminalite_education/data/fig_crimes.pickle', 'rb') as handle:
            fig_crimes = pickle.load(handle)

        self.main_layout = html.Div(
            children=[
                html.H3(
                    children="Analyse de l'éducation et de la criminalité à Chicago"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="edu-main-graph",
                            figure=fig_education,
                            style={"width": "54%", "display": "inline-block"},
                        ),
                        dcc.Graph(
                            id="crim-main-graph",
                            figure=fig_crimes,
                            style={"width": "45%", "display": "inline-block"},
                        ),
                    ]
                ),
                html.Br(),
                dcc.Markdown(
                    """
            Nous avons souhaité nous intéresser au lien entre éducation et criminalité. Pour cela, nous nous sommes penchés sur le cas de Chicago.
                
            La carte de gauche met en relation le taux de suspension des élèves de la primaire au lycée, par quartier, durant l'année scolaire 2015-2016.
            La carte de droite met en relation le nombre de crimes par quartier au cours des années 2015 et 2016.

            On constate une relation entre les 2 cartes obtenues. Dans l'extrême nord de la ville, on remarque que les crimes et suspensions sont faibles.
            En revanche, dans le sud de la ville les crimes et suspensions augmentent et sont répartis similairement selon les quartiers. 
            Les deux indicateurs sont particulièrement hauts dans le centre géographique de la ville.
            Enfin, on peut supposer que le taux très élevé de suspensions dans le quartier numéro 3 est une aberration (valeur qui sort anormalement du lot).

            En ce qui concerne les crimes, la base de donnée est très lourde : 7 531 858 lignes (1,7go). Il était impossible de la lire en une seule fois. 
            En la lisant seulement avec un **read_csv** classique, le noyau meurt systématiquement. En utilisant des **chunks**, la RAM de l'ordinateur meurt également.
            Nous avons finalement effectué la lecture en 2 étapes afin de lire seulement les dates puis le reste des colonnes pour les dates intéressantes.
            Pour plus d'informations voir le [notebook get-data-crimes.ipynb](https://github.com/Adrien-ANTON-LUDWIG/delta/blob/main/APAAL_criminalite_education/get-data-crime.ipynb).

            Concernant les données sur l'éducation, nous avions prévu plusieurs datasets (un par année scolaire) afin d'étudier l'évolution sur plusieurs années.
            Malheureusement, nous avons été limités par les ressources nécessaires pour traiter le fichier des crimes.
            Nous nous sommes donc limités aussi à l'année scolaire 2015-2016 pour les données d'éducation.
            
            Enfin, les deux datasets ne reposaient pas sur le même découpage géographique de la ville.
            Pour remédier à ce problème, nous avons utilisé les coordonnées GPS des écoles et les données géographiques (fichier .geojson) des quartiers pour les relier.
            Pour plus d'informations voir le [notebook get-data-education.ipynb](https://github.com/Adrien-ANTON-LUDWIG/delta/blob/main/APAAL_criminalite_education/get-data-education.ipynb).

            #### À propos

            * Sources : https://data.cityofchicago.org
            * (c) 2022 Adèle PLUQUET & Adrien ANTON LUDWIG
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
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == "__main__":
    crim_edu = Criminalite_Education()
    crim_edu.app.run_server(debug=True, port=8051)
