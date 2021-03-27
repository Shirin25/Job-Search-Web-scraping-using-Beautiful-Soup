from urllib.request import urlopen
from urllib.parse import urlparse
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd
from datetime import datetime


def find_job_from(website,job_title,location,attributes,filename="result7.xls"):
	if website=='Indeed':
		job_soup=load_indeed_jobs_div(job_title,location)
		job_list, num_listings = extract_job_information_indeed(job_soup, attributes)
	in_excel(job_list,filename)

	

def load_indeed_jobs_div(job_title, location):
    getVars = {'q' : job_title, 'l' : location, 'fromage' : 'last', 'sort' : 'date'}
    url = ('https://www.indeed.com/q-India-jobs.html?vjk=7b0ecb99659e2f88' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_title_indeed(job_elem):
	title_box=job_elem.find('h2',attrs={'class':'title'})
	title=title_box.text.strip()
	return title

def extract_company_indeed(job_elem):
	company_box=job_elem.find('span',attrs={'class':'company'})
	company=company_box.text.strip()
	return company

def extract_link_indeed(job_elem):
	link=job_elem.find('a')['href']
	link='https://in.indeed.com/?r=India'+link
	return link

def extract_date_indeed(job_elem):
	date_box=job_elem.find('span',attrs={'class':'date'})
	date=date_box.text.strip()
	return date


def extract_job_information_indeed(job_soup,attributes):
	job_elems = job_soup.find_all('div', attrs={'class':'jobsearch-SerpJobCard'})

	cols =[]
	extracted_info=[]

	if 'titles' in attributes:
		titles=[]
		cols.append('titles')
		for job_elem in job_elems:
			titles.append(extract_job_title_indeed(job_elem))
		extracted_info.append(titles)

	if 'companies' in attributes:
		companies=[]
		cols.append('companies')
		for job_elem in job_elems:
			companies.append(extract_company_indeed(job_elem))
		extracted_info.append(companies)

	if 'links' in attributes:
		links=[]
		cols.append('links')
		for job_elem in job_elems:
			links.append(extract_link_indeed(job_elem))
		extracted_info.append(links)

	if 'date_list' in attributes:
		date_list=[]
		cols.append('date_list')
		for job_elem in job_elems:
			date_list.append(extract_date_indeed(job_elem))
		extracted_info.append(date_list)

	job_list={}

	for j in range(len(cols)):
		job_list[cols[j]]=extracted_info[j]

	num_listings=len(extracted_info[0])
	return job_list,num_listings
	print('{} new job postings retrieved, Stored in {}.'.format(num_listings,filename))

def in_excel(job_list,filename):
	jobs=pd.DataFrame(job_list)
	jobs.to_excel(filename)


