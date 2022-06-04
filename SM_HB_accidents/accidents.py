import pandas as pd
import os
import dash
from dash import html, Dash, dependencies, dcc
import glob
import plotly.express as px

class Accidents():
    def __init__(self, application = None):
        df_final_test = pd.read_csv("SM_HB_accidents/data/final_df.csv").astype('int64')
        self.df = df_final_test
        # Traitement affichage

        self.categories = {
                "Catégorie de route" : "catr",
                "Déclivité de la route" : "prof",
                "Surface de la route" : "surf",
                "Type de collision" : "col",
                "Conditions atmosphériques" : "atm",
                "Type d'intersection de la voie" : "int",
                "Conditions d'éclairage de la route" : "lum",
                "Tracé de la route" : "plan" }

        #Dash integration

        self.main_layout = html.Div([
            html.H3(children=['Contextualisation des accidents de la route']),
            html.Div([dcc.Graph(id='accidents-main-graph')], style={'width':'100%'}),
            html.Div([
                dcc.RadioItems(id='line-to-histo',
                    options= [
                        {'label' : "Histogramme", 'value':1},
                        {'label' : "Lignes", 'value':0} ],
                    value=1,
                    style={'display':'inline-block', 'width':'50%'}),
                dcc.Dropdown(id='cat-changer',
                    options = list(self.categories),
                    value="Catégorie de route",
                    searchable = False,
                    style={'display':'inline-block', 'width': '50%'})
                ]),
            html.Br(),
            dcc.Markdown("""
            Le graphe ci-dessus est interactif :
            * Choisissez de l'afficher en histogramme, ou en lignes
            * Choisissez le paramètre que vous souhaitez étudier
            * Un clic simple sur une catégorie l'excluera du graphe, un double-clic n'affichera qu'elle

            Toutes les données portent sur les années 2015 à 2020, en France.

            #### Observations

            * En ce qui concerne la déclivité, la surface, les conditions atmosphériques, les intersections et le tracé de la route, on observe une vaste majorité d'accidents dans une "normale" (route droite, plate, sèche, etc.).
            * On observe cependant sans surprise que le nombre d'accidents en intersection reste proportionellement bien plus élevé que sur route droite.
            * Les routes communales et départementales semblent statistiquement plus mortifères que les autres (moins entretenues, moins de vigilance,..).
            * Les accidents sont prévalents le jour car les routes sont bien plus fréquentées. Cependant, on observe en moyenne autant d'accidents la nuit pour une fréquentation inférieure (manque de luminosité fatiguant plus vite, fatigue entraînant une baisse de vigilance).
            * On obverse aussi une forte baisse des accidents sur les routes tracées en 's' à partir de 2018. Les routes tracées en 's' sont principalement départementales ou nationales et cette baisse est liée au changement de limitation de vitesse sur ces routes, passant de 90km/h à 80km/h.
            * Les mois de mars et surtout d'avril 2020 sont marqués par une drastique baisse des accidents en toute catégories, facilement corrélable avec la période de confinement, entrainant une baisse radicale de la frequentation des routes.


            """),
            html.Div([dcc.Graph(id='correl-graph')]),
            html.Div([
                dcc.Dropdown(id='column1',
                    options = list(self.categories),
                    value="Tracé de la route",
                    style={'display':'inline-block', 'width':'50%'}),
                dcc.Dropdown(id='column2',
                    options = list(self.categories),
                    value="Type d'intersection de la voie",
                    searchable = False,
                    style={'display':'inline-block', 'width': '50%'})
                ]),
            html.Br(),
            dcc.Markdown("""
            Ce graphe corrèle des paramètres deux à deux, choisissez les paramètres.

            * On observe encore une grande majorité de valeurs dans la "normale", quels que soient les paramètres que l'on corrèle.
            * On peut expliquer ce phénomène par la prévalence de cette "normalité" dans les différents facteurs. La majorité des routes sont plates et droite, par exemple.


            ####  A propos

            * Sources : https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/
            * Code source : https://github.com/StephaneMbll/delta
            * (c) 2022 Hugo Boux & Stephane Mabille


                        """),
            ], style = {
                'backgroundColor' : 'white',
                'padding': '10px 50px 10px 50px'
                })

        if application:
            self.app = application
        else:
            self.app = Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                dependencies.Output('accidents-main-graph', 'figure'),
                [ dependencies.Input('line-to-histo', 'value'),
                    dependencies.Input('cat-changer', 'value'),
                    ])(self.histo_line_callback)
        self.app.callback(
                dependencies.Output('correl-graph', 'figure'),
                [ dependencies.Input('column1', 'value'),
                    dependencies.Input('column2', 'value')
                    ])(self.correl_callback)

    def histo_line_callback(self, histo , strg):
        strg = self.categories[strg]
        data = self.df
        add = []
        tmp_param_name = switch_categorie(strg)
        for annee in range(2015, 2021):
            tmp_annee = data[data["an"] == annee]
            for mois in range(1, 13):
                tmp = tmp_annee[tmp_annee["mois"] == mois]
                month_convert = pd.to_datetime(str(mois) + str(annee), format='%m%Y').strftime("%Y-%m")
                tmp_count = tmp[strg].value_counts()
                for i in range(0, len(tmp_count)):
                    add.append([month_convert, tmp_param_name[tmp_count.index[i]-1], tmp_count.values[i]])
            df = pd.DataFrame(add, columns=["Date", strg, "Count_" + str(strg)])
        if (histo):
            fig = px.bar(labels= {'x': 'Date', 'y': "Nombre d'accident"}, title=switch_titre(strg))
        else:
            fig = px.line(labels= {'x': 'Date', 'y': "Nombre d'accident"}, title=switch_titre(strg))
        fig_test = df.groupby(strg)['Count_' + strg].sum().sort_values(ascending=False)
        for param in range(0, len(fig_test.index)):
            tmp_df = df[(switcher_categorie(strg,df) == fig_test.index[param])]
            if (histo):
                fig.add_bar(x=tmp_df["Date"], y=tmp_df["Count_" + str(strg)], name=fig_test.index[param] + " = " + str(fig_test.values[param]))
            else:
                fig.add_scatter(x=tmp_df["Date"], y=tmp_df["Count_" + str(strg)], name=fig_test.index[param] + " = " + str(fig_test.values[param]))
        return fig

    def correl_callback(self, column1, column2):
        data = self.df
        column1 = self.categories[column1]
        column2 = self.categories[column2]
        fig = px.histogram(data, x = data[column1].astype('int64').apply(lambda i: switch_categorie(column1)[i-1]),
                color = data[column2].astype('int64').apply(lambda i: switch_categorie(column2)[i-1]),
                color_discrete_sequence=color_list_test,
                labels = {'x':switch_legende(column1), "color":switch_legende(column2)},
                title="Nombre d'accident en fonction " + switch_titre_histo(column1) + " et " + switch_titre_histo(column2)
                )
        fig.update_layout(legend=dict( orientation = "h",
            yanchor = "bottom", y = 1.05,
            xanchor = "right", x = 1 ),
            autosize=True)
        fig.update_yaxes(automargin=True)
        return fig

