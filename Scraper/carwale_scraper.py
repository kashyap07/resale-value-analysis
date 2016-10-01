#! /usr/bin/python3
# DA project

import csv
import os
import requests
import threading
from bs4 import BeautifulSoup

url_str = 'http://www.carwale.com/'
company_names = ['audi', 'bmw', 'chevrolet', 'datsun', 'fiat', 'forcemotors', 'ford', 'honda', 'hyundai', 'jaguar', 'landrover', 'mahindra', 'marutisuzuki', 'mercedesbenz', 'mitsubishi', 'nissan', 'renault', 'skoda', 'tata', 'toyota', 'volkswagen', 'volvo']
companies = 22
cc = 0 # company-count

all_url = []
while cc < companies:
	all_url.append(url_str + company_names[cc] + '-cars/')
	cc = cc + 1

full_list = []
def get_cars():
	for the_url in all_url:
		src = requests.get(the_url)
		soup = BeautifulSoup(src.text, 'lxml')
		for link in soup.findAll('a', {'class': 'font18'}):
			href = str('http://www.carwale.com' + link.get('href'))
			car_name = str(link.string)
			print(car_name)
			#print(href)

			detail_list = []
			detail_list.append(car_name)
			#detail_list.append(href)
			detail_list.append(car_avg_price(href))
			full_list.append(detail_list)

def car_avg_price(car_url):
	src = requests.get(car_url)
	soup = BeautifulSoup(src.text, 'lxml')
	for car in soup.findAll('span', {'class': 'text-bold'})[-6:-5]:
		car_str = str(car.text)
		car_str = car_str[46:-43]
		# lot of trial-error
		# use cost of top-end model as avg. on-road value
		# seems-legit
		if(car_str[-1:] == 'C'):	# special case of crore
			car_str = car_str[:-1]
			price = int(10000000 * float(car_str))
		else:
			price = int(100000 * float(car_str))
		return price


if __name__ == '__main__':
	t1 = threading.Thread(target=get_cars)
	t1.start()
	t1.join()

	outfile = open('./car_list.csv', 'w')
	writer = csv.writer(outfile)
	writer.writerow(['CAR NAME', 'AVG. ON-ROAD PRICE'])
	writer.writerows(full_list)

	print('\nDONE !')