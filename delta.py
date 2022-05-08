import dash
from dash import dcc
from dash import html
from australiaweather import australiaweather
from australiaweather import mesureweather
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
wth = australiaweather.DataDetail(app)
msr = mesureweather.StationStats(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[ 
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("Australia weather cost")),
                              dcc.Link(html.Button("Echelle de donnée", style={'width':"100%"}), href='/australiaweather'),
                              html.Br(),
                              dcc.Link(html.Button('Mesure', style={'width':"100%"}), href='/mesureweather'),
                              html.Br(),
                              #dcc.Link(html.Button('Décès journaliers', style={'width':"100%"}), href='/deces'),
                              #html.Br(),
                              html.Br(),
                              html.Br(),
                              #html.Center(html.A('Code source', href='https://github.com/oricou/delta')),
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

# "complete" layout (not sure that I need that)
app.validation_layout = html.Div([
    main_layout,
    to_be_done_page,
    wth.main_layout,
])

# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/australiaweather':
        return wth.main_layout
    elif pathname == '/mesureweather':
        return msr.main_layout
    #elif pathname == '/deces':
        #return dec.main_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
