import pandas as pd
import snscrape.modules.twitter
import pandas as pd
from datetime import datetime
import os
import pandas as pd
import numpy as np
import datetime
from tqdm.notebook import tqdm_notebook
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


'''
THis script will create a folder with all the tweets about a keyword on a range of date
Tweets of the same day will be put into one csv file 
'''
text = input(
    'Enter query text to be matched (or leave it blank by pressing enter)')


since = input(
    'Enter startdate in this format yyyy-mm-dd (or leave it blank by pressing enter): ')

until = input(
    'Enter enddate in this format yyyy-mm-dd (or leave it blank by pressing enter): ')

count = int(input(
    'Enter max number of tweets or enter -1 to retrieve all possible tweets: '))

likes = input('Exclude likes? (y/n): ')

retweet = input('Exclude Retweets? (y/n): ')

replies = input('Exclude Replies? (y/n): ')


def search(text, username, since, until, retweet, replies):

    global filename


        q = text
         if username != '':
                q += f" from:{username}"
         if until == '':
                until = datetime.datetime.strftime(datetime.date.today(), '%Y-%m-%d')
        q += f" until:{until}"
         if since == '':
                since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') -
                                                   datetime.timedelta(days=7), '%Y-%m-%d')
        q += f" since:{since}"
         if retweet == 'y':
                q += f" exclude:retweets"
         if replies == 'y':
                q += f" exclude:replies"
         if username != '' and text != '':
                filename = f"{since}_{until}_{username}_{text}.csv"
         elif username != "":
                filename = f"{since}_{until}_{username}.csv"
         else:
                filename = f"{since}_{until}_{text}.csv"
         print(filename)
        return q


q = search(text, username, since, until, retweet, replies)

# Creating list to append tweet data

tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list

if count == -1:
    for i, tweet in enumerate(tqdm_notebook(sntwitter.TwitterSearchScraper(q).get_items())):
        tweets_list1.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.lang,
                             tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
else:
    with tqdm_notebook(total=count) as pbar:
        # declare a username
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            if i >= count:  # number of tweets you want to scrape
                break
            tweets_list1.append([tweet. Date, tweet.id, tweet.rawContent, tweet.user.username, tweet.lang,
                                tweet.hashtags, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
            pbar.update(1)

# Creating a dataframe from the tweets list above
tweets_df1 = pd.DataFrame(tweets_list1, columns=['DateTime', 'TweetId', 'Text', 'Username',
                          'Language', 'Hashtags', 'ReplyCount', 'RetweetCount', 'LikeCount', 'QuoteCount', 'Media'])
