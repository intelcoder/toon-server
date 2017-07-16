from .toon_list_scraper_base import ToonListScraperBase
from .utils import append_fragment_to_url
import re


class KakaoToonListScraper(ToonListScraperBase):
    def __init__(self):
        self.base_url = "http://page.kakao.com"
        super().__init__()

    def get_toon_list(self, toon_list_soup, weekday):
        pass

    def get_toonlist_soup(self, weekday):
        request_url = self._get_request_url(weekday)
        print(request_url)
        soup = self.get_soup(request_url)
        return soup.findAll("li", {"class": ["list", "_ajaxCallList"]})

    def get_all_toon_list(self, soup, weekdays):
        pass

    def _get_request_url(self, weekday_index):
        return f"http://page.kakao.com/main/ajaxCallWeeklyList?navi=1&day={weekday_index}&inkatalk=0&inChannel=0&categoryUid=10&subCategoryUid=1000"
