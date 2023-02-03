import AzureSQL_DDL as az
import tweet_analysis as tw
import pandas as pd

kw = ["mcdonalds",'Burger King']
time = '_2022-06-01_2022-12-31.csv'

raw_df = pd.read_csv('./outputs/'+kw[1]+time)
raw_df.dropna(subset=['Embedded_text', 'Emojis'], how='all', inplace = True)
trans_df = tw.combine_df(raw_df)
bol, kw_id = az.keyword_hist("Burger King")
az.update_records(trans_df,kw_id)


tw.check_object(trans_df['Retweets']).loc[1234]