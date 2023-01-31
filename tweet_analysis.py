import pandas as pd
import datetime
import numpy as np
pepsi = pd.read_csv('./outputs/pepsi_2022-06-01_2022-12-31.csv')
pepsi = pepsi.dropna(subset=['Embedded_text'])
import nltk
# nltk.download('vader_lexicon')
import matplotlib.pyplot as plt

def sum_tweets (df):
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
    return total_likes, total_comments, total_retweets, total_scores, comments_ratio, likes_ratio, retweets_ratio


def max_tweets (df):
    max_cm = df['Comments'].max()
    max_likes = df['Likes'].max()
    max_retweets = df['Retweets'].max()
    url_cm = df[df['Comments'] == df['Comments'].max()]['Tweet URL']
    url_likes = df[df['Likes'] == df['Likes'].max()]['Tweet URL']
    url_retweets = df[df['Retweets'] == df['Retweets'].max()]['Tweet URL']

    return max_cm, max_likes, max_retweets, url_cm, url_likes, url_retweets



def removetime (df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
    groupbytimestamp =  df['Timestamp'].reset_index()
    groupbytimestamp = df.groupby(['Timestamp']).size()

    return groupbytimestamp






# import matplotlib.pyplot as plt


# fig, ax = plt.subplots()
# tweets_per_day.plot(kind='line', ax=ax)
# ax.set_xticklabels(tweets_per_day.index.strftime('%y-%m-%d'))

# tweets_per_day.plot(kind='line')
# plt.ylabel('Number of tweets')
# plt.xlabel('Timestamp')
# plt.title('Tweets per day')
# plt.show()




    
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



def gen_freq(df, kw, num=80):
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
