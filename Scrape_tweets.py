from Scweet_master.Scweet.scweet import scrape
import time
# from Scweet.user import get_user_information, get_users_following, get_users_followers


def run_scrape(words, since, until,interval, geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    return data

word = 'Coca-cola'
since = '2022-06-01'
until = '2022-12-31'
interval = 3

US_geo = '41.4925374,-99.9018131,1500km'

tic = time.time()
data = run_scrape(word, since, until,interval ,US_geo)
tac = time.time()
print(f'runtime: {round(tac-tic,2)/60} mins')

# data.to_csv('./outputs/coca-cola_220601_221231_int3.csv')