import pandas as pd

def get_data(file, columns=[], ffill=False):
    df =  pd.read_pickle(file)

    if len(columns):
        df = df.filter(columns)

    return df.fillna(method='ffill') if ffill else df.fillna(0)




def get_tweeter_threads(file):
    threads = get_data(file, columns=['created_at', 'num_comments', 'score', 'upvote_ratio'])
    threads.created_at = threads.created_at.apply(lambda x: x[:10])
    threads = threads.groupby('created_at').agg(list)
    threads.num_comments = threads.num_comments.apply(lambda x: sum(x))
    threads.score = threads.score.apply(lambda x: sum(x))
    threads.upvote_ratio = threads.upvote_ratio.apply(lambda x: sum(x)/float(len(x)))
    return threads