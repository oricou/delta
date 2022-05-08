import dash
from dash import dcc
from dash import html
import pickle

import pandas as pd
import json
import plotly.express as px
from IPython.display import Image

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)

file = open('data/save_data', 'rb')
data = pickle.load(file)
file.close()

departements = json.load(open('data/departements-version-simplifiee.geojson'))

dfJoinCity = data[0]
dfJoinRegion = data[1]
dfJoinMonth = data[2]
dfByYear = data[3]


carte = px.scatter_mapbox(dfJoinCity, lat="gps_lat", lon="gps_lng", hover_name="Commune", hover_data=["Nombre de catastrophe"],
                        color="Nombre de catastrophe log",
                        color_continuous_scale='jet',
                        size_max=50, zoom=5, height=800, mapbox_style="carto-positron")

region = px.choropleth_mapbox(dfJoinRegion, geojson=departements, 
                           locations='department_code', featureidkey = 'properties.code', # join keys
                           color='Nombre de catastrophe', color_continuous_scale="jet",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                              height=800,
                          )

month = px.bar(dfJoinMonth,x="Mois",y="Nombre de catastrophe")
year = px.bar(dfByYear,x="Année",y="Nombre de catastrophe")

carte.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
region.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children = [
    html.Div(children = [
        html.H3(children='Carte des catastrophes naturelles en France métropolitaine depuis 1982.'),

        html.H6(children='''
            Nous laissons au lecteur le soin de faire sa propre interprétation de nos différents graphiques.
        ''')
        ], style={
                'lineHeight' : '60px',
                'borderWidth' : '1px',
                'borderStyle' : 'dashed',
                'borderRadius' : '5px',
                'textAlign' : 'center',

        }),
    html.Br(),
    html.Br(),
    
################################################################################################################################
    html.Div(children = [
        html.H3(children='Carte des catastrophes naturelles en France métropolitaine depuis 1982 par ville et village.'),
        html.Br(),
        dcc.Graph(
            id='graph-carte',
            figure=carte
        ),
        
        dcc.Markdown("""
            Cette carte est interactive. Vous pouvez vous amuser à zoomer et dézoomer pour rechercher une ville particulière ou analyser une région plus précisément. Les couleurs sont générées logarithmiquement à partir du nombre de catastrophes par ville. Passez votre souris sur une ville pour obtenir des informations comme le nombre de catastrophes.
            """),
        
        html.H6(children="Notes :"),
        
        dcc.Markdown("""
               * Nous pouvons remarquer les différentes régions qui sont les plus touchées par les catastrophes.
               * Le bassin d'Arcachon.
               * Un couloir de Bordeaux à Perpignan à cause de la chaîne des Pyrénées et du massif central. Les orages sont bloqués entre les montagnes et la pluie et les rivières descendent dans les vallées, ce qui ajoute des risques d'inondations, de glissements de terrain et de coulées de boue.
               * La côte méditerranéenne.
               * La côte orientale de la Corse.
               * Le couloir entre le massif central et les Alpes.
               * La région parisienne, étant une région très urbaine, l'eau est plus difficile à évacuer car les sols sont travaillés et goudronnés.
               * Le Nord de la France, souvent soumis à de fortes rafales de vent.
        """)
    ]),
        
        
################################################################################################################################
    
    html.Br(),
    html.Div(children = [
        html.H3(children='Carte des catastrophes naturelles en France métropolitaine depuis 1982 par région'),
        html.Br(),
        dcc.Graph(
            id='region-graph',
            figure=region
        ),
        
        html.H6(children="Notes :"),
        
        dcc.Markdown("""
               * On peut noter que les trois départements les plus impactés sont la Haute Garonne, la Gironde et le Pas De Calais.     
               * Ici, nous voyons le problème de manière plus générale, nous voyons moins l'impact de la côte, de la grande ville etc. mais plutôt les différentes régions comme les montagnes, le bassin d'Archachon pour les tempêtes atlantiques et encore le nord de la France pour les fortes rafales de vent.
        """)
    ]),  
################################################################################################################################
    
    html.Br(),
        html.Div(children = [
        html.H3(children='Graphique à barres représentant le nombre de catastrophes par mois'),
        dcc.Graph(
            id='month-graph',
            figure=month
        ),
        
        html.H6(children="Notes :"),
        
        dcc.Markdown("""
               * Nous notons ici que les catastrophes se produisent le plus souvent en été et en hiver, lorsque les températures sont les plus extrêmes.     
               * On voit ici que les données peuvent être un peu biaisées, on voit que le mois de décembre est globalement supérieur aux autres mois, ceci est notamment dû à la tempête de décembre 1999 (comme on peut le voir sur le graphique suivant).
        """)
    ]),
################################################################################################################################
        html.Br(),
        html.Div(children = [
        html.H3(children='Graphique à barres représentant le nombre de catastrophes par année'),
        dcc.Graph(
            id='year-graph',
            figure=year
        ),
        
        html.H6(children="Notes :"),
        
        dcc.Markdown("""
               * On peut voir ici que la tempête de 1999 a été violente.
               """)
    ])
    
    
], style={
        'margin' : '30px 60px 10px 60px',
})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8052)
