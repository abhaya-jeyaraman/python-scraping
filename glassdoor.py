# script to scrape company details from glassdoor to a csv file
"""
@author: abhaya
"""

import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs

def getCompanies(card):
    company_name = ''
    company_description= '' 
    company_industry = ''
    company_rating= ''
    company_size = ''
    company_name_tag = card.find('h2', {"data-test": "employer-short-name"})
    company_rating_tag = card.find('span', {"data-test": "rating"})
    company_size_tag = card.find('span', {"data-test": "employer-size"})
    company_industry_tag = card.find('span', {"data-test": "employer-industry"})
    company_description_upper_tag = card.find('div', {"class": "order-5"})
    if company_description_upper_tag:
        company_description_tag = company_description_upper_tag.find('p')
        company_description = company_description_tag.text
    else:
        company_description = None
    if company_name_tag:
        company_name = company_name_tag.text
    else:
         company_name = None
    if company_rating_tag:
        company_rating = company_rating_tag.text
    else:
         company_rating = None
    if company_size_tag:
        company_size = company_size_tag.text
    else:
        company_size = None
    if company_industry_tag:
        company_industry = company_industry_tag.text
    else:
        company_industry = None
    data = [company_name, company_industry, company_rating, company_size, company_description]
    return data

def main():
    url = 'https://www.glassdoor.com/Explore/browse-companies.htm?page=1'
    companies = []
    i=1
    # extract the job data
    while i<50:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        cards = soup.find_all('div',{"class": "col-md-8"})
        for card in cards[0]:
            company = getCompanies(card)
            if all(company) is True:
                companies.append(company)
        i = i + 1
        try:
            url = 'https://www.glassdoor.com/Explore/browse-companies.htm?page=' + str(i)
        except AttributeError:
            break   
    with open('glassdoor.csv', 'w') as f:

        write = csv.writer(f)
    
        write.writerow(['Company name', 'Industry', 'Rating', 'Size', 'Description'])
        write.writerows(companies)
# run the main program
main()
