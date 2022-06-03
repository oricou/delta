import pandas as pd
from difflib import SequenceMatcher

# A la base nous avons code les fonctions suivantes dans les fichiers .ipynb mais comme les consignes demandait de creer un fichier get_data.py, 
# nous avons recopie toutes les cellules des fichiers.ipynb dans ce fichier. 

def Avg_Age():

    #Nous allons lire la donnée de l'age des joueurs de la Premier League en 2004 et créer un nouveau fichier csv contenant deux collones:
    #La premiere colonne correspond au club
    #La deuxieme colonne correpond à l'age moyen des joueurs du club

    PL2004Age = pd.read_csv('data/AgesJoueurs/2004/english_premier_league.csv')
    PL2004Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2004/Avg_PL2004Age.csv')

    liga2004Age = pd.read_csv('data/AgesJoueurs/2004/spanish_primera_division.csv')
    liga2004Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2004/Avg_liga2004Age.csv')

    ligue1_2004Age = pd.read_csv('data/AgesJoueurs/2004/french_ligue_1.csv')
    ligue1_2004Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2004/Avg_ligue1_2004Age.csv')

    bundeshliga2004Age = pd.read_csv('data/AgesJoueurs/2004/german_bundesliga_1.csv')
    bundeshliga2004Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2004/Avg_bundeshliga2004Age.csv')

    serieA2004Age = pd.read_csv('data/AgesJoueurs/2004/italian_serie_a.csv')
    serieA2004Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2004/Avg_serieA2004Age.csv')

    PL2005Age = pd.read_csv('data/AgesJoueurs/2005/english_premier_league.csv')
    PL2005Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2005/Avg_PL2005Age.csv')

    liga2005Age = pd.read_csv('data/AgesJoueurs/2005/spanish_primera_division.csv')
    liga2005Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2005/Avg_liga2005Age.csv')

    ligue1_2005Age = pd.read_csv('data/AgesJoueurs/2005/french_ligue_1.csv')
    ligue1_2005Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2005/Avg_ligue1_2005Age.csv')

    bundeshliga2005Age = pd.read_csv('data/AgesJoueurs/2005/german_bundesliga_1.csv')
    bundeshliga2005Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2005/Avg_bundeshliga2005Age.csv')

    serieA2005Age = pd.read_csv('data/AgesJoueurs/2005/italian_serie_a.csv')
    serieA2005Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2005/Avg_serieA2005Age.csv')


    PL2006Age = pd.read_csv('data/AgesJoueurs/2006/english_premier_league.csv')
    PL2006Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2006/Avg_PL2006Age.csv')


    liga2006Age = pd.read_csv('data/AgesJoueurs/2006/spanish_primera_division.csv')
    liga2006Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2006/Avg_liga2006Age.csv')

    ligue1_2006Age = pd.read_csv('data/AgesJoueurs/2006/french_ligue_1.csv')
    ligue1_2006Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2006/Avg_ligue1_2006Age.csv')

    bundeshliga2006Age = pd.read_csv('data/AgesJoueurs/2006/german_bundesliga_1.csv')
    bundeshliga2006Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2006/Avg_bundeshliga2006Age.csv')

    serieA2006Age = pd.read_csv('data/AgesJoueurs/2006/italian_serie_a.csv')
    serieA2006Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2006/Avg_serieA2006Age.csv')
    
    PL2007Age = pd.read_csv('data/AgesJoueurs/2007/english_premier_league.csv')
    PL2007Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2007/Avg_PL2007Age.csv')

    liga2007Age = pd.read_csv('data/AgesJoueurs/2007/spanish_primera_division.csv')
    liga2007Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2007/Avg_liga2007Age.csv')

    ligue1_2007Age = pd.read_csv('data/AgesJoueurs/2007/french_ligue_1.csv')
    ligue1_2007Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2007/Avg_ligue1_2007Age.csv')

    bundeshliga2007Age = pd.read_csv('data/AgesJoueurs/2007/german_bundesliga_1.csv')
    bundeshliga2007Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2007/Avg_bundeshliga2007Age.csv')

    serieA2007Age = pd.read_csv('data/AgesJoueurs/2007/italian_serie_a.csv')
    serieA2007Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2007/Avg_serieA2007Age.csv')

    PL2008Age = pd.read_csv('data/AgesJoueurs/2008/english_premier_league.csv')
    PL2008Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2008/Avg_PL2008Age.csv')


    liga2008Age = pd.read_csv('data/AgesJoueurs/2008/spanish_primera_division.csv')
    liga2008Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2008/Avg_liga2008Age.csv')

    ligue1_2008Age = pd.read_csv('data/AgesJoueurs/2008/french_ligue_1.csv')
    ligue1_2008Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2008/Avg_ligue1_2008Age.csv')

    bundeshliga2008Age = pd.read_csv('data/AgesJoueurs/2008/german_bundesliga_1.csv')
    bundeshliga2008Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2008/Avg_bundeshliga2008Age.csv')

    serieA2008Age = pd.read_csv('data/AgesJoueurs/2008/italian_serie_a.csv')
    serieA2008Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2008/Avg_serieA2008Age.csv')

    PL2009Age = pd.read_csv('data/AgesJoueurs/2009/english_premier_league.csv')
    PL2009Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2009/Avg_PL2009Age.csv')


    liga2009Age = pd.read_csv('data/AgesJoueurs/2009/spanish_primera_division.csv')
    liga2009Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2009/Avg_liga2009Age.csv')

    ligue1_2009Age = pd.read_csv('data/AgesJoueurs/2009/french_ligue_1.csv')
    ligue1_2009Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2009/Avg_ligue1_2009Age.csv')

    bundeshliga2009Age = pd.read_csv('data/AgesJoueurs/2009/german_bundesliga_1.csv')
    bundeshliga2009Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2009/Avg_bundeshliga2009Age.csv')

    serieA2009Age = pd.read_csv('data/AgesJoueurs/2009/italian_serie_a.csv')
    serieA2009Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2009/Avg_serieA2009Age.csv')

    PL2010Age = pd.read_csv('data/AgesJoueurs/2010/english_premier_league.csv')
    PL2010Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2010/Avg_PL2010Age.csv')


    liga2010Age = pd.read_csv('data/AgesJoueurs/2010/spanish_primera_division.csv')
    liga2010Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2010/Avg_liga2010Age.csv')

    ligue1_2010Age = pd.read_csv('data/AgesJoueurs/2010/french_ligue_1.csv')
    ligue1_2010Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2010/Avg_ligue1_2010Age.csv')

    bundeshliga2010Age = pd.read_csv('data/AgesJoueurs/2010/german_bundesliga_1.csv')
    bundeshliga2010Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2010/Avg_bundeshliga2010Age.csv')

    serieA2010Age = pd.read_csv('data/AgesJoueurs/2010/italian_serie_a.csv')
    serieA2010Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2010/Avg_serieA2010Age.csv')

    PL2011Age = pd.read_csv('data/AgesJoueurs/2011/english_premier_league.csv')
    PL2011Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2011/Avg_PL2011Age.csv')

    liga2011Age = pd.read_csv('data/AgesJoueurs/2011/spanish_primera_division.csv')
    liga2011Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2011/Avg_liga2011Age.csv')

    ligue1_2011Age = pd.read_csv('data/AgesJoueurs/2011/french_ligue_1.csv')
    ligue1_2011Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2011/Avg_ligue1_2011Age.csv')

    bundeshliga2011Age = pd.read_csv('data/AgesJoueurs/2011/german_bundesliga_1.csv')
    bundeshliga2011Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2011/Avg_bundeshliga2011Age.csv')

    serieA2011Age = pd.read_csv('data/AgesJoueurs/2011/italian_serie_a.csv')
    serieA2011Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2011/Avg_serieA2011Age.csv')


    PL2012Age = pd.read_csv('data/AgesJoueurs/2012/english_premier_league.csv')
    PL2012Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2012/Avg_PL2012Age.csv')

    liga2012Age = pd.read_csv('data/AgesJoueurs/2012/spanish_primera_division.csv')
    liga2012Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2012/Avg_liga2012Age.csv')

    ligue1_2012Age = pd.read_csv('data/AgesJoueurs/2012/french_ligue_1.csv')
    ligue1_2012Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2012/Avg_ligue1_2012Age.csv')

    bundeshliga2012Age = pd.read_csv('data/AgesJoueurs/2012/german_bundesliga_1.csv')
    bundeshliga2012Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2012/Avg_bundeshliga2012Age.csv')

    serieA2012Age = pd.read_csv('data/AgesJoueurs/2012/italian_serie_a.csv')
    serieA2012Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2012/Avg_serieA2012Age.csv')

    PL2013Age = pd.read_csv('data/AgesJoueurs/2013/english_premier_league.csv')
    PL2013Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2013/Avg_PL2013Age.csv')

    liga2013Age = pd.read_csv('data/AgesJoueurs/2013/spanish_primera_division.csv')
    liga2013Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2013/Avg_liga2013Age.csv')

    ligue1_2013Age = pd.read_csv('data/AgesJoueurs/2013/french_ligue_1.csv')
    ligue1_2013Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2013/Avg_ligue1_2013Age.csv')

    bundeshliga2013Age = pd.read_csv('data/AgesJoueurs/2013/german_bundesliga_1.csv')
    bundeshliga2013Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2013/Avg_bundeshliga2013Age.csv')

    serieA2013Age = pd.read_csv('data/AgesJoueurs/2013/italian_serie_a.csv')
    serieA2013Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2013/Avg_serieA2013Age.csv')

    PL2014Age = pd.read_csv('data/AgesJoueurs/2014/english_premier_league.csv')
    PL2014Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2014/Avg_PL2014Age.csv')

    liga2014Age = pd.read_csv('data/AgesJoueurs/2014/spanish_primera_division.csv')
    liga2014Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2014/Avg_liga2014Age.csv')

    ligue1_2014Age = pd.read_csv('data/AgesJoueurs/2014/french_ligue_1.csv')
    ligue1_2014Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2014/Avg_ligue1_2014Age.csv')

    bundeshliga2014Age = pd.read_csv('data/AgesJoueurs/2014/german_bundesliga_1.csv')
    bundeshliga2014Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2014/Avg_bundeshliga2014Age.csv')

    serieA2014Age = pd.read_csv('data/AgesJoueurs/2014/italian_serie_a.csv')
    serieA2014Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2014/Avg_serieA2014Age.csv')

    PL2015Age = pd.read_csv('data/AgesJoueurs/2015/english_premier_league.csv')
    PL2015Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2015/Avg_PL2015Age.csv')

    liga2015Age = pd.read_csv('data/AgesJoueurs/2015/spanish_primera_division.csv')
    liga2015Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2015/Avg_liga2015Age.csv')

    ligue1_2015Age = pd.read_csv('data/AgesJoueurs/2015/french_ligue_1.csv')
    ligue1_2015Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2015/Avg_ligue1_2015Age.csv')

    bundeshliga2015Age = pd.read_csv('data/AgesJoueurs/2015/german_bundesliga_1.csv')
    bundeshliga2015Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2015/Avg_bundeshliga2015Age.csv')

    serieA2015Age = pd.read_csv('data/AgesJoueurs/2015/italian_serie_a.csv')
    serieA2015Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2015/Avg_serieA2015Age.csv')

    PL2016Age = pd.read_csv('data/AgesJoueurs/2016/english_premier_league.csv')
    PL2016Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2016/Avg_PL2016Age.csv')

    liga2016Age = pd.read_csv('data/AgesJoueurs/2016/spanish_primera_division.csv')
    liga2016Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2016/Avg_liga2016Age.csv')

    ligue1_2016Age = pd.read_csv('data/AgesJoueurs/2016/french_ligue_1.csv')
    ligue1_2016Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2016/Avg_ligue1_2016Age.csv')

    bundeshliga2016Age = pd.read_csv('data/AgesJoueurs/2016/german_bundesliga_1.csv')
    bundeshliga2016Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2016/Avg_bundeshliga2016Age.csv')

    serieA2016Age = pd.read_csv('data/AgesJoueurs/2016/italian_serie_a.csv')
    serieA2016Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2016/Avg_serieA2016Age.csv')

    PL2017Age = pd.read_csv('data/AgesJoueurs/2017/english_premier_league.csv')
    PL2017Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2017/Avg_PL2017Age.csv')

    liga2017Age = pd.read_csv('data/AgesJoueurs/2017/spanish_primera_division.csv')
    liga2017Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2017/Avg_liga2017Age.csv')

    ligue1_2017Age = pd.read_csv('data/AgesJoueurs/2017/french_ligue_1.csv')
    ligue1_2017Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2017/Avg_ligue1_2017Age.csv')

    bundeshliga2017Age = pd.read_csv('data/AgesJoueurs/2017/german_bundesliga_1.csv')
    bundeshliga2017Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2017/Avg_bundeshliga2017Age.csv')

    serieA2017Age = pd.read_csv('data/AgesJoueurs/2017/italian_serie_a.csv')
    serieA2017Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2017/Avg_serieA2017Age.csv')

    PL2018Age = pd.read_csv('data/AgesJoueurs/2018/english_premier_league.csv')
    PL2018Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2018/Avg_PL2018Age.csv')

    liga2018Age = pd.read_csv('data/AgesJoueurs/2018/spanish_primera_division.csv')
    liga2018Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2018/Avg_liga2018Age.csv')

    ligue1_2018Age = pd.read_csv('data/AgesJoueurs/2018/french_ligue_1.csv')
    ligue1_2018Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2018/Avg_ligue1_2018Age.csv')

    bundeshliga2018Age = pd.read_csv('data/AgesJoueurs/2018/german_bundesliga_1.csv')
    bundeshliga2018Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2018/Avg_bundeshliga2018Age.csv')

    serieA2018Age = pd.read_csv('data/AgesJoueurs/2018/italian_serie_a.csv')
    serieA2018Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2018/Avg_serieA2018Age.csv')

    PL2019Age = pd.read_csv('data/AgesJoueurs/2019/english_premier_league.csv')
    PL2019Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2019/Avg_PL2019Age.csv')

    liga2019Age = pd.read_csv('data/AgesJoueurs/2019/spanish_primera_division.csv')
    liga2019Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2019/Avg_liga2019Age.csv')

    ligue1_2019Age = pd.read_csv('data/AgesJoueurs/2019/french_ligue_1.csv')
    ligue1_2019Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2019/Avg_ligue1_2019Age.csv')

    bundeshliga2019Age = pd.read_csv('data/AgesJoueurs/2019/german_bundesliga_1.csv')
    bundeshliga2019Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2019/Avg_bundeshliga2019Age.csv')

    serieA2019Age = pd.read_csv('data/AgesJoueurs/2019/italian_serie_a.csv')
    serieA2019Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2019/Avg_serieA2019Age.csv')

    PL2020Age = pd.read_csv('data/AgesJoueurs/2020/english_premier_league.csv')
    PL2020Age.groupby('club_name')[['age']].mean().to_csv('data/AverageAge/2020/Avg_PL2020Age.csv')

    liga2020Age = pd.read_csv('data/AgesJoueurs/2020/spanish_primera_division.csv')
    liga2020Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2020/Avg_liga2020Age.csv')

    ligue1_2020Age = pd.read_csv('data/AgesJoueurs/2020/french_ligue_1.csv')
    ligue1_2020Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2020/Avg_ligue1_2020Age.csv')

    bundeshliga2020Age = pd.read_csv('data/AgesJoueurs/2020/german_bundesliga_1.csv')
    bundeshliga2020Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2020/Avg_bundeshliga2020Age.csv')

    serieA2020Age = pd.read_csv('data/AgesJoueurs/2020/italian_serie_a.csv')
    serieA2020Age.groupby('club_name')['age'].mean().to_csv('data/AverageAge/2020/Avg_serieA2020Age.csv')

