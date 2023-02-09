import pyodbc
import pandas as pd
import datetime


# Connection settings
def connect_asql():
    server = 'jde-server.database.windows.net'
    database = 'tweet_trend'
    username = 'chlaw'
    password = 'Abc1234567890abC'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server +
                          ';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD=' + password)
    return cnxn


# look for historical keywords, reture T/F, keyword_id
def keyword_hist(kw):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM JMJ.keywords')
    kw_ls = []
    row = cursor.fetchone()
    while row:
        kw_row = []
        kw_row = [elem for elem in row]
        kw_ls.append(kw_row[1])
        row = cursor.fetchone()
    cursor.close()
    if kw in kw_ls:
        return True, kw_ls.index(kw)+1
    else:
        return False, None


keyword_hist('KFC')

# find date range of history tweets


def hist_date_range(kw_id):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute(f'''SELECT max(time_stamp) FROM JMJ.tweets
                        WHERE keyword_id = {kw_id};    ''')
    row = cursor.fetchone()
    earliest_tweet = row[0].strftime("%Y-%m-%d")
    cursor.execute(f'''SELECT min(time_stamp) FROM JMJ.tweets
                        WHERE keyword_id = {kw_id};    ''')
    row = cursor.fetchone()
    oldest_tweet = row[0].strftime("%Y-%m-%d")
    cursor.close()
    return earliest_tweet, oldest_tweet

# ============insert data


def tweet2query(df, kw_id):
    query = '''INSERT INTO JMJ.tweets (keyword_id, user_name, time_stamp, comments_no, likes_no, retweets_no, word_token, text_neg, text_neu, text_pos, text_comp, emoji_sent, tweet_url) VALUES (
    {kw_id},
    {username},
    '{timestamp}',
    {comment},
    {like},
    {retweet},
    {word_token},
    {text_neg},
    {text_neu},
    {text_pos},
    {text_compound},
    {emoji_sent},
    '{tweet_url}'
    );'''
    return query.format(kw_id=kw_id, username='NULL' if pd.isna(df.Username) else "'"+df.Username+"'", timestamp=df.Timestamp, comment=0 if pd.isna(df.Comments) else df.Comments, like=0 if pd.isna(df.Likes) else df.Likes, retweet=0 if pd.isna(df.Retweets) else df.Retweets, word_token='NULL' if pd.isnull(df['word_token']) else "'"+df['word_token']+"'", text_neg=df['neg'], text_neu=df['neu'], text_pos=df['pos'], text_compound=df['compound'], emoji_sent=df['emoji_sent'], tweet_url=df['Tweet URL'])


# print(tweet2query(trans_df.iloc[1234],2))

def update_records(df, kw_id):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    for lab, row in df.iterrows():
        query = tweet2query(row, kw_id)
        try:
            cursor.execute(query)
            cnxn.commit()
        except:
            print('error', lab)
            continue
        print('finish ', lab)
    cursor.close()
    print('update finished')


def new_keywords(keyword):
    query = f'''INSERT INTO JMJ.keywords (keyword)
    VALUES (keyword);'''
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute(query)
    cnxn.commit()
    cursor.close()


# ======================Query data

def download_from_db(kw_id, since, until):
    query = f"SELECT * FROM JMJ.tweets WHERE keyword_id = {kw_id};"
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    df_list = [elem for elem in row]
    df = pd.DataFrame()
    while row:
        df_ls = []
        df_list = [elem for elem in row]
        df_tem = pd.DataFrame([df_list])
        df = pd.concat([df, df_tem])
        row = cursor.fetchone()
    df.columns = ['tweet_id', 'keyword_id', 'user_name', 'time_stamp', 'comments_no', 'likes_no',
                  'retweets_no', 'word_token', 'text_neg', 'text_neu', 'text_pos', 'text_comp', 'emoji_sent', 'tweet_url']
    df.drop(['tweet_id'], axis=1, inplace=True)
    return df