### END OF CLASS ###

def switch_categorie(strg):
    switcher = {
            "catr": ["Autoroute","Route nationale","Route Départementale","Voie Communales","Hors réseau public","Parc de stationnement ouvert à la circulation publique","Routes de métropole urbaine","","autre"],
            "plan": ["Partie rectiligne","En courbe à gauche","En courbe à droite","En « S »"],
            "surf": ["Normale","Mouillée","Flaques","Inondée","Enneigée","Boue","Verglacée","Corps gras – huile","Autre"],
            "prof": ["Plat","Pente","Sommet de côte","Bas de côte"],
            "lum": ["Jour", "Semi-nuit", "Nuit noire", "Nuit éclairage éteint", "Nuit avec éclairage"],
            "atm": ["Normale","Pluie légère","Pluie forte","Neige - grêle","Brouillard - fumée","Vent fort - tempête","Temps éblouissant","Temps couvert","Autre"],
            "col": ["Deux véhicules - Frontale", "Deux véhicules - Par l'arrière", "Deux véhicules - Par le coté", "Trois véhicules et + en chaîne", "Trois véhicules et + collisions multiples", "Autre", "Sans collision"],
            "int": ["Hors intersection","Intersection en X","Intersection en T","Intersection en Y","Intersection à plus de 4 branches","Giratoire","Place","Passage à niveau", "Autre intersection"]
            }
    return switcher.get(strg)

def switch_titre(strg):
    switcher = {
            "catr": "Nombre d'accident en fonction de la catégorie de la route",
            "plan": "Nombre d'accident en fonction du tracé en plan de la route",
            "surf": "Nombre d'accident en fonction de l'état de la surface de la route",
            "prof": "Nombre d'accident en fonction de la déclivité de la route",
            "lum": "Nombre d'accident en fonction des conditions d'éclairage de la route",
            "atm": "Nombre d'accident en fonction des conditions atmosphériques",
            "col": "Nombre d'accident en fonction du type de collision",
            "int": "Nombre d'accident en fonction du type d'intersection de la voie" 
            }
    return switcher.get(strg)

def switch_titre_histo(strg):
        switcher = {
            "catr": "de la catégorie de la route",
            "plan": "du tracé en plan",
            "surf": "de l'état de la surface",
            "prof": "de la déclivité",
            "lum": "de l'éclairage",
            "atm": "des conditions atmosphériques",
            "col": "du type de collision",
            "int": "du type d'intersection de la voie" 
        }
        return switcher.get(strg)

def switcher_categorie(strg, df_test):
    if (strg == "catr"):
        return df_test.catr
    elif (strg == "plan"):
        return df_test.plan
    elif (strg == "surf"):
        return df_test.surf
    elif (strg == "lum"):
        return df_test.lum
    elif (strg == "atm"):
        return df_test.atm
    elif (strg == "col"):
        return df_test.col
    elif (strg == "int"):
        return df_test.int
    else:
        return df_test.prof


#return switch_line_bar(Trufal, strg, df_test)

def switch_legende(strg):
    switcher = {
            "catr": "categorie de la route",
            "plan": "tracé en plan de la route",
            "surf": "état de la surface de la route",
            "prof": "déclivité de la route",
            "lum": "éclairage de la route",
            "atm": "conditions atmosphériques",
            "col": "type de collision",
            "int": "intersection de la voie" 
            }
    return switcher.get(strg)

color_list_test=["#7ad151","#9FBDFC","#43bf71","#95A6FB", "#21918d", "#8C8CF9", "#2a788e", "#D161EC","#482575"]



if __name__ == '__main__':
    SMBH = Accidents()
    SMBH.app.run_server(debug=True, port=8051)