def concat():

    liga0405Rk = pd.read_excel('data/liga/liga0405.xls')
    liga0506Rk = pd.read_excel('data/liga/liga0506.xls')
    liga0607Rk = pd.read_excel('data/liga/liga0607.xls')
    liga0708Rk = pd.read_excel('data/liga/liga0708.xls')
    liga0809Rk = pd.read_excel('data/liga/liga0809.xls')
    liga0910Rk = pd.read_excel('data/liga/liga0910.xls')
    liga1011Rk = pd.read_excel('data/liga/liga1011.xls')
    liga1112Rk = pd.read_excel('data/liga/liga1112.xls')
    liga1213Rk = pd.read_excel('data/liga/liga1213.xls')
    liga1314Rk = pd.read_excel('data/liga/liga1314.xls')
    liga1415Rk = pd.read_excel('data/liga/liga1415.xls')
    liga1516Rk = pd.read_excel('data/liga/liga1516.xls')
    liga1617Rk = pd.read_excel('data/liga/liga1617.xls')
    liga1718Rk = pd.read_excel('data/liga/liga1718.xls')
    liga1819Rk = pd.read_excel('data/liga/liga1819.xls')
    liga1920Rk = pd.read_excel('data/liga/liga1920.xls')
    liga2021Rk = pd.read_excel('data/liga/liga2021.xls')

    concat  = pd.concat([liga0405Rk, liga0506Rk, liga0607Rk, liga0708Rk, liga0809Rk, liga0910Rk, liga1011Rk, liga1112Rk, liga1213Rk, liga1314Rk, liga1415Rk, liga1516Rk, liga1617Rk, liga1718Rk, liga1819Rk, liga1920Rk, liga2021Rk], axis=0).to_csv("data/concat/liga.csv")


    # In[12]:


    PL0405Rk = pd.read_excel('data/PL/PL0405.xls')
    PL0506Rk = pd.read_excel('data/PL/PL0506.xls')
    PL0607Rk = pd.read_excel('data/PL/PL0607.xls')
    PL0708Rk = pd.read_excel('data/PL/PL0708.xls')
    PL0809Rk = pd.read_excel('data/PL/PL0809.xls')
    PL0910Rk = pd.read_excel('data/PL/PL0910.xls')
    PL1011Rk = pd.read_excel('data/PL/PL1011.xls')
    PL1112Rk = pd.read_excel('data/PL/PL1112.xls')
    PL1213Rk = pd.read_excel('data/PL/PL1213.xls')
    PL1314Rk = pd.read_excel('data/PL/PL1314.xls')
    PL1415Rk = pd.read_excel('data/PL/PL1415.xls')
    PL1516Rk = pd.read_excel('data/PL/PL1516.xls')
    PL1617Rk = pd.read_excel('data/PL/PL1617.xls')
    PL1718Rk = pd.read_excel('data/PL/PL1718.xls')
    PL1819Rk = pd.read_excel('data/PL/PL1819.xls')
    PL1920Rk = pd.read_excel('data/PL/PL1920.xls')
    PL2021Rk = pd.read_excel('data/PL/PL2021.xls')

    concat  = pd.concat([PL0405Rk, PL0506Rk, PL0607Rk, PL0708Rk, PL0809Rk, PL0910Rk, PL1011Rk,PL1112Rk, PL1213Rk, PL1314Rk, PL1415Rk, PL1516Rk, PL1617Rk, PL1718Rk, PL1819Rk, PL1920Rk, PL2021Rk], axis=0).to_csv("data/concat/PL.csv")


    # In[11]:


    serieA0405Rk = pd.read_excel('data/serieA/serieA0405.xls')
    serieA0506Rk = pd.read_excel('data/serieA/serieA0506.xls')
    serieA0607Rk = pd.read_excel('data/serieA/serieA0607.xls')
    serieA0708Rk = pd.read_excel('data/serieA/serieA0708.xls')
    serieA0809Rk = pd.read_excel('data/serieA/serieA0809.xls')
    serieA0910Rk = pd.read_excel('data/serieA/serieA0910.xls')
    serieA1011Rk = pd.read_excel('data/serieA/serieA1011.xls')
    serieA1112Rk = pd.read_excel('data/serieA/serieA1112.xls')
    serieA1213Rk = pd.read_excel('data/serieA/serieA1213.xls')
    serieA1314Rk = pd.read_excel('data/serieA/serieA1314.xls')
    serieA1415Rk = pd.read_excel('data/serieA/serieA1415.xls')
    serieA1516Rk = pd.read_excel('data/serieA/serieA1516.xls')
    serieA1617Rk = pd.read_excel('data/serieA/serieA1617.xls')
    serieA1718Rk = pd.read_excel('data/serieA/serieA1718.xls')
    serieA1819Rk = pd.read_excel('data/serieA/serieA1819.xls')
    serieA1920Rk = pd.read_excel('data/serieA/serieA1920.xls')
    serieA2021Rk = pd.read_excel('data/serieA/serieA2021.xls')

    concat  = pd.concat([serieA0405Rk, serieA0506Rk, serieA0607Rk, serieA0708Rk, serieA0809Rk, serieA0910Rk, serieA1011Rk, serieA1112Rk, serieA1213Rk, serieA1314Rk, serieA1415Rk, serieA1516Rk, serieA1617Rk, serieA1718Rk, serieA1819Rk, serieA1920Rk, serieA2021Rk], axis=0).to_csv("data/concat/serieA.csv")


    # In[9]:


    bundeshliga0405Rk = pd.read_excel('data/bundesliga/bundeshliga0405.xls')
    bundeshliga0506Rk = pd.read_excel('data/bundesliga/bundeshliga0506.xls')
    bundeshliga0607Rk = pd.read_excel('data/bundesliga/bundeshliga0607.xls')
    bundeshliga0708Rk = pd.read_excel('data/bundesliga/bundeshliga0708.xls')
    bundeshliga0809Rk = pd.read_excel('data/bundesliga/bundeshliga0809.xls')
    bundeshliga0910Rk = pd.read_excel('data/bundesliga/bundeshliga0910.xls')
    bundeshliga1011Rk = pd.read_excel('data/bundesliga/bundeshliga1011.xls')
    bundeshliga1112Rk = pd.read_excel('data/bundesliga/bundeshliga1112.xls')
    bundeshliga1213Rk = pd.read_excel('data/bundesliga/bundeshliga1213.xls')
    bundeshliga1314Rk = pd.read_excel('data/bundesliga/bundeshliga1314.xls')
    bundeshliga1415Rk = pd.read_excel('data/bundesliga/bundeshliga1415.xls')
    bundeshliga1516Rk = pd.read_excel('data/bundesliga/bundeshliga1516.xls')
    bundeshliga1617Rk = pd.read_excel('data/bundesliga/bundeshliga1617.xls')
    bundeshliga1718Rk = pd.read_excel('data/bundesliga/bundeshliga1718.xls')
    bundeshliga1819Rk = pd.read_excel('data/bundesliga/bundeshliga1819.xls')
    bundeshliga1920Rk = pd.read_excel('data/bundesliga/bundeshliga1920.xls')
    bundeshliga2021Rk = pd.read_excel('data/bundesliga/bundeshliga2021.xls')

    concat  = pd.concat([bundeshliga0405Rk, bundeshliga0506Rk, bundeshliga0607Rk, bundeshliga0708Rk, bundeshliga0809Rk, 
                        bundeshliga0910Rk, bundeshliga1011Rk, bundeshliga1112Rk, bundeshliga1213Rk, bundeshliga1314Rk, 
                        bundeshliga1415Rk, bundeshliga1516Rk, bundeshliga1617Rk, bundeshliga1718Rk, bundeshliga1819Rk, 
                        bundeshliga1920Rk, bundeshliga2021Rk], axis=0).to_csv("data/concat/bundeshliga.csv")


    # In[14]:


    ligue10405Rk = pd.read_excel('data/ligue1/ligue10405.xls')
    ligue10506Rk = pd.read_excel('data/ligue1/ligue10506.xls')
    ligue10607Rk = pd.read_excel('data/ligue1/ligue10607.xls')
    ligue10708Rk = pd.read_excel('data/ligue1/ligue10708.xls')
    ligue10809Rk = pd.read_excel('data/ligue1/ligue10809.xls')
    ligue10910Rk = pd.read_excel('data/ligue1/ligue10910.xls')
    ligue11011Rk = pd.read_excel('data/ligue1/ligue11011.xls')
    ligue11112Rk = pd.read_excel('data/ligue1/ligue11112.xls')
    ligue11213Rk = pd.read_excel('data/ligue1/ligue11213.xls')
    ligue11314Rk = pd.read_excel('data/ligue1/ligue11314.xls')
    ligue11415Rk = pd.read_excel('data/ligue1/ligue11415.xls')
    ligue11516Rk = pd.read_excel('data/ligue1/ligue11516.xls')
    ligue11617Rk = pd.read_excel('data/ligue1/ligue11617.xls')
    ligue11718Rk = pd.read_excel('data/ligue1/ligue11718.xls')
    ligue11819Rk = pd.read_excel('data/ligue1/ligue11819.xls')
    ligue11920Rk = pd.read_excel('data/ligue1/ligue11920.xls')
    ligue12021Rk = pd.read_excel('data/ligue1/ligue12021.xls')

    concat  = pd.concat([ligue10405Rk, ligue10506Rk, ligue10607Rk, ligue10708Rk, ligue10809Rk, 
                        ligue10910Rk, ligue11011Rk, ligue11112Rk, ligue11213Rk , ligue11314Rk, 
                        ligue11415Rk, ligue11516Rk, ligue11617Rk, ligue11718Rk, ligue11819Rk, 
                        ligue11920Rk, ligue12021Rk], axis=0).to_csv("data/concat/ligue1.csv")

def Years():

    list_years = ['2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13',
            '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21']

    liga = pd.read_csv('data/concat/liga.csv')
    PL = pd.read_csv('data/concat/PL.csv')
    serieA = pd.read_csv('data/concat/serieA.csv')
    ligue1 = pd.read_csv('data/concat/ligue1.csv')
    bundesliga = pd.read_csv('data/concat/bundeshliga.csv')

    list = []
    list_bundes = []

    for y in range(17):
        for i in range(20):
            list.append(list_years[y])
        for i in range(18):
            list_bundes.append(list_years[y])

    liga['Years'] = list
    PL['Years'] = list
    serieA['Years'] = list
    ligue1['Years'] = list
    bundesliga['Years'] = list_bundes

    liga.to_csv('data/concat_years/liga.csv', index=False)
    PL.to_csv('data/concat_years/PL.csv', index=False)
    serieA.to_csv('data/concat_years/serieA.csv', index=False)
    ligue1.to_csv('data/concat_years/ligue1.csv', index=False)
    bundesliga.to_csv('data/concat_years/bundesliga.csv', index=False)

def Age():

    def is_string_similar(s1: str, s2: str, threshold: float = 0.82):
        return SequenceMatcher(a=s1, b=s2).ratio() > threshold

    def age_league(league, leaguexxxx, list_clubsleaguexxxx, start_index):
        list_age_league_per_year = []
        for i in range(start_index, start_index + 20):
            for x in range (20):
                if is_string_similar(s1=league['Squad'].loc[i], s2=list_clubsleaguexxxx[x]):
                    list_age_league_per_year.append(leaguexxxx['age'].loc[leaguexxxx['club_name'] == list_clubsleaguexxxx[x]]) #the age of the club in list_clubsliga2004
                    break

        return list_age_league_per_year

    def age_bundesliga(league, leaguexxxx, list_clubsleaguexxxx, start_index):
        list_age_league_per_year = []
        for i in range(start_index, start_index + 18):
            for x in range (18):
                if is_string_similar(s1=league['Squad'].loc[i], s2=list_clubsleaguexxxx[x]):
                    list_age_league_per_year.append(leaguexxxx['age'].loc[leaguexxxx['club_name'] == list_clubsleaguexxxx[x]]) #the age of the club in list_clubsliga2004
                    break

        return list_age_league_per_year

    def single_list(L):
        new_list = []
        for e in L:
            for element in e:
                new_list.append(element)
        return new_list

    def to_string(L):
        new_list = []
        for e in L:
            new_list.append(str(e))
        return new_list

    def parse_string(s):
        i = 0
        new_string = ""
        while (s[i] != ' '):
            i+=1
        while(s[i] == ' '):
            i+=1
        while (s[i] != '\n'):
            new_string += s[i]
            i+=1
        return new_string

    def parse_list(L):
        new_list = []
        for e in L:
            new_list.append(parse_string(e))
        return new_list

    def to_float(L):
        new_list = []
        for e in L:
            new_list.append(float(e))
        return new_list

            

    liga = pd.read_csv('data/concat_years/liga.csv')

    liga2004 = pd.read_csv('data/AverageAge/2004/Avg_liga2004Age.csv')
    liga2005 = pd.read_csv('data/AverageAge/2005/Avg_liga2005Age.csv')
    liga2006 = pd.read_csv('data/AverageAge/2006/Avg_liga2006Age.csv')
    liga2007 = pd.read_csv('data/AverageAge/2007/Avg_liga2007Age.csv')
    liga2008 = pd.read_csv('data/AverageAge/2008/Avg_liga2008Age.csv')
    liga2009 = pd.read_csv('data/AverageAge/2009/Avg_liga2009Age.csv')
    liga2010 = pd.read_csv('data/AverageAge/2010/Avg_liga2010Age.csv')
    liga2011 = pd.read_csv('data/AverageAge/2011/Avg_liga2011Age.csv')
    liga2012 = pd.read_csv('data/AverageAge/2012/Avg_liga2012Age.csv')
    liga2013 = pd.read_csv('data/AverageAge/2013/Avg_liga2013Age.csv')
    liga2014 = pd.read_csv('data/AverageAge/2014/Avg_liga2014Age.csv')
    liga2015 = pd.read_csv('data/AverageAge/2015/Avg_liga2015Age.csv')
    liga2016 = pd.read_csv('data/AverageAge/2016/Avg_liga2016Age.csv')
    liga2017 = pd.read_csv('data/AverageAge/2017/Avg_liga2017Age.csv')
    liga2018 = pd.read_csv('data/AverageAge/2018/Avg_liga2018Age.csv')
    liga2019 = pd.read_csv('data/AverageAge/2019/Avg_liga2019Age.csv')
    liga2020 = pd.read_csv('data/AverageAge/2020/Avg_liga2020Age.csv')

    list_clubsliga2004 = liga2004['club_name'].to_list()
    list_clubsliga2005 = liga2005['club_name'].to_list()
    list_clubsliga2006 = liga2006['club_name'].to_list()
    list_clubsliga2007 = liga2007['club_name'].to_list()
    list_clubsliga2008 = liga2008['club_name'].to_list()
    list_clubsliga2009 = liga2009['club_name'].to_list()
    list_clubsliga2010 = liga2010['club_name'].to_list()
    list_clubsliga2011 = liga2011['club_name'].to_list()
    list_clubsliga2012 = liga2012['club_name'].to_list()
    list_clubsliga2013 = liga2013['club_name'].to_list()
    list_clubsliga2014 = liga2014['club_name'].to_list()
    list_clubsliga2015 = liga2015['club_name'].to_list()
    list_clubsliga2016 = liga2016['club_name'].to_list()
    list_clubsliga2017 = liga2017['club_name'].to_list()
    list_clubsliga2018 = liga2018['club_name'].to_list()
    list_clubsliga2019 = liga2019['club_name'].to_list()
    list_clubsliga2020 = liga2020['club_name'].to_list()

    list_age_liga = []

    list_age_liga.append(age_league(liga, liga2004, list_clubsliga2004, 0))
    list_age_liga.append(age_league(liga, liga2005, list_clubsliga2005, 20))
    list_age_liga.append(age_league(liga, liga2006, list_clubsliga2006, 40))
    list_age_liga.append(age_league(liga, liga2007, list_clubsliga2007, 60))
    list_age_liga.append(age_league(liga, liga2008, list_clubsliga2008, 80))
    list_age_liga.append(age_league(liga, liga2009, list_clubsliga2009, 100))
    list_age_liga.append(age_league(liga, liga2010, list_clubsliga2010, 120))
    list_age_liga.append(age_league(liga, liga2011, list_clubsliga2011, 140))
    list_age_liga.append(age_league(liga, liga2012, list_clubsliga2012, 160))
    list_age_liga.append(age_league(liga, liga2013, list_clubsliga2013, 180))
    list_age_liga.append(age_league(liga, liga2014, list_clubsliga2014, 200))
    list_age_liga.append(age_league(liga, liga2015, list_clubsliga2015, 220))
    list_age_liga.append(age_league(liga, liga2016, list_clubsliga2016, 240))
    list_age_liga.append(age_league(liga, liga2017, list_clubsliga2017, 260))
    list_age_liga.append(age_league(liga, liga2018, list_clubsliga2018, 280))
    list_age_liga.append(age_league(liga, liga2019, list_clubsliga2019, 300))
    list_age_liga.append(age_league(liga, liga2020, list_clubsliga2020, 320))


    new_list_single = single_list(list_age_liga)
    new_list_single_string = to_string(new_list_single)
    #print(len(new_list_single))
    only_avg_list = parse_list(new_list_single_string)
    only_avg_list_float = to_float(only_avg_list)
    #print(only_avg_list_float)

    liga['Age'] = only_avg_list_float
    liga.to_csv('data/concat_years_age/liga.csv', index=False)

    #list => faire de list_age_liga pas une liste de liste, mais une seule liste avec une fonction...
    #liga['Age'] = list
    #liga.to_csv('data/concat_years_age/liga.csv', index=False)


    # In[2]:


    PL = pd.read_csv('data/concat_years/PL.csv')

    PL2004 = pd.read_csv('data/AverageAge/2004/Avg_PL2004Age.csv')
    PL2005 = pd.read_csv('data/AverageAge/2005/Avg_PL2005Age.csv')
    PL2006 = pd.read_csv('data/AverageAge/2006/Avg_PL2006Age.csv')
    PL2007 = pd.read_csv('data/AverageAge/2007/Avg_PL2007Age.csv')
    PL2008 = pd.read_csv('data/AverageAge/2008/Avg_PL2008Age.csv')
    PL2009 = pd.read_csv('data/AverageAge/2009/Avg_PL2009Age.csv')
    PL2010 = pd.read_csv('data/AverageAge/2010/Avg_PL2010Age.csv')
    PL2011 = pd.read_csv('data/AverageAge/2011/Avg_PL2011Age.csv')
    PL2012 = pd.read_csv('data/AverageAge/2012/Avg_PL2012Age.csv')
    PL2013 = pd.read_csv('data/AverageAge/2013/Avg_PL2013Age.csv')
    PL2014 = pd.read_csv('data/AverageAge/2014/Avg_PL2014Age.csv')
    PL2015 = pd.read_csv('data/AverageAge/2015/Avg_PL2015Age.csv')
    PL2016 = pd.read_csv('data/AverageAge/2016/Avg_PL2016Age.csv')
    PL2017 = pd.read_csv('data/AverageAge/2017/Avg_PL2017Age.csv')
    PL2018 = pd.read_csv('data/AverageAge/2018/Avg_PL2018Age.csv')
    PL2019 = pd.read_csv('data/AverageAge/2019/Avg_PL2019Age.csv')
    PL2020 = pd.read_csv('data/AverageAge/2020/Avg_PL2020Age.csv')

    list_clubsPL2004 = PL2004['club_name'].to_list()
    list_clubsPL2005 = PL2005['club_name'].to_list()
    list_clubsPL2006 = PL2006['club_name'].to_list()
    list_clubsPL2007 = PL2007['club_name'].to_list()
    list_clubsPL2008 = PL2008['club_name'].to_list()
    list_clubsPL2009 = PL2009['club_name'].to_list()
    list_clubsPL2010 = PL2010['club_name'].to_list()
    list_clubsPL2011 = PL2011['club_name'].to_list()
    list_clubsPL2012 = PL2012['club_name'].to_list()
    list_clubsPL2013 = PL2013['club_name'].to_list()
    list_clubsPL2014 = PL2014['club_name'].to_list()
    list_clubsPL2015 = PL2015['club_name'].to_list()
    list_clubsPL2016 = PL2016['club_name'].to_list()
    list_clubsPL2017 = PL2017['club_name'].to_list()
    list_clubsPL2018 = PL2018['club_name'].to_list()
    list_clubsPL2019 = PL2019['club_name'].to_list()
    list_clubsPL2020 = PL2020['club_name'].to_list()

    list_age_PL = []

    list_age_PL.append(age_league(PL, PL2004, list_clubsPL2004, 0))
    list_age_PL.append(age_league(PL, PL2005, list_clubsPL2005, 20))
    list_age_PL.append(age_league(PL, PL2006, list_clubsPL2006, 40))
    list_age_PL.append(age_league(PL, PL2007, list_clubsPL2007, 60))
    list_age_PL.append(age_league(PL, PL2008, list_clubsPL2008, 80))
    list_age_PL.append(age_league(PL, PL2009, list_clubsPL2009, 100))
    list_age_PL.append(age_league(PL, PL2010, list_clubsPL2010, 120))
    list_age_PL.append(age_league(PL, PL2011, list_clubsPL2011, 140))
    list_age_PL.append(age_league(PL, PL2012, list_clubsPL2012, 160))
    list_age_PL.append(age_league(PL, PL2013, list_clubsPL2013, 180))
    list_age_PL.append(age_league(PL, PL2014, list_clubsPL2014, 200))
    list_age_PL.append(age_league(PL, PL2015, list_clubsPL2015, 220))
    list_age_PL.append(age_league(PL, PL2016, list_clubsPL2016, 240))
    list_age_PL.append(age_league(PL, PL2017, list_clubsPL2017, 260))
    list_age_PL.append(age_league(PL, PL2018, list_clubsPL2018, 280))
    list_age_PL.append(age_league(PL, PL2019, list_clubsPL2019, 300))
    list_age_PL.append(age_league(PL, PL2020, list_clubsPL2020, 320))


    new_list_single_PL = single_list(list_age_PL)

    new_list_single_string_PL = to_string(new_list_single_PL)
    only_avg_list_PL = parse_list(new_list_single_string_PL)
    only_avg_list_float_PL = to_float(only_avg_list_PL)


    PL['Age'] = only_avg_list_float_PL
    PL.to_csv('data/concat_years_age/PL.csv', index=False)


    # In[3]:


    serieA = pd.read_csv('data/concat_years/serieA.csv')

    serieA2004 = pd.read_csv('data/AverageAge/2004/Avg_serieA2004Age.csv')
    serieA2005 = pd.read_csv('data/AverageAge/2005/Avg_serieA2005Age.csv')
    serieA2006 = pd.read_csv('data/AverageAge/2006/Avg_serieA2006Age.csv')
    serieA2007 = pd.read_csv('data/AverageAge/2007/Avg_serieA2007Age.csv')
    serieA2008 = pd.read_csv('data/AverageAge/2008/Avg_serieA2008Age.csv')
    serieA2009 = pd.read_csv('data/AverageAge/2009/Avg_serieA2009Age.csv')
    serieA2010 = pd.read_csv('data/AverageAge/2010/Avg_serieA2010Age.csv')
    serieA2011 = pd.read_csv('data/AverageAge/2011/Avg_serieA2011Age.csv')
    serieA2012 = pd.read_csv('data/AverageAge/2012/Avg_serieA2012Age.csv')
    serieA2013 = pd.read_csv('data/AverageAge/2013/Avg_serieA2013Age.csv')
    serieA2014 = pd.read_csv('data/AverageAge/2014/Avg_serieA2014Age.csv')
    serieA2015 = pd.read_csv('data/AverageAge/2015/Avg_serieA2015Age.csv')
    serieA2016 = pd.read_csv('data/AverageAge/2016/Avg_serieA2016Age.csv')
    serieA2017 = pd.read_csv('data/AverageAge/2017/Avg_serieA2017Age.csv')
    serieA2018 = pd.read_csv('data/AverageAge/2018/Avg_serieA2018Age.csv')
    serieA2019 = pd.read_csv('data/AverageAge/2019/Avg_serieA2019Age.csv')
    serieA2020 = pd.read_csv('data/AverageAge/2020/Avg_serieA2020Age.csv')

    list_clubsserieA2004 = serieA2004['club_name'].to_list()
    list_clubsserieA2005 = serieA2005['club_name'].to_list()
    list_clubsserieA2006 = serieA2006['club_name'].to_list()
    list_clubsserieA2007 = serieA2007['club_name'].to_list()
    list_clubsserieA2008 = serieA2008['club_name'].to_list()
    list_clubsserieA2009 = serieA2009['club_name'].to_list()
    list_clubsserieA2010 = serieA2010['club_name'].to_list()
    list_clubsserieA2011 = serieA2011['club_name'].to_list()
    list_clubsserieA2012 = serieA2012['club_name'].to_list()
    list_clubsserieA2013 = serieA2013['club_name'].to_list()
    list_clubsserieA2014 = serieA2014['club_name'].to_list()
    list_clubsserieA2015 = serieA2015['club_name'].to_list()
    list_clubsserieA2016 = serieA2016['club_name'].to_list()
    list_clubsserieA2017 = serieA2017['club_name'].to_list()
    list_clubsserieA2018 = serieA2018['club_name'].to_list()
    list_clubsserieA2019 = serieA2019['club_name'].to_list()
    list_clubsserieA2020 = serieA2020['club_name'].to_list()

    list_age_serieA = []

    list_age_serieA.append(age_league(serieA, serieA2004, list_clubsserieA2004, 0))
    list_age_serieA.append(age_league(serieA, serieA2005, list_clubsserieA2005, 20))
    list_age_serieA.append(age_league(serieA, serieA2006, list_clubsserieA2006, 40))
    list_age_serieA.append(age_league(serieA, serieA2007, list_clubsserieA2007, 60))
    list_age_serieA.append(age_league(serieA, serieA2008, list_clubsserieA2008, 80))
    list_age_serieA.append(age_league(serieA, serieA2009, list_clubsserieA2009, 100))
    list_age_serieA.append(age_league(serieA, serieA2010, list_clubsserieA2010, 120))
    list_age_serieA.append(age_league(serieA, serieA2011, list_clubsserieA2011, 140))
    list_age_serieA.append(age_league(serieA, serieA2012, list_clubsserieA2012, 160))
    list_age_serieA.append(age_league(serieA, serieA2013, list_clubsserieA2013, 180))
    list_age_serieA.append(age_league(serieA, serieA2014, list_clubsserieA2014, 200))
    list_age_serieA.append(age_league(serieA, serieA2015, list_clubsserieA2015, 220))
    list_age_serieA.append(age_league(serieA, serieA2016, list_clubsserieA2016, 240))
    list_age_serieA.append(age_league(serieA, serieA2017, list_clubsserieA2017, 260))
    list_age_serieA.append(age_league(serieA, serieA2018, list_clubsserieA2018, 280))
    list_age_serieA.append(age_league(serieA, serieA2019, list_clubsserieA2019, 300))
    list_age_serieA.append(age_league(serieA, serieA2020, list_clubsserieA2020, 320))



    new_list_single_serieA = single_list(list_age_serieA)

    new_list_single_string_serieA = to_string(new_list_single_serieA)

    only_avg_list_serieA = parse_list(new_list_single_string_serieA)
    only_avg_list_float_serieA = to_float(only_avg_list_serieA)

    serieA['Age'] = only_avg_list_float_serieA


    #list => faire de list_age_serieA pas une liste de liste, mais une seule liste avec une fonction...
    #serieA['Age'] = list
    serieA.to_csv('data/concat_years_age/serieA.csv', index=False)


    # In[7]:


    ligue1 = pd.read_csv('data/concat_years/ligue1.csv')

    ligue12004 = pd.read_csv('data/AverageAge/2004/Avg_ligue1_2004Age.csv')
    ligue12005 = pd.read_csv('data/AverageAge/2005/Avg_ligue1_2005Age.csv')
    ligue12006 = pd.read_csv('data/AverageAge/2006/Avg_ligue1_2006Age.csv')
    ligue12007 = pd.read_csv('data/AverageAge/2007/Avg_ligue1_2007Age.csv')
    ligue12008 = pd.read_csv('data/AverageAge/2008/Avg_ligue1_2008Age.csv')
    ligue12009 = pd.read_csv('data/AverageAge/2009/Avg_ligue1_2009Age.csv')
    ligue12010 = pd.read_csv('data/AverageAge/2010/Avg_ligue1_2010Age.csv')
    ligue12011 = pd.read_csv('data/AverageAge/2011/Avg_ligue1_2011Age.csv')
    ligue12012 = pd.read_csv('data/AverageAge/2012/Avg_ligue1_2012Age.csv')
    ligue12013 = pd.read_csv('data/AverageAge/2013/Avg_ligue1_2013Age.csv')
    ligue12014 = pd.read_csv('data/AverageAge/2014/Avg_ligue1_2014Age.csv')
    ligue12015 = pd.read_csv('data/AverageAge/2015/Avg_ligue1_2015Age.csv')
    ligue12016 = pd.read_csv('data/AverageAge/2016/Avg_ligue1_2016Age.csv')
    ligue12017 = pd.read_csv('data/AverageAge/2017/Avg_ligue1_2017Age.csv')
    ligue12018 = pd.read_csv('data/AverageAge/2018/Avg_ligue1_2018Age.csv')
    ligue12019 = pd.read_csv('data/AverageAge/2019/Avg_ligue1_2019Age.csv')
    ligue12020 = pd.read_csv('data/AverageAge/2020/Avg_ligue1_2020Age.csv')

    list_clubsligue12004 = ligue12004['club_name'].to_list()
    list_clubsligue12005 = ligue12005['club_name'].to_list()
    list_clubsligue12006 = ligue12006['club_name'].to_list()
    list_clubsligue12007 = ligue12007['club_name'].to_list()
    list_clubsligue12008 = ligue12008['club_name'].to_list()
    list_clubsligue12009 = ligue12009['club_name'].to_list()
    list_clubsligue12010 = ligue12010['club_name'].to_list()
    list_clubsligue12011 = ligue12011['club_name'].to_list()
    list_clubsligue12012 = ligue12012['club_name'].to_list()
    list_clubsligue12013 = ligue12013['club_name'].to_list()
    list_clubsligue12014 = ligue12014['club_name'].to_list()
    list_clubsligue12015 = ligue12015['club_name'].to_list()
    list_clubsligue12016 = ligue12016['club_name'].to_list()
    list_clubsligue12017 = ligue12017['club_name'].to_list()
    list_clubsligue12018 = ligue12018['club_name'].to_list()
    list_clubsligue12019 = ligue12019['club_name'].to_list()
    list_clubsligue12020 = ligue12020['club_name'].to_list()

    list_age_ligue1 = []

    list_age_ligue1.append(age_league(ligue1, ligue12004, list_clubsligue12004, 0))
    list_age_ligue1.append(age_league(ligue1, ligue12005, list_clubsligue12005, 20))
    list_age_ligue1.append(age_league(ligue1, ligue12006, list_clubsligue12006, 40))
    list_age_ligue1.append(age_league(ligue1, ligue12007, list_clubsligue12007, 60))
    list_age_ligue1.append(age_league(ligue1, ligue12008, list_clubsligue12008, 80))
    list_age_ligue1.append(age_league(ligue1, ligue12009, list_clubsligue12009, 100))
    list_age_ligue1.append(age_league(ligue1, ligue12010, list_clubsligue12010, 120))
    list_age_ligue1.append(age_league(ligue1, ligue12011, list_clubsligue12011, 140))
    list_age_ligue1.append(age_league(ligue1, ligue12012, list_clubsligue12012, 160))
    list_age_ligue1.append(age_league(ligue1, ligue12013, list_clubsligue12013, 180))
    list_age_ligue1.append(age_league(ligue1, ligue12014, list_clubsligue12014, 200))
    list_age_ligue1.append(age_league(ligue1, ligue12015, list_clubsligue12015, 220))
    list_age_ligue1.append(age_league(ligue1, ligue12016, list_clubsligue12016, 240))
    list_age_ligue1.append(age_league(ligue1, ligue12017, list_clubsligue12017, 260))
    list_age_ligue1.append(age_league(ligue1, ligue12018, list_clubsligue12018, 280))
    list_age_ligue1.append(age_league(ligue1, ligue12019, list_clubsligue12019, 300))
    list_age_ligue1.append(age_league(ligue1, ligue12020, list_clubsligue12020, 320))

    #print(list_age_ligue1)

    new_list_single_ligue1 = single_list(list_age_ligue1)

    new_list_single_string_ligue1 = to_string(new_list_single_ligue1)
    only_avg_list_ligue1 = parse_list(new_list_single_string_ligue1)
    only_avg_list_float_ligue1 = to_float(only_avg_list_ligue1)

    #list => faire de list_age_ligue1 pas une liste de liste, mais une seule liste avec une fonction...
    ligue1['Age'] = only_avg_list_float_ligue1
    #ligue1
    ligue1.to_csv('data/concat_years_age/ligue1.csv', index=False)


    # In[5]:


    bundesliga = pd.read_csv('data/concat_years/bundesliga.csv')

    bundesliga2004 = pd.read_csv('data/AverageAge/2004/Avg_bundeshliga2004Age.csv')
    bundesliga2005 = pd.read_csv('data/AverageAge/2005/Avg_bundeshliga2005Age.csv')
    bundesliga2006 = pd.read_csv('data/AverageAge/2006/Avg_bundeshliga2006Age.csv')
    bundesliga2007 = pd.read_csv('data/AverageAge/2007/Avg_bundeshliga2007Age.csv')
    bundesliga2008 = pd.read_csv('data/AverageAge/2008/Avg_bundeshliga2008Age.csv')
    bundesliga2009 = pd.read_csv('data/AverageAge/2009/Avg_bundeshliga2009Age.csv')
    bundesliga2010 = pd.read_csv('data/AverageAge/2010/Avg_bundeshliga2010Age.csv')
    bundesliga2011 = pd.read_csv('data/AverageAge/2011/Avg_bundeshliga2011Age.csv')
    bundesliga2012 = pd.read_csv('data/AverageAge/2012/Avg_bundeshliga2012Age.csv')
    bundesliga2013 = pd.read_csv('data/AverageAge/2013/Avg_bundeshliga2013Age.csv')
    bundesliga2014 = pd.read_csv('data/AverageAge/2014/Avg_bundeshliga2014Age.csv')
    bundesliga2015 = pd.read_csv('data/AverageAge/2015/Avg_bundeshliga2015Age.csv')
    bundesliga2016 = pd.read_csv('data/AverageAge/2016/Avg_bundeshliga2016Age.csv')
    bundesliga2017 = pd.read_csv('data/AverageAge/2017/Avg_bundeshliga2017Age.csv')
    bundesliga2018 = pd.read_csv('data/AverageAge/2018/Avg_bundeshliga2018Age.csv')
    bundesliga2019 = pd.read_csv('data/AverageAge/2019/Avg_bundeshliga2019Age.csv')
    bundesliga2020 = pd.read_csv('data/AverageAge/2020/Avg_bundeshliga2020Age.csv')

    list_clubsbundesliga2004 = bundesliga2004['club_name'].to_list()
    list_clubsbundesliga2005 = bundesliga2005['club_name'].to_list()
    list_clubsbundesliga2006 = bundesliga2006['club_name'].to_list()
    list_clubsbundesliga2007 = bundesliga2007['club_name'].to_list()
    list_clubsbundesliga2008 = bundesliga2008['club_name'].to_list()
    list_clubsbundesliga2009 = bundesliga2009['club_name'].to_list()
    list_clubsbundesliga2010 = bundesliga2010['club_name'].to_list()
    list_clubsbundesliga2011 = bundesliga2011['club_name'].to_list()
    list_clubsbundesliga2012 = bundesliga2012['club_name'].to_list()
    list_clubsbundesliga2013 = bundesliga2013['club_name'].to_list()
    list_clubsbundesliga2014 = bundesliga2014['club_name'].to_list()
    list_clubsbundesliga2015 = bundesliga2015['club_name'].to_list()
    list_clubsbundesliga2016 = bundesliga2016['club_name'].to_list()
    list_clubsbundesliga2017 = bundesliga2017['club_name'].to_list()
    list_clubsbundesliga2018 = bundesliga2018['club_name'].to_list()
    list_clubsbundesliga2019 = bundesliga2019['club_name'].to_list()
    list_clubsbundesliga2020 = bundesliga2020['club_name'].to_list()

    list_age_bundesliga = []

    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2004, list_clubsbundesliga2004, 0))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2005, list_clubsbundesliga2005, 18))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2006, list_clubsbundesliga2006, 36))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2007, list_clubsbundesliga2007, 54))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2008, list_clubsbundesliga2008, 72))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2009, list_clubsbundesliga2009, 90))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2010, list_clubsbundesliga2010, 108))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2011, list_clubsbundesliga2011, 126))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2012, list_clubsbundesliga2012, 144))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2013, list_clubsbundesliga2013, 162))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2014, list_clubsbundesliga2014, 180))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2015, list_clubsbundesliga2015, 198))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2016, list_clubsbundesliga2016, 216))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2017, list_clubsbundesliga2017, 234))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2018, list_clubsbundesliga2018, 252))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2019, list_clubsbundesliga2019, 270))
    list_age_bundesliga.append(age_bundesliga(bundesliga, bundesliga2020, list_clubsbundesliga2020, 288))

    #print(list_age_bundesliga)
    new_list_single_bundesliga = single_list(list_age_bundesliga)
    new_list_single_string_bundesliga = to_string(new_list_single_bundesliga)
    #print(len(new_list_single))
    only_avg_list_bundesliga = parse_list(new_list_single_string_bundesliga)
    only_avg_list_float_bundesliga = to_float(only_avg_list_bundesliga)

    bundesliga['Age'] = only_avg_list_float_bundesliga

    #list => faire de list_age_bundesliga pas une liste de liste, mais une seule liste avec une fonction...
    #bundesliga['Age'] = list
    bundesliga.to_csv('data/concat_years_age/bundesliga.csv', index=False)

