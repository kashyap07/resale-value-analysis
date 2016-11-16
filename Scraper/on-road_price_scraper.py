#! /usr/bin/python3
# DA project

# ctrl-c to stop looping

import csv
import os
import sys
import signal
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

cities = ['Bangalore', 'Chennai', 'Hyderabad', 'Kolkata', 'Mumbai (Central)', 'Delhi (Central)']
url_str = 'http://www.carwale.com/'
company_names = ['audi', 'bmw', 'chevrolet', 'datsun', 'fiat', 'forcemotors', 'ford', 'honda', 'hyundai', 'jaguar', 'landrover', 'mahindra', 'marutisuzuki', 'mercedesbenz', 'mitsubishi', 'nissan', 'renault', 'skoda', 'tata', 'toyota', 'volkswagen', 'volvo']
companies = 22
cc = 0 # company-count

url1 = 'http://www.carwale.com/marutisuzuki-cars/'

ffox = FirefoxBinary('/home/kashyap/my_programs/firefox45/firefox')
browser = webdriver.Firefox(firefox_binary=ffox)
browser.maximize_window()

all_url = []
while cc < companies:
	all_url.append(url_str + company_names[cc] + '-cars/')
	cc = cc + 1

car_info = []

def __loop_through():
	global browser
	for link in all_url:
		__create_list(link)
	print(car_info)


# ok, thus pissed
# brute force ftw
def __create_list(url):
	global browser

	browser.get(url)
	try:
		no_btn = browser.find_element_by_id('btnYes')
		no_btn.click()
	except:
		pass

	try:
		while True:
			rdy = input('Press y to continue, n to break loop\n')
			if rdy == 'y':
				time.sleep(2)
				for city in cities:
					citySelect = Select(browser.find_element_by_id('drpPqCity'))
					try:
						citySelect.select_by_visible_text(str(city))
						car_info.append(__get_info())
					except:
						pass
			else:
				break

	except KeyboardInterrupt:
		pass


def __create_list_automatically_doesnt_actually_work(url):
	global browser
	flag = True

	browser.get(url)
	try:
		no_btn = browser.find_element_by_id('btnYes')
		no_btn.click()
	except:
		pass

	time.sleep(1)
	li = browser.find_elements_by_css_selector('a#btnChkOnRoadPrice.btn.btn-orange.btn-xs')
	count = len(li)

	while count != 0:
		el = li[-count]
		browser.execute_script("return arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-10);", el)
		el.click()
		time.sleep(1)
		while flag == True:
			for city in cities:
				citySelect = Select(browser.find_element_by_id('drpPqCity'))
				try:
					citySelect.select_by_visible_text(str(city))
					car_info.append(__get_info())
				except:
					pass

			uip = input('continue ?')
			if uip == 'n':
				flag = False
			else:
				print('waiting for input')
				time.sleep(4)
			count = count - 1


def __get_info():
	global browser
	global outfile
	indiv_l = []
	browser.execute_script("window.scrollTo(0, 0)")
	time.sleep(1)
	name = browser.find_element_by_id('pq-jcarousel').text
	price = browser.find_elements_by_css_selector('b')[1].text.replace(',', '')
	location = browser.find_elements_by_class_name('tblDefault')[1].text[15:31].replace(')', '').replace('(', '').replace(',', '').replace(' ', '').replace('Central', '')
	location = re.sub('\d+', '', location)
	comp_name = __get_company(name)
	cntr = comp_name + ' '
	ntr = name.replace(cntr, '')
	indiv_l.append(comp_name)
	indiv_l.append(ntr)
	indiv_l.append(location)
	indiv_l.append(price)
		
	print(indiv_l)
	return indiv_l


def __get_company(name):
	if 'Audi' in name:
		return 'Audi'
	if 'BMW' in name:
		return 'BMW'
	if 'Chevrolet' in name:
		return 'Chevrolet'
	if 'Datsun' in name:
		return 'Datsun'
	if 'Fiat' in name:
		return 'Fiat'
	if 'Force Motors' in name:
		return 'Force Motors'
	if 'Ford' in name:
		return 'Ford'
	if 'Homda' in name:
		return 'Honda'
	if 'Hyundai' in name:
		return 'Hyundai'
	if 'Jaguar' in name:
		return 'Jaguar'
	if 'Land Rover' in name:
		return 'Land Rover'
	if 'Mahindra' in name:
		return 'Mahindra'
	if 'Maruti Suzuki' in name:
		return 'Maruti Suzuki'	
	if 'Mercedes-Benz' in name:
		return 'Mercedes-Benz'
	if 'Mitsubishi' in name:
		return 'Mitsubishi'
	if 'Nissan' in name:
		return 'Nissan'
	if 'Renault' in name:
		return 'Renault'
	if 'Skoda' in name:
		return 'Skoda'
	if 'Tata' in name:
		return 'Tata'
	if 'Toyota' in name:
		return 'Toyota'
	if 'Volkswagen' in name:
		return 'Volkswagen'
	if 'Volvo' in name:
		return 'Volvo'
	

if __name__ == '__main__':
	__loop_through()

	timestr = time.strftime('%%%d_%H:%M:%S')
	outfile = open('./carwale_list@' + timestr + '.csv', 'w')
	writer = csv.writer(outfile)
	writer.writerow(['COMPANY NAME', 'NAME AND TRIM', 'LOCATION', 'ON-ROAD PRICE'])
	writer.writerows(car_info)
	
	print('\nDONE !')