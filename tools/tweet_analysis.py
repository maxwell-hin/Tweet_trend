import pandas as pd
import datetime
import numpy as np
import os
# os.getcwd()
# os.chdir("/Users/jen/Desktop/PJ/Tweet_trend")
df = pd.read_csv("test.csv")
# pepsi.dropna(subset=['Embedded_text', 'Emojis'], how='all', inplace = True)
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
import matplotlib.pyplot as plt


# raw_df = pd.read_csv("./outputs/Mcdonalds_downsample.csv", index_col=0)
# df = raw_df.iloc[:100].copy()
# df["Comments"] = df['Comments'].astype("int")
# df.info()







#=================Sentiment Analysis




def tokenize_and_process(sentence, kw=None):
    tokens = word_tokenize(sentence)
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    forbidden_word = ['http','fuck','nigger','damn','shit','Replying', 'replying','reply','twitter']
    if kw!=None:
        kw = ''.join(c for c in kw if c.isalnum())
    meaningful_words = [lemmatizer.lemmatize(stemmer.stem(word.lower())) for word in tokens if word.lower() not in stop_words and word not in punctuation and word not in forbidden_word and word.isalpha() and word.encode("utf-8").isascii() and word != kw.lower()]
    return meaningful_words




def df_text_token2list(raw_df, kw=None):
    words_list_list = []
    for lab,row in raw_df.iterrows():
        try:
            words_list_list.append(tokenize_and_process(row['Embedded_text'],kw))
        except: 
            words_list_list.append(None)
    word_list = []
    for tw_word in words_list_list:
        word_list.extend(tw_word)
    return word_list


def flatten_tokens(df):
    word_list = []
    for row in df['word_token']:
        tokens = row.split(',')
        word_list.extend(tokens)
    return word_list


def gen_freq(df, kw=None, num=20):
    word_list = flatten_tokens(df)
    word_freq = pd.Series(word_list).value_counts()
    return word_freq[:num]

gen_freq(df)

#======Tranforming raw to trans_df
def emo_sent_score(raw_df):
    from emosent_py.emosent_b.emosent import get_emoji_sentiment_rank
    emoji_list = []
    for lab, row in raw_df.iterrows():
        if row['Emojis'] == []:
            emoji_list.append(0)
        elif row['Emojis'] != []:
            emojis_each_tweets = len(''.join(row['Emojis'])) #turn list to string
            score = 0           
            for each_emoji in ''.join(row['Emojis']):
                try:
                    score = score + get_emoji_sentiment_rank(each_emoji)['sentiment_score']

                except Exception as err:
                    emojis_each_tweets = emojis_each_tweets -1
                    pass 
            if emojis_each_tweets == 0:
                emoji_list.append(0)
            else:
                score_each_tweets = score/emojis_each_tweets
                emoji_list.append(score_each_tweets)
    return emoji_list

# raw_df['Emojis'].iloc[97] 
# df = raw_df.sample(5000).reset_index(drop=True)
# emo_sent_score(df)


def sent2token(sentence):
    words = tokenize_and_process(sentence)
    return words

def keyword_sent_score(raw_df):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    score_df_keyword = pd.DataFrame()
    for keyword_text in raw_df['Embedded_text']:
        try:
            token_join = ' '.join(sent2token(keyword_text))
            score = SentimentIntensityAnalyzer().polarity_scores(keyword_text)
        except: 
            score = SentimentIntensityAnalyzer().polarity_scores('') 
        score_df=pd.DataFrame(score, index=[0])
        score_df_keyword = pd.concat([score_df_keyword,score_df])
    score_df_keyword=score_df_keyword.reset_index(drop=True)
    return score_df_keyword




#===================Transform to trans_df

def emosent_df(raw_df):
    emoji_sentdf = pd.DataFrame({'emoji_sent':emo_sent_score(raw_df)})
    # print(emoji_sentdf)
    return emoji_sentdf

def check_object(col):
    if col.dtype == 'O': #object
        col = col.str.replace(',','')
    return col


def raw_user_df(raw_df):
    tweet_raw_col = raw_df[['Username','Tweet URL','Timestamp','Comments','Likes','Retweets','Quotes']]
    #confirm dtype of cls and remove strange symbols
    tweet_raw_col = tweet_raw_col.assign(Comments=check_object(tweet_raw_col.loc[:,'Comments']))
    tweet_raw_col = tweet_raw_col.assign(Likes=check_object(tweet_raw_col.loc[:,'Likes']))
    tweet_raw_col = tweet_raw_col.assign(Retweets=check_object(tweet_raw_col.loc[:,'Retweets']))
    tweet_raw_col = tweet_raw_col.assign(Retweets=check_object(tweet_raw_col.loc[:,'Quotes']))
    tweet_raw_col = tweet_raw_col.reset_index(drop=True)
    # print(rawdf)
    return tweet_raw_col


def create_wordls(raw_df):
    text_ls = pd.DataFrame()
    for lab,row in raw_df.iterrows():
        try:
            text_chain = ','.join(sent2token(row['Embedded_text']))
        except: text_chain = ''
        text_ls = pd.concat([text_ls, pd.Series(text_chain)])
    text_ls = pd.DataFrame(text_ls).reset_index(drop=True)
    text_ls.columns = ['word_token']
    return text_ls



