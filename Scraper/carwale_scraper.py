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
			detail_list = []
			detail_list = car_detail(href)
			if detail_list[2] != -1:
				full_list.append(detail_list)
				print('added ' + detail_list[0] + ' ' + detail_list[1])
			else:
				print('price not found for ' + detail_list[0] + ' ' + detail_list[1])


def car_detail(car_url):	# returns a list
	details = []
	src = requests.get(car_url)
	soup = BeautifulSoup(src.text, 'lxml')

	span_found = soup.findAll('span', {'itemprop': 'title'})
	comp_str = span_found[1].text
	car_str = str(span_found[2].text)[1:]
	details.extend([comp_str, car_str])
	try:
		price_str = ((str((soup.findAll('span', {'class': 'text-bold'})[-6:-5])[0].text)).replace(' ', '').replace('\n', '').replace('\r', ''))[:-1]
		# ex showroom price of top end model is at [-6:-5]
		# [0] since findAll returns a list
		# try-except sine some dont have values
	except:
		details.append(-1)
		# will remove the list out later
		return details
	if price_str[-1] == 'C':
		price_str = price_str[:-1]
		price = int(10000000 * float(price_str))
	else:
		price = int(100000 * float(price_str))
	details.append(price)

	return details


if __name__ == '__main__':
	t1 = threading.Thread(target=get_cars)
	t1.start()
	t1.join()

	outfile = open('./car_list.csv', 'w')
	writer = csv.writer(outfile)
	writer.writerow(['CAR NAME', 'AVG. ON-ROAD PRICE'])
	writer.writerows(full_list)

	print('\nDONE !')