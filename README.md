# Car_Pricing
An end-to-end ML project developing a car pricing tool.

In this project, I scraped car information and prices from the internet, cleaned and analysed the data and built a regression model to predict car prices. I settled on using the xgboost XGBRegressor which achieved a CV RMSE of 10089.60 (**1739.32** on obs <£100k) and an RMSE on unseen test data of 8016.97 (**2929.24** on obs <£100k). 

From the RMSE results it is clear that the model works reasonably well on most cars (indeed the majority of the cars scraped were <£100k), but is volatile for high-priced cars. In the future I plan to look at scraping more high-price data, building another model on these and determining criteria as to which model should be applied to an unseen test observation. Due to autotrader being primarily used cars, I expect the model may also struggle on brand new cars.

The website I chose to scrape from was UK car website Autotrader. I will not be uploading any of the data but have uploaded the scraping script. 

* Scraped car data from Autotrader using BeautifulSoup and Selenium
* Built XGB model
* Used Flask to create an API, taking user inputs into the model and returning a predicted value
* Wrote simple HTML GUI for Flask app

![alt text](https://github.com/JacobHP/XGBoost_Car_Pricing/blob/master/Flask%20API/Car_Pricing_API.png?raw=true)

You can try the API as follows:
* Download app1.py, xgb_car_price.sav from the Flask API folder and index.html from the templates folder within this. 
* Save these to a folder structured folder->{app1.py, xgb_car_price.sav, templates->{index.html}}
* Run this from terminal/command prompt. Open http://127.0.0.1:5000/ in your browser to run locally.
* On terminal: set cd to the folder containing app1.py, then enter 'python3 app1.py' and submit




