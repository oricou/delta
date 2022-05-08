import dash
from dash import dcc
from dash import html
from stats import stats
from maps import maps

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
maps = maps.MapStats(app)
stats = stats.Stats(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[ 
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("$$$ for environment")),
                              dcc.Link(html.Button("Statistics", style={'width':"100%"}), href='/stats'),
                              html.Br(),
                              dcc.Link(html.Button('Maps', style={'width':"100%"}), href='/maps'),
                              html.Br(),
                              html.Br(),
                              html.Br(),
                          ]),
                 html.Div(id='page_content', className="ten columns"),
            ]),
])


home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("Choisissez le jeu de données dans l'index à gauche."),
])

to_be_done_page = html.Div([
    dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
])

app.layout = main_layout


# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stats':
        return stats.main_layout
    elif pathname == '/maps':
        return maps.main_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
