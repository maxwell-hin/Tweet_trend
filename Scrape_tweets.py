import pandas as pd
# from Scweet_master.Scweet.scweet import scrape
import tools.tweet_analysis as tw
import tools.AzureSQL_DDL as az
import tools.preprocessing as pp
from datetime import datetime
import snscrape.modules.twitter as sntwitter
import re


def init_question():
    num_kw = int(input('How many keywords you would like to compare?: '))
    kw_ls = []
    ticker_ls = []
    for i in range(0, num_kw):
        tem = input(f'Please input keyword {i+1}: ')
        tem_ticks = input(
            f"Please input the tickers of {tem}: \n(input 'no' if stock price comparison is not wanted) ")
        kw_ls.append(tem)
        if tem_ticks == 'no':
            ticker_ls.append('n')
        else:
            ticker_ls.append(tem_ticks)
    since = input('Which is the start date of tweets? e.g. 2022-06-01: ')
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    assert pattern.match(since), print(
        '!!Please input the date in the format of YYYY-MM-DD!!')
    until = input('Which is the end date of tweets? e.g. 2022-11-21: ')
    assert pattern.match(until), print(
        '!!Please input the date in the format of YYYY-MM-DD!!')
    return kw_ls, ticker_ls, since, until


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
                                  tweet.replyCount, tweet.retweetCount, tweet.quoteCount, tweet.hashtags, tweet.cashtags, tweet.url])
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
                             'Timestamp', 'Username', 'Embedded_text', 'Likes', 'Comments', 'Retweets', 'Quotes', 'Hashtags', 'Cashtags', 'Tweet URL'])
    return tweets_df


# US_geo = '41.4925374,-99.9018131,1500km'

