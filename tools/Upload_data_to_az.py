import tools.AzureSQL_DDL as az
import tools.tweet_analysis as tw
import pandas as pd


trans_df = pd.read_csv('test.csv')

az.update_records(trans_df)

# data = az.download_from_db(2,'2020-06-01','2020-06-08')
# data.columns
# data