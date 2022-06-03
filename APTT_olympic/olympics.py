import dash
from dash import dcc
from dash import html
import pandas as pd
import folium


def get_custom_scale(df):
    if df['Country'].max() > 10:
        custom_scale = (df['Country'].quantile((0, 0.5, 0.7, 0.8, 0.85, 0.9, 0.97, 1))).to_list()
    elif df['Country'].max() > 9:
        custom_scale = [1, 2, 3, 5, 7, 9, df['Country'].quantile(1)]
    elif df['Country'].max() > 8:
        custom_scale = [1, 2, 3, 5, 7, 8, df['Country'].quantile(1)]
    elif df['Country'].max() > 7:
        custom_scale = [1, 2, 3, 5, 7, df['Country'].quantile(1)]
    elif df['Country'].max() > 6:
        custom_scale = [1, 2, 3, 5, 6, df['Country'].quantile(1)]
    elif df['Country'].max() > 5:
        custom_scale = [1, 2, 3, 5, df['Country'].quantile(1)]
    elif df['Country'].max() > 4:
        custom_scale = [1, 2, 3, 4, df['Country'].quantile(1)]
    elif df['Country'].max() > 3:
        custom_scale = [1, 2, 3, df['Country'].quantile(1)]
    else:
        custom_scale = [1, 2, 3.001, 4]
    return custom_scale


