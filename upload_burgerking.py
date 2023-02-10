import tools.AzureSQL_DDL as az
import tools.tweet_analysis as tw
import pandas as pd
import tools.preprocessing as pp

raw_df = pd.read_csv("outputs/McDonald's_2022-06-01_2022-12-31.csv")
raw_df = pp.clean_df(raw_df)
trans_df = tw.combine_df(raw_df)


# trans = pd.concat([trans_df2, trans_df], ignore_index=True)


az.update_records(trans_df[:10], 1)


df = az.download_from_db(1, '2022-06-01', '2022-06-13')

# az.connect_asql()
# query = "UPDATE JMJ.tweets SET tweet_id"
