#! /usr/bin/python3
# DA project

# ctrl-c to stop looping

import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

ffox = FirefoxBinary('/home/kashyap/my_programs/firefox45/firefox')
browser = webdriver.Firefox(firefox_binary=ffox)
browser.maximize_window()

# test url
url1 = 'http://www.carwale.com/marutisuzuki-cars/'

cities = ['Bangalore', 'Chennai', 'Hyderabad', 'Kolkata', 'Mumbai (Central)', 'Delhi (Central)']
car_info = []

# TODO: function to generqate urls of all companies
#		and get back to previous car
#		csv


def __get_info():
	global browser
	indiv_l = []
	browser.execute_script("window.scrollTo(0, 0)")
	time.sleep(1)
	name = browser.find_element_by_id('pq-jcarousel').text
	price = browser.find_elements_by_css_selector('b')[1].text.replace(',', '')
	location = browser.find_elements_by_class_name('tblDefault')[1].text[15:31].replace(')', '').replace('(', '').replace(',', '').replace(' ', '').replace('Central', '')
	location = re.sub('\d+', '', location)
	indiv_l.append(name)
	indiv_l.append(location)
	indiv_l.append(price)
	print(indiv_l)
	return indiv_l

def __create_list(url):
	global browser
	browser.get(url)
	try:
		no_btn = browser.find_element_by_id('btnYes')
		no_btn.click()
	except:
		pass

	time.sleep(1)
	el = browser.find_element_by_css_selector('a#btnChkOnRoadPrice.btn.btn-orange.btn-xs')
	el.click()

	try:
		while True:
			for city in cities:
				time.sleep(1)
				selection = Select(browser.find_element_by_id('drpPqCity'))
				try:
					selection.select_by_visible_text(str(city))
					car_info.append(__get_info())
				except Exception as e:
					raise e
			print('waiting for input')
			time.sleep(5)
	except KeyboardInterrupt:
		print('stopped')

	print(car_info)


if __name__ == '__main__':
	__create_list(url1)
	print('done')