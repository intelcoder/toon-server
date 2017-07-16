import datetime

from .episode_scraper_base import EpisodeScraperBase
from urllib.parse import urljoin


class KakaoEpisodeScraper(EpisodeScraperBase):

    def __init__(self):
        super().__init__()

    def get_latest_episode(self, episode_list_soup):

        latest_episode = episode_list_soup.find('li')
        return self.get_episode_data(latest_episode)

    def get_episode_data(self, episode):
        uploaded_time = episode.find(
            'span', {"class": "date"}).getText().strip().replace('.', '-')
        return {
            "episode_title": episode.img['alt'],
            "uploaded_at": uploaded_time,
            "no": episode['data-productid'],
            "thumbnail_url": episode.img['src']
        }

    def get_webtoon_detail(self, soup):
        pass

    def get_episode(self, soup, no):
        pass

    def get_episode_soup(self, toon_id, page=1):
        url = self._get_url_queries(toon_id, page)
        return self.get_soup(url)

    def get_episode_list(self, soup):
        ul = soup.find('ul', {"class": "listMain"})
        return ul

    def _get_url_queries(self, toon_id, page=1):
        return f"http://page.kakao.com/home/{toon_id}?orderby=desc&page={page}"
