import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, KFold, cross_val_score
from sklearn.metrics import mean_squared_error
import pickle
from xgboost import XGBRegressor


df_final=pd.read_csv('data_for_model.csv', index_col=0)
y=df_final['Price']
df_final.drop('Price', axis=1, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(df_final,y, test_size=0.2, random_state=64, shuffle=True)


def test_base_models(): #this function was used to base-test models, of which xgboost was far superior
    models=[]
    for model in models:
        model.fit(X_train, y_train)
        print(model.__class__.__name__)
        print(pred_test(model))


##hyperparameter tuning. Did a mixture of this to a limited degree and some for loops for single parameters
#def optimise_model(model, parameters):
    #kf=KFold(5, shuffle=True, random_state=23).get_n_splits(X_train.values)
    #grid=GridSearchCV(model, parameters, cv=kf, scoring='neg_mean_squared_error')
    #grid.fit(X_train, y_train)
    #print('Best estimator: ', grid.best_estimator_)
    #print('Score_logged: ', np.sqrt(-1*grid.best_score_))
    #print('Std: ', np.sqrt(grid.cv_results_['std_test_score'][grid.best_index_]))
    #print('Score: ', np.exp(np.sqrt(-1*grid.best_score_))-1)
    #return grid.best_estimator_

#scoring function (returning normal price rmse rather than rmse of the logs)
def exp_score(estimator, X, y):
    y_pred=estimator.predict(X)
    y_pred=np.exp(y_pred)-1
    y=np.exp(y)-1
    rmse=np.sqrt(mean_squared_error(y, y_pred))
    return rmse

def cv_train_score(estimator):
    kf=KFold(5, shuffle=True, random_state=23).get_n_splits(X_train.values)
    cvscore=cross_val_score(estimator, X_train, y_train,scoring=exp_score, cv=kf)
    print('CV: ',cvscore.mean())
    return cvscore.mean()
    
#predicting test data
def pred_test(model):
    y_pred=model.predict(X_test)
    y_test_orig=np.exp(y_test)-1
    y_pred_orig=np.exp(y_pred)-1
    print('Test RMSE: ',np.sqrt(mean_squared_error(y_test_orig, y_pred_orig)))
    return y_pred_orig

def plot_residuals(estimator):
    y_train_pred=np.exp(estimator.predict(X_train))-1 
    y_test_pred=np.exp(estimator.predict(X_test))-1 
    y_train_exp=np.exp(y_train)-1
    y_test_exp=np.exp(y_test)-1
    res_train=abs(y_train_pred-y_train_exp)
    res_test=abs(y_test_pred-y_test_exp)
   
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.scatter(y_train_exp, res_train)
    plt.title('Training Residuals')
    plt.subplot(1,2,2)
    plt.scatter(y_test_exp, res_test)
    plt.title('Test Residuals')



xgb_final=XGBRegressor(learning_rate=0.07, n_estimators=1700, max_depth=7)
xgb_final.fit(X_train, y_train)
cv_train_score(xgb_final)
pred_test(xgb_final)
plot_residuals(xgb_final)


feats_important=xgb_final.get_booster().get_score(importance_type='gain')
feats=list(feats_important.keys())
vals=list(feats_important.values())
feat_imp=pd.DataFrame(data=vals, index=feats, columns=['score']).sort_values(by='score',ascending=False)
feat_imp.plot(kind='bar')

filename="xgb_car_price.sav"
pickle.dump(xgb_final, open(filename, 'wb'))


#Creating datasets for residual analysis: 

y_test_pred=np.exp(xgb_final.predict(X_test))-1
y_train_pred=np.exp(xgb_final.predict(X_train))-1
y_test_exp=np.exp(y_test)-1
y_train_exp=np.exp(y_train)-1
res_test=abs(y_test_exp-y_test_pred)
res_train=abs(y_train_exp-y_train_pred)
res_tr=pd.DataFrame(y_train_exp.values,columns=['act'])
res_te=pd.DataFrame(y_test_exp.values, columns=['act'])
res_tr['res']=res_train.values
res_te['res']=res_test.values
res_tr.to_csv('training_residuals.csv')
res_te.to_csv('test_residuals.csv')









