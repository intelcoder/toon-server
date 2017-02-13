from .webtoon_scraper_base import WebtoonScraperBase
from abc import ABCMeta, abstractmethod


class ToonListScraperBase(WebtoonScraperBase, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_toon_list(self, soup, weekday):
        pass

    @abstractmethod
    def _get_request_url(self, weekday):
        pass

