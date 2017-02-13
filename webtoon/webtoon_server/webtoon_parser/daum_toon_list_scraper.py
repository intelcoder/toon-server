from .toon_list_scraper_base import ToonListScraperBase
from .utils import append_fragment_to_url
import re


class DaumToonListScraper(ToonListScraperBase):
    def __init__(self):
        self.base_url = "http://webtoon.daum.net"
        super().__init__()

    def get_toon_list(self, toon_list_soup, weekday):
        toon_data = []
        for toon in toon_list_soup:
            for li in toon.findAll('li'):
                author = li.find('span', {"class": "txt_info"}).getText().split(' ')[1]
                image_detail = self.get_image_detail(li.a.img)
                link = li.a['href']
                result = re.search(r'/webtoon/view/', link)
                toon_id = link[result.end():len(link)]
                toon_data.append({
                    "toon_id": toon_id,
                    "title": image_detail['alt'],
                    "author": author,
                    "thumbnail_url": image_detail['src'],
                    "weekday": weekday,
                })
        return toon_data

    def get_toonlist_soup(self, weekday):
        request_url = self._get_request_url(weekday)
        soup = self.get_soup(request_url)
        toon_list_soup = soup.find('div', {'data-view': 'day'}).findAll('ul', {'class': 'list_wt'})
        return toon_list_soup

    def get_all_toon_list(self, soup, weekdays):
        pass

    def _get_request_url(self, weekday):
        params = {"day": weekday}
        return append_fragment_to_url(self.base_url, params)
