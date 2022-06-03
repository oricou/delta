import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from MDMR_NYPDCallsMeteoNY.helpers.design import background_color, font_color, font_family, color_green, color_blue
from MDMR_NYPDCallsMeteoNY.helpers.utils import load_calls_correlation_data, load_weather_data

calls = load_calls_correlation_data()
weather = load_weather_data()


class DataManager:
    dataframe = {}
    max_size = {}
    weather_data = {}


def types_of_calls(freq="M", value=None):
    data = DataManager.dataframe.get(freq)
    weather_data = DataManager.weather_data.get(freq)

    if data is None:
        data = (
            calls.groupby(["desc", 'date'])
                .size()
                .reset_index(0)
                .groupby(["desc"])
                .resample(freq)
                .sum()
                .reset_index(0)
                .rename(columns={0: "number"})
        )

        weather_data = weather.tavg.resample(freq).mean()

        DataManager.max_size[freq] = data.number.max()
        DataManager.dataframe[freq] = data
        DataManager.weather_data[freq] = weather_data

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data.loc[value].desc,
                         y=data.loc[value].number,
                         marker_color=px.colors.qualitative.Plotly,
                         name="Catégories",
                         hovertemplate="%{y} appels pour '%{x}'"), secondary_y=False)

    fig.add_trace(go.Scatter(x=weather_data.index,
                             y=weather_data,
                             line_color=color_green,
                             line_width=0.8,
                             name="Température",
                             hovertemplate="%{y}°C le %{x:%d/%m/%y}"), secondary_y=True)

    fig.add_vline(x=value, line_color=color_green, line_width=0.8, secondary_y=True)

    fig.data[1].update(xaxis='x2')
    fig.layout.shapes[0].xref = 'x2'

    # Set x-axis title
    fig.update_xaxes(title_text="Catégories")

    frequency = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    # Set y-axes titles
    fig.update_yaxes(title_text=f"Nombre d'appels par {frequency}", secondary_y=False)
    fig.update_yaxes(title_text=f"Température moyenne par {frequency}", secondary_y=True)

    fig.update_layout(
        xaxis2={'anchor': 'y', 'overlaying': 'x', 'side': 'top'},
        yaxis_domain=[0, 0.94],
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        yaxis_range=[0, DataManager.max_size[freq]],
        legend=dict(yanchor="top", y=0.94, xanchor="left", x=0.01),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
