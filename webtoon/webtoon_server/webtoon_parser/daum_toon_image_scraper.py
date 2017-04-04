from .toon_image_scraper_base import ToonImageScraperBase


class DaumToonImageScraper(ToonImageScraperBase):
    def __init__(self):
        self.baseUrl = "http://webtoon.daum.net/webtoon/viewer/"
        super().__init__()

    def scrap_images(self, soup):
        toons = soup.find("div", {"id": "imgView"}).findAll('img')
        return [toon['src'] for toon in toons]

    def _append_url_query(self, id, no):
        return self.baseUrl + no

    def get_toon_image_soup(self, id, no):

        request_url = self._append_url_query(id, no)
        print(request_url)
        return self.get_soup(request_url)
