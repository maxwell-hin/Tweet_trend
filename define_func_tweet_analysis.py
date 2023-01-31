import pandas as pd
import os
pepsi = pd.read_csv('./outputs/pepsi_2022-06-01_2022-12-31.csv')
KFC01_to_20 =pd.read_csv('./outputs/KFC_2022-01-01_2023-01-20.csv')
#pepsi
#os.getcwd()

def sum_tweets (df):
    total_tweets = len(df) 
    total_likes = df['Likes'].sum() 
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum() 
    return total_tweets, total_likes, total_comments, total_retweets

scores = sum_tweets (pepsi)
print(scores)
print("Total tweets : "+ str(scores[0]))
print("Total comments: "+ str(scores[1]))
print("Total likes: "+ str(scores[2]))
print("Total retweets: "+ str(scores[3]))

def ratio_tweets (df):
    total_likes = df['Likes'].sum()
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum()
    total_scores = total_likes + total_comments + total_retweets
    if total_scores == 0:
        return 0, 0, 0, 0, 0, 0, 0
    likes_ratio = total_likes/total_scores
    comments_ratio = total_comments/total_scores
    retweets_ratio = total_retweets/total_scores
    return total_likes, total_comments, total_retweets, total_scores, comments_ratio, likes_ratio, retweets_ratio
    
scores_two = ratio_tweets (pepsi)
print("Total Scores:", scores_two[3])
print("Comments Ratio:", scores_two[4])
print("Likes Ratio:", scores_two[5])
print("Retweets Ratio:", scores_two[6])

def max_tweets (df):
    max_cm = df['Comments'].max()
    max_likes = df['Likes'].max()
    max_retweets = df['Retweets'].max()
    url_cm = df[df['Comments'] == df['Comments'].max()]['Tweet URL']
    url_likes = df[df['Likes'] == df['Likes'].max()]['Tweet URL']
    url_retweets = df[df['Retweets'] == df['Retweets'].max()]['Tweet URL']

    return max_cm, max_likes, max_retweets, url_cm, url_likes, url_retweets

# scores_three = max_tweets(pepsi)
# print('The max number of comments: ' + str(scores_three[0]), 'URL: ' + str(scores_three[3]))
# print('The max number of likes: ' + str(scores_three[1]), 'URL: ' + str(scores_three[4]))
# print('The max number of retweets: ' + str(scores_three[2]),'URL: ' + str(scores_three[5]))


def removetime (df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
    groupbytimestamp =  df['Timestamp'].reset_index()
    groupbytimestamp = df.groupby(['Timestamp']).size()

    return groupbytimestamp

tweets_per_day = removetime(pepsi)
print(tweets_per_day)


# pd.date_range(start='01/06/2022', end='31/12/2022')


import datetime
import numpy as np
# import matplotlib.pyplot as plt


# fig, ax = plt.subplots()
# tweets_per_day.plot(kind='line', ax=ax)
# ax.set_xticklabels(tweets_per_day.index.strftime('%y-%m-%d'))

tweets_per_day.plot(kind='line')
plt.ylabel('Number of tweets')
plt.xlabel('Timestamp')
plt.title('Tweets per day')
plt.show()


from emosent_py.emosent_b.emosent import get_emoji_sentiment_rank

    
def emo_list(emo_list001):
    emoji_list = []
    for lab, row in emo_list001.iterrows():
        if pd.isnull(row['Emojis']) != False:
            emoji_list.append(0)
        elif pd.isnull(row['Emojis']) == False:
            # if len(row['Emojis']) == 1:
            #     try:
            #         emoji_list.append(get_emoji_sentiment_rank(row['Emojis'])['sentiment_score'])
            #     except:
            #         pass
            if len(row['Emojis']) >= 1:
                # row['Emojis'].split(" ")
                # print(row['Emojis'])
                emojis_each_tweets = len(row['Emojis'].split(" ")) 
                # emojis_each_tweets

                score = 0           
                for each_emoji in row['Emojis'].split(" "):
                    try:
                        # print(get_emoji_sentiment_rank(each_emoji)['sentiment_score'])
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

      

# print(score)         
# print(emoji_list)
# print(score_each_tweets)
# len(emoji_list)


#from textblob import TextBlob
# import sys
import nltk
nltk.download('vader_lexicon')
# import re
# import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk.stem import SnowballStemmer

# def percentage(part,whole):
#  return 100 * float(part)/float(whole)
# positive = 0
# negative = 0
# neutral = 0
# polarity = 0
# tweet_list = []
# neutral_list = []
# negative_list = []
# positive_list = []




def keyword_data(keyword):
    score_df_keyword = pd.DataFrame()
    for keyword_text in keyword['Embedded_text']:
      score = SentimentIntensityAnalyzer().polarity_scores(str(keyword_text))
      score_df=pd.DataFrame(score, index=[0])
    # score_df_pepsi=score_df_pepsi.append(score_df)
      score_df_keyword = pd.concat([score_df_keyword,score_df])
    score_df1=score_df_keyword.reset_index(drop=True)
# print(score_df1)
    return score_df1


def emosent_df(keyword_list_emo):
    emoji_sentdf = pd.DataFrame({'emoji_sent':emo_list(keyword_list_emo)})
    # print(emoji_sentdf)
    return emoji_sentdf


def raw_user_df(raw_user_data):
    rawdf = raw_user_data[['UserName','Timestamp','Tweet URL']]
    # print(rawdf)
    return rawdf

def combine_df(lets_say_pepsi):
    df4 = pd.concat([raw_user_df(lets_say_pepsi),emosent_df(lets_say_pepsi),keyword_data(lets_say_pepsi)], axis=1)
    #print(df4.head())
    # print(df4.info())
    return print(df4)


combine_df(KFC01_to_20)
