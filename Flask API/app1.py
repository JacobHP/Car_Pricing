import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

def feature_converter(features):
    feat_dict={}
    feat_dict['year']=int(features[1])
    feat_dict['miles']=int(features[2])
    feat_dict['engine']=float(features[3])
    feat_dict['power']=int(features[4])
    feat_dict['owners']=int(features[8])
    feat_dict['doors']=int(features[9])
    feat_dict['issue_flag']=int(features[10]=='Y')
    for style in ['Coupe', 'Estate','Hatchback','MPV','Pickup','SUV','Saloon']:
        feat_dict['style_'+style]=int(features[5]==style)
    feat_dict['transmission_Manual']=int(features[6]=='Manual')
    feat_dict['fuel_Petrol']=int(features[7]=='Petrol')
    for make in ['Alfa Romeo','Aston Martin','Audi','BMW','Bentley','Chevrolet',\
                 'Chrysler','Citroen','DS','Dacia','Daihatsu','Dodge','Ferrari',\
                     'Fiat','Ford','Honda','Hyundai','Infiniti','Isuzu','Jaguar','Jeep',\
                         'KIA','Lamborghini', 'Land Rover','Lexus','MG','MINI','Maserati',\
                             'Mazda','McLaren','Mercedes-Benz','Mitsubishi','Nissan','Peugeot',\
                                 'Porsche','Renault','Rolls-Royce','Rover','SEAT','SKODA','Saab',\
                                     'Smart','Ssangyong','Subaru','Suzuki','Toyota','Vauxhall','Volkswagen',\
                                         'Volvo']:
        feat_dict['make_'+make]=int(features[0]==make)
        #if not from model build then will be 0, indicating it is an Abarth which may be a problem
    df=pd.DataFrame(feat_dict, index=[0])
    return df



app=Flask(__name__)
model=pickle.load(open('xgb_car_price.sav', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    For rendering results on HTML GUI
    """
    features=[x for x in request.form.values()]
    final_features=feature_converter(features)
    prediction_logd=model.predict(final_features)[0]
    prediction=np.exp(prediction_logd)-1
    output=round(prediction,0)
    return render_template('index.html', prediction_text='Price should be approximately £ {:.2f}'.format(output))

if __name__ == '__main__':
    app.run(debug=True)
