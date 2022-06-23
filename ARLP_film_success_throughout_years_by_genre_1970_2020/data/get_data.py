import pandas as pd
import numpy as np
import glob
from scipy import stats

def contains(container, elt):
  return elt in container

def load_csv():
  all_files = glob.glob("ARLP_film_success_throughout_years_by_genre_1970_2020/data/*[0-9].pkl")
  li = []

  for filename in all_files:
      csv = pd.read_pickle(filename)
      li.append(csv)

  return pd.concat(li)
  
def clean_rating(df):
  df.loc[df['rating'] == 'Unrated', 'rating'] = 'Not Rated' #changing 'Unrated' movies to 'Not Rated'
  df.loc[(df['rating'] == 'E') | (df['rating'] == 'Open')| (df['rating'] == 'TV-G')| (df['rating'] == 'E10+'), 'rating'] = 'G'
  df.loc[(df['rating'] == 'MA-13') | (df['rating'] == 'TV-13')| (df['rating'] == 'TV-14'), 'rating'] = 'PG-13'
  df.loc[(df['rating'] == 'TV-Y7-FV'), 'rating'] = 'TV-Y7'
  df.loc[(df['rating'] == 'MA-17') | (df['rating'] == 'TV-MA')| (df['rating'] == 'X'), 'rating'] = 'NC-17'
  df.loc[(df['rating'] == 'TV-PG') | (df['rating'] == 'M') | (df['rating'] == 'M/PG') | (df['rating'] == 'GP'), 'rating'] = 'PG'
  df.rating.fillna('Unknown', inplace=True)
  df.loc[(df['name'] == 'Murder Manual') & (df['rating'] == '18'), 'rating'] = 'PG-13'
  
def drop_duplicates(df):
  #We sort the movies by their amount of Nan. So in case of duplicates we keep the one with more infos.
  df = df.iloc[df.isnull().sum(axis=1).mul(-1).argsort()].drop_duplicates(subset=['name', 'released'], keep='last')
  df[df.duplicated(subset=['name', 'released'])]
  return df
  
def clean_score(df):
  def total_score(imdb_score, rotten_score):
    if imdb_score == None or pd.isna(imdb_score):
      return rotten_score / 10
    if rotten_score == None or pd.isna(rotten_score):
      return imdb_score
    return round((imdb_score + rotten_score/10) / 2, 1)

  df.imdb_score = df.imdb_score.astype('float64')
  df.rotten_score = df.rotten_score.astype('float64')
  df['total_score'] = df.apply(lambda df: total_score(df['imdb_score'], df['rotten_score']), axis=1)
  
def clean_suspicious_data(df):
  #Movies with big budget and low votes is really suspicious hence the drop
  tmp = df.copy()
  tmp.budget.fillna(0, inplace=True)
  tmp.gross.fillna(0, inplace=True)
  tmp['profit'] = np.abs(tmp['gross'] - tmp['budget'])
  tmp.loc[tmp['votes'] == 0, 'votes'] = 1
  ratio = tmp['profit'] / tmp['votes']
  zscore = stats.zscore(ratio)
  df.drop(df[zscore > 1].index, inplace=True)
  
def clean_irrelevant_data(df):
  low_votes = 100 # arbitrary choice for under which we consider data may not be correct and the note may not be representative
  before = len(df)
  df.drop(df[(df['votes'] == 0)].index, inplace=True) #if no votes then it is a very very small movie and there's no critic to prove it even exists, most of them don't have a budget nor a release date
  no_votes = len(df)
  df.drop(df[df['runtime'].isna()].index, inplace=True) #We want to remove shortfilms, if we don't have length we assume it is a shortfilm.
  no_runtime = len(df)
  df.drop(df[(df['votes'] < low_votes) & df['budget'].isna()].index, inplace=True) #if there are only a few votes the note may not be representative and if we also don't have budget then there is nothing we can really do with the data
  no_budget_low_votes = len(df)
  df.drop(df[df['runtime'] < 60].index, inplace=True) #Drop short films
  no_shortfilms = len(df)
  df.drop(df[df['year'] > 2020].index, inplace=True)
  no_movies_after_2020 = len(df)

def clean_genre(df_):
  return df_[df_.apply(lambda df: not contains(df['genre'], 'Talk-Show')
                              and not contains(df['genre'], 'Reality-TV')
                              and not contains(df['genre'], 'News')
                              and not contains(df['genre'], 'Game-Show'), axis=1)]
                              
def pre_treatment(df):
  before = len(df)
  df.reset_index(inplace=True, drop=True)

  clean_rating(df)
  df = drop_duplicates(df)

  #DIRECTOR IS WRITER
  def director_is_writer(directors, writers):
    if directors == None or writers == None:
      return 0
    for director in directors:
      for writer in writers:
        if director in writer:
          return 1
    return 0

  df['director_is_writer'] = df.apply(lambda df: director_is_writer(df['director'], df['writer']), axis=1)

  #PROFIT
  df.budget = df.budget.astype('float64')
  df.gross = df.gross.astype('float64')
  df['profit'] = df['gross'] - df['budget']

  clean_score(df)

  #OTHER
  df.runtime = df.runtime.astype('float64')
  df.votes = df.votes.astype('float64')
  df.votes.fillna(0, inplace=True)
  df.company = df.company.apply(lambda d: d if isinstance(d, list) else [])
  df.writer = df.writer.apply(lambda d: d if isinstance(d, list) else [])
  df.genre = df.genre.apply(lambda d: d if isinstance(d, list) else [])

  df.released = pd.to_datetime(df.released)
  df.loc[~df.released.isna(), 'year'] = df.released.dt.year

  removed_dup = len(df)

  df = clean_genre(df)
  clean_irrelevant_data(df)
  clean_irrelevant = len(df)

  clean_suspicious_data(df)
  clean_suspicious = len(df)
  
  return df
  
def extract_data():
    df = load_csv()
    df = pre_treatment(df)
    return df