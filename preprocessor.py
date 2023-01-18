import pandas as pd
def preprocess(df):
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['total victims']  = df['n_killed'] + df['n_injured']
    df.drop_duplicates(inplace=True)
    return df