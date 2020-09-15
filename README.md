# Car_Pricing
An end-to-end ML project developing a car pricing tool.

In this project, I scraped car information and prices from the internet, cleaned and analysed the data and built a regression model to predict car prices. I settled on using a **TBC** model which achieved a CV RMSE of **TBC** and an RMSE on unseen test data of **TBC**. 

The current website I have chosen to scrape from is UK car website Autotrader. I will not be uploading any of the data but will upload the scraping script. 

# 1. Scraping 

I used Selenium and BeautifulSoup (bs4) to scrape information from UK car website Autotrader. I have not uploaded any of the scraped data here but the script is available to reproduce similar data. 

Initial Limitations: 
* Autotrader limited to first 100 pages (i.e. even if there were 40k cars of a brand, I could only scrape ~1300 for a given search setting). 
* Website has measures in place to combat repeated requests. I did not test the limits of these measures.

Solutions:
* I wrote an script that would scrape data for brands based on search setting, searching for Price (L-H), Price (H-L) and 'relevance. For more common brands, I could run with multiple search settings then removed any duplicates. For less common brands I could just search on one setting
* I utilised the time library to pause the script at certain intervals to appear more humanlike. As a consequence the script is fairly slow (I had it scrape in the background during other activities)

Further considerations: 
* One could argue that data was not entirely independently sampled as a result of the ordering searches. However methodology provided a reasonable attempt and no adverse effects of this were found during the analysis or modelling. 

Data was scraped into different csv files then these were combined, with duplicate entries removed.


# 2. Cleaning

The cleaning process had two distinct parts. The first was getting the data in a somewhat useable state, the second was the more finer/detailed cleaning. 

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

TODO. 

# 4. Feature Engineering


# 5. Modelling


# 6. Building an API 








