import csv
from unidecode import unidecode
import bs4
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import string
import requests

def setUp(starting_url):
	chrome_options = webdriver.ChromeOptions()
	profile = {
		"download.prompt_for_download": False, #To auto download the file
		"download.directory_upgrade": True,
		"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
	}
	chrome_options.add_experimental_option("prefs", profile)
	chrome_options.add_argument("--start-maximized")
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(starting_url)
	time.sleep(1)
	return driver

def getURLs():
	urls = []
	f = open('mop_urls_or.txt', 'r')
	for line in f:
		urls.append(line.rstrip('\n'))
	return urls

def getLicensePlates():
	lps = []
	f = open('flockOR200.txt', 'r')
	for line in f:
		lps.append(line.rstrip('\n'))
	return lps

def populateSearchPage(driver, url):
	driver.get(url)
	time.sleep(1)
	vehicle_info = driver.find_element(By.XPATH, '//*[@id="option-Vehicle"]/div/div/forge-button/div')
	vehicle_info.click()
	time.sleep(3)
	state_dropdown = driver.find_element(By.XPATH, '//*[@id="VehicleRegistrationState-select"]')
	state_dropdown.click()
	time.sleep(1)
	state_dropdown.send_keys('O')
	state_dropdown.send_keys(Keys.DOWN)
	state_dropdown.send_keys(Keys.DOWN)
	state_dropdown.send_keys(Keys.ENTER)
	time.sleep(1)
	return driver

def searchLicensePlate(driver, lp):
	print(lp)
	lp_search_field = driver.find_element(By.XPATH, '//*[@id="VehicleLicensePlateNumber"]')
	lp_search_field.click()
	lp_search_field.clear()
	lp_search_field.send_keys(lp)
	time.sleep(.1)
	search_button = driver.find_element(By.XPATH, '//*[@id="search_form"]/form/div[2]/forge-button//div')
	search_button.click()
	time.sleep(3)
	return driver

def main():
	with open("mop_oregon_hits.csv", mode='a') as fw:
		writer = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		#writer.writerow(['license_plate', 'url'])
		lps = getLicensePlates()
		urls = getURLs()
		driver = setUp(urls[0])
		for url in urls:
			print(url)
			driver = populateSearchPage(driver, url)
			for lp in lps:
				driver = searchLicensePlate(driver, lp)
				try:
					close_error_button = driver.find_element(By.XPATH, '//*[@id="close-error-dialog-0"]')
					close_error_button.click()
					time.sleep(1)
				except:
					soup = BeautifulSoup(driver.page_source, "html.parser")
					if soup.find('div', {'role':'alert'}) is None:
						writer.writerow([lp, url])
						print('HIT: {} - {}'.format(lp, url))
						driver = populateSearchPage(driver, url)
					elif soup.find('div', {'id':'search_summary'}) is not None:
						driver = populateSearchPage(driver, url)

if __name__ == '__main__':
	main()