if __name__ == "__main__":
    # return keywords, knowing the date range
    kw_ls, ticker_ls, since, until = init_question()
    compare_ls = []
    for word in kw_ls:  # create df for analysis for each keywords and append to compare_ls
        # find if kw has been searh
        trigger, kw_id = az.keyword_hist(word)
        if trigger:  # if keywords has been searched
            hist_start, hist_end = az.hist_date_range(kw_id)

            # ====within
            if datetime.strptime(hist_start, '%Y-%m-%d') <= datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d') >= datetime.strptime(until, '%Y-%m-%d'):

                # download data
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)

            # ====only earlier
            elif datetime.strptime(hist_start, '%Y-%m-%d') > datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d') >= datetime.strptime(until, '%Y-%m-%d'):

                #scrape & clean
                # data = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)
                data = snscraperper(word, since=since, until=hist_start)
                data = pp.clean_df(data)

                # Transform, sentiment analysis, word_tokenized
                trans_data = tw.combine_df(data, word)

                # upload to db
                az.update_records(trans_data, kw_id)

                # download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)

            # ====only latest
            elif datetime.strptime(hist_start, '%Y-%m-%d') <= datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d') < datetime.strptime(until, '%Y-%m-%d'):

                #scrape & clean
                data = snscraperper(word, since=hist_end, until=until)
                data = pp.clean_df(data)

                # Transform, sentiment analysis, word_tokenized
                trans_data = tw.combine_df(data, word)

                # upload to db
                az.update_records(trans_data, kw_id)

                # download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)

            # ====both earlier than hist_since or later than hist_until
            elif datetime.strptime(hist_end, '%Y-%m-%d') <= datetime.strptime(since, '%Y-%m-%d') or datetime.strptime(hist_start, '%Y-%m-%d') >= datetime.strptime(until, '%Y-%m-%d'):

                #scrape & clean
                # data = run_scrape(word = word, since=since, until=until, interval = 3, geocode=US_geo)
                data = snscraperper(word, since=since, until=until)
                data = pp.clean_df(data)

                # Transform, sentiment analysis, word_tokenized
                df = tw.combine_df(data, word)

                # upload to db
                az.update_records(trans_data, kw_id)

            # ====both outside
            else:
                #scrape & clean
                # data_1 = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)
                data_1 = snscraperper(word, since=since, until=hist_start)
                # data_2 = run_scrape(word = kw, since=hist_end, until=until, interval = 3, geocode=US_geo)
                data_2 = snscraperper(word, since=hist_end, until=until)
                data = pd.concat([data_1, data_2], reset_index=True)
                data = pp.clean_df(data)

                # Transform, sentiment analysis, word_tokenized
                trans_data = tw.combine_df(data, word)

                # upload to db
                az.update_records(trans_data, kw_id)

                # download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)

        else:  # if kw has not been search

            #scrape & clean
            # data = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)
            data = snscraperper(word, since=since, until=until)
            data = pp.clean_df(data)

            # update new keyword to db
            az.new_keywords(word)

            # Transform, sentiment analysis, word_tokenized
            trans_data = tw.combine_df(data)

            # upload to db
            az.update_records(trans_data, kw_id)

            # download from db
            df = az.download_from_db(kw_id=kw_id, since=since, until=until)

        compare_ls.append(df)

    # Visualization ==================================================================================
    # =show the summary for each keywords enter
    for ind, word in enumerate(kw_ls):
        print(f'''Summary for {word}:
            Total no. of tweets: {tw.sum_tweets(compare_ls[ind])[0]}
            Total no. of likes: {tw.sum_tweets(compare_ls[ind])[1]}
            Total no. of comments: {tw.sum_tweets(compare_ls[ind])[2]}
            Total no. of retweets: {tw.sum_tweets(compare_ls[ind])[3]}
            Total no. of quotes: {tw.sum_tweets(compare_ls[ind])[4]}\n
            ''')

    # =Which tweets has maximum
    for ind, word in enumerate(kw_ls):
        print(f'''Maximum number of likes for '{word}': {tw.max_tweets(compare_ls[ind])[0]}, \nurl: {tw.max_tweets(compare_ls[ind])[4]}\n
    Maximum number of comments for '{word}': {tw.max_tweets(compare_ls[ind])[1]}, \nurl: {tw.max_tweets(compare_ls[ind])[5]}\n
    Maximum number of retweets for '{word}': {tw.max_tweets(compare_ls[ind])[2]}, \nurl: {tw.max_tweets(compare_ls[ind])[6]}\n
    Maximum number of quotes for '{word}': {tw.max_tweets(compare_ls[ind])[3]}, \nurl: {tw.max_tweets(compare_ls[ind])[7]}\n
    ''')

    # =ratio
    for ind, word in enumerate(kw_ls):
        print(f'''CLS Ratio for {word}:
        Total no. of likes: {tw.ratio_tweets(compare_ls[ind])[4]}
        Total no. of comments: {tw.ratio_tweets(compare_ls[ind])[5]}
        Total no. of retweets: {tw.ratio_tweets(compare_ls[ind])[6]}
        Total no. of quotes: {tw.ratio_tweets(compare_ls[ind])[7]}
        ''')

    # =popularity, sentiment and stock
    for ind, word in enumerate(kw_ls):
        if ticker_ls[ind] != 'n':
            tw.plot(compare_ls[ind], word, since, until, ticker=ticker_ls[ind])
        else:
            tw.plot(compare_ls[ind], word, since, until)

    # =wordcloud
    # frequecy of top 20 words
    for ind, word in enumerate(kw_ls):
        print(
            f'{word.capitalize()} has the following common words:\n{tw.gen_freq(compare_ls[ind])}\n')

    # show wordcloud
    wordcloud_bool = input('Would you like to show word cloud[y/n]? ')
    if wordcloud_bool == 'y':
        for ind, word in enumerate(kw_ls):
            print(f"Wordcloud for '{word.capitalize()}'")
            tw.word_cloud(compare_ls[ind], word)

        # regenerate wordcloud
        regen_wc = input(
            'Would you like to regenerate another wordcloud with other number of words?(y/n)')
        while regen_wc == 'y':
            num_cmword = int(
                input("How many number of words you would like to show on the wordcloud? "))
            for ind, word in enumerate(kw_ls):
                print(f"Wordcloud for '{word}'")
                tw.word_cloud(compare_ls[ind], word, num=num_cmword)

            regen_wc = input(
                'Would you like to regenerate another wordcloud with other number of words?(y/n)')

    print('Tweet_app end')
