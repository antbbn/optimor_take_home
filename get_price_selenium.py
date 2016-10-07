from selenium import webdriver
import time

class O2GetPrice:
  url = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"
  def __init__(self, url=None):
    if url is not None:
      self.url = url

  driver_path = "./selenium_drivers/chromedriver"
  def start_browser(self, path=None):
    if path is not None:
      self.driver_path = path
    self.browser = webdriver.Chrome(executable_path = self.driver_path)
    self.browser.get(self.url)

  def stop_browser(self):
    self.browser.quit()

  # Necessary methods to use in a with statement
  def __enter__(self):
    self.start_browser()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.stop_browser

  # accepts a country string and returns an array with two prices
  # the first one is the "Pay Monthly", the second one is the "Pay & Go"
  def get_standard_prices(self,country):
    inputarea = self.browser.find_element_by_id('countryName')  
    inputarea.clear()
    inputarea.send_keys(country+'\n')
    time.sleep(1)
    result = []
    for div_id in ["paymonthlyTariffPlan","payandgoTariffPlan"]:
      price = self.browser.find_element_by_xpath('//*[@id="{}"]//*[@id="standardRatesTable"]/tbody/tr[1]/td[2]'.format(div_id))
      price_str = price.get_attribute('innerText')
      result.append(float(price_str[1:])) # the [1:] gets rid of the pound symbol
    time.sleep(3)
    return result



if __name__ == "__main__":
  countries_to_get = ["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]

  with O2GetPrice() as o2:
    for country in countries_to_get:
      print country, o2.get_standard_prices(country)
