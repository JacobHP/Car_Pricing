import pandas as pd
import numpy as np

df=pd.read_csv('master_final.csv', index_col=0)

#log-transform target
df['Price']=np.log1p(df['Price'])

df.drop(['ULEZ','CatN'], axis=1, inplace=True)
df=pd.get_dummies(df, drop_first=True)
df.to_csv('data_for_model.csv')
