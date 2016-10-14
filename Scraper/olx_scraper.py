#! /usr/bin/python3
# DA project

import csv
import os
import threading
from bs4 import BeautifulSoup

cities = ['ahmedabad', 'bangalore', 'chandigarhcity', 'chennai', 'coimbatore', 'gurgaon', 'hyderabad', 'jaipur', 'kochi', 'kolkata', 'lucknow', 'ludhiana', 'mumbai', 'newdelhi', 'pune', 'thiruvananthapuram']

base1 = 'https://www.olx.in/'
base2 = '/cars/?search%5Bfilter_float_year%3Afrom%5D=2010'

city_url = []
for city in cities:
	u = base1 + city + base2
	city_url.append(u)

def create_urls(url, soup):
	pg = soup.findAll('a', {'class': 'block br3 brc8 large tdnone lheight24'})
	total_pages = int(pg[-1].text.replace('\r', '').replace('\n', '').replace(' ', ''))
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
				url_list = []
				url_list.append(car_str)
				url_list.append(car_url)
				print(url_list)
				#full_list.append(url_list)


if __name__ == '__main__':
	get_car_link_list()

	print('\nDONE !')