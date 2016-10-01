#! /usr/bin/python3
#DA project

import csv
import os
import requests
from bs4 import BeautifulSoup

url_str = 'https://www.olx.in/cars/?search%5Bfilter_float_year%3Afrom%5D=2014'

#total_pages = 391
total_pages = 3
current_page = 0
all_url = []
while current_page < total_pages:
	all_url.append(url_str + '&page=' + '2')
	current_page = current_page + 1
# todo

full_list = []
def get_cars():
	for page_url in all_url:	
		src = requests.get(page_url)
		soup = BeautifulSoup(src.text, 'lxml')
		for link in (soup.findAll('a', {'class': 'marginright5 link linkWithHash detailsLink'})):
			car_url = link.get('href')
			car_name = link.find('span').text
			url_list = []
			url_list.append(car_name)
			url_list.append(car_url)
			# also include manufacturer name while entering individual car
			full_list.append(url_list)

if __name__ == '__main__':
	get_cars()

	outfile = open('./olx_car_list.csv', 'w')
	writer = csv.writer(outfile)
	writer.writerow(['TITLE', 'URL'])
	writer.writerows(full_list)