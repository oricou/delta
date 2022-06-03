from MDMR_NYPDCallsMeteoNY.helpers.utils import (
    load_calls_correlation_data,
    load_weather_data,
    remove_outliers,
)

from MDMR_NYPDCallsMeteoNY.helpers.design import (
    background_color,
    font_color,
    font_family,
    color_blue,
    color_green,
)

import plotly.express as px

calls = load_calls_correlation_data()
weather = load_weather_data()


def display_correlation_scatter(freq="M", size_value=0):
    nb_calls = remove_outliers(calls.resample(freq).size())
    tavg = remove_outliers(weather.tavg.resample(freq).mean())
    prcp = remove_outliers(weather.prcp.resample(freq).mean())
    wspd = remove_outliers(weather.wspd.resample(freq).mean())

    size_values = [prcp, wspd]
    hover_text = ["mm de précipitation", "km/h de vent"]

    fig = px.scatter(
        x=tavg,
        y=nb_calls,
        size=size_values[size_value],
        color_discrete_sequence=[color_blue],
        trendline_color_override=color_green,
    )

    fig.update_traces(
        hovertemplate="Température: %{x}°C<br>%{y} appels<br>%{marker.size:.2f}"
        + hover_text[size_value]
    )

    frequency = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    fig.update_xaxes(title_text=f"Température moyenne par {frequency}")
    fig.update_yaxes(title_text=f"Nombre d'appels par {frequency}")

    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
