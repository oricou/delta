import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html


class Presidentielles():
    def __init__(self, application=None):

        # ------------------------------------------ #
        # Création des figures pour les sondages
        # ------------------------------------------ #

        # Figure tour 1
        # Lecture du dataset
        df = pd.read_csv('./presidentielle/data/sondages_tour_1.csv')

        fig_sond_t1 = px.line(df, y="intentions", x="date_enquete", color="candidat",
                              title='Sondage en vu du premier tous des présidentielles par candidat',
                              labels={
                                  "intentions": "Intentions de vote",
                                  "date_enquete": "Temps",
                                  "candidat": "Candidats"
                              })

        # Figure tour 2
        # Lecture du dataset
        df = pd.read_csv('./presidentielle/data/sondages_tour_2.csv')
        df_lepen = df[df["candidat"] == "Marine Le Pen"]
        df_macron = df[df["candidat"] == "Emmanuel Macron"]

        fig_sond_t2 = go.Figure()
        fig_sond_t2.add_trace(go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["intentions"], name="Marine Le Pen",
                                         line=dict(color='royalblue', width=2)))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["erreur_sup"], name="Erreur Sup : Marine Le Pen",
                       line=dict(color='royalblue', width=2, dash='dash')))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["erreur_inf"], name="Erreur Inf : Marine Le Pen",
                       line=dict(color='royalblue', width=2, dash='dot')))


        df_macron["res"] = 58.5
        fig_sond_t2.add_trace(go.Scatter(x=df_macron["date_enquete"], y=df_macron["intentions"], name="Emmanuel Macron",
                                         line=dict(color='firebrick', width=2)))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_macron["date_enquete"], y=df_macron["erreur_sup"], name="Erreur Sup : Emmanuel Macron",
                       line=dict(color='firebrick', width=2, dash='dash')))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_macron["date_enquete"], y=df_macron["erreur_inf"], name="Erreur Inf : Emmanuel Macron",
                       line=dict(color='firebrick', width=2, dash='dot')))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_macron["date_enquete"], y=df_macron["res"], name="Res : Emmanuel Macron",
                       line=dict(color='green', width=1, dash='dot')))
        df_lepen["res"] = 41.45
        fig_sond_t2.add_trace(
            go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["res"], name="Res : Marine Le Pen",
                       line=dict(color='red', width=1, dash='dot')))

        fig_sond_t2.update_layout(title='Sondages présidentiels du second tour avec prise en compte de l\'erreur',
                                  xaxis_title='Temps',
                                  yaxis_title='Pourcentage de vote')

        # --------------------------------------------- #
        # Création des figures pour le temps de parole
        # --------------------------------------------- #

        # Lecture du dataset
        df_tdp = pd.read_csv('./presidentielle/data/temps_de_parole_presidentielles_2022.csv')

        # Figure tour 1
        df_tdp = pd.read_csv('./presidentielle/data/temps_de_parole_presidentielles_2022.csv')
        self.df_tdp = df_tdp
        # Figure tour 2
        fig_tdp_t2 = px.bar(df_tdp[(df_tdp['Période'] == '2022-04-08') & (
                (df_tdp['Candidat'] == 'Macron') | (df_tdp['Candidat'] == 'Lepen'))], x='Candidat', y="Somme",
                            color='Chaîne', barmode="group", labels={
                "Période": "Temps en jours",
                "Somme": "Temps de parole en minutes",
                "Chaîne": "Chaînes",
                "Candidat": "Candidats"
            }, title="Temps de parole pour chaque candidats en fonction des médias")

        fig_tdp_cum = px.bar(df_tdp[df_tdp['Période'].isin(['2022-03-27', '2022-04-03', '2022-04-08'])], x='Candidat',
                             y="Somme",
                             color='Chaîne', labels={
                "Période": "Temps en jours",
                "Somme": "Temps de parole en minutes",
                "Chaîne": "Chaînes",
                "Candidat": "Candidats"
            },
                             title="Temps de parole cumulés sur tous les médias pour chaque candidat. Durant la période officiele de campagne")

        self.main_layout = html.Div(children=[
            html.H2(children='Sondages présidentiels et temps de parole dans les médias'),
            html.H3(children='Premier tour'),
            html.Div(
                [dcc.Graph(id='sond_t1', figure=fig_sond_t1)], style={'width': '100%', }),
            dcc.Markdown("""
             ##### Notes :
             - L'arrivée de certains candidats fait perdre des voix à certains qu'ils ne regagneront jamais même 
             si le candidat n'est se retire de la présidentielle (Mme Taubira et M. Jadot)
             - Mme Le Pen et M. Mélenchon sont monté dans les sondages sur les 2 dernières semaines et ont fait 
             perdre des voix aux autres candidats
            """),
            html.Div(
                [dcc.Graph(id='bar-with-slider'),
                 dcc.Slider(id='bar_slider', step=None,
                            marks={
                                0: '2022-03-13',
                                1: '2022-03-20',
                                2: '2022-03-27',
                                3: '2022-04-03',
                                4: '2022-04-08',
                            },
                            value=0),
                 ], style={'width': '100%', }),
            dcc.Markdown(""" 
            ##### Notes :
            - Certains médias parlent beaucoup plus des élections présidentielles que d'autres
            - Le temps de parole totale des candidats dans les médias ne reflète pas leur passage ou non au second tour 
            (Mme Le Pen a passé beaucoup moins de temps dans les médias que Mme Pecresse et a pourtant accédé au second tour)
            - Plus on se rapproche du vote plus les médias essayent de données un temps de parole
            équitable aux candidats
            """),
            html.Div(
                [dcc.Graph(id='sond_t1_cum', figure=fig_tdp_cum)], style={'width': '100%', }),
            dcc.Markdown("""
                     ##### Notes :
                     - Les candidats n'ont pas un temps de parole équitable
                     - Des candidats sont sur représenté par rapport à leur score final et d'autres sont sous représentés 
                     par rapport à leur score final
                    """),
            html.H3(children='Second tour'),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig_sond_t2)], style={'width': '100%', }),
            dcc.Markdown("""
             ##### Notes :
             - Les sondages datant d'avant le second tour sont les sondages qui représentent les 
             intentions de vote opposants Mme Le Pen et M. Macron
             - Mme Le Pen et M. Macron ont toujours été très proches au niveau des sondages
             - Sur la période du second tour et en prenant en comptent les erreurs de sondages 
             Mme Le Pen est passé devant M. Macron plusieurs fois
            """),
            html.Div(
                [dcc.Graph(id='dtp_t2', figure=fig_tdp_t2)], style={'width': '100%'}),
            dcc.Markdown("""
             ##### Notes :
             - Les deux candidats du second tour n'ont pas été représentés équitablement durant la période de l'entre-deux tours
             - Certains médias représentent plus M. Macron et d'autres Mme. Le Pen
            """),
            html.Br(),
            html.H3(children='À propos'),
            dcc.Markdown(""" 
                        * Données sondages : [Nsppolls](https://github.com/nsppolls/nsppolls/blob/master/presidentielle.csv)
                        * Données temps de parole : [CSA](https://www.csa.fr/Proteger/Garantie-des-droits-et-libertes/Proteger-le-pluralisme-politique/La-presidentielle-2022)
                        * (c) 2022 Guillaume Larue et Enguerrand de Gentile Duquesne
                        """),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('bar-with-slider', 'figure'),
            dash.dependencies.Input('bar_slider', 'value'))(self.update_graph)

    def update_graph(self, selected_date):
        date_tmp = ['2022-03-13', '2022-03-20', '2022-03-27', '2022-04-03', '2022-04-08']
        filtered_df = self.df_tdp[self.df_tdp['Période'] == date_tmp[selected_date]]

        fig = px.bar(filtered_df, x='Candidat', y="Somme",
                     color='Chaîne', barmode="group",
                     labels={
                         "Période": "Temps en jours",
                         "Somme": "Temps de parole en minutes",
                         "Chaîne": "Chaînes",
                         "Candidat": "Candidats"
                     }, title="Temps de parole pour chaque candidats en fonction des médias")

        fig.update_layout(transition_duration=500)

        return fig


if __name__ == '__main__':
    mpj = Presidentielles()
    mpj.app.run_server(debug=True, port=8051)
