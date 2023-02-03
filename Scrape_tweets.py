import pandas as pd
from Scweet_master.Scweet.scweet import scrape
import time
import AzureSQL_DDL as az
from datetime import datetime
import tweet_analysis as tw



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
        



def run_scrape(words, since, until,interval,geocode):
    data = scrape(words=words, since=since, until=until, from_account=None, interval=interval,
                  headless=False, display_type="Latest", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, limit=float('inf'), geocode=geocode)
    data.dropna(subset=['Embedded_text', 'Emojis'], how='all', inplace = True)
    return data
data = pd.read_csv('./outputs/pepsi_2022-06-01_2022-12-31.csv')


# tic = time.time()
# data = run_scrape("McDonald's", '2022-01-01T06:00:30 000Z', '2022-01-03T06:00:30 000Z',1)
# tac = time.time()
# print(f'runtime: {round(tac-tic,2)/60} mins')

US_geo = '41.4925374,-99.9018131,1500km'



if __name__ == "__main__":
    #return keywords, knowing the date range
    kw, num_kw, since, until = init_question()
    kw_ls = kw.split(',')
    compare_ls = []
    for word in kw_ls: #create df for analysis for each keywords and append to compare_ls
        
        #find if kw has been searh
        trigger, kw_id = az.keyword_hist(word)
        if trigger: # if keywords has been searched
            hist_start, hist_end = az.hist_date_range(kw_id)
            
            #====within done
            if datetime.strptime(hist_start, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):
                
                #download data
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
                
            #====only earlier   
            elif datetime.strptime(hist_start, '%Y-%m-%d')>datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):
                
                #scrape data
                data = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)       
                
                #Transform
                trans_data = tw.combine_df(data)
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)
                
            #====only latest
            elif datetime.strptime(hist_start, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') and datetime.strptime(hist_end, '%Y-%m-%d')<datetime.strptime(until, '%Y-%m-%d'):
                
                #similar to above
                a = 3    
                
                
                
            #====both earlier than hist_since or later than hist_until 
            elif datetime.strptime(hist_end, '%Y-%m-%d')<=datetime.strptime(since, '%Y-%m-%d') or datetime.strptime(hist_start, '%Y-%m-%d')>=datetime.strptime(until, '%Y-%m-%d'):     

                #scrape data
                data = run_scrape(word = word, since=since, until=until, interval = 3, geocode=US_geo)   
                
                #Transform
                trans_data = tw.combine_df(data)
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                
                
                
            #====both outside
            else:
                #scrape data
                data = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)
                
                data_2 = run_scrape(word = kw, since=hist_end, until=until, interval = 3, geocode=US_geo)         
                
                data = pd.concat([data, data_2], reset_index=True)
                
                #Transform
                trans_data = tw.combine_df(data)
                
                
                #upload to db
                az.update_records(trans_data, kw_id) 
                                
                #download from db
                df = az.download_from_db(kw_id=kw_id, since=since, until=until)

        else:#if kw has not been search      
            
            #scrape data
            data = run_scrape(word = word, since=since, until=hist_start, interval = 3, geocode=US_geo)
            
            #update new keyword to db
            az.new_keywords(word)
            
            
            #Transform
            trans_data = tw.combine_df(data)
                
                
                
            #upload to db
            az.update_records(trans_data, kw_id) 
                            
            #download from db
            df = az.download_from_db(kw_id=kw_id, since=since, until=until)
        
        compare_ls.append(df)
        
    
    
    #Visualization 
    #=show the summary for each keywords enter
    for ind, word in enumerate(kw_ls):
        print(f'''Summary for {word}:
            Total no. of tweets: {tw.sum_tweets(compare_ls[ind][0])}
            Total no. of likes: {tw.sum_tweets(compare_ls[ind][1])}
            Total no. of comments: {tw.sum_tweets(compare_ls[ind][2])}
            Total no. of retweets: {tw.sum_tweets(compare_ls[ind][3])}
            ''')
        
    #=Which tweets has maximum 
    for ind, word in enumerate(kw_ls):
        print(f'''Maximum number of likes for '{word}': {tw.max_tweets(compare_ls[ind])[0]}, {tw.max_tweets(compare_ls[ind])[3]}
            Maximum number of comments for '{word}': {tw.max_tweets(compare_ls[ind])[1]}, {tw.max_tweets(compare_ls[ind])[4]}
            Maximum number of retweets for '{word}': {tw.max_tweets(compare_ls[ind])[2]}, {tw.max_tweets(compare_ls[ind])[5]}
            ''') 


    #=ratio
    for ind, word in enumerate(kw_ls):
        print(f'''CLS Ratio for {word}:
            Total no. of likes: {tw.ratio_tweets(compare_ls[ind][3])}
            Total no. of comments: {tw.ratio_tweets(compare_ls[ind][4])}
            Total no. of retweets: {tw.ratio_tweets(compare_ls[ind][5])}
            ''')

    
    #=popularity

dfd


    #=wordcloud
    for ind, word in enumerate(kw_ls):   
        print(f'{word.capitalize()} has the following common words:/n{tw.gen_freq((compare_ls[ind],kw))}')   

    wordcloud_bool = input('Would you like to show word cloud[y/n]? ')
    if wordcloud_bool == 'y':
        for ind, word in enumerate(kw_ls):
            print(f"Wordcloud for '{word.capitalize()}'")
            tw.word_cloud(compare_ls[ind], kw ,word)
        regen_wc = input('Would you like to regenerate another wordcloud with other number of words?')
        while regen_wc == 'y':
            num_cmword = int(input("How many number of words you would like to show on the wordcloud? "))
            for ind, word in enumerate(kw_ls):
                print(f"Wordcloud for '{word.capitalize()}'")
                tw.word_cloud(compare_ls[ind], kw ,num_cmword)

            regen_wc = input('Would you like to regenerate another wordcloud with other number of words?')
    
    print('Tweet_app end')
        
            


    



# word = 'abc'
# print(f'''Summary for {word} between {since} and {until}:
# Total tweets tw.sum_tweets(df)''')