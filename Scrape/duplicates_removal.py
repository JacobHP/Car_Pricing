#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Due to our scraping methods to get a broad range of the most popular brands, we may have obtained duplicates
where ascending and descending overlap with relevant. These will need to be removed.
"""
import pandas as pd

high_freq=['AUDI','BMW','CITROEN','FIAT','FORD','HONDA','HYUNDAI','JAGUAR','KIA',\
   'LAND%20ROVER','MAZDA','MERCEDES-BENZ','MINI','MITSUBISHI','NISSAN','PEUGEOT',\
       'PORSCHE','RENAULT','SEAT','SKODA','SUZUKI','TOYOTA','VAUXHALL','VOLKSWAGEN',\
           'VOLVO']


def remove_dup(df1,df2):
    '''
    df1 is rel or asc, df2 is desc or rel (respectively
    '''
    list_df1=[[row[0],row[1], row[2], row[3]] for row in zip(df1['Title'],df1['Grabber'],df1['Specs'],df1['Price'])]
    list_df2=[[row[0],row[1], row[2], row[3]] for row in zip(df2['Title'],df2['Grabber'],df2['Specs'],df2['Price'])]    
    
    for row in list_df1:
        if row[3]< list_df2[0][3]:
            continue
        else: 
            if row in list_df2:
                list_df1.remove(row)
    new_df=pd.DataFrame(list_df1, columns=['Title','Grabber','Specs','Price'])
    return new_df
        



for brand in high_freq: 
    rel=pd.read_csv(brand+'_data.csv')
    asc=pd.read_csv(brand+'_data_asc.csv')
    desc=pd.read_csv(brand+'_data_desc.csv')
    
    for df in [rel,asc, desc]:
        df['Price']=df['Price'].apply(lambda x: float(''.join(n for n in x if (n.isdigit() or n =='.'))))
        df.sort_values(by='Price', inplace=True)
    
    asc_new=remove_dup(asc,rel)
    rel_new=remove_dup(rel,asc)
    
    asc_new.to_csv(brand+'_data_asc.csv')
    rel_new.to_csv(brand+'_data.csv')