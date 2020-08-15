
#combining CSVs into a single master

import pandas as pd

list_brands=['HONDA','FORD','AUDI','BMW','JAGUAR','LAND%20ROVER','MERCEDES-BENZ','NISSAN','PORSCHE','RENAULT','SEAT',\
             'SKODA','TOYOTA','VAUXHALL','VOLKSWAGEN','VOLVO','PEUGEOT','MITSUBISHI','HYUNDAI','FIAT','CITROEN',\
                 'ABARTH','ALFA%20ROMEO','ASTON%20MARTIN','BENTLEY','BUGATTI','CHEVROLET','CHRYSLER','KIA','MAZDA',\
                     'MINI','SUZUKI','DACIA','DAIHATSU','DODGE','DS%20AUTOMOBILES','FERRARI','INFINITI','ISUZU','JEEP',\
                         'LAMBORGHINI','LEXUS','MASERATI','MCLAREN','MG','ROLLS-ROYCE','ROVER','SAAB','SMART','SSANGYONG',\
                             'SUBARU','TESLA']

df_master=pd.DataFrame(columns=['Title','Grabber','Specs','Price']) 

for brand in list_brands:
    temp1=pd.read_csv(brand+'_data_relevance.csv')
    df_master=pd.concat([df_master, temp1], axis=0)
    try:
        temp2=pd.read_csv(brand+'_data_asc.csv')
        temp3=pd.read_csv(brand+'_data_desc.csv')
        df_master=pd.concat([df_master,temp2,temp3], axis=0)
    except FileNotFoundError: 
        continue

df_master.to_csv('Master_data.csv')

    