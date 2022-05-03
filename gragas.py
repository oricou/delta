import dash
from dash import dcc
from dash import html
from planisphere import planisphere
from consommation import consommation

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Gragas", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
pla = planisphere.Planisphere(app)
con = consommation.Consommation(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[ 
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("Gragas")),
                              dcc.Link(html.Button("Consommation selon le PIB", style={'width':"100%"}), href='/consommation'),
                              html.Br(),
                              dcc.Link(html.Button("Planisphère", style={'width':"100%"}), href='/planisphere'),
                              html.Br(),
                              html.Br(),
                              html.Br(),
                              html.Center(html.A('Code source', href='https://github.com/El-Bicente/gragas')),
                          ]),
                 html.Div(id='page_content', className="ten columns"),
            ]),
])


home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("Choisissez la catégorie dans l'index à gauche."),
])

to_be_done_page = html.Div([
    dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
])

app.layout = main_layout

# "complete" layout (not sure that I need that)
app.validation_layout = html.Div([
    main_layout,
    to_be_done_page,
])

# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/planisphere':
        return pla.main_layout
    elif pathname == '/consommation':
        return con.main_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
