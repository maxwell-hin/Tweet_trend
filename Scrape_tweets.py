from Scweet_master.Scweet.scweet import scrape
# from Scweet.user import get_user_information, get_users_following, get_users_followers


def run_scrape(words, since, until,interval, geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    return data

word = 'Coca-cola'
since = '2020-10-01'
until = '2020-10-03'
interval = 3

US_geo = '41.4925374,-99.9018131,1500km'


data = run_scrape(word, since, until,interval ,US_geo)
