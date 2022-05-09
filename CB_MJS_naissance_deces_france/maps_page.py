import dash
from dash import html
from dash import dcc
from CB_MJS_naissance_deces_france import birth_map, maps_2020


class MapsPage:
    def __init__(self, application=None):

        self.birth_map = birth_map.Birth_Map(application)
        self.maps_2020 = maps_2020.Carte(application)

        self.main_layout = html.Div(children=[
            html.H2(children='Cartes des taux de natalité et mortalité par départements en France'),

            html.Div([
                html.Button('Natalité', id='birth-button',
                            style={'width': '33%', 'display': 'inline-block'}),
                html.Button('2020', id='2020-button',
                            style={'width': '33%', 'display': 'inline-block'}),
            ], style={'display': 'flex',
                      'justifyContent': 'space-evenly', }),

            html.Div(id='subpage-maps-page', children=[
                dcc.Markdown("""
                Cliquez sur l'un des bouttons suivants pour afficher la ou les cartes correspondantes.
                """)
            ], style={
                'justifyContent': 'center'
            }),

        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px'
        })

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('subpage-maps-page', 'children'),
            [dash.dependencies.Input('birth-button', 'n_clicks'),
             dash.dependencies.Input('2020-button', 'n_clicks')])(self.birth_button_on_click)

    def birth_button_on_click(self, b1, b2):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if 'birth-button' in changed_id:
            return self.birth_map.main_layout
        elif '2020-button' in changed_id:
            return self.maps_2020.main_layout
