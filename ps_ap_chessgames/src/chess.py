from typing import OrderedDict
from dash import Dash, Input, Output, callback_context
from dash.dependencies import State
import pandas as pd
import os

from ps_ap_chessgames.src.layout import make_layout, valid_button_style
import ps_ap_chessgames.src.utils as ut
import ps_ap_chessgames.src.labels as data


class Chess:
    def init_cls(self, dump1):
        self.selected_games = self.chess_games.copy()
        self.graph = None
        self.filter_funcs = OrderedDict()
        self.filter_descs = {}

    def __init__(self, application=None):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        self.chess_games = pd.read_csv(
            os.path.join(
                os.path.dirname(file_directory),
                "data/lichess_db_standard_rated_2013-11.csv",
            ),
            dtype=data.types,
        )
        self.main_layout = make_layout(self.chess_games)

        if application:
            self.app = application
        else:
            self.app = Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output("cls_init", "children"), Input("cls_init", "children")
        )(self.init_cls)

        self.app.callback(
            Output("graph", "figure"),
            inputs=[
                Input("x_drop_down", "value"),
                Input("y_drop_down", "value"),
                Input("filter_valid", "n_clicks"),
                Input("WhiteElo", "n_clicks"),
                Input("BlackElo", "n_clicks"),
                Input("TimeControl", "n_clicks"),
                Input("Opening", "n_clicks"),
                Input("cls_init", "children"),
            ],
        )(self.update_graph)

        self.app.callback(
            [
                Output("WhiteElo", "style"),
                Output("WhiteElo", "children"),
                Output("BlackElo", "style"),
                Output("BlackElo", "children"),
                Output("TimeControl", "style"),
                Output("TimeControl", "children"),
                Output("Opening", "style"),
                Output("Opening", "children"),
            ],
            inputs=[
                Input("filter_valid", "n_clicks"),
                Input("graph", "figure"),
                Input("WhiteElo", "n_clicks"),
                Input("BlackElo", "n_clicks"),
                Input("TimeControl", "n_clicks"),
                Input("Opening", "n_clicks"),
            ],
        )(self.update_active_filters)

        self.app.callback(
            Output("extracted_data", "children"),
            inputs=[
                Input("filter_valid", "n_clicks"),
                Input("graph", "figure"),
                Input("WhiteElo", "n_clicks"),
                Input("BlackElo", "n_clicks"),
                Input("TimeControl", "n_clicks"),
                Input("Opening", "n_clicks"),
            ],
        )(self.extract_data)

        self.app.callback(
            Output("filters", "options"),
            inputs=[
                Input("filter_valid", "n_clicks"),
                Input("graph", "figure"),
                Input("WhiteElo", "n_clicks"),
                Input("BlackElo", "n_clicks"),
                Input("TimeControl", "n_clicks"),
                Input("Opening", "n_clicks"),
            ],
        )(self.update_filters_opt)

        self.app.callback(
            [
                Output("start_value", "min"),
                Output("start_value", "max"),
                Output("start_value", "value"),
                Output("end_value", "min"),
                Output("end_value", "max"),
                Output("end_value", "value"),
                Output("fancy_slider", "min"),
                Output("fancy_slider", "max"),
                Output("fancy_slider", "value"),
                Output("time_drop_down", "options"),
                Output("opening_drop_down", "options"),
            ],
            inputs=[
                Input("filters", "value"),
                Input("filter_valid", "n_clicks"),
                Input("graph", "figure"),
                Input("start_value", "value"),
                Input("end_value", "value"),
                Input("fancy_slider", "value"),
            ],
            state=[
                State("start_value", "min"),
                State("start_value", "max"),
                State("time_drop_down", "options"),
                State("opening_drop_down", "options"),
            ],
        )(self.update_filter_selector_opt)

        self.app.callback(
            [
                Output("slider", "style"),
                Output("time", "style"),
                Output("opening", "style"),
                Output("filter_buttons", "style"),
                Output("filters", "value"),
            ],
            inputs=[
                Input("filters", "value"),
                Input("filter_cancel", "n_clicks"),
                Input("filter_valid", "n_clicks"),
            ],
        )(self.update_filter_selector)

        self.app.callback(
            [Output("filter_valid", "disabled"), Output("filter_valid", "style")],
            inputs=[
                Input("start_value", "value"),
                Input("end_value", "value"),
                Input("fancy_slider", "value"),
                Input("time_drop_down", "value"),
                Input("opening_drop_down", "value"),
                Input("filters", "value"),
            ],
        )(self.compute_filters)

    def update_filters_opt(self, dump1, dump2, dump3, dump4, dump5, dump6):
        available_filters = data.x_labels.copy()
        for filter in self.filter_funcs.keys():
            del available_filters[filter]

        return available_filters

    def update_active_filters(self, dump1, dump2, dump3, dump4, dump5, dump6):
        styles = [
            {"margin-right": "15px", "display": "None"},
            "Elo blancs: ",
            {"margin-right": "15px", "display": "None"},
            "Elo noirs: ",
            {"margin-right": "15px", "display": "None"},
            "Mode de jeu: ",
            {"margin-right": "15px", "display": "None"},
            "Ouverture: ",
        ]

        if not callback_context.triggered:
            return tuple(styles)

        for i, key in enumerate(data.x_labels.keys()):
            if key in self.filter_funcs.keys():
                styles[i * 2]["display"] = "block"
                styles[(i * 2) + 1] += self.filter_descs[key]

        return tuple(styles)

    def update_filter_selector_opt(
        self,
        selected_filter,
        dump1,
        dump2,
        start,
        end,
        slider,
        min,
        max,
        time_opt,
        open_opt,
    ):
        opts = [min, max, min, min, max, max, min, max, [min, max], time_opt, open_opt]
        if not callback_context.triggered:
            return opts

        caller_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        if caller_id == "filter_valid":
            return self.compute_drop_down_opt(opts)
        elif caller_id == "filters":
            return self.compute_slider_opt(selected_filter, opts)
        else:
            return self.compute_slider_val(start, end, slider, opts)

    def compute_drop_down_opt(self, opts):
        sorted_time = self.selected_games.sort_values(
            "TimeControl",
            key=lambda serie: [
                ut.to_int_list(format) for format in serie.str.split("+")
            ],
        )
        grp_by_time = sorted_time.groupby("TimeControl", sort=False)
        grp_by_time = ut.drop_smallest_grp(grp_by_time, "TimeControl")
        time_controls = list(grp_by_time.groups.keys())
        opts[9] = time_controls

        grp_by_opening = self.selected_games.groupby("Opening", sort=True)
        grp_by_opening = ut.drop_smallest_grp(grp_by_opening, "Opening")
        openings = list(grp_by_opening.groups.keys())
        opts[10] = openings
        return opts

    def compute_slider_opt(self, selected_filter, opts):
        if selected_filter is not None and selected_filter[-3:] == "Elo":
            min = self.selected_games[selected_filter].min()
            min = min - min % 100
            max = self.selected_games[selected_filter].max()
            max = max + 100 - max % 100
            opts = [min, max, min, min, max, max, min, max, [min, max]] + opts[9:]

        return opts

    def compute_slider_val(self, start, end, slider, opts):
        trigger_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        start_value = start if trigger_id == "start_value" else slider[0]
        end_value = end if trigger_id == "end_value" else slider[1]
        opts[2] = min(start_value, end_value)
        opts[5] = max(start_value, end_value)

        opts[2] = opts[0] if opts[2] < opts[0] else opts[2]
        opts[5] = opts[4] if opts[5] > opts[4] else opts[5]

        if opts[5] - opts[2] < 100:
            opts[5] += opts[5] < opts[4]
            opts[2] -= opts[5] >= opts[4]

            new_end = opts[5] + 100 - opts[5] % 100
            if new_end <= opts[4]:
                opts[5] = new_end
            else:
                opts[2] -= opts[2] % 100

        opts[8] = slider if trigger_id == "fancy_slider" else [opts[2], opts[5]]

        return opts

    def update_filter_selector(self, selected_filter, dump1, dump2):
        styles = [
            {"display": "None"},
            {"display": "None"},
            {"display": "None"},
            {"display": "None"},
            selected_filter,
        ]
        self.selected_filter = selected_filter
        trigger = callback_context.triggered
        if (
            not trigger
            or trigger[0]["prop_id"] == "filter_cancel.n_clicks"
            or trigger[0]["prop_id"] == "filter_valid.n_clicks"
        ):
            styles[4] = None
            return tuple(styles)

        styles[3]["display"] = "block"
        if selected_filter[-3:] == "Elo":
            styles[0]["display"] = "block"
        elif selected_filter == "TimeControl":
            styles[1]["display"] = "block"
        elif selected_filter == "Opening":
            styles[2]["display"] = "block"

        return tuple(styles)

    def extract_data(self, dump1, dump2, dump3, dump4, dump5, dump6):
        datas = data.datas_dict.copy()

        grp_by_opening = self.selected_games.groupby("Opening")
        grp_by_opening = ut.drop_smallest_grp(grp_by_opening, "Opening")
        most_used_opening = ut.get_largest_grp(grp_by_opening)

        to_str = lambda rates, desc: "{} ( {} % {} )".format(
            rates.idxmax(), int(round(rates.max())), desc
        )
        w_winrates = ut.compute_rate(grp_by_opening, "1-0", "0-1", "Result")
        datas["Opening"][1]["White"][1] = to_str(w_winrates, "de victoires")
        b_winrates = ut.compute_rate(grp_by_opening, "0-1", "1-0", "Result")
        datas["Opening"][1]["Black"][1] = to_str(b_winrates, "de victoires")
        drawrates = ut.compute_rate(grp_by_opening, "1/2-1/2", ["0-1", "1-0"], "Result")
        datas["Opening"][1]["Draw"][1] = to_str(drawrates, "d'égalités")
        timerates = ut.compute_rate(grp_by_opening, "Time forfeit", None, "Termination")
        datas["Opening"][1]["Time"][1] = to_str(timerates, "des parties")
        playedrate = round((most_used_opening[1] / self.selected_games.shape[0]) * 100)
        moststr = f"{most_used_opening[0]} ( {int(playedrate)} % des parties )"
        datas["Opening"][1]["Most"][1] = moststr

        grp_by_control = self.selected_games.groupby("TimeControl")
        grp_by_control = ut.drop_smallest_grp(grp_by_control, "TimeControl")
        most_used_control = ut.get_largest_grp(grp_by_control)

        w_winrates = ut.compute_rate(grp_by_control, "1-0", "0-1", "Result")
        datas["TimeControl"][1]["White"][1] = to_str(w_winrates, "de victoires")
        b_winrates = ut.compute_rate(grp_by_control, "0-1", "1-0", "Result")
        datas["TimeControl"][1]["Black"][1] = to_str(b_winrates, "de victoires")
        drawrates = ut.compute_rate(grp_by_control, "1/2-1/2", ["0-1", "1-0"], "Result")
        datas["TimeControl"][1]["Draw"][1] = to_str(drawrates, "d'égalités")
        timerates = ut.compute_rate(grp_by_control, "Time forfeit", None, "Termination")
        datas["TimeControl"][1]["Time"][1] = to_str(timerates, "des parties")
        playedrate = round((most_used_control[1] / self.selected_games.shape[0]) * 100)
        moststr = f"{most_used_control[0]} ( {int(playedrate)} % des parties )"
        datas["TimeControl"][1]["Most"][1] = moststr

        return [ut.to_html_list(datas)]

    def compute_filters(self, dump1, dump2, elo_range, time_control, opening, dump3):
        trigger = callback_context.triggered
        button_style = valid_button_style.copy()

        id = trigger[0]["prop_id"].split(".")[0]
        if id == "filters":
            button_style["border-color"] = "gray"
            button_style["color"] = "gray"
            return True, button_style

        if id == "start_value" or id == "end_value" or id == "fancy_slider":
            column = self.selected_filter
            current_filter = lambda elm: elo_range[0] <= elm[column] <= elo_range[1]
            filter_desc = str(elo_range)
        elif id == "time_drop_down":
            current_filter = lambda elm: elm["TimeControl"] == time_control
            filter_desc = time_control
        else:
            current_filter = lambda elm: elm["Opening"] == opening
            filter_desc = opening

        self.current_filter = (self.selected_filter, current_filter, filter_desc)
        return False, button_style

    def update_graph(self, x_axis, y_axis, dump1, dump2, dump3, dump4, dump5, dump6):
        trigger = callback_context.triggered
        if x_axis is None or y_axis is None:
            return self.graph

        if trigger:
            id = trigger[0]["prop_id"].split(".")[0]
            if id in data.x_labels.keys():
                del self.filter_funcs[id]
                del self.filter_descs[id]
                self.on_filter_change()
            elif id == "filter_valid":
                filter, func, desc = self.current_filter
                self.filter_funcs[filter] = func
                self.filter_descs[filter] = desc
                self.on_filter_change()

        init_trigger = not trigger or trigger[0]["prop_id"] == "cls_init.children"
        if init_trigger or trigger[0]["prop_id"] == "x_drop_down.value":
            self.x_axis = x_axis
            self.compute_x()

            if self.plot_method != "scatter":
                self.grp_by_x = ut.drop_smallest_grp(
                    self.grp_by_x, self.x_axis, self.x_selector
                )

        if init_trigger or trigger[0]["prop_id"] == "y_drop_down.value":
            self.y_axis = y_axis

        self.graph = self.compute_plot()
        return self.graph

    def on_filter_change(self):
        self.selected_games = self.chess_games.copy()
        for filter_func in self.filter_funcs.values():
            self.selected_games = self.selected_games[
                self.selected_games.apply(filter_func, axis=1)
            ]

        self.compute_x()
        if self.plot_method != "scatter":
            self.grp_by_x = ut.drop_smallest_grp(
                self.grp_by_x, self.x_axis, self.x_selector
            )

    def compute_x(self):
        self.x_selector = self.x_axis
        self.x_mapper = lambda x: x
        self.plot_method = "bar"
        self.grp_by_x = self.selected_games.groupby(self.x_selector)

        if self.x_axis[-3:] == "Elo":
            cut_range = ut.compute_range(self.selected_games, self.x_axis, 5)
            self.x_selector = pd.cut(self.selected_games[self.x_axis], cut_range)
            self.x_mapper = lambda interval: int(round(interval.mid))
            self.plot_method = "scatter"
            self.grp_by_x = self.selected_games.groupby(self.x_selector)

        elif self.x_axis == "TimeControl":
            sorted_controls = self.selected_games.sort_values(
                "TimeControl",
                key=lambda serie: [
                    ut.to_int_list(format) for format in serie.str.split("+")
                ],
            )
            self.grp_by_x = sorted_controls.groupby(self.x_axis, sort=False)

        elif self.x_axis != "Opening":
            raise ValueError(self.x_axis, "is an unknown x axis selector")

    def compute_y(self):
        if self.y_axis[-7:] == "Winrate":
            color = self.y_axis[:-7]
            color_win = "1-0" if color == "White" else "0-1"
            winrates = ut.compute_rate(
                self.grp_by_x, color_win, color_win[::-1], "Result"
            )
            self.plot_data = winrates.rename(self.y_axis).round(2).reset_index()
            self.y_range = [-5, 105]

        elif self.y_axis == "TimeTermination":
            timerates = ut.compute_rate(
                self.grp_by_x, "Time forfeit", None, "Termination"
            )
            self.plot_data = timerates.rename(self.y_axis).round(2).reset_index()
            self.y_range = [-5, 105]

        else:
            raise ValueError(self.y_axis, "is an unknown y axis selector")

    def compute_plot(self):
        self.compute_y()
        self.plot_data[self.x_axis] = self.plot_data[self.x_axis].apply(self.x_mapper)
        figure = data.methods_dict[self.plot_method](
            self.plot_data,
            x=self.x_axis,
            y=self.y_axis,
            labels={
                self.x_axis: data.x_labels[self.x_axis],
                self.y_axis: data.y_labels[self.y_axis],
            },
        )
        figure.update_yaxes(range=self.y_range)
        return figure


if __name__ == "__main__":
    chs = Chess()
    chs.app.run_server(debug=True, port="8051")
