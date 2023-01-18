import numpy as np
def fetch_medal_tally(df, year, state):
    medal_df = df.drop_duplicates(subset=['year','city', 'state', 'n_killed', 'n_injured'])
    flag = 0
    if year == 'Overall' and state == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and state != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['state'] == state]
    if year != 'Overall' and state == 'Overall':
        temp_df = medal_df[medal_df['year'] == int(year)]
    if year != 'Overall' and state != 'Overall':
        temp_df = medal_df[(medal_df['year'] == year) & (medal_df['state'] == state)]

    if flag == 1:
        x = temp_df.groupby('year').sum()[['n_killed', 'n_injured']].sort_values('year').reset_index()
    else:
        x = temp_df.groupby('state').sum()[['n_killed', 'n_injured']].sort_values('n_killed',
                                                                                      ascending=False).reset_index()

    x['total'] = x['n_injured'] + x['n_killed']
    x['n_killed'] = x['n_killed'].astype('int')
    x['n_injured'] = x['n_injured'].astype('int')

    return x

def state_year_list(df):
    years = df['year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    state = np.unique(df['state'].dropna().values).tolist()
    state.sort()
    state.insert(0, 'Overall')

    return years,state
def data_over_time(df,col,selected_state):
    df2 = df[df[col]== selected_state]
    df1 =df2.groupby('year')['total victims'].sum().to_frame()
    df1 = df1.reset_index(level=0)
    return df1
def city_bar(df,selected_state):
    df1= df[df['state']==selected_state]
    df2 =df1.groupby('city')['total victims'].sum().to_frame()
    df2 = df2.reset_index(level=0)
    return df2
def top_10(df,col):
    if col=='city':
        num = 10
    else:
        num=16
    data = df[[col,'n_killed']].nlargest(num, 'n_killed')[col].to_frame().reset_index().rename(columns={"index": "n_killed"})
    return data
def state_city(df):
    cities = df['city'].unique().tolist()
    cities.sort()
    cities.insert(0, 'Overall')

    state = np.unique(df['state'].dropna().values).tolist()
    state.sort()
    state.insert(0, 'Overall')


