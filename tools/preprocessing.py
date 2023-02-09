import pandas as pd
import advertools as adv
import random
pd.options.mode.chained_assignment = None  # default='warn'

# raw_df = pd.read_csv("./outputs/McDonald's_2022-06-01_2022-12-31.csv")
# df_downsample = pd.read_csv("./outputs/Mcdonalds_downsample.csv")


def remove_emoji(sentence):
    ind_ls = []
    for ind, pos in enumerate(adv.extract_emoji(sentence)['emoji_counts']):
        if pos == 1:
            ind_ls.append(ind)
    ind_ls = ind_ls[::-1]
    for i in ind_ls:
        sentence = sentence[:i] + sentence[i+1:]
    return sentence

def create_emoji_ls(sentence):
    emoji_ls = adv.extract_emoji(sentence)['emoji_flat']
    return emoji_ls

def clean_df(raw_df):
    raw_df.columns = ['index', 'Timestamp', 'Username', 'Embedded_text', 'Likes', 'Comments', 'Retweets', 'Quotes', 'Tweet URL'] 
    raw_df = raw_df.drop_duplicates(subset=['index','Tweet URL'])
    raw_df.drop('index', inplace=True, axis=1)
    raw_df.dropna(subset=['Tweet URL'], inplace=True)
    raw_df['Timestamp'] = raw_df['Timestamp'].apply(lambda x: x[:10])
    raw_df_downsample = raw_df.groupby(raw_df['Timestamp']).sample(frac=0.08, random_state=random.randint(0,1000))
    raw_df_downsample.reset_index(drop=True)
    raw_df_downsample['Comments'] = raw_df_downsample['Comments'].astype('int')
    raw_df_downsample['Retweets'] = raw_df_downsample['Retweets'].astype('int')
    raw_df_downsample['Likes'] = raw_df_downsample['Likes'].astype('int')
    raw_df_downsample['Quotes'] = raw_df_downsample['Quotes'].astype('int')
    raw_df_downsample['Emojis'] = raw_df_downsample['Embedded_text'].apply(create_emoji_ls)
    raw_df_downsample['Embedded_text'] = raw_df_downsample['Embedded_text'].apply(remove_emoji)
    return raw_df_downsample

# data = clean_df(raw_df)
# type(data['Emojis'].iloc[0])
# import time
# start = time.time()
# raw_df_downsample['Emojis'] = raw_df_downsample['Embedded_text'].apply(create_emoji_ls)
# end = time.time()
# t = round(end - start,2)
# print('Runtime: ',round(t,2),'s')

# import time
# start = time.time()
# raw_df_downsample['Embedded_text'] = raw_df_downsample['Embedded_text'].apply(remove_emoji)
# end = time.time()
# t = round(end - start,2)
# print('Runtime: ',round(t,2),'s')


# raw_df_downsample.drop('index',inplace=True, axis=1)
# raw_df_downsample.sample(20)
# raw_df_downsample = raw_df_downsample.astype({'Comments': 'int64', 'Likes': 'int64', 'Quotes': 'int64', 'Retweets': 'int64'})
# raw_df_downsample.info()
# raw_df_downsample.to_csv('Mcdonalds_downsample.csv')