def concat_leagues():

    liga = pd.read_csv('concat_years_age/liga.csv')
    PL = pd.read_csv('concat_years_age/PL.csv')
    serieA= pd.read_csv('concat_years_age/serieA.csv')
    ligue1 = pd.read_csv('concat_years_age/ligue1.csv')
    bundesliga = pd.read_csv('concat_years_age/bundesliga.csv')

    leagues = pd.concat([liga, PL, serieA, ligue1, bundesliga], axis=0)
    #leagues_clean = leagues.drop(["Unnamed: 14","xG","xGA","xGD","xGD/90","Pts/G"], axis=1)
    list_league_name = []

    for x in range (340):
        list_league_name.append("liga")
    for y in range (340):
        list_league_name.append("PL")
    for z in range (340):
        list_league_name.append("serieA")
    for a in range (340):
        list_league_name.append("ligue1")
    for b in range (306):
        list_league_name.append("bundesliga")

    leagues['league'] = list_league_name
    leagues = leagues.astype({'Market Value':'float'})
    #leagues['Market Value'] = leagues['Market Value'].astype(float)

    leagues.to_csv("concat_leagues/league.csv")
    #leagues_clean.drop(["Unnamed: 0"], axis=1).to_csv("data/concat_leagues/leagues.csv")

concat_leagues()