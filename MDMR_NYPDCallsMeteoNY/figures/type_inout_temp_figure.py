from MDMR_NYPDCallsMeteoNY.helpers.utils import load_calls_correlation_data
import plotly.express as px
from MDMR_NYPDCallsMeteoNY.helpers.design import background_color, font_color, font_family, color_blue

calls = load_calls_correlation_data()


class DataManager:
    dataframe = {}
    max_size = {}


def in_out_of_calls(freq="M", value=None):
    data = DataManager.dataframe.get(freq)

    if data is None:
        data = (
            calls.groupby(["place", 'date'])
            .size()
            .reset_index(0)
            .groupby(["place"])
            .resample(freq)
            .sum()
            .reset_index(0)
            .rename(columns={0: "number"})
        )

        DataManager.max_size[freq] = data.number.max()
        DataManager.dataframe[freq] = data

    fig = px.bar(data.loc[value], x="place", y="number", color='place')

    fig.update_traces(hovertemplate="Lieu: %{x}<br>%{y:.2f} appels")

    frequency = "mois" if freq == "M" else "semaine" if freq == "W" else "jour"

    fig.update_yaxes(title_text=f"Nombre d'appels par {frequency}")
    fig.update_xaxes(title_text="Lieux")

    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, DataManager.max_size[freq]],
        margin=dict(l=10, r=10, b=10, t=50, pad=4),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        autosize=True,
        font_family=font_family,
        font_color=font_color,
    )

    return fig
