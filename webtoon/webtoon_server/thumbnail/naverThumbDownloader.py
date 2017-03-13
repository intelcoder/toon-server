from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode
from .webtoonParserBase import WebtoonParserBase

weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class NaverThumbnailDownloader(WebtoonParserBase):
    def __init__(self, beautifulSoup=BeautifulSoup, weekday_list=weekday_list):
        self.baseUrl = 'http://comic.naver.com/webtoon/weekdayList.nhn'
        self.weekday_list = weekday_list
        super().__init__(beautifulSoup)

    def get_all_thumbnail_and_info(self):
        pass

    def get_request_url(self, param):
        return self.baseUrl + '?' + urlencode(param)

    def get_weekday_list(self):
        return self.weekday_list

    def get_thumbnail(self, weekday):
        param = {'week': weekday}
        request_url = self.get_request_url(param)
        thumb_list = self.get_image_list(self.get_soup(request_url))
        webtoons = []
        for thumb in thumb_list:
            thumb_container = thumb.find('div', {'class': 'thumb'}).a
            img = thumb_container.img
            thumb_a_detail = self.get_thumbnail_link_data(thumb_container)
            img_detail = self.get_image_detail(img)
            rating = thumb.dl.find('div', {'class': 'rating_type'}).strong.getText()
            webtoons.append(
                {
                    **thumb_a_detail,
                    **img_detail,
                    'rating': thumb.dl.find('div', {'class': 'rating_type'}).strong.getText()
                }
            )

        return {'webtoons': webtoons, 'dayOfWeek': weekday}

    def get_thumbnail_link_data(self, soup_a_tag):
        url_query = parse_qs(urlparse(soup_a_tag['href']).query)
        toon_id = url_query['titleId'][0]
        return {
            'id': toon_id,
        }

    def get_image_list(self, soup):
        return soup.find('ul', {'class': 'img_list'}).findAll('li')

