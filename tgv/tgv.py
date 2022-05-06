import os
import dash
import plotly.express as px
from dash.dependencies import Input, Output

import folium
import branca.colormap as cm
from make_df import make_df
from front import make_layout, get_stylesheet


class TGV:

    cur_path = os.path.dirname(__file__)
    a_propos_path = os.path.join(cur_path, "a-propos.md")
    pas_de_taux = [
        "Nombre de circulations prévues",
        "Retard moyen de tous les trains au départ",
        "Retard moyen de tous les trains à l'arrivée"
    ]

    def update_map_visibility(self, map):
        match map:
            case "Trajet":
                return {"display": "block"}
            case "Gare":
                return {"display": "none"}

    def update_hist_visibility(self, map):
        match map:
            case "Trajet":
                return {"display": "none"}
            case "Gare":
                return {"display": "block"}


    def update_map(self, year, colonne, filter, data):
        """
        Create graph mapping train stations and lines to the lateness of the trains
        """

        year += 2018
        france_line = folium.Map(location=[46.8, 2], zoom_start=6)
        df_trajet = self.df_trajet[(self.df_trajet.index == str(year))]
        if data == "Taux":
            df_trajet[colonne] = df_trajet.apply(
                lambda x: x[colonne] / x["Nombre de circulations prévues"] * 100, axis=1
            )
        df_trajet = df_trajet[
            (df_trajet[colonne] >= filter[0]) & (df_trajet[colonne] <= filter[1])
        ]
        max_traffic = df_trajet[colonne].max()
        min_traffic = df_trajet[colonne].min()
        colormap = cm.LinearColormap(
            ["green", "orange", "red"], vmin=min_traffic, vmax=max_traffic
        )
        france_line.add_child(colormap)

        for i in range(len(self.df_gares["WGS 84"])):
            france_line.add_child(
                folium.Marker(
                    location=self.df_gares["WGS 84"].iloc[i],
                    popup="Gare: {}<br>Région SNCF: {}<br>Coordonnées: {}".format(
                        self.df_gares["Gare"].iloc[i],
                        self.df_gares["Région SNCF"].iloc[i],
                        self.df_gares["WGS 84"].iloc[i],
                    ),
                    icon=folium.Icon(color="green"),
                )
            )

        for i in range(len(df_trajet["Coord_départ"])):

            traffic = df_trajet[colonne].iloc[i]
            folium.PolyLine(
                (
                    df_trajet["Coord_départ"].iloc[i],
                    df_trajet["Coord_arrivée"].iloc[i],
                ),
                color=colormap.rgb_hex_str(traffic),
                weight=traffic / max_traffic * 2 + 1,
                opacity=1,
                popup="{}: {}<br>Départ: {}<br>Arrivée: {}".format(
                    colonne,
                    df_trajet[colonne].iloc[i],
                    df_trajet["Gare de départ"].iloc[i],
                    df_trajet["Gare d'arrivée"].iloc[i],
                ),
            ).add_to(france_line)

        france_line.save("mymapnew.html")
        return open("mymapnew.html", "r").read()

    def update_hist(self, year, colonne, filter, data):
        year += 2018
        df_grouped = (
            self.df_trajet[self.df_trajet.index == str(year)]
            .groupby("Gare de départ")
            .sum()
            .reset_index()
        )
        if data == "Taux":
            df_grouped[colonne] = df_grouped.apply(
                lambda x: x[colonne] / x["Nombre de circulations prévues"] * 100, axis=1
            )
        if (
            colonne == "Retard moyen de tous les trains au départ"
            or colonne == "Retard moyen de tous les trains à l'arrivée"
        ):
            return px.histogram(
                df_grouped[
                    (df_grouped[colonne] >= filter[0])
                    & (df_grouped[colonne] <= filter[1])
                ],
                x="Gare de départ",
                y=colonne,
                histfunc="avg",
            )
        return px.histogram(
            df_grouped[
                (df_grouped[colonne] >= filter[0]) & (df_grouped[colonne] <= filter[1])
            ],
            x="Gare de départ",
            y=colonne,
            histfunc="sum",
        )

    def update_filter(self, year, colonne, map, data):
        year += 2018
        if map == "Trajet":
            df = self.df_trajet[self.df_trajet.index == str(year)]
        elif (
            colonne == "Retard moyen de tous les trains au départ"
            or colonne == "Retard moyen de tous les trains à l'arrivée"
        ):
            df = (
                self.df_trajet[self.df_trajet.index == str(year)]
                .groupby("Gare de départ")
                .mean()
            )
        else:
            df = (
                self.df_trajet[self.df_trajet.index == str(year)]
                .groupby("Gare de départ")
                .sum()
            )

        if data == "Taux":
            df[colonne] = df.apply(
                lambda x: x[colonne] / x["Nombre de circulations prévues"] * 100, axis=1
            )

        return (
            df[colonne].min(),
            df[colonne].max(),
            [df[colonne].min(), df[colonne].max()],
        )

    def update_datatype(self, colonne, data):
        if colonne in self.pas_de_taux:
            return "Brut", [
                {"label": "Brut", "value": "Brut"},
                {"label": "Taux (%)", "value": "Taux", "disabled": True},
            ]
        return data, [
            {"label": "Brut", "value": "Brut"},
            {"label": "Taux (%)", "value": "Taux"},
        ]

    def __init__(self, application: dash.Dash = None):
        self.main_layout = make_layout()
        self.df_trajet, self.df_coord, self.df_gares = make_df()
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__, external_stylesheets=get_stylesheet())
            self.app.layout = self.main_layout

        self.app.callback(
            Output("tgv-main-graph", "style"), [Input("plot-switch", "value")]
        )(self.update_map_visibility)

        self.app.callback(
            Output("hist-graph", "style"), [Input("plot-switch", "value")]
        )(self.update_hist_visibility)

        self.app.callback(
            Output("tgv-main-graph", "srcDoc"),
            [
                Input("tgv-year-slider", "value"),
                Input("tgv-y-axis-dropdown", "value"),
                Input("debit-filter-type-slider", "value"),
                Input("datatype-switch", "value"),
            ],
        )(self.update_map)

        self.app.callback(
            Output("hist-graph", "figure"),
            [
                Input("tgv-year-slider", "value"),
                Input("tgv-y-axis-dropdown", "value"),
                Input("debit-filter-type-slider", "value"),
                Input("datatype-switch", "value"),
            ],
        )(self.update_hist)

        self.app.callback(
            Output("debit-filter-type-slider", "min"),
            Output("debit-filter-type-slider", "max"),
            Output("debit-filter-type-slider", "value"),
            [
                Input("tgv-year-slider", "value"),
                Input("tgv-y-axis-dropdown", "value"),
                Input("plot-switch", "value"),
                Input("datatype-switch", "value"),
            ],
        )(self.update_filter)

        self.app.callback(
            Output("datatype-switch", "value"),
            Output("datatype-switch", "options"),
            [Input("tgv-y-axis-dropdown", "value"), Input("datatype-switch", "value")],
        )(self.update_datatype)


if __name__ == "__main__":
    tgv = TGV()
    tgv.app.run_server(debug=True, port=8051)
