from textblob import TextBlob 
import sys 
import tweepy 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import os 
import nltk 
import pycountry 
import re 
import string
from wordcloud import WordCloud, STOPWORDS 
from PIL import Image 
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from langdetect import detect 
from nltk.stem import SnowballStemmer 
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def percentage(part,whole):
 return 100 * float(part)/float(whole)



x=pd.read_csv("mcdonalds_2022-06-01_2022-12-31.csv")
y=pd.read_csv("pepsi_2022-06-01_2022-12-31.csv")
x_full=x['Embedded_text'].dropna()

positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
for tweet in x_full:
 

 tweet_list.append(tweet)
 analysis = TextBlob(tweet)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 polarity += analysis.sentiment.polarity
 
 if neg > pos:
  negative_list.append(tweet)
  negative += 1
 elif pos > neg:
  positive_list.append(tweet)
  positive += 1
 
 elif pos == neg:
  neutral_list.append(tweet)
  neutral += 1

noOfTweet = len(x_full)
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')
print(noOfTweet)
print(positive)
print(negative)
print(neutral)
print(polarity)