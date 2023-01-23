from Scweet_master.Scweet.scweet import scrape
# from Scweet.user import get_user_information, get_users_following, get_users_followers


def run_scrape(words, since, until, geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=3,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    return data


data = run_scrape('Coca-Cola', '2020-10-01', '2020-10-03',
                  '41.4925374,-99.9018131,1500km')
