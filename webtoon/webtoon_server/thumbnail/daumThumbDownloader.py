from bs4 import BeautifulSoup
import urllib.request
import lxml
import os
import re
import time
from urllib.parse import urlparse, parse_qs, urlencode
from selenium import webdriver
from abc import ABCMeta, abstractmethod
from thumbnail import Thumbnail


phantomPath = "C:/Users/fiddlest/Documents/djangofirst/driver/phantomjs.exe"
dayWeekList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
# dayWeekList = ['mon']
driver = webdriver.PhantomJS(executable_path=phantomPath)
# driver = webdriver.Chrome("../../../driver/chromedriver.exe")

class DaumThumbnailDownloader(Thumbnail):
     def __init__(self, driver, beautifulSoup, dayWeekList = dayWeekList):
        self.baseUrl = "http://webtoon.daum.net/"
        super().__init__( driver, beautifulSoup)