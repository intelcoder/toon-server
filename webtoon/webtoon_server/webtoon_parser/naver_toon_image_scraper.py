from urllib.parse import urlencode

from .utils import append_query_to_url
from .toon_image_scraper_base import ToonImageScraperBase


class NaverToonImageScraper(ToonImageScraperBase):
    def __init__(self):
        self.baseUrl = "http://comic.naver.com/webtoon/detail.nhn"
        self.default_soup_delay = 0
        super().__init__()

    def scrap_images(self, soup):
        toon_img_container = soup.find('div', {'class': 'wt_viewer'})
        toons = toon_img_container.findAll('img')
        toon_image_list = [toon['src'] for idx, toon in enumerate(toons)]
        return toon_image_list

    # http://comic.naver.com/webtoon/detail.nhn?titleId=20853&no=107
    def _append_url_query(self, id, no):
        params = {'titleId': id, 'no': no}
        return append_query_to_url(self.baseUrl, params)

    def get_toon_image_soup(self, id, no):
        request_url = self._append_url_query(id, no)
        return self.get_soup(request_url, self.default_soup_delay)
