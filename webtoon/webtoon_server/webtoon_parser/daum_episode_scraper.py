from .episode_scraper_base import EpisodeScraperBase
from urllib.parse import urljoin


class DaumEpisodeScraper(EpisodeScraperBase):
    def __init__(self):
        self.base_url = "http://webtoon.daum.net/webtoon/view"
        super.__init__()

    def get_webtoon_detail(self):
        pass


    def get_episode(self, soup, no):
        pass


    def get_episode_list(self, soup):
        pass

    def _get_soup(self, request_url):
        return self.get_soup(request_url)

    def _get_url_queries(self, toon_id, page):
        return urljoin(self.base_url, toon_id)
