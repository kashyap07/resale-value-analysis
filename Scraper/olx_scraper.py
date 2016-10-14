#! /usr/bin/python3
# DA project

import csv
import os
import requests
import threading
from bs4 import BeautifulSoup

#cities = ['ahmedabad', 'bangalore', 'chandigarhcity', 'chennai', 'coimbatore', 'gurgaon', 'hyderabad', 'jaipur', 'kochi', 'kolkata', 'lucknow', 'ludhiana', 'mumbai', 'newdelhi', 'pune', 'thiruvananthapuram']
cities = ['bangalore']

base1 = 'https://www.olx.in/'
base2 = '/cars/?search%5Bfilter_float_year%3Afrom%5D=2010'

city_url = []
full_list = []
for city in cities:
	u = base1 + city + base2
	city_url.append(u)

def create_urls(url, soup):
	pg = soup.findAll('a', {'class': 'block br3 brc8 large tdnone lheight24'})
	#total_pages = int(pg[-1].text.replace('\r', '').replace('\n', '').replace(' ', ''))
	total_pages = 2
	current_page = 2
	all_url = []
	while current_page <= total_pages:
		all_url.append(url + '&page=' + str(current_page))
		current_page = current_page + 1
	return all_url

def get_car_link_list():
	for page_url in city_url:
		src = requests.get(page_url)
		soup = BeautifulSoup(src.text, 'lxml')
		for url in create_urls(page_url, soup):
			pg_src = requests.get(url)
			pg_soup = BeautifulSoup(pg_src.text, 'lxml')
			for link in pg_soup.findAll('a', {'class': 'marginright5 link linkWithHash detailsLink'}):
				car_url = link.get('href')
				car_str = link.find('span').text
				indiv_list = []
				indiv_list.append(car_str)
				indiv_list.extend(get_details(car_url))
				
				print(indiv_list)
				if indiv_list[1] != -1:
					full_list.append(indiv_list)

def get_details(url):
	src = requests.get(url)
	soup = BeautifulSoup(src.text, 'lxml')
	detail_list = []
	city = soup.findAll('a', {'class': 'link nowrap'})[0].text[5:]
	found = soup.findAll('strong', {'class': 'block'})
	company = found[0].text.strip()
	model = found[1].text.strip()
	year = found[2].text.strip()
	fuel = found[3].text.strip()
	driven = found[4].text.replace('km', '').replace(',', '').strip()
	price = soup.find('strong', {'class': 'xxxx-large margintop7 inlblk not-arranged'}).text
	detail_list.extend([city, company, model, year, fuel, driven, price])
	if detail_list[1] == 'Other Brands' or detail_list[2] == 'Others':
		detail_list = [-1]
	return detail_list
	


if __name__ == '__main__':
	get_car_link_list()

	outfile = open('./olx_list.csv', 'w')
	writer = csv.writer(outfile)
	writer.writerow(['DESCRIPTION', 'LOCATION', 'MANUFACTURER', 'MODEL', 'YEAR', 'FUEL', 'KMS DRIVEN', 'PRICE'])
	writer.writerows(full_list)

	print('\nDONE !')