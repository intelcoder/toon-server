from abc import ABCMeta, abstractmethod

from .webtoon_scraper_base import WebtoonScraperBase

class EpisodeScraperBase(WebtoonScraperBase, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    # This function will scrap webtoon description and latest no. Webtoon data need to be updated
    @abstractmethod
    def get_webtoon_detail(self, soup):
        pass

    # get episode details ( title , updated date, rating, thumbnail url )
    @abstractmethod
    def get_episode(self, soup, no):
        pass


    # getAll episodes on webtoon ( episode title, rating, image)
    # return array of episode
    @abstractmethod
    def get_episode_list(self, soup):
        pass

    @abstractmethod
    def _get_url_queries(self, toon_id, page):
        pass
