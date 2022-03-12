
# Script to scrape indeed job listings

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs

def get_url(position, location):
    template = 'https://www.indeed.com/jobs?q={}'
    url = template.format(position+' '+location)
    return url

# extacts all the details w.r.t a specific listing (company name, job title, salary, post date, location)
def getJobs(soup, job):
    table_list = job.findAll('table')
    h2_tag = table_list[0].find_all('h2', {"class": "jobTitle"})
    company_name_tag = table_list[0].find('span', {"class": "companyName"})
    if company_name_tag != None: 
        company_name = company_name_tag.text
    else:
        company_name = None
    company_location_tag = table_list[0].find('div', {"class": "companyLocation"})
    company_location = company_location_tag.find(text=True, recursive=False)
    salary_tag = table_list[0].find('div', {"class": "salaryOnly"})
    if salary_tag != None: 
        children = salary_tag.findChildren("div" , recursive=False)
        salary = children[0].text
    else:
        salary = None
    posted_tag = soup.find('span',{"class": "date"})
    posted = posted_tag.find(text=True, recursive=False)
    span_tag = h2_tag[0].find_all('span')
    for span in span_tag:
        if span.has_attr('title'):
            job_title = span['title']
    # returns all the details specific to a listing in a list
    data = [job_title, company_name, company_location, posted, salary]
    return data

# extracts all the job listings
def fetch_job_data(position, location):
    print('Searching for', position, 'jobs in', location, '...')
    job_listings = []
    url = get_url(position, location)
    
    
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div',{"id": "mosaic-provider-jobcards"})
        jobs = cards[0].find_all('div', {"class": "job_seen_beacon"})
        for job in jobs:
            listing = getJobs(soup, job)
            job_listings.append(listing)
        try:
            # to move through the pages
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            #print(url)
            page = parse_qs(urlparse(url).query)['start'][0]
            # to fetch the top 60 job listings
            if page:
                if(int(page) >= 40):
                    break
        except AttributeError:
            break
        # adds all the listings into a datafram
    return pd.DataFrame(job_listings, columns=['Job Title','Company', 'Location', 'Post date', 'Salary'])


