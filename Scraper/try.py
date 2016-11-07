#! /usr/bin/python3
# DA project

import os
import sys
import string
import csv
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

ffox = FirefoxBinary('/home/kashyap/my_programs/firefox45/firefox')
browser = webdriver.Firefox(firefox_binary=ffox)
browser.maximize_window()
browser.get('http://www.carwale.com/marutisuzuki-cars/')

car_info = []

no_btn = browser.find_element_by_id('btnYes')
no_btn.click()

el = browser.find_element_by_css_selector('a#btnChkOnRoadPrice.btn.btn-orange.btn-xs')
el.click()

name = browser.find_element_by_id('pq-jcarousel').text
price = browser.find_elements_by_css_selector('b')[1].text.replace(',', '')
car_info.append(name)
car_info.append(price)


drp_dwn = browser.find_element_by_id('selectcustom-input-box-holder')
drp_dwn.click()

variants = browser.find_elements_by_id('selectOptionList')
for i in variants:
	i.click()
	name = browser.find_element_by_id('pq-jcarousel').text
	price = browser.find_elements_by_css_selector('b')[1].text.replace(',', '')
	car_info.append(name)
	car_info.append(price)
	browser.back()



print(car_info)