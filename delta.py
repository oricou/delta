import re
import dash
import flask
from dash import dcc
from dash import html
from energies import energies
from population import population
from deces import deces
from MC_AB_consommationEtProductionEnergétique import petrole
from SG_AH_pollution_des_transports import pollution
from pbmc_accidents_routiers import pbmc_accidents_routiers as pbmc
from APTT_olympic import olympics
from YA_CDL_Energy_generation import Energy_generation
from EVHB_velib import velib
from kkhj_happinessPerceptionReality import happinessPerceptionReality
from mzgl_inegalites_de_revenus import mzgl_inegalites_de_revenus
from ARPA_inequality_per_political_party import inequalities
from ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe import environment
from MDMR_NYPDCallsMeteoNY import NYPD_dash_visualisation as NYWeather
from ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant import pollution
from phllhlv_emissionglobalwarming import global_warming
from tdmr_quality_of_life_and_worktime import tdmr_quality_of_life_and_worktime as tdmr
from strl_EvolutionDesSalairesAnnuelsMoyens import income
from cerg_cancer import cancer
from ACJW_MusicPopularityFactor import Music
from RCNT_sujetTelevise import sujetTelevise
from ym_jf_energy_mix import energymix
from afhy_electricite import electricite
from NINL_Impact_de_lexposition_aux_particules_fines_face_a_celui_de_la_pollution_sur_lesperance_de_vie_en_europe import impact
from ps_ap_chessgames.src import chess
from JD_NJ_Etude_de_la_pollution import dash_app_pollution
from ybjd_deces_en_france_selon_le_revenu_par_departement import ybjd_deces_en_france_selon_le_revenu_par_departement as ybjd
from TA_MG_SpotifyMusicPopularity import spotify
from aa_sc_metacritic import metacritic
from TBGP_salaires_inflation import app as tbgp_si_lib
from EFEB_Etude_sur_levolution_des_retards_TGV_depuis_2018 import chart as EFEB_chart, map as EFEB_map
from jcwg_naissance_deces import naissance_deces
from YBYB_Analyse_football import football
from avel_top_100_billboard_usa import top_100_billboard_usa
from abih import abih
from TBGT_population_vs_train_speed import TBGT_population_vs_train_speed as tbgt_lib
from postbac import postbac
from presidentielle import presidentielle
from EC_CD_Evolution_des_Mariages_en_France import mariages_en_France as md_lib
from ma_aj_netflix import netflix
from TFRT_obesity import obesity_calories
from hcbjbd_Deces_dans_le_monde_classe_par_cause import deathanalysis
from lmsb_animalcrossing import lmsb_animalcrossing as ac
from SM_HB_accidents import accidents
from parrainage import parrainage
from tpmm_RGPD import RGPD
#from bars import bars
from companies import companies
from dc_sujet import covid_basics
from rbmb_electricityVSgaz import electricityVSgaz
from NHAJ_BMO_and_attractive_zone import bmo
from lptr_radar_accidents import radar_accidents
from tc_urban import urban
from __LeagueOfLegendsChampionsStats import champs_win_rate
from fwgp_formations import formations as formations_lib
from APAAL_criminalite_education import criminalite_education
from ADHD_Movies import movies
from pgab_accidents import accidents as pgab_accidents
from ab_wg_apb_parcoursup import apb_parcoursup
from ARLP_film_success_throughout_years_by_genre_1970_2020 import filmsuccess
from AMEG_vaccination import AMEG_vaccination
from PMPR_WineStats import dataAnalysis
from mf_nc_guerre_ukraine import ukraine
from corporate_impact import corp_impact
from HH_MT_Etude_population_française import dash_pop
# from MP_pib import pib

