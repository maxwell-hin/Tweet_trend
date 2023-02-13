from datetime import datetime
import snscrape.modules.twitter as sntwitter
import tools.AzureSQL_DDL as az
import tools.tweet_analysis as tw
import pandas as pd
import tools.preprocessing as pp

# raw_df = pd.read_csv("outputs/McDonald's_2022-06-01_2022-12-31.csv")
raw_df = pp.clean_df(raw_df)
trans_df = tw.combine_df(raw_df)


# # trans = pd.concat([trans_df2, trans_df], ignore_index=True)


# az.update_records(trans_df[:10], 1)


# df = az.download_from_db(1, '2022-06-01', '2022-06-13')

# # az.connect_asql()
# # query = "UPDATE JMJ.tweets SET tweet_id"


def query(text, since, until):
    q = text  # keyword
    q += f" until:{until}"
    q += f" since:{since}"
    q += f" geocode:41.4925374,-99.9018131,1500km"
    return q


def snscraperper(text, since, until, interval=1):
    d = interval
    tweet_list = []

    # create date list with specific interval s
    dt_rng = pd.date_range(start=since, end=until, freq=f'{d}D')

    # Scrape for each day
    for dt in dt_rng:
        # since to until = since + 1 day
        q = query(text, since=datetime.strftime(dt, '%Y-%m-%d'),
                  until=datetime.strftime(dt+pd.to_timedelta(1, 'D'), '%Y-%m-%d'))
        print('start scraping {date}'.format(
            date=datetime.strftime(dt, '%Y-%m-%d')))

        counter = 0
        try:
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
                tweet_list.append([tweet.date, tweet.user.username, tweet.rawContent,  tweet.likeCount,
                                  tweet.replyCount, tweet.retweetCount, tweet.quoteCount, tweet.url])
                counter += 1
                if counter % 500 == 0:
                    print(f'{counter} scrapped')

            print('finished scraping {date}, # of tweets: {no_tweet}'.format(
                date=datetime.strftime(dt, '%Y-%m-%d'), no_tweet=counter))
        except:
            print('error occured in {date}'.format(
                date=datetime.strftime(dt, '%Y-%m-%d')))
            continue

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweet_list, columns=[
                             'Timestamp', 'Username', 'Embedded_text', 'Likes', 'Comments', 'Retweets', 'Quotes', 'Tweet URL'])
    return tweets_df


df = snscraperper("Playstation", '2022-01-01', '2022-12-31')
df.to_csv('Playstation_0101_1231.csv')


df = pd.read_csv('Playstation_0101_1231.csv')

df = pp.clean_df(df)
trans_df = tw.combine_df(df, kw='Playstation')

word_freq = tw.gen_freq(trans_df)
