import pyodbc
import pandas as pd
import datetime


#Connection settings
def connect_asql(): 
    server = 'jde-server.database.windows.net'
    database = 'tweet_trend'
    username = 'chlaw'
    password = 'Abc1234567890abC'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    return cnxn


#look for historical keywords, reture T/F, keyword_id
def keyword_hist(kw):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM keywords')
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


#find date range of history tweets 
def hist_date_range(kw_id):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute(f'''SELECT max(time_stamp) FROM tweets
                        WHERE keyword_id = {kw_id};    ''')
    row = cursor.fetchone()
    earliest_tweet = row[0].strftime("%Y-%m-%d")
    cursor.execute(f'''SELECT min(time_stamp) FROM tweets
                        WHERE keyword_id = {kw_id};    ''')
    row = cursor.fetchone()
    oldest_tweet = row[0].strftime("%Y-%m-%d")
    cursor.close()
    return earliest_tweet, oldest_tweet

#============insert data
def tweet2query(df, kw_id):  
    query = f'''INSERT INTO tweets (keyword_id, user_name, time_stamp, comments_no, likes_no, retweets_no, text_neg, text_neu, text_pos, text_comp, emoji_sent, tweet_url) VALUES (
    {kw_id},
    '{'NULL' if pd.isna(df.UserName) else df.UserName}',
    '{df.Timestamp}',
    {0 if pd.isna(df.Comments) else df.Comments},
    {0 if pd.isna(df.Likes) else df.Likes},
    {0 if pd.isna(df.Retweets) else df.Retweets},
    {df['neg']},
    {df['neu']},
    {df['pos']},
    {df['compound']},
    {df['emoji_sent']},
    '{df['Tweet URL']}'
    )'''
    return query


def update_records(df, kw_id):
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    for lab, row in df.iterrows():
        query = tweet2query(row,kw_id)
        cursor.execute(query) 
        cnxn.commit()
        print('finish ',lab)
    cursor.close()   

bol, kw_id = keyword_hist('Pepsi')
update_records(df, kw_id)

df.iloc[34]

def new_keywords(keyword):
    query = f'''INSERT INTO keywords (keyword)
    VALUES (keyword);'''
    cnxn = connect_asql()
    cursor = cnxn.cursor()
    cursor.execute(query) 
    cnxn.commit()
    cursor.close()


#======================Query data

def download_from_db(kw_id, since, until):
    query = f"SELECT * FROM tweets WHERE keyword_id = {kw_id};"
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
        df = pd.concat([df,df_tem])
        row = cursor.fetchone()
    return df





