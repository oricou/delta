from turtle import rt
import dash
from dash import dcc
from dash import html
from movie_data_analysis.producteurs import producteurs
from movie_data_analysis.evolution_production import evolution_production
from movie_data_analysis.theme_popularite import theme_popularite

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Movie industry analysis", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
prd = producteurs.Producer(app)
mvP = evolution_production.MovieProduction(app)
tmA = theme_popularite.ThemeAnalysis(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[ 
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("Movie Data")),
                              dcc.Link(html.Button("Evolution de la production de films", style={'width':"100%"}), href='/production'),
                              html.Br(),
                              dcc.Link(html.Button('Corrélation entre thème et popularité', style={'width':"100%"}), href='/themepopularite'),
                              html.Br(),
                              dcc.Link(html.Button('Analyse de l\'impact des producteurs', style={'width':"100%"}), href='/producteurs'),
                              html.Br(),
                              html.Br(),
                              html.Center(html.A('Code source', href='https://github.com/CarlitoCepillo/pybd_movie_project')),
                          ]),
                 html.Div(id='page_content', className="ten columns"),
            ]),
])


home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("Choisissez le jeu de données ci-dessus.",),
], style={"margin-left": "40%","width":"400px"})

to_be_done_page = html.Div([
    dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
])

app.layout = main_layout

# "complete" layout (not sure that I need that)
app.validation_layout = html.Div([
    main_layout,
    to_be_done_page,
    mvP.main_layout,
])

# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/production':
        return mvP.main_layout
    elif pathname == '/themepopularite':
        return tmA.main_layout
    elif pathname == '/producteurs':
        return prd.main_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
