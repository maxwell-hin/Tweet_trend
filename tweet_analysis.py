import pandas as pd
import datetime
import numpy as np
pepsi = pd.read_csv('./outputs/pepsi_2022-06-01_2022-12-31.csv')
pepsi = pepsi.dropna(subset=['Embedded_text'])
import nltk
# nltk.download('vader_lexicon')
import matplotlib.pyplot as plt

def sum_ratio_tweets (df):
    total_tweets = len(df) 
    total_likes = df['Likes'].sum() 
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum() 
    return total_tweets, total_likes, total_comments, total_retweets



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
    return total_likes, total_comments, total_retweets, likes_ratio, comments_ratio, retweets_ratio


def max_tweets (df):
    max_cm = df['Comments'].max()
    max_likes = df['Likes'].max()
    max_retweets = df['Retweets'].max()
    url_cm = df[df['Comments'] == df['Comments'].max()]['Tweet URL']
    url_likes = df[df['Likes'] == df['Likes'].max()]['Tweet URL']
    url_retweets = df[df['Retweets'] == df['Retweets'].max()]['Tweet URL']

    return max_likes, max_cm, max_retweets,  url_likes, url_cm, url_retweets



def removetime (df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
    groupbytimestamp =  df['Timestamp'].reset_index()
    groupbytimestamp = df.groupby(['Timestamp']).size()

    return groupbytimestamp

   
def emo_list(raw_df):
    from emosent_py.emosent_b.emosent import get_emoji_sentiment_rank
    emoji_list = []
    for lab, row in raw_df.iterrows():
        if pd.isnull(row['Emojis']) != False:
            emoji_list.append(0)
        elif pd.isnull(row['Emojis']) == False:

            if len(row['Emojis']) >= 1:
                emojis_each_tweets = len(row['Emojis'].split(" ")) 
                score = 0           
                for each_emoji in row['Emojis'].split(" "):
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

            

def keyword_data(raw_df):

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    score_df_keyword = pd.DataFrame()
    for keyword_text in df['Embedded_text']:
      score = SentimentIntensityAnalyzer().polarity_scores(str(keyword_text))
      score_df=pd.DataFrame(score, index=[0])
      score_df_keyword = pd.concat([score_df_keyword,score_df])
    score_df1=score_df_keyword.reset_index(drop=True)
    return score_df1



# emoji_sentdf = pd.DataFrame({'emoji_sent':emoji_list})
# print(emoji_sentdf)

# rawdf = pepsi[['UserName','Timestamp','Tweet URL']]
# print(rawdf)

# df4 = pd.concat([emoji_sentdf,rawdf,score_df1], axis=1)
# print(df4.head())
# print(df4.info())


# =============Visualization

#word_cloud
def tokenize_and_process(sentence, kw):
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from string import punctuation
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    tokens = word_tokenize(sentence)
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    forbidden_word = ['fuck','nigger','damn','shit']
    meaningful_words = [lemmatizer.lemmatize(stemmer.stem(word.lower())) for word in tokens if word.lower() not in stop_words and word not in punctuation and word not in forbidden_word and word.isalpha() and word.encode("utf-8").isascii() and word != kw]
    return meaningful_words


def word_token2list(df, kw):
    words_list = []
    for lab,row in df.iterrows():
        words_list.append(tokenize_and_process(row['Embedded_text'],kw))
    return words_list



def gen_freq(df, kw, num=20):
    words = []
    word_list = word_token2list(df, kw)
    for tw_word in word_list:
        words.extend(tw_word)
    word_freq = pd.Series(words).value_counts()
    return word_freq[:num]

# gen_freq(df, 'Pepsi')

def word_cloud(df, kw ,num=80):
    from wordcloud import WordCloud
    import random
    colormaps = ['Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c']
    
    #Generate word cloud
    wc = WordCloud(width=700, height=320, background_color='white', colormap = random.choice(colormaps),random_state=random.randint(0,100)).generate_from_frequencies(gen_freq(df, kw, num=80))

    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


#Popolarity and sentiment Plot

df5 = df4.copy()

import datetime
def removetime1 (df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
    return df['Timestamp']

remove_time1 = removetime1(df5)
df5['Timestamp'] = remove_time1
print(remove_time1)
print(df5)
# print(df5.info())

def popularity_score (df):
    total_tweets = len(df) 
    total_likes = df['Likes'].sum() 
    total_comments = df['Comments'].sum()
    total_retweets = df['Retweets'].sum() 
    total_scores = total_tweets*0.5 + total_likes*0.1 + total_comments*0.2 + total_retweets*0.2
    return total_scores

score_pop = popularity_score (df5)
print("Total Scores:", score_pop)

import numpy as np
import matplotlib.pyplot as plt

def daily_popularity_score (df):
    daily_sum_tweets = df.groupby('Timestamp').apply(popularity_score)
    return daily_sum_tweets

daily_popularity_score = daily_popularity_score(df5)
print(daily_popularity_score)
# daily_popularity_score.max()


# daily_popularity_score.plot(kind='line')
# plt.ylabel('Daily Popularity Score')
# plt.xlabel('Timestamp')
# plt.title('Popularity Scores per day')
# plt.show()

def sentiment_score (df):
    compound_score = df[['Timestamp','compound']]
    daily_sum_score = pd.merge(compound_score,emoji_sentdf,left_index=True, right_index=True, how='outer')
    daily_sum_score['sum'] = daily_sum_score['compound'] + daily_sum_score['emoji_sent']
    daily_sentiment_score = daily_sum_score.groupby('Timestamp').sum()
    daily_sentiment_score = daily_sentiment_score.set_index('Timestamp')
    daily_sentiment_score
    sentiment_score = daily_sentiment_score['sum']
    sentiment_score
    return sentiment_score

sentiment_score = sentiment_score (df5)
print(sentiment_score)

compound_score = df5[['Timestamp','compound']]
compound_score
daily_sum_score = pd.merge(compound_score,emoji_sentdf,left_index=True, right_index=True, how='outer')
daily_sum_score['total_sent'] = daily_sum_score['compound'] + daily_sum_score['emoji_sent']
daily_sentiment_score = daily_sum_score.groupby('Timestamp').sum()
sentiment_score = daily_sentiment_score['total_sent']
sentiment_score


# sentiment_score.plot(kind='line')
# plt.ylabel('Daily Sentiment Score')
# plt.xlabel('Timestamp')
# plt.title('Sentiment Scores per day')
# plt.show()

import matplotlib.pyplot as plt

def normalized (df):
    normalized_df=(df-df.min())/(df.max()-df.min())
    return normalized_df

normalized_popularity_score = normalized(daily_popularity_score)
normalized_popularity_score

normalized_sentiment_score = normalized(sentiment_score)
normalized_sentiment_score.index


# x = sentiment_score.index
# y = daily_popularity_score
# z = sentiment_score

# print(sentiment_score)
# plt.figure()
# plt.subplot(121)
# plt.plot(x, y, color="orange", marker="*")
 
# plt.subplot(122)
# plt.plot(x, z, color="yellow", marker="*")
# plt.show()

x = normalized_sentiment_score.index
y = normalized_popularity_score
z = normalized_sentiment_score

plt.figure()
plt.subplot(121)
plt.plot(x, y, color="orange", marker="*")
 
plt.subplot(122)
plt.plot(x, z, color="yellow", marker="*")
plt.show()