class Olympic:
    def get_data(self, filename):
        try:
            df = pd.read_csv(self.path + filename)
        except FileNotFoundError:
            self.path = "APTT_olympic/"
            df = pd.read_csv(self.path + filename)
        if filename != 'data/stripped.csv':
            df = df.drop(["City", "Sport", "Gender", "Athlete"], axis=1)
            df = df[df["Year"] >= 1918]
            df.drop(df.index[(df['Country'] == 'YUG') | (df['Country'] == 'TCH') | (df['Country'] == 'AHO') | (
                    df['Country'] == 'EUN') | (df['Country'] == 'IOP') | (df['Country'] == 'IOA')], inplace=True)
        return df

    def __init__(self, application=None):
        self.path = ""
        self.dropdown = 1
        self.event = ""
        self.discipline = "All"
        summer = Olympic.get_data(self, "data/summer.csv")
        winter = Olympic.get_data(self, "data/winter.csv")
        stripped = Olympic.get_data(self, "data/stripped.csv")
        stripped['Event'] = 'Stripped'
        stripped['Discipline'] = 'Stripped'
        self.olympic = pd.concat([summer, winter, stripped])
        event = sorted(self.olympic['Event'].unique())
        event.insert(0, "All")
        discipline = sorted(self.olympic['Discipline'].unique())
        discipline.insert(0, "All")
        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de médailles olympiques par pays'),
            html.H4(id="titre-carte", children=""),
            html.Iframe(id="map", srcDoc=open(self.path + 'map.html', 'r').read(), width='100%', height='600'),
            html.Div([
                html.Div([html.Div('Épreuves spécifiques:', style={'width': '20em', 'fontSize': '25px'}),
                          dcc.RadioItems(
                              id='med-spe',
                              options=[{'label': 'Marathon', 'value': 'Marathon'},
                                       {'label': 'Épée Individuel', 'value': 'Épée Individual'},
                                       {'label': '10 000m Patinage de vitesse', 'value': 'patinage'},
                                       {'label': 'Médailles volées', 'value': 'Stripped'}],
                              labelStyle={'display': 'block'},
                              value='Marathon'
                          )
                          ], style={'width': '20em'}),
                html.Br(),
                html.Div([html.Div('Discipline'),
                          dcc.Dropdown(
                              id='med-dis',
                              options=discipline,
                              disabled=False,
                          )]),
                html.Br(),
                html.Div([html.Div('Épreuve'),
                          dcc.Dropdown(
                              id='med-event',
                              options=event,
                              disabled=False,
                          )]),
                html.Br(),
                dcc.Markdown("""
                Cette carte, représentant tous les pays, est interactive. En passant la souris sur celle-ci, vous verrez une infobulle
                apparaître contenant le nom du pays ainsi que le nombre de médailles obtenu par celui-ci suivant l'épreuve sélectionnée. 
                
                #### Introduction :
                
                Nous avons décidé de mettre en avant quelques épreuves qui nous semblaient intéressantes. Plus particulièrement, de montrer
                l'importance de certains pays dans des épreuves spécifiques. De plus, il nous semblait indispensable d'afficher a l'échelle mondiale
                le nombre de médailles olympiques volées par pays.

                Vous découvrirez par vous-mêmes que dans la plupart des épreuves olympiques, certains pays sont tout le temps présents. On peut
                penser aux Etats-Unis, à la Russie, la Chine et aussi aux pays de l'Europe de l'Ouest (France, Royaume-Uni, Allemagne, Italie, ...)
                La raison peut être plutôt simple à expliquer qui serait une question d'argent mis en place dans ces sports olympiques, des infrastructures
                établies, au final des moyens mis en place pour le développement de ces sports.

                Ainsi, par rapport à cette constatation, nous voulions à la fois la vérifier, mais aussi prouver qu'il n'y a pas que ces pays-là dans
                ce monde olympique. Il y a des "exceptions". Également, nous voulions aussi accentuer un point d'une manière plus controversée sur le dopage
                et donc sur les médailles dites "volées".
                
                Nous avons donc décidé de mettre en avant la discipline du Marathon dans un premier temps
                pour montrer que ce sont l'Ethiopie et le Kenya qui sont les maîtres de cette épreuve. Il n'y a pas vraiment de consensus qui expliquerait ce phénomène,
                certains parlent de culture, d'autres d'alimentation ou d'environnement.
                
                Ensuite, d'une manière plus logique nous avons choisi l'escrime où la France et l'Italie
                dominent cette épreuve, comme nous l'avons dit assez logiquement par rapport à une question
                de moyens mis en place, d'infrastructure, mais surtout par une histoire du duel notamment au 17-18ème siècle avec les mousquetaires.
                
                Enfin, nous avons décidé de mettre en avant le patinage de vitesse qui est une épreuve totalement
                dominée par les Pays-Bas, d'une part puisque ce sport fut inventé dans ce même pays, mais aussi d'une autre
                part parce que ce sport est comme dit au-dessus plus qu'important et fait partie de la culture de ce pays, avec des courses uniques au monde comme l'Elfstedentocht, course d'endurance de 200 km.

                #### Notes :
                
                Le menu déroulant 'Discipline' permet choisir une discipline en particulier pour affiner la recherche par épreuves.
                Modifier la discipline ne change pas la carte.
                
                Le menu déroulant 'Épreuve' permet de choisir une épreuve en particulier que vous souhaitez afficher.
                
                Si vous souhaitez afficher toutes les médailles d'une discipline ou simplement toutes les médailles,
                il suffit de choisir l'épreuve 'all'.
                    
                #### À propos
                   * Sources : 
                      * [Dataset des médailles](https://www.kaggle.com/amirba/olympic-sports-and-medals-18962021) disponible sur Kaggle
                      * [Dataset des médailles volées](https://en.wikipedia.org/wiki/List_of_stripped_Olympic_medals) sur Wikipédia
                   * Auteurs : 
                      * Alex Poiron
                      * Tom Thil
                """)
            ], style={
                'backgroundColor': 'white',
                'padding': '10px 50px 10px 50px',
            })]
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('map', 'srcDoc'),
            dash.dependencies.Output('titre-carte', 'children'),
            [dash.dependencies.Input('med-spe', 'value'),
             dash.dependencies.Input('med-event', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('med-event', 'options'),
            [dash.dependencies.Input('med-dis', 'value')])(self.set_discipline)

    def set_discipline(self, discipline):
        self.discipline = discipline
        dataset = self.olympic
        if discipline != "All" and discipline is not None:
            dataset = dataset[dataset["Discipline"] == self.discipline]
        events = sorted(dataset['Event'].unique())
        events.insert(0, 'All')
        return events

    def update_graph(self, spe_event, dropdown):
        dataset = self.olympic
        titre = "Épreuve : "
        if not self.event == spe_event:
            self.set_discipline('All')
            event, self.event = spe_event, spe_event
            if spe_event == "patinage":
                self.set_discipline('Speed skating')
                event, self.event = "10000M", "10000M"
        else:
            event, self.event = dropdown, spe_event

        if self.discipline != "All" and self.discipline is not None:
            titre = "Discipline : " + self.discipline + "      " + titre
            dataset = dataset[dataset["Discipline"] == self.discipline]
        if event is None:
            event = "Marathon"
        titre = titre + event
        if event != 'All':
            event = dataset[dataset["Event"] == event]
        else:
            event = dataset

        data = event["Country"].value_counts()
        df = pd.DataFrame.from_dict(data)
        df["ISO"] = list(df.index.values)
        fig = folium.Map(location=[28.5736, 9.0750], tiles=None, zoom_start=2, max_bounds=True, min_zoom=1)
        folium.Rectangle([(-20000, -20000), (20000, 20000)], fill=True, fill_color="#29c5ff").add_to(fig)
        url = self.path
        custom_scale = get_custom_scale(df)

        choro = folium.Choropleth(
            geo_data=f'{url}data/countries.geojson',
            name='choropleth',
            data=df,
            columns=['ISO', 'Country'],
            key_on='feature.properties.ISO_A3',
            threshold_scale=custom_scale,
            fill_color="RdPu",
            fill_opacity=1,
            line_opacity=0.8,
            Highlight=True,
            line_color='black',
            nan_fill_color="White",
            legend_name="Nombre de médailles"
        ).add_to(fig)
        for c in choro.geojson.data['features']:
            if c['properties']['ISO_A3'] in df['ISO']:
                c['properties']['Médailles'] = float(df.loc[c['properties']['ISO_A3'], 'Country'])
            else:
                c['properties']['Médailles'] = 0
            c['properties']['Pays'] = c['properties']['Country']
        folium.GeoJsonTooltip(['Pays', 'Médailles']).add_to(choro.geojson)
        folium.LayerControl().add_to(fig)
        fig.save(self.path + "map.html")
        return open(self.path + 'map.html', 'r').read(), titre


if __name__ == '__main__':
    olym = Olympic()
    olym.app.run_server(debug=True, port=8052)
