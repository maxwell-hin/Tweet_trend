import pandas as pd
from Scweet_master.Scweet.scweet import scrape
import time
# from Scweet.user import get_user_information, get_users_following, get_users_followers


def init_question():
    num_kw = int(input('How many keywords you would like to compare?: '))
    kw = ''
    for i in range(0, num_kw):
        tem = input(f'Please input keyword {i+1}: ')
        kw = kw + tem + ' '
    since = input('Which is the start date of tweets?: ')
    until = input('Which is the end date of tweets?: ')
    return kw, since, until
        





def run_scrape(words, since, until,interval, geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    return data

word = 'Benz'
since = '2022-06-01'
until = '2022-12-31'
interval = 3

US_geo = '41.4925374,-99.9018131,1500km'

tic = time.time()
data = run_scrape(word, since, until,interval ,US_geo)
tac = time.time()
print(f'runtime: {round(tac-tic,2)/60} mins')

# import pandas as pd
# data.to_csv('./outputs/coca-cola_220601_221231_int3.csv')
# data = pd.read_csv('./outputs/Burger King_2022-06-01_2022-12-31.csv')
# data[data['Emojis'].notnull()]['Emojis'].iloc[0]




# print(score)         
print(emoji_list)
# print(score_each_tweets)
len(emoji_list)