def combine_df(raw_df):
    trans_df = pd.concat([raw_user_df(raw_df),emosent_df(raw_df),keyword_sent_score(raw_df),create_wordls(raw_df)],axis=1)
    #print(df4.head())
    # print(df4.info())
    return trans_df


# trans_df = combine_df(raw_df)

# emoji_sentdf = pd.DataFrame({'emoji_sent':emoji_list})
# print(emoji_sentdf)

# rawdf = pepsi[['UserName','Timestamp','Tweet URL']]
# print(rawdf)

# df4 = pd.concat([emoji_sentdf,rawdf,score_df1], axis=1)
# print(df4.head())
# print(df4.info())


# =============Visualization

# def clean_data(df):


def sum_ratio_tweets (df):
    total_tweets = len(df) 
    total_likes = df['Likes'].sum() 
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum() 
    total_quotes = df['Quotes'].sum()
    return total_tweets, total_likes, total_comments, total_retweets, total_quotes

# test = sum_ratio_tweets (df)
# test

def ratio_tweets (df):
    total_likes = df['Likes'].sum()
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum()
    total_quotes = df['Quotes'].sum()
    total_scores = total_likes + total_comments + total_retweets + total_quotes
    if total_scores == 0:
        return 0, 0, 0, 0, 0, 0, 0
    likes_ratio = total_likes/total_scores
    comments_ratio = total_comments/total_scores
    retweets_ratio = total_retweets/total_scores
    quotes_ratio = total_quotes/total_scores
    return total_likes, total_comments, total_retweets, total_quotes, likes_ratio, comments_ratio, retweets_ratio, quotes_ratio

# test = ratio_tweets (df)
# test


def max_tweets (df):
    max_cm = df['Comments'].max()
    max_likes = df['Likes'].max()
    max_retweets = df['Retweets'].max()
    max_quotes = df['Quotes'].max()
    url_cm = df[df['Comments'] == df['Comments'].max()]['Tweet URL']
    url_likes = df[df['Likes'] == df['Likes'].max()]['Tweet URL']
    url_retweets = df[df['Retweets'] == df['Retweets'].max()]['Tweet URL']
    url_quotes = df[df['Quotes'] == df['Quotes'].max()]['Tweet URL']

    return [max_likes, max_cm, max_retweets, max_quotes, url_likes, url_cm, url_retweets, url_quotes]




#word_cloud123



def word_cloud(df, kw ,num=80):
    from wordcloud import WordCloud
    import random
    colormaps = ['Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c']
    
    #Generate word cloud
    wc = WordCloud(width=700, height=320, background_color='white', colormap = random.choice(colormaps),random_state=random.randint(0,100)).generate_from_frequencies(gen_freq(df, kw=kw, num=80))

    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
#Popolarity and sentiment Plot
# df5 = df4.copy()

def removetime1 (df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
    return df['Timestamp']



#need==============
# remove_time1 = removetime1(df5)
# df5['Timestamp'] = remove_time1
# print(remove_time1)
# print(df5)






# print(df5.info())
def popularity_score (df):
    total_tweets = len(df) 
    total_likes = df['Likes'].sum() 
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum() 
    total_quotes = df['Quotes'].sum()
    total_scores = total_tweets*0.3 + total_likes*0.1 + total_comments*0.2 + total_retweets*0.2 + total_quotes*0.2
    return total_scores


#need==============
# score_pop = popularity_score(df)
# print("Total Scores:", score_pop)


def daily_popularity_score (df):
    daily_sum_tweets = df.groupby('Timestamp').apply(popularity_score)
    return daily_sum_tweets


#need==============
# daily_popularity_score = daily_popularity_score(df5)
# print(daily_popularity_score)

def sentiment_score (df):
    compound_score = df[['Timestamp','compound']]
    daily_sum_score = pd.merge(compound_score,emoji_sentdf,left_index=True, right_index=True, how='outer')
    daily_sum_score['sum'] = daily_sum_score['compound'] + daily_sum_score['emoji_sent']
    daily_sentiment_score = daily_sum_score.groupby('Timestamp').sum()
    daily_sentiment_score = daily_sentiment_score.set_index('Timestamp')
    sentiment_score = daily_sentiment_score['sum']
    sentiment_score
    return sentiment_score

#need==============
# sentiment_score = sentiment_score (df5)
# print(sentiment_score)




def normalized (df):
    normalized_df=(df-df.min())/(df.max()-df.min())
    return normalized_df


#need==============
# normalized_popularity_score = normalized(daily_popularity_score)
# normalized_popularity_score
# normalized_sentiment_score = normalized(sentiment_score)
# normalized_sentiment_score.index



def plot (sentiment_score, daily_popularity_score):
    x = sentiment_score.index
    y = daily_popularity_score
    z = sentiment_score
    
    plt.figure()
    plt.subplot(121)
    plt.plot(x, y, color="orange", marker="*")

    plt.subplot(122)
    plt.plot(x, z, color="green", marker="*")
    plt.show()

#need==============
# plot_sentiment_and_popularity = plot(sentiment_score, daily_popularity_score)