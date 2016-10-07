#!/usr/bin/env python

from selenium import webdriver
import sys
import time

class O2GetPrice:
  # This is the main URL of the form
  url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"
  sleep_after = 3
  def __init__(self, url=None, sleep_after=None):
    if url is not None:
      self.url = url
    if sleep_after is not None:
      self.sleep_after = sleep_after

  # This is the path to the selenium webdriver you want to use
  driver_path = "./selenium_drivers/chromedriver"
  def start_browser(self, path=None):
    if path is not None:
      self.driver_path = path
    self.browser = webdriver.Chrome(executable_path = self.driver_path)
    # This avoids a time.sleep after writing the country name
    # and waits for the paymonthly and paygo divs to become available
    self.browser.implicitly_wait(10)
    self.browser.get(self.url)

  def stop_browser(self):
    self.browser.quit()

  # Necessary methods to use in a with statement
  def __enter__(self):
    self.start_browser()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.stop_browser()

  # accepts a country string and returns an array with two prices
  # the first one is the "Pay Monthly", the second one is the "Pay & Go"
  def get_standard_prices(self,country):
    # We first write the country in the textarea
    try:
      # need to address this here since the empty string causes the form to
      # return the prices for Abkhazia
      if country.strip() == "":
      	raise Exception("Empty country")
      inputarea = self.browser.find_element_by_id('countryName')  
      inputarea.clear()
      inputarea.send_keys(country+'\n') # the '\n' ensures that a request is sent
      # When we input a wrong country the class changes 
      # we need to check this because we clearing the input area
      # does not remove the previous search results and causes the function
      # to return the old prices
      if "error" in  inputarea.get_attribute("class"):
      	raise Exception("Country not found")
    except Exception as e:
      # log the error
      sys.stderr.write("Input problems: {},{}".format(country, e))
      return [None,None]

    # and now we gather the prices
    result = []
    for div_id in ["paymonthlyTariffPlan","payandgoTariffPlan"]:
      try:
      	price = self.browser.find_element_by_xpath('//*[@id="{}"]//*[@id="standardRatesTable"]/tbody/tr[1]/td[2]'.format(div_id))
      	price_str = price.get_attribute('innerText')
      	result.append(float(price_str[1:])) # the [1:] gets rid of the pound symbol
      except Exception as e:
      	result.append(None)
      	# log the error
      	sys.stderr.write("Unable to find price: {},{},{}".format(country, div_id, e))
    
    # we sleep here so the user doesn't have to
    # but it's not strictly necessary
    time.sleep(self.sleep_after)
    return result



if __name__ == "__main__":
  countries_to_get = ["", "Canada", "Wakanda", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]

  with O2GetPrice() as o2:
    for country in countries_to_get:
      print country, o2.get_standard_prices(country)
