# Car_Pricing
An end-to-end ML project developing a car pricing tool.

In this project, I scraped car information and prices from the internet, cleaned and analysed the data and built a regression model to predict car prices. I settled on using the xgboost XGBRegressor which achieved a CV RMSE of 10089.60 (**1739.32** on obs <£100k) and an RMSE on unseen test data of 8016.97 (**2929.24** on obs <£100k). 

From the RMSE results it is clear that the model works reasonably well on most cars (indeed the majority of the cars scraped were <£100k), but is volatile for high-priced cars. In the future I plan to look at scraping more high-price data, building another model on these and determining criteria as to which model should be applied to an unseen test observation. Due to autotrader being primarily used cars, I expect the model may also struggle on brand new cars.

The website I chose to scrape from was UK car website Autotrader. I will not be uploading any of the data but have uploaded the scraping script. 

# 1. Scraping 

I used Selenium and BeautifulSoup (bs4) to scrape the data. 

I wrote a script that would scrape data for brands based on search setting, searching for Price (L-H), Price (H-L) and 'relevance'. For more common brands, I could run with multiple search settings then removed any duplicates. For less common brands I could just search on one setting. Data was scraped into different csv files then these were combined, with duplicate entries removed.

Limitations: 
* Autotrader limited to first 100 pages (i.e. even if there were 40k cars of a brand, I could only scrape ~1300 for a given search setting). 
* Website has measures in place to combat repeated requests. I did not push the limits of these measures and scraped conservatively by using sleep functions.

Further considerations: 
* One could argue that data was not entirely independently sampled as a result of the ordering searches. However methodology provided a reasonable attempt and no obvious adverse effects of this were found during the analysis or modelling. 

# 2. Cleaning

The cleaning process had two distinct parts. The first was getting the data in a somewhat useable state, the second was the more finer/detailed cleaning: dealing with missing values, obvious outliers, ensuring consistency in categoricals etc. 

**Part 1**

The data for each car from the scrape was made up of a Title string (with no consistency i.e. typed by the user rather than selected), a grabber (text possibly containing some useful info), a list of specs (not necessarily containing all specs), and the Price. 

* I applied a literal_eval to convert the specs string to a list (easier) and used regex and simple string searches to search through the list elements to extract specs. 
* As an initial way to get the title I simply split it into a list of words and extracted the first 2. 
* I created an 'issue_flag' feature using common grabber keywords ("spares or repairs", "failed mot" etc.) 

**Part 2** 

I initially dealt with missing values: 

* Removed serv_hist feature due to majority missing. 
* Most missing year were also missing miles and vice versa. As such I removed the entries missing years and miles. 
* Missing fuel, doors, power, engine, style and transmission features were filled using modes or medians for the specific make or model
* Filled missing owner values with mode by year.
* Removed any remaining missing values. 

I then proceeded to: 
* Clean make and model up to just obtain the make and ensure consistency (e.g. capitalisation etc.)
* Remove extreme values that were likely caused by user-input issue (i.e. ridiculously high values or ones obviously in the wrong place). 


# 3. Exploratory analysis 

Due to the simplicity of the data and satisfying initial view, this was kept fairly short. Key highlights were as follows: 

* Numerical features all displayed reasonable correlation (abs > 0.5) with Price
![alt text](https://github.com/JacobHP/XGBoost_Car_Pricing/blob/master/Analysis/NumCorrs.png?raw=true)
* Categoricals all displayed clear relationships with Price. In addition to visualisation I performed ANOVA which was conclusive in there being a difference in means between categories. 
![alt text](https://github.com/JacobHP/XGBoost_Car_Pricing/blob/master/Analysis/Cats.png?raw=true)
* Cheapest cars were from the early 2000s, moving away in either direction saw increases in price. 
![alt text](https://github.com/JacobHP/XGBoost_Car_Pricing/blob/master/Analysis/Year.png?raw=true)
# 4. Feature Engineering

* Log-transformed target (in the hope of pushing more values to the right for learning - model performed slightly better as a result)
* Encoding categoricals: One-Hot Encoding using pd.get_dummies
* Dropping ULEZ and CatN - This due to wanting to keep the model simple for the API. Did not cause significant drop in RMSE. 


# 5. Modelling

* Split data into training and out-of-sample validation.
* Tested base models for Linear Regression, Lasso, Ridge, ElasticNet, LinearSVR, PolynomialSVR, RandomForestRegressor, LGBMRegressor (lightgbm) and XGBRegressor (xgboost). XGBRegressor was a clear winner.
* Optimised hyperparameters for XGBRegressor using a mixture of single-parameter tuning and GridSearchCV
* Created a scoring function to return the RMSE of predictions in terms of their actual value after exponential transformation. Applied this in both the CV scoring and scoring on validation data.

# 6. Results and Residual Analysis

* As alluded to in the introduction, the CV and validation RMSE was poor. However upon analysis it became apparent that this was due to high-priced cars suffering from significant error in predictions.
![alt text](https://github.com/JacobHP/XGBoost_Car_Pricing/blob/master/Modelling/Figures/Residuals.png?raw=true)

* I attempted some obvious feature engineering to remove this problem however it did not have a significant effect
* RMSE on cars <100k was fairly low as shown in the additional Residual Analysis. Hence the model is fit-for-purpose for the majority of cars but is not suitable for extreme prices. 
* Two obvious solutions are to 1) Scrape more high-price data -i.e. luxury car sites. 2) Build a seperate model on the higher prices and determine criteria as to whether a car is scored on the low-price or high-price model. (I prefer the first approach). 

# 7. Building an API 

* Used Flask to create an API, taking user inputs into the model and returning a predicted value
* Wrote simple HTML GUI for Flask app

Until I get round to setting it up on gihub.io, you can try the API as follows:
* Download app1.py, xgb_car_price.sav from the Flask API folder and index.html from the templates folder within this. 
* Save these to a folder structured folder->{app1.py, xgb_car_price.sav, templates->{index.html}}
* Run this from terminal/command prompt. Open http://127.0.0.1:5000/ in your browser to run locally.
* On terminal: set cd to the folder containing app1.py, then enter 'python3 app1.py' and submit




