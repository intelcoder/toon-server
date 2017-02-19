from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webtoon_server.config import phantom_path

driver = webdriver.PhantomJS(executable_path=phantom_path)


class WebtoonScraperBase():
    def __init__(self, driver=driver, beautifulSoup=BeautifulSoup):
        self.driver = driver
        self.bs = beautifulSoup

    # get soup from html
    def get_soup(self, url, delay=5):
        html = self._get_html_source(url, delay)
        return self.bs(html, 'lxml')

    def _get_html_source(self, url, delay):
        # sometimes browser need to wait till source code load finish
        self.driver.get(url)
        time.sleep(delay)
        return self.driver.page_source

    def close_driver(self):
        self.driver.quit()

    def get_image_detail(self, img_div):
        src = img_div['src']
        alt = img_div['alt']
        return {
            'src': src,
            'alt': alt
        }
