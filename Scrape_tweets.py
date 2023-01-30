import pandas as pd
from Scweet_master.Scweet.scweet import scrape
import time
import AzureSQL_DDL as az
from datetime import datetime



def init_question():
    num_kw = int(input('How many keywords you would like to compare?: '))
    kw = ''
    for i in range(0, num_kw):
        tem = input(f'Please input keyword {i+1}: ')
        kw = kw + tem + ' '
    kw = kw[:-1]
    since = input('Which is the start date of tweets? e.g. 2022-06-01: ')
    until = input('Which is the end date of tweets? e.g. 2022-11-21: ')
    return kw, num_kw, since, until
        



def run_scrape(words, since, until,interval, geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    return data





US_geo = '41.4925374,-99.9018131,1500km'

tic = time.time()
data = run_scrape(word, since, until,interval ,US_geo)
tac = time.time()
print(f'runtime: {round(tac-tic,2)/60} mins')

# import pandas as pd
# data.to_csv('./outputs/coca-cola_220601_221231_int3.csv')
# data = pd.read_csv('./outputs/Burger King_2022-06-01_2022-12-31.csv')
# data[data['Emojis'].notnull()]['Emojis'].iloc[0]




if __name__ == "__main__":
    #return keywords, knowing the date range
    kw, num_kw, since, until = init_question()
    kw_ls = kw.split(' ')
    for word in kw_ls:
        
        #find if kw has been searh
        trigger, kw_id = az.keyword_hist(word)
        
        if trigger:
            hist_start, hist_end = az.hist_date_range(kw_id)
            
            #====within
            if datetime.strptime(hist_start, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):
                
                #download data
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
            
            
            #====both earlier than hist_since or later than hist_until 
            elif datetime.strptime(hist_end, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') or datetime.strptime(hist_start, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d') :     

                #scrape data
                data = run_scrape(word = kw, since=since, until=until, interval = 3, geocode=US_geo)   
                
                #Transform
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                
                
                #Visualization
                
            #====only earlier   
            elif datetime.strptime(hist_start, '%Y-%m-%d')>datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):
                
                #scrape data
                data = run_scrape(word = kw, since=since, until=hist_start, interval = 3, geocode=US_geo)       
                
                #Transform
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
            
            #====only latest
            elif datetime.strptime(hist_start, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')<datetime.strptime(until, '%Y-%m-%d'):
                
                #similar to above
                a = 3
                
                
                
            #====both outside
            else:
                #scrape data
                data = run_scrape(word = kw, since=since, until=hist_start, interval = 3, geocode=US_geo)
                
                data_2 = run_scrape(word = kw, since=hist_end, until=until, interval = 3, geocode=US_geo)         
                
                data = pd.concat([data, data_2], reset_index=True)
                
                #Transform
                
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
                

            

