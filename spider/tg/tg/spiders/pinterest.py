# -*- coding: utf-8 -*-
import scrapy
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC


class PinterestSpider(scrapy.Spider):
  name = 'pinterest'
  allowed_domains = ['br.pinterest.com']

  # Initalize the webdriver    
  def __init__(self):
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/google-chrome-stable'
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('window-size=1200x600')
    prefs = {'download.default_directory': '/crawler/downloads',
             'download.prompt_for_download': False,
             'download.directory_upgrade': True,
             'safebrowsing.enabled': False,
             'safebrowsing.disable_download_protection': True}

    options.add_experimental_option("prefs", prefs)
    self.driver = webdriver.Chrome(chrome_options=options)

  # Parse through each Start URLs
  def start_requests(self):
    start_urls = ['https://br.pinterest.com/search/pins/?q=outfit&rs=typed&term_meta[]=outfit%7Ctyped']
    for url in start_urls:
      yield scrapy.Request(url=url, callback=self.parse)

  # Parse function: Scrape the webpage and store it
  def parse(self, response):
      self.driver.get(response.url)
      # Output filenamedoc
      filename = "angular_data.csv"
      with open(filename, 'a+') as f:
          writer = csv.writer(f)
          # Selector for all the names from the link with class 'ng-binding'
          wait = WebDriverWait(self.driver, 10)
          pg = wait.until(EC.presence_of_element_located((By.XPATH, "//img")))
          names = self.driver.find_elements_by_css_selector("img")
          for name in names:
              print(name.get_attribute("src"))
              title = name.text
              writer.writerow([title])
      self.log('Saved file %s' % filename)