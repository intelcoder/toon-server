
from .webtoon_scraper_base import WebtoonScraperBase
from abc import ABCMeta, abstractmethod

class ToonImageScraperBase(WebtoonScraperBase, metaclass=ABCMeta):


    def __init__(self):
        super().__init__()

    @abstractmethod
    def scrap_images(self, soup):
        pass

    @abstractmethod
    def _append_url_query(self, id, no):
        pass

    @abstractmethod
    def get_toon_image_soup(self, id, no):
        pass