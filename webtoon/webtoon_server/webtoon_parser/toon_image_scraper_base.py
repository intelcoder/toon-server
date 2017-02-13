
from .webtoon_scraper_base import WebtoonScraperBase
from abc import ABCMeta, abstractmethod

class ToonImageScraperBase(WebtoonScraperBase, metaclass=ABCMeta):


    def __init__(self):
        self.baseUrl = "http://comic.naver.com/webtoon/detail.nhn"
        super().__init__()

    @abstractmethod
    def scrap_images(self):
        pass

    @abstractmethod
    def _append_url_query(self, id, no):
        pass

    @abstractmethod
    def get_toon_image_soup(self, request_url):
        pass