import dash
import numpy as np
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import mzgl_inegalites_de_revenus.get_data as gd

# List all percentile to extract in the ine_df
mzgl_list_yaxis = [f"p{i}p{i+1}" for i in range(0, 100)]
# Markers of the years slider
mzgl_str_year_slider = {str(y): str(y) for y in range(1995, 2021, 5)}


def gini(array):
    """
    Calculate the Gini coefficient
    """
    array, cumul = np.sort(array), 0.0
    sum = array[0]
    for i in range(1, array.shape[0]):
        sum += cumul * 0.01 + ((0.01 * array[i]) / 2)
        cumul += array[i]
    return round((0.5 - sum) * 2.0, 4)


class Inegalites_de_revenus:
    START = "Start"
    STOP = "Stop"

    def __init__(self, application=None):
        self.continent_colors = {
            "Afrique": "brown",
            "Amérique": "navy",
            "Asie": "gold",
            "Europe": "green",
            "Océanie": "red",
        }
        self.yaxis_colors = {
            "p0p10": "red",
            "p0p50": "blue",
            "p90p100": "green",
            "p99p100": "yellow",
        }
        self.countries_df = gd.get_countries_df()
        self.populations_df = gd.get_population_df()
        self.gdp_df = gd.get_gdp_df()
        self.cpi_df = gd.get_corruption_df()
        self.dem_df = gd.get_democratie_index_df()
        self.ine_df = gd.get_inegalities_df(self.countries_df)
        # Calculate all Gini coefficient only one time
        self.ine_df = self.ine_df.join(
            (
                self.ine_df[self.ine_df.index.isin(mzgl_list_yaxis, level="Percentile")]
                .groupby(level=[0, 2])["value"]
                .agg([gini])
            ),
            on=["alpha3", "Year"],
        ).sort_index()
        self.main_layout = html.Div(
            [
                html.Div(
                    className="row",
                    children=[
                        html.H2("Inégalités de revenus dans le monde"),
                    ],
                ),
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="ten columns",
                            children=[
                                html.Center(
                                    [
                                        html.H4([], id="mzgl-title-main-graph"),
                                        html.Div([dcc.Graph(id="mzgl-main-graph")]),
                                        html.Br(),
                                        html.Div(
                                            [
                                                dcc.Slider(
                                                    id="mzgl-Year-Slider",
                                                    step=1,
                                                    value=1995,
                                                ),
                                                dcc.Interval(  # fire a callback periodically
                                                    id="mzgl-ine-auto-stepper",
                                                    interval=1500,  # in milliseconds
                                                    max_intervals=-1,  # start running
                                                    n_intervals=0,
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        html.Div(id="mzgl-div-country"),
                                        html.Div(
                                            children=[
                                                dcc.Graph(
                                                    id="mzgl-left-graph",
                                                    style={
                                                        "width": "49.5%",
                                                        "display": "inline-block",
                                                    },
                                                ),
                                                dcc.Graph(
                                                    id="mzgl-right-graph",
                                                    style={
                                                        "width": "50%",
                                                        "display": "inline-block",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "borderTop": "thin lightgrey solid",
                                                "borderBottom": "thin lightgrey solid",
                                                "justifyContent": "center",
                                            },
                                        ),
                                    ]
                                ),
                                dcc.Markdown(
                                    """
                                ### Informations à propos des axes:
                                * Sur l'axe des abscisse:
                                    * Un indice de démocratie faible indique que le pays est PEU démocratique.
                                    * Un indice de corruption élevé indique qu'il y a PEU de corruption dans le pays.
                                    * Le produit intérieur brut est calculé avec des US $ de 2021.
                                * Sur l'axe des ordonée:
                                    * Le coefficient de Gini est entre 0 et 1. Il permet de rendre compte des inégalités de répartition des revenus dans un pays. Plus ce coefficient est proche de 0, plus on se rapproche de l'égalité parfaite.
                                    * Les percentiles permettent seulement en compte les adultes de plus de 20 ans.
                                ### Formatage des axes:
                                Pour l'indicateur "Produit intérieur brut par habitant", un autoscaling sur l'axe des abscisses est appliqué afin de suivre l'augmentation du PIB.
                                #### Observations sur les résultats
                                * En moyenne, les inégalités de répartition de revenus ont augmenté à travers le monde depuis 1995.
                                * On remarque, qu'une mauvaise répartition des richesses n'est pas liée à un problème de corruption ou de démocratie. Des pays démocratiques et peu corrompus, comme les USA ou le Japon, sont tout aussi inégalitaires que des pays peu démocratiques et corrompus, comme Haïti ou la Russie.
                                * De même, le PIB par habitant n'est pas indicateur de l'inégalité: en Afrique, on a une grande variance dans les inégalités avec des pays ayant un PIB par habitant similaire.
                                * L'Europe et l'Océanie ont des inégalités de revenus bien plus faibles que les autres et possèdent tous deux l'indice de démocratie ou de corruption moyen le plus faible.
                                * On en conclut que l'importance de l'inégalité de revenus dans un pays ne semble pas être liée au niveau de démocratie, de corruption ou de développement de celui-ci. On remarque que les pays de l'Europe et de l'Océanie sont en moyenne plus égalitaires que sur les autres continents.
                                ### À propos
                                Données :
                                - [Population, Banque mondiale](https://data.worldbank.org/indicator/SP.POP.TOTL?name_desc=false)
                                - [PIB par personnes, Banque mondiale](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)
                                - [Inégalités de revenus, World inegalities database](https://wid.world/data/)
                                - [Index de corruption, Transparency International](https://www.transparency.org/en/cpi/2021)
                                - [Index de démocratie, Gapminder](https://www.gapminder.org/data/documentation/democracy-index/)
                                * (c) 2022 Gauthier Lombard, Mathieu Zimmermann
                                """
                                ),
                            ],
                        ),
                        html.Div(
                            className="two columns",
                            children=[
                                html.Div("Indicateurs en ordonnée"),
                                dcc.RadioItems(
                                    id="mzgl-select-Y",
                                    options=[
                                        {
                                            "label": "1% les plus riches",
                                            "value": "p99p100",
                                        },
                                        {
                                            "label": "10% les plus riches",
                                            "value": "p90p100",
                                        },
                                        {
                                            "label": "50% les plus pauvres",
                                            "value": "p0p50",
                                        },
                                        {
                                            "label": "10% les plus pauvres",
                                            "value": "p0p10",
                                        },
                                        {
                                            "label": "Coefficient de Gini",
                                            "value": "G",
                                        },
                                    ],
                                    value="p99p100",
                                    labelStyle={"display": "block"},
                                ),
                                html.Br(),
                                html.Div("Indicateurs en abscisse"),
                                dcc.RadioItems(
                                    id="mzgl-select-X",
                                    options=[
                                        {
                                            "label": "Indice de corruption",
                                            "value": "C",
                                        },
                                        {
                                            "label": "Indice de démocratie",
                                            "value": "Indice de démocratie",
                                        },
                                        {
                                            "label": "PIB par habitant",
                                            "value": "P",
                                        },
                                    ],
                                    value="C",
                                    labelStyle={"display": "block"},
                                ),
                                html.Br(),
                                html.Div("Continents"),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="mzgl-checklist-continent",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in sorted(
                                                    self.continent_colors.keys()
                                                )
                                            ],
                                            value=sorted(self.continent_colors.keys()),
                                            labelStyle={"display": "block"},
                                        ),
                                    ]
                                ),
                                html.Button(
                                    self.START,
                                    id="mzgl-ine-button-start-stop",
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        )
        # application should have its own layout and use self.main_layout as a page or in a component
        if application:
            self.app = application
        else:
            self.app = dash.Dash(
                __name__, title="Les inégalités de revenus dans le monde"
            )
            self.app.layout = self.main_layout

        self.app.callback(
            [
                dash.dependencies.Output("mzgl-Year-Slider", "min"),
                dash.dependencies.Output("mzgl-Year-Slider", "max"),
                dash.dependencies.Output("mzgl-Year-Slider", "value"),
                dash.dependencies.Output("mzgl-Year-Slider", "marks"),
            ],
            [
                dash.dependencies.Input("mzgl-select-X", "value"),
                dash.dependencies.Input("mzgl-ine-auto-stepper", "n_intervals"),
            ],
            [
                dash.dependencies.State("mzgl-Year-Slider", "value"),
                dash.dependencies.State("mzgl-ine-button-start-stop", "children"),
            ],
        )(self.update_year_slider)
        self.app.callback(
            dash.dependencies.Output("mzgl-main-graph", "figure"),
            [
                dash.dependencies.Input("mzgl-select-Y", "value"),
                dash.dependencies.Input("mzgl-select-X", "value"),
                dash.dependencies.Input("mzgl-Year-Slider", "value"),
                dash.dependencies.Input("mzgl-checklist-continent", "value"),
            ],
        )(self.update_main_graph)
        self.app.callback(
            dash.dependencies.Output("mzgl-title-main-graph", "children"),
            [
                dash.dependencies.Input("mzgl-select-Y", "value"),
                dash.dependencies.Input("mzgl-select-X", "value"),
            ],
        )(self.update_title)
        self.app.callback(
            dash.dependencies.Output("mzgl-div-country", "children"),
            dash.dependencies.Input("mzgl-main-graph", "hoverData"),
        )(self.get_country)
        self.app.callback(
            dash.dependencies.Output("mzgl-left-graph", "figure"),
            [
                dash.dependencies.Input("mzgl-main-graph", "hoverData"),
                dash.dependencies.Input("mzgl-Year-Slider", "value"),
                dash.dependencies.Input("mzgl-select-Y", "value"),
            ],
        )(self.create_left_graph)
        self.app.callback(
            dash.dependencies.Output("mzgl-right-graph", "figure"),
            [
                dash.dependencies.Input("mzgl-main-graph", "hoverData"),
                dash.dependencies.Input("mzgl-select-X", "value"),
            ],
        )(self.create_right_graph)
        self.app.callback(
            dash.dependencies.Output("mzgl-ine-button-start-stop", "children"),
            dash.dependencies.Input("mzgl-ine-button-start-stop", "n_clicks"),
            dash.dependencies.State("mzgl-ine-button-start-stop", "children"),
        )(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output("mzgl-ine-auto-stepper", "max_interval"),
            [dash.dependencies.Input("mzgl-ine-button-start-stop", "children")],
        )(self.run_movie)

    def update_title(self, yaxis, xaxis):
        """
        Manage slider of the scatter plot
        """
        yaxis_title = "les 10% les plus pauvres"
        if yaxis == "p99p100":
            yaxis_title = "les 1% les plus riches"
        elif yaxis == "p0p50":
            yaxis_title = "les 50% les plus pauvres"
        elif yaxis == "p90p100":
            yaxis_title = "les 10% les plus riches"
        title = " ".join(
            [
                "Évolution par pays de la part des revenus détenus par",
                yaxis_title,
                "vs ",
            ]
        )
        if yaxis == "G":
            title = "Coefficient de Gini vs "
        if xaxis == "C":
            title += "Indice de corruption"
        elif xaxis == "P":
            title += "Produit intérieur brut par habitant"
        else:
            title += "Indice de démocratie"
        return title

    def get_country(self, hoverData):
        """
        Retrieve country name from hoverData
        """
        if hoverData is None:
            return self.countries_df.iloc[np.random.randint(len(self.countries_df))][
                "Country_Name"
            ]
        return hoverData["points"][0]["hovertext"]

    def yaxis_graph(self, code, yaxis):
        title, y_axis_title = (
            "Évolution de la part des revenus des 1% les plus riches",
            "Pourcentage des revenus des 1% les plus riches",
        )
        df = self.ine_df.loc[(code, yaxis, slice(None)), :].sort_index()
        if yaxis == "p0p50":
            title, y_axis_title = (
                "Évolution de la part des revenus des 50% les plus pauvres",
                "Pourcentage des revenus des 50% les plus pauvres",
            )
        elif yaxis == "p0p10":
            title, y_axis_title = (
                "Évolution de la part des revenus des 10% les plus pauvres",
                "Pourcentage des revenus des 10% les plus pauvres",
            )
        elif yaxis == "p90p100":
            title, y_axis_title = (
                "Évolution de la part des revenus des 10% les plus riches",
                "Pourcentage des revenus des 10% les plus riches",
            )
        data = [
            go.Scatter(
                name="Indice de corruption",
                x=df.index.get_level_values(level=2).array,
                y=df["value"].array * 100,
                mode="lines",
                hovertemplate="Année: %{x}<br>Part des revenus: %{y}%<extra></extra>",
            )
        ]
        return go.Figure(
            data=data,
            layout={
                "title": title,
                "xaxis": {"title": "Années"},
                "yaxis": {"title": y_axis_title, "type": "linear"},
                "autosize": True,
                "showlegend": False,
            },
        )

    def create_left_graph(self, hoverData, year, yaxis):
        code = (
            self.countries_df.reset_index()
            .set_index(["Country_Name"])
            .loc[self.get_country(hoverData)]["alpha3"]
        )
        if yaxis != "G":
            return self.yaxis_graph(code, yaxis)
        tmp = self.ine_df.reset_index(level=1).sort_index().loc[(code, year), :]
        tmp = tmp[tmp["Percentile"].isin(mzgl_list_yaxis)]
        cumsum = list(np.cumsum(np.sort(tmp["value"].array)) * 100)
        cumsum[-1] = 100
        data = [
            go.Scatter(
                x=[x for x in range(1, 101)],
                y=cumsum,
                hovertemplate="%{x}% des adultes les moins aisées se partagent %{y:.2f}% des revenues avant taxes<extra></extra>",
                mode="lines",
            ),
            go.Scatter(
                name="Ligne d'égalité",
                x=[0, 100],
                y=[0, 100],
                mode="lines",
                hoverinfo=["skip", "skip"],
            ),
        ]
        fig = go.Figure(
            data=data,
            layout={
                "title": f"Indice de Gini - {year}",
                "xaxis": {
                    "title": "Part cumulée des plus de 20 ans avec les revenus du plus faible au plus élevé",
                    "fixedrange": True,
                },
                "yaxis": {
                    "title": f"Partage cumulé des revenus en {year}",
                    "type": "linear",
                    "fixedrange": True,
                },
                "autosize": True,
                "showlegend": False,
                "margin": {"l": 40, "b": 40, "r": 20, "t": 30},
            },
        )
        fig.add_annotation(
            xref="paper",
            yref="paper",
            font=dict(color="black", size=14),
            x=0.05,
            y=0.95,
            text=f"Coefficient de Gini: {tmp.iloc[0].gini}",
            showarrow=False,
        )
        fig.add_annotation(
            xref="paper",
            yref="paper",
            font=dict(color="black", size=14),
            x=0.5,
            y=0.55,
            text="Ligne d'égalité",
            showarrow=False,
            textangle=-31.5,
        )
        return fig

    def create_right_graph(self, hoverData, xaxis):
        x_axis_df, title, y_axis_title, country_name = (
            self.dem_df,
            "Évolution de l'indice de démocratie",
            "Indice de démocratie",
            self.get_country(hoverData),
        )
        code, data = (
            self.countries_df.reset_index()
            .set_index(["Country_Name"])
            .loc[country_name]["alpha3"],
            None,
        )
        if xaxis == "C":
            x_axis_df, title, y_axis_title = (
                self.cpi_df,
                "Évolution de la corruption",
                "Indice de corruption",
            )
            x_axis_df = x_axis_df.loc[(code)]
            data = [
                go.Scatter(
                    name="Indice de corruption",
                    x=x_axis_df.index.get_level_values(level=0).array,
                    y=x_axis_df["score"].array,
                    mode="lines",
                    hovertemplate="Année: %{x}<br>Indice de corruption: %{y}<extra></extra>",
                )
            ]
        elif xaxis == "P":
            x_axis_df, title, y_axis_title = (
                self.gdp_df.loc[(code)],
                "Produit intérieur brut par habitant (en US $ de 2021)",
                "",
            )
            data = [
                go.Scatter(
                    name="Produit intérieur brut par habitant",
                    x=x_axis_df.index.array,
                    y=x_axis_df.values,
                    mode="lines",
                    hovertemplate="Année: %{x}<br>PIB par habitant: %{y}<extra></extra>",
                )
            ]
        else:
            x_axis_df = x_axis_df.loc[(code)]
            data = [
                go.Scatter(
                    name="Indice de démocratie",
                    x=x_axis_df.index.get_level_values(level=0).array,
                    y=x_axis_df["score"].array,
                    mode="lines",
                    hovertemplate="Année: %{x}<br>Indice de démocratie: %{y}<extra></extra>",
                )
            ]
        return go.Figure(
            data=data,
            layout={
                "title": title,
                "xaxis": {"title": "Années"},
                "yaxis": {"title": y_axis_title, "type": "linear"},
                "autosize": True,
                "showlegend": False,
            },
        )

    def update_year_slider(self, xaxis, n_intervals, year, text):
        is_running = 0
        if text == self.STOP:
            is_running = 1
        x_axis_df = self.dem_df
        if xaxis == "C":
            x_axis_df = self.cpi_df
        elif xaxis == "P":
            if year + is_running > 2020 or year < 1995:
                return (
                    1995,
                    2020,
                    1995,
                    mzgl_str_year_slider,
                )
            return (
                1995,
                2020,
                year + is_running,
                mzgl_str_year_slider,
            )
        years = x_axis_df.reset_index()["Year"]
        min_year, max_year = years.min(), years.max()
        if year + is_running > max_year or year < min_year:
            return (
                min_year,
                max_year,
                min_year,
                {str(y): str(y) for y in range(min_year, max_year + 1, 5)},
            )
        return (
            min_year,
            max_year,
            year + is_running,
            {str(y): str(y) for y in range(min_year, max_year + 1, 5)},
        )

    def update_main_graph(self, yaxis, xaxis, year, regions):
        x_axis_df, yaxis_title, xmax, tmp = (
            self.dem_df,
            "Part des revenus des 10% les plus pauvres",
            100,
            None,
        )
        if yaxis != "G":
            tmp = self.ine_df.loc[(slice(None), yaxis, year), :]
        else:
            tmp = self.ine_df.loc[(slice(None), "p99p100", year), :]
        tmp = tmp.reset_index(level=1).sort_index()
        if len(regions) != 5:
            tmp = tmp[tmp["region"].isin(regions)]
        if xaxis == "C":
            x_axis_df, xaxis = self.cpi_df, "Indice de corruption"
        elif xaxis == "P":
            xmax, x_axis_df = -1, self.gdp_df.loc[slice(None), [str(year)]]
            x_axis_df["Year"], xaxis = (
                year,
                "Produit intérieur brut par habitant (en US $ de 2021)",
            )
            x_axis_df = (
                x_axis_df.reset_index()
                .set_index(["alpha3", "Year"])
                .rename(columns={str(year): "score"})
            )
        res = (
            tmp.join(x_axis_df, on=["alpha3", "Year"], sort=True)
            .join(
                self.populations_df.loc[:, str(year)]
                .rename("population")
                .astype("int64")
            )
            .dropna()
        )
        if yaxis == "G":
            fig = px.scatter(
                res,
                x="score",
                y="gini",
                size="population",
                size_max=60,
                hover_name="Country_Name",
                color="region",
                color_discrete_map=self.continent_colors,
                custom_data=["Country_Name", "population"],
            )
            fig.update_yaxes(range=[0.3, 0.8])
            fig.update_layout(
                xaxis=dict(title=xaxis, type="linear"),
                yaxis=dict(title="Coefficient de Gini", type="linear"),
                margin={"l": 0, "b": 1, "t": 1, "r": 0},
                hovermode="closest",
                showlegend=False,
            )
            fig.update_traces(
                hovertemplate="".join(
                    [
                        "<b>%{customdata[0]}</b><br><br>Coefficient de Gini: %{y}<br>Population: %{customdata[1]:,}<br>",
                        xaxis,
                        ": %{x}<extra></extra>",
                    ]
                )
            )
            if xmax != -1:
                fig.update_xaxes(range=[0, xmax])
            return fig
        res["value"] *= 100
        fig = px.scatter(
            res,
            x="score",
            y="value",
            size="population",
            size_max=60,
            hover_name="Country_Name",
            color="region",
            color_discrete_map=self.continent_colors,
            custom_data=["Country_Name", "population"],
        )
        if xmax != -1:
            fig.update_xaxes(range=[0, xmax])
        fig.update_yaxes(range=[0, 0.7])
        if yaxis == "p99p100":
            fig.update_yaxes(range=[0, 35.0])
            yaxis_title = "Part des revenus des 1% les plus riches"
        elif yaxis == "p0p50":
            fig.update_yaxes(range=[0, 30.0])
            yaxis_title = "Part des revenus des 50% les plus pauvres"
        elif yaxis == "p90p100":
            fig.update_yaxes(range=[25.0, 70.0])
            yaxis_title = "Part des revenus des 10% les plus riches"
        fig.update_layout(
            xaxis=dict(title=xaxis, type="linear"),
            yaxis=dict(title=yaxis_title, type="linear"),
            margin={"l": 0, "b": 1, "t": 1, "r": 0},
            hovermode="closest",
            showlegend=False,
        )
        fig.update_traces(
            hovertemplate="".join(
                [
                    "<b>%{customdata[0]}</b><br><br>Part des revenus: %{y} %<br>Population: %{customdata[1]:,}<br>",
                    xaxis,
                    ": %{x}<extra></extra>",
                ]
            )
        )
        return fig

    def button_on_click(self, n_clicks, text):
        """
        start and stop the movie
        """
        if text == self.START:
            return self.STOP
        return self.START

    def run_movie(self, text):
        """
        this one is triggered by the previous one because we cannot have 2 outputs
        in the same callback
        """
        if text == self.START:  # then it means we are stopped
            return 0
        return -1

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)
