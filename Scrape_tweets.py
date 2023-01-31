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
        kw = kw + tem + ','
    kw = kw[:-1]
    since = input('Which is the start date of tweets? e.g. 2022-06-01: ')
    until = input('Which is the end date of tweets? e.g. 2022-11-21: ')
    return kw, num_kw, since, until
        



def run_scrape(words, since, until,interval):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'))
    data.dropna(subset=['Embedded_text'],inplace=True)
    return data







tic = time.time()
data = run_scrape("McDonald's", '2022-01-01', '2023-01-20',30)
tac = time.time()
print(f'runtime: {round(tac-tic,2)/60} mins')





if __name__ == "__main__":
    #return keywords, knowing the date range
    kw, num_kw, since, until = init_question()
    kw_ls = kw.split(',')
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
            elif datetime.strptime(hist_end, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') or datetime.strptime(hist_start, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):     

                #scrape data
                data = run_scrape(word = kw, since=since, until=until, interval = 3)   
                
                #Transform
                
                
                #Visualization
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                
                
                
                
                
                
                
            #====only earlier   
            elif datetime.strptime(hist_start, '%Y-%m-%d')>datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):
                
                #scrape data
                data = run_scrape(word = kw, since=since, until=hist_start, interval = 3)       
                
                #Transform
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
                
                
                #Visualization
                
            
            #====only latest
            elif datetime.strptime(hist_start, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')<datetime.strptime(until, '%Y-%m-%d'):
                
                #similar to above
                a = 3
                
                
                
            #====both outside
            else:
                #scrape data
                data = run_scrape(word = kw, since=since, until=hist_start, interval = 3)
                
                data_2 = run_scrape(word = kw, since=hist_end, until=until, interval = 3)         
                
                data = pd.concat([data, data_2], reset_index=True)
                
                #Transform
                
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
                
                
                #Visualization

            

