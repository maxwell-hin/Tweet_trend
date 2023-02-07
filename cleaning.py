import pandas as pd

burger_king =pd.read_csv('outputs/burger_king.csv')
McDonald =pd.read_csv('outputs/McDonald.csv')
McDonald.info()

burger_king.info()

def data_cleaning(keyword_df):
    drop_na_df = keyword_df.dropna(axis=0 ,how='any' ,subset=['Retweets','Likes','Comments'])
    drop_na_df.info()
    keyword_df.info()

#### double check na is droped 
    drop_na_df['Comments'].isna().sum()
    drop_na_df['Retweets'].isna().sum()
    drop_na_df['Likes'].isna().sum()
    drop_na_df['Quotes'].isna().sum()

######  transfer as int type 
    drop_na_df['Comments'] = drop_na_df['Comments'].astype('int')
    drop_na_df['Retweets'] = drop_na_df['Retweets'].astype('int')
    drop_na_df['Likes'] = drop_na_df['Likes'].astype('int')
    drop_na_df.info()  
    return drop_na_df

data_cleaning(burger_king)

