import sys
import requests
import json
from bs4 import BeautifulSoup

url_all_countries = "http://international.o2.co.uk/internationaltariffs/getallcountries"
url_country = "http://international.o2.co.uk/internationaltariffs/getintlcallcosts?countryId={}"

all_countries_req = requests.get(url_all_countries)
if all_countries_req is None or all_countries_req.status_code != requests.codes.ok:
  print "Failed request"
  sys.exit(-1)

try:
  all_countries = json.loads(all_countries_req.content)
except Exception as e:
  print "Error parsing json ",e
  sys.exit(-1)

print "Done with all countries"

# the json contains a list of dictionaries with these keys
# {"name","isdCode","countryId","zone","networkOperators","european" }
# so we have to cycle trough it to find the ones of interest
countries_to_get = ["Canada", "Germany", "Iceland", "Pakistan", "Singapore", "South Africa"]

countries_ids_to_get = {} 
for country in all_countries:
 if country['name'] in countries_to_get:
   countries_ids_to_get[country['name']] = country['countryId'] 


for country_name, country_id in countries_ids_to_get.iteritems():
  country_req = requests.get(url_country.format(country_id))
  if country_req is None or country_req.status_code != requests.codes.ok:
    print "Failed request"
    sys.exit(-1)
  #with open("{}.html".format(country_name),"w") as testfile:
  #  testfile.write(country_req.content)
  soup = BeautifulSoup(country_req.content)
  print country_name,
  for div_id in ["paymonthlyTariffPlan","payandgoTariffPlan"]:
    div = soup.find(id=div_id)
    standard_rates_table = div.find(id='standardRatesTable')
    trs = standard_rates_table.find_all('tr')
    tds = trs[0].find_all('td')
    print div_id, float(tds[1].string[1:]),
  print



