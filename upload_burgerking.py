import tools.AzureSQL_DDL as az
import tools.tweet_analysis as tw
import pandas as pd
import tools.preprocessing as pp
raw_df = pd.read_csv("outputs/McDonald's_2022-06-01_2022-12-31.csv")
raw_df2 = pd.read_csv("outputs/burger_king.csv")

raw_df = pp.clean_df(raw_df)
raw_df2 = pp.clean_df(raw_df2)
trans_df = tw.combine_df(raw_df)
trans_df2 = tw.combine_df(raw_df2)


# trans = pd.concat([trans_df2, trans_df], ignore_index=True)


az.update_records(trans_df, 1)
az.update_records(trans_df2, 2)


# az.connect_asql()
# query = "UPDATE JMJ.tweets SET tweet_id"
