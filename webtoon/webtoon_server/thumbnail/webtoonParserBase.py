from bs4 import BeautifulSoup
import time
from abc import ABCMeta



class WebtoonParserBase(metaclass=ABCMeta):

    def __init__(self, beautifulSoup):
        self.driver = webdriver.PhantomJS(executable_path=phantom_path)
        self.bs = BeautifulSoup

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
        self.driver.close()


    def get_image_detail(self, soupImgDiv):
        src = soupImgDiv['src']
        alt =  soupImgDiv['alt']
        return {
            'src' : src,
            'alt' : alt
        }

