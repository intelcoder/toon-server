from .webtoon_scraper_base import WebtoonScraperBase
from .utils import append_query_to_url
import re


class KakaoImageScraper(WebtoonScraperBase):
    def __init__(self):
        super().__init__()
        self.base_url = "http://page.kakao.com/viewer"

    def scrap_images(self, soup):
        imgContainers = soup.findAll('input')
        return [container['value'] for container in imgContainers if container["class"][0] == "originSrc"]

    def get_toon_image_soup(self, id, no=None):
        request_url = append_query_to_url(self.base_url, {"productId": id})
        return self.get_soup(request_url)
