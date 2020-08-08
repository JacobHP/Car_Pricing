# Car_Pricing
An end-to-end data science project developing a car pricing tool.

In this project, I scrape car information and prices from the internet, analyse the data and build a regression model to predict car prices based on the specs. 

A high-level plan is as follows: 

* Build a scraping script (Done)
* Scrape the data (In progress)
* Clean the data (In progress)
* Analyse the data ()
* Feature engineering ()
* Model build ()
* API (TBC)

The current website I have chosen to scrape from is UK car website Autotrader. I will not be uploading any of the data but will upload the scraping script. 

# 1. Scraping 

We use the Selenium and BeautifulSoup (bs4) packages. The script has been written with flexibility in mind to enable easy modification of searching high-to-low, lot-to-high or by relevance. As such there are 3 almost identical functions. For popular cars, all 3 were ran scraping the 1300 highest, 1300 lowest and 1300 most relevant. For less popular only one needed running. 

Note: 
* Autotrader limits to first 100 pages
* time.sleep was used to make the scraping appear as humanlike as possible. This could likely be sped up significantly. The scraping took a long time but I mostly did it while I was at work
* Due to the nature of the website, the sampling isn't entirely independent, however should provide a reasonable attempt
