import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import datetime




def query(text, since, until):
    q = text #keyword
    q += f" until:{until}"
    q += f" since:{since}"
    return q





def snscraperper(text,since, until, interval=3):
    d= interval
    tweet_list = []

    #create date list with specific interval s
    dt_rng = pd.date_range(start=since,end=until,freq=f'{d}D')

    #Scrape for each day
    for dt in dt_rng:
        #since to until = since + 1 day
        q = query(text, since = datetime.strftime(dt,'%Y-%m-%d'), until = datetime.strftime(dt+pd.to_timedelta(1,'D'),'%Y-%m-%d'))
        print('start scraping {date}'.format(date = datetime.strftime(dt,'%Y-%m-%d')))
        
        counter = 0
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
            tweet_list.append([tweet.date, tweet.user.username, tweet.rawContent,  tweet.likeCount,tweet.replyCount, tweet.retweetCount, tweet.quoteCount, tweet.url])
            counter+=1
            if counter%500 == 0: print(f'{counter} scrapped')

        print('finished scraping {date}, # of tweets: {no_tweet}'.format(date = datetime.strftime(dt,'%Y-%m-%d'), no_tweet = counter))
        
    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweet_list, columns=['Timestamp','Username', 'Embedded_text','Likes','Comments', 'Retweets', 'Quotes', 'Tweet URL'])
    return tweets_df

text = 'KFC' 
since = '2022-06-01'
until = '2022-12-31'
interval = 3

data = snscraperper(text, since, until, interval=3)
data.to_csv('KFC.csv')