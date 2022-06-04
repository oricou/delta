from typing import OrderedDict
import plotly.express as px

max_grps_nb = 30

types = {
    "Event": "string",
    "Site": "string",
    "Round": "string",
    "Date": "string",
    "White": "string",
    "Black": "string",
    "Result": "string",
    "UTCDate": "string",
    "UTCTime": "string",
    "WhiteElo": "float64",
    "BlackElo": "float64",
    "WhiteRatingDiff": "float64",
    "BlackRatingDiff": "float64",
    "ECO": "string",
    "Opening": "string",
    "TimeControl": "string",
    "Termination": "string",
    "BlackTitle": "string",
    "WhiteTitle": "string",
    "Moves": "string",
}


methods_dict = {"scatter": px.scatter, "bar": px.bar}

datas_dict = OrderedDict(
    [
        (
            "Opening",
            (
                "Ouvertures: ",
                OrderedDict(
                    [
                        ("White", ["La plus favorable aux blancs: ", None]),
                        ("Black", ["La plus favorable aux noirs: ", None]),
                        ("Draw", ["Celle qui fait le plus d'égalité: ", None]),
                        (
                            "Time",
                            [
                                "Celle qui fait le plus de parties se finissant au temps: ",
                                None,
                            ],
                        ),
                        ("Most", ["La plus jouée: ", None]),
                    ]
                ),
            ),
        ),
        (
            "TimeControl",
            (
                "Modes de jeu: ",
                OrderedDict(
                    [
                        ("White", ["Le plus favorable aux blancs: ", None]),
                        ("Black", ["Le plus favorable aux noirs: ", None]),
                        ("Draw", ["Celui qui fait le plus d'égalité: ", None]),
                        (
                            "Time",
                            [
                                "Celui qui fait le plus de parties se finissant au temps: ",
                                None,
                            ],
                        ),
                        ("Most", ["Le plus joué: ", None]),
                    ]
                ),
            ),
        ),
    ]
)

x_labels = {
    "WhiteElo": "Classement des blancs",
    "BlackElo": "Classement des noirs",
    "TimeControl": "Mode de jeu",
    "Opening": "Ouverture utilisée",
}

y_labels = {
    "WhiteWinrate": "Pourcentage de victoire des blancs",
    "BlackWinrate": "Pourcentage de victoire des noirs",
    "TimeTermination": "Pourcentage de partie finies au temps",
}
