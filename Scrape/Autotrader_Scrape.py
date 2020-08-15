#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:08:52 2020

@author: Jacob
"""
"""
Scrapes from Autotrader (National UK) based on car brand. I ran this for each brand seperately.
Checking number of pages is done manually. No error is recorded if beyond page range
Could do a check if page is empty and then break when not. But kind of unnecessary as I manually looked through
the brands anyway and so could check page number. 
"""
import  bs4
from selenium import webdriver
from time import sleep
import pandas as pd

def scrape(pages, brand,postcode,method='relevance'):
    """
    Parameters
    ----------
    pages : int
        number of pages to scrape - max is 100
    brand : string
        brand of car to scrape.UPPERCASE. denote space by %20
    postcode : string
        uk postcode, all lowercase e.g. sw11ty (i just made this up)
    method : TYPE, string, optional
        String from ['relevance','asc','desc'] The default is 'relevance'.

    Returns
    -------
    None. saves csv

    """
    scraped_list=[]
    driver=webdriver.Firefox()
    for i in range(1, pages+1):       
        driver.get('https://www.autotrader.co.uk/car-search?sort='+method+'&postcode='+postcode+'&radius=1500&make='+brand+'&page='+str(i)) 
        #can change radius if more local scrape required
        sleep(30)
        page_source=driver.page_source
        content=bs4.BeautifulSoup(page_source, 'lxml')
        listings=content.findAll("li", {"class": "search-page__result"})
        for listing in listings:
            info_container=listing.find("div", {"class": "information-container"})
            title_container = info_container.find("a", {"class": "js-click-handler listing-fpa-link tracking-standard-link"})
            title = title_container.text
            grabber_container=info_container.find("p", {"class": "listing-attention-grabber"}) #new
            grabber = grabber_container.text #new
            key_specs=listing.find("ul", {"class":"listing-key-specs"})
            specs=[]
            key_specs=key_specs.findAll("li")
            for spec in key_specs:
                specs.append(spec.text)
            price = listing.find("div", {"class": "vehicle-price"}).text
            scraped_list.append([title, grabber, specs, price]) #new
        if i%100==0:
            sleep(300)
    df=pd.DataFrame(scraped_list, columns=['Title','Grabber', 'Specs', 'Price'])
    df.to_csv(brand+'_da3ta_'+method+'.csv')
    print('Scrape '+ brand +' '+method+ ' complete')
    driver.close()