#@profile
def init():
    app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
    server = app.server
    pop = population.WorldPopulationStats(app)
    dec = deces.Deces(app)
    nrg = energies.Energies(app)
    pm =  pbmc.Pbmc(app)
    oly = olympics.Olympic(app)
    eeg = Energy_generation.EuropeEnergyGeneration(app)
    vel = velib.Velib(app)
    hap = dec # happinessPerceptionReality.HappinessPerceptionReality(app)
    ine_rev = mzgl_inegalites_de_revenus.Inegalites_de_revenus(app)
    alvs = environment.EuropeanEnvironmentStudies(app)
    nypd_weather = NYWeather.MDMR_NYPDCallsMeteoNY(app)
    globalwarming = global_warming.GlobalWarming(app)
    td = tdmr.Tdmr(app)
    pet = dec # petrole.Petrole(app)
    inc = income.Income(app)
    pol = pollution.Pollution(app)
    cncr = cancer.Cancer(app)
    mus = Music.Song(app)
    ine_gini = inequalities.Inequalities(app)
    suj = sujetTelevise.TvSubject(app)
    nrgmix = energymix.EnergyMix(app)
    ele = electricite.Eletricite(app)
    imp = impact.Impact(app)
    chs = chess.Chess(app)
    pol = dash_app_pollution.PollutionFrancaise(app)
    drd = ybjd.DecesFranceRevenu(app)
    spo = spotify.Spotify(app)
    meta = metacritic.Metacritic(app)
    tbgp_si = tbgp_si_lib.SalaryInflation(app)
    jcwg_nd = naissance_deces.Naissance(app)
    foot = football.Football(app)
    billboard = top_100_billboard_usa.Top100BillboardUSA(app)
    meteor = abih.Abih(app)
    tbgt = dec # tbgt_lib.TBGT(app)
    psb = postbac.PostBac(app)
    pres = presidentielle.Presidentielles(app)
    md = md_lib.Mariage(app)
    net = netflix.NetflixStats(app)
    obcal = obesity_calories.Obesity_calories(app)
    ana = deathanalysis.DeathAnalysis(app)
    ani = ac.Animal(app)
    tgv1 = EFEB_chart.Chart(app)
    acc = accidents.Accidents(app)
    par = parrainage.Parrainage(app)
    rgpd = RGPD.RGPD(app)
    bar = dec # bars.Bars(app)
    comp = companies.FrenchCompaniesStats(app)
    covid = covid_basics.CovidBasics(app)
    elcVgaz = electricityVSgaz.Stats(app)
    bmo_ = dec # bmo.Bmo(app)
    rd_acc = radar_accidents.Radar_Accidents(app)
    urb = urban.UrbanPolutionStats(app)
    lol = champs_win_rate.ChampWinRate(app)
    for_sup = formations_lib.Formations(app)
    crim_edu = criminalite_education.Criminalite_Education(app)
    mvs = movies.MoviesStats(app)
    pgab_acc = pgab_accidents.Accidents(app)
    apb = apb_parcoursup.APB_PARCOURSUP(app)
    filmsuc = filmsuccess.FilmSuccess(app)
    vac = AMEG_vaccination.Vaccinations(app)
    wine = dataAnalysis.WineStats(app)
    ukr = ukraine.Ukraine(app)
    c_i = corp_impact.CorporateImpact(app)
    popfr = dash_pop.Population(app)
    # pint = pib.Pib(app)

    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    main_layout = html.Div([
        html.Div(className = "row",
                 children=[ 
                     dcc.Location(id='url', refresh=False),
                     html.Div(className="two columns",
                              children = [
                                  html.Center(html.H2("Δelta δata")),
                                  dcc.Link(html.Button("Prix d'énergies", style={'width':"100%"}), href='/energies'),
                                  dcc.Link(html.Button('Natalité vs revenus', style={'width':"100%"}), href='/population'),
                                  dcc.Link(html.Button('Décès journaliers', style={'width':"100%"}), href='/deces'),
                                  dcc.Link(html.Button('MDMR_NYPDCallsMeteoNY', style={'width':"100%"}), href='/MDMR_NYPDCallsMeteoNY'),
                                  dcc.Link(html.Button('Accident Routiers', style={'width':"100%", 'margin':0, 'padding': 0}), href='/accidents_routiers'),
                                  dcc.Link(html.Button('Accidents de la route', style={'width':"100%"}), href='/pgab_accidents'),
                                  dcc.Link(html.Button('Médailles Olympique', style={'width': "100%"}), href='/olympics'),
                                  dcc.Link(html.Button("Génération d'énergie UE", style={'width':"100%"}), href='/Energy_generation'),
                                  dcc.Link(html.Button('Utilisation Vélibs', style={'width':"100%"}), href='/EVHB_velib'),
                                  dcc.Link(html.Button('Conception du bonheur', style={'width':"100%"}), href='/bonheur'),
                                  dcc.Link(html.Button('Inégalités de revenus', style={'width':"100%"}), href='/mzgl_inegalites'),
                                  dcc.Link(html.Button('Politique et Environnement', style={'width':"100%"}), href='/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe'),
                                  dcc.Link(html.Button('Polutions/Pétroles', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Global Warming', style={'width':"100%"}), href='/global_warming'),
                                  dcc.Link(html.Button('impact temps de travail', style={'width':"100%", 'padding':'inherit'}), href='/travail'),
                                  dcc.Link(html.Button('Pétrole en Europe', style={'width':"100%"}), href='/petrole'),
                                  dcc.Link(html.Button('Evolution des salaires', style={'width':"100%", 'padding':'inherit'}), href='/salaires'),
                                  dcc.Link(html.Button('Pollution des transports', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Répartition des cancers', style={'width':"100%"}), href='/cancer'),
                                  dcc.Link(html.Button('Popularité des musiques', style={'width':"100%"}), href='/music'),
                                  dcc.Link(html.Button('Inégalités en Europe', style={'width':"100%"}), href='/inequality'),
                                  dcc.Link(html.Button('Sujet tv', style={'width':"100%"}), href='/sujetTV'),
                                  dcc.Link(html.Button('Electricité monde', style={'width':"100%"}), href='/energymix'),
                                  dcc.Link(html.Button("Électricité", style={'width':"100%"}), href='/electricite'),
                                  dcc.Link(html.Button('Espérance de vie vs pollution', style={'width':"100%"}), href='/impact'),
                                  dcc.Link(html.Button("Parties d'échecs", style={"width": "100%"}), href="/chess"),
                                  dcc.Link(html.Button('Etude de la pollution', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Décès selon le revenu', style={'width':"100%"}), href='/ybjd_deces_en_france_selon_le_revenu_par_departement'),
                                  dcc.Link(html.Button('Popularité des musiques', style={'width':"100%"}), href='/spotify'),
                                  dcc.Link(html.Button('Analyse Metacritic', style={'width':"100%"}), href='/aa_sc_metacritic'),
                                  dcc.Link(html.Button('Salaires / inflation', style={'width':"100%"}), href='/tbgp-salaires-inflation'),
                                  dcc.Link(html.Button('Naissances et décès', style={'width':"100%"}), href='/jcwg_naissance_deces'),
                                  dcc.Link(html.Button("Football Classement, Age, €", style={'width':"100%"}), href='/football'),
                                  dcc.Link(html.Button('Top 100 Billboard USA', style={'width':"100%"}), href='/usa_billboard'),
                                  dcc.Link(html.Button('Les météorites', style={'width':"100%"}), href='/meteor'),
                                  dcc.Link(html.Button("Retards des TGVs depuis 2018", style={"width": "100%"}), href="/efeb_tgv_1",),
                                  dcc.Link(html.Button('Population vs Grandes Lignes', style={'width':"100%", 'margin':0, 'padding': 0}), href='/population_vs_train_speed'),
                                  dcc.Link(html.Button('Postbac', style={'width':"100%"}), href='/postbac'),
                                  dcc.Link( html.Button('Présidentielle', style={'width': "100%", 'margin-bottom': '5px'}), href='/presidentielle'),
                                  dcc.Link(html.Button('Mariages', style={'width':"100%"}), href='/EC_DC_Evolution_des_Mariages_en_France'),
                                  dcc.Link(html.Button('Popularité vs sensibilité', style={'width':"100%"}), href='/netflix'),
                                  dcc.Link(html.Button('Lien obésité/calories', style={'width':"100%"}), href='/TFRT_obesity'),
                                  dcc.Link(html.Button('Analyse des Décès', style={'width':"100%"}), href='/deathanalysis'),
                                  dcc.Link(html.Button('Animal Crossing', style={'width':"100%"}),href='/lmsb_animalcrossing'),
                                  dcc.Link(html.Button("Accidents routiers", style={'width':"100%"}), href='/accidents'),
                                  dcc.Link(html.Button('Parrainage', style={'width':"100%"}), href='/parrainage'),
                                  dcc.Link(html.Button('tpmm_RGPD', style={'width':"100%"}), href='/rgpd'),
                                  dcc.Link(html.Button('Bars en France', style={'width':"100%"}), href='/bars'),
                                  dcc.Link(html.Button( "Création d'Entreprises", style={'width': "100%"}), href='/companies'),
                                  dcc.Link(html.Button('Covid basics', style={'width':"100%"}), href='/covid_stats'),
                                  dcc.Link(html.Button('Énergie vs Gaz à effet de serre', style={'width':"100%"}), href='/rbmb_electricityVSgaz'),
                                  dcc.Link(html.Button("Répartission d'offres d'emploi", style={ 'width': "100%"}), href='/bmo'),
                                  dcc.Link(html.Button('Radars vs accidents', style={'width':"100%"}), href='/radar_accidents'),
                                  dcc.Link(html.Button('CO₂ vs Urbanisation', style={'width':"100%"}), href='/tc_urban'),
                                  dcc.Link(html.Button('League Of Legends Statistics', style={'width': "100%"}), href='/lol'),
                                  dcc.Link(html.Button('Parité formations sup', style={'width': "100%"}), href='/formations'),
                                  dcc.Link(html.Button("Criminalité et Education", style={"width": "100%"}), href="/criminalite-education"),
                                  dcc.Link(html.Button('Rentabilité des films', style={'width':"100%"}), href='/ADHD_Movies'),
                                  dcc.Link( html.Button("APB / Parcoursup", style={"width": "100%"}), href="/ab-wg_apb-parcoursup",),
                                  dcc.Link(html.Button('Succès des films par genre', style={'width':"100%"}), href='/filmsuccess'),
                                  dcc.Link(html.Button('Vaccination COVID-19', style={'width':'100%'}), href='/AMEG_vaccination'),
                                  dcc.Link(html.Button('Vins dans le monde', style={'width':"100%"}), href='/PMPR_WineStats'),
                                  dcc.Link(html.Button('Ukraine', style={'width':"100%"}), href='/ukraine'),
                                  dcc.Link(html.Button('Corporate Envt Impact', style={'width':"100%"}), href='/corp_impact'),
                                  dcc.Link(html.Button('Population Française', style={'width':"100%"}), href='/popfr'),
                                  # dcc.Link(html.Button('Accès à Internet vs PIB', style={'width':"100%"}), href='/pib'),
                                  html.Br(),
                                  html.Br(),
                                  html.Br(),
                                  html.Center(html.A('Code source', href='https://github.com/oricou/delta')),
                              ]),
                     html.Div(id='page_content', className="ten columns"),
                ]),
    ])

    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    home_page = html.Div([
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Markdown("Choisissez le jeu de données dans l'index à gauche."),
    ])

    to_be_done_page = html.Div([
        dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
    ])

    app.layout = main_layout

    # "complete" layout (not sure that I need that)
    app.validation_layout = html.Div([
        main_layout,
        to_be_done_page,
        pop.main_layout,
    ])

    # Update the index
    @app.callback(dash.dependencies.Output('page_content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/energies':
            return nrg.main_layout
        elif pathname == '/population':
            return pop.main_layout
        elif pathname == '/deces':
            return dec.main_layout
        elif pathname == '/accidents_routiers':
            return pm.main_layout
        elif pathname == '/pgab_accidents':
            return pgab_acc.main_layout
        elif pathname == '/olympics':
            return oly.main_layout
        elif pathname == '/Energy_generation':
            return eeg.main_layout
        elif pathname == '/EVHB_velib':
            return vel.main_layout
        elif pathname == '/bonheur':
            return hap.main_layout
        elif pathname == '/inegalites':
            return ine_rev.main_layout
        elif pathname == '/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe':
            return alvs.main_layout
        elif pathname == '/MDMR_NYPDCallsMeteoNY':
            return nypd_weather.main_layout
        elif pathname == '/pollution':
            return pol.main_layout
        elif pathname == '/global_warming':
            return globalwarming.main_layout
        elif pathname == '/travail':
            return td.main_layout
        elif pathname == '/petrole':
            return pet.main_layout
        elif pathname == '/salaires':
            return inc.main_layout
        elif pathname == '/pollution':
            return pol.main_layout
        elif pathname == '/cancer':
            return cncr.main_layout
        elif pathname == '/music':
            return mus.main_layout
        elif pathname == '/inequality':
            return ine_gini.main_layout
        elif pathname == '/sujetTV':
            return suj.main_layout
        elif pathname == '/energymix':
            return nrgmix.main_layout
        elif pathname == '/electricite':
            return ele.main_layout
        elif pathname == '/impact':
            return imp.main_layout
        elif pathname == "/chess":
            return chs.main_layout
        elif pathname == "/pollution" :
            return pol.main_layout
        elif pathname == '/ybjd_deces_en_france_selon_le_revenu_par_departement':
            return drd.main_layout
        elif pathname == '/spotify':
            return spo.main_layout
        elif pathname == '/aa_sc_metacritic':
            return meta.main_layout
        elif pathname == '/tbgp-salaires-inflation':
            return tbgp_si.main_layout
        elif pathname == '/jcwg_naissance_deces':
            return jcwg_nd.main_layout
        elif pathname == '/football':
            return foot.main_layout
        elif pathname == '/usa_billboard':
            return billboard.main_layout
        elif pathname == '/meteor':
            return meteor.main_layout
        elif pathname == '/population_vs_train_speed':
            return tbgt.main_layout
        elif pathname == '/postbac':
            return psb.main_layout
        elif pathname == '/presidentielle':
            return pres.main_layout
        elif pathname == '/EC_DC_Evolution_des_Mariages_en_France' :
            return md.main_layout
        elif pathname == '/netflix':
            return net.main_layout
        elif pathname == '/TFRT_obesity':
            return obcal.main_layout
        elif pathname == '/deathanalysis':
            return ana.main_layout
        elif pathname == '/lmsb_animalcrossing':
            return ani.main_layout
        elif pathname == '/accidents':
            return acc.main_layout
        elif pathname == '/parrainage':
            return par.main_layout
        elif pathname == '/rgpd':
            return rgpd.main_layout
        elif pathname == '/efeb_tgv_1':
            return tgv1.main_layout
        elif pathname == '/bars':
           return bar.main_layout
        elif pathname == '/companies':
            return comp.main_layout
        elif pathname == '/covid_stats':
            return covid.main_layout
        elif pathname == '/rbmb_electricityVSgaz':
            return elcVgaz.layout
        elif pathname == '/bmo':
            return bmo_.main_layout
        elif pathname == '/radar_accidents':
            return rd_acc.main_layout
        elif pathname == '/tc_urban':
            return urb.main_layout
        elif pathname == '/lol':
            return lol.main_layout
        elif pathname == '/formations':
            return for_sup.main_layout
        elif pathname == "/criminalite-education":
            return crim_edu.main_layout
        elif pathname == '/ADHD_Movies':
            return mvs.main_layout
        elif pathname == "/ab-wg_apb-parcoursup":
            return apb.main_layout
        elif pathname == '/filmsuccess':
            return filmsuc.main_layout
        elif pathname == '/AMEG_vaccination':
            return vac.main_layout
        elif pathname == '/PMPR_WineStats':
            return wine.main_layout
        elif pathname == '/ukraine':
            return ukr.main_layout
        elif pathname == '/corp_impact':
            return c_i.main_layout
        elif pathname == '/popfr':
            return popfr.main_layout    
        # elif pathname == "/pib":
        #     return pint.main_layout
        else:
            return home_page
    return app
    

app = init()
server = app.server

if __name__ == '__main__':
    profile = False
    if not profile:
        app.run_server(debug=True)
