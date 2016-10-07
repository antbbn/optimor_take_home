import sys
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"

countries_to_get = ["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]

#path_to_phantomjs = './phantomjs-2.1.1-macosx/bin/phantomjs' # change path as needed
#browser = webdriver.PhantomJS(executable_path = path_to_phantomjs)
path_to_chromedriver = './selenium_drivers/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

browser.get(url)
for country in countries_to_get:
  inputarea = browser.find_element_by_id('countryName')  
  inputarea.clear()
  inputarea.send_keys(country+'\n')
  time.sleep(1)
  print country,
  for div_id in ["paymonthlyTariffPlan","payandgoTariffPlan"]:
    div = browser.find_element_by_id(div_id)
    price = div.find_element_by_xpath('//*[@id="standardRatesTable"]/tbody/tr[1]/td[2]')
    print div_id, price.get_attribute('innerText')
  time.sleep(3)

#for country_name, country_id in countries_ids_to_get.iteritems():
#  soup = BeautifulSoup()
#  print country_name,
#  for div_id in ["paymonthlyTariffPlan","payandgoTariffPlan"]:
#    div = soup.find(id=div_id)
#    standard_rates_table = div.find(id='standardRatesTable')
#    trs = standard_rates_table.find_all('tr')
#    tds = trs[0].find_all('td')
#    print div_id, float(tds[1].string[1:]),
#  print
#
#
#
