import plotly.graph_objects as go
from plotly.subplots import make_subplots
from MDMR_NYPDCallsMeteoNY.helpers.utils import (
    load_weather_data,
    load_calls_correlation_data,
    remove_outliers,
)

from MDMR_NYPDCallsMeteoNY.helpers.design import (
    background_color,
    font_color,
    font_family,
    color_blue,
    color_green,
)


calls = load_calls_correlation_data()
weather = load_weather_data()


def display_correlation_plot(freq="M"):
    nb_calls = remove_outliers(calls.resample(freq).size())
    avg = remove_outliers(weather.tavg.resample(freq).mean())

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=nb_calls, line_color=color_blue, name="Appels",
                   hovertemplate="%{y} appels le %{x:%d/%m/%y}"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=nb_calls.index, y=avg, line_color=color_green, name="Température",
                   hovertemplate="%{y}°C le %{x:%d/%m/%y}"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        margin=dict(l=10, r=10, b=10, t=50, pad=2),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    frequency = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    # Set y-axes titles
    fig.update_yaxes(
        title_text=f"Nombre d'appels par {frequency}", secondary_y=False)
    fig.update_yaxes(
        title_text=f"Température moyenne par {frequency}", secondary_y=True
    )

    return fig
