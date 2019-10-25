# -*- coding: utf-8 -*-
import scrapy, csv, os, time, urllib, hashlib

from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC

MAX_RETRIES = 10

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

      wait = WebDriverWait(self.driver, 10)
      pg = wait.until(EC.presence_of_element_located((By.XPATH, "//img")))

      for i in range(0, 7):
        for i in range(0, 10):
          self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(3)
        selenium_images = self.driver.find_elements_by_css_selector("img")
        images = []
        for image in selenium_images:
            images.append(image)
        self.download_images(images)

  def download_images(self, images):
    for image in images:
      if not os.path.exists('/crawler/downloads'):
          os.makedirs('/crawler/downloads')
      hash = hashlib.sha1(image.get_attribute("src").encode("UTF-8")).hexdigest()
      # image_name = image.get_attribute("alt").replace(" ", "").replace("/", "").replace(".", "").replace(",", "")
      urlretrieve(image.get_attribute("src"), "/crawler/downloads/" + hash + ".png")
