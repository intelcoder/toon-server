import datetime

from .episode_scraper_base import EpisodeScraperBase
from urllib.parse import urljoin


class DaumEpisodeScraper(EpisodeScraperBase):
    def __init__(self):
        super().__init__()
        self.base_url = "http://webtoon.daum.net/webtoon/view/"


    def get_webtoon_detail(self, soup):
        """
        This function will be used to update details of webtoon
        For daum
        :param soup: BeautifulSoup
        :return: webtoon detatils in dictionary type
        """

        # initial value
        description = ''
        title = ''
        rating = 0

        toon_detail_container = soup.find('div', {'class': 'product_intro'})

        if toon_detail_container:
            details = toon_detail_container.find('div', {'class': 'desc_product'})
            title = details.find('h3', {'class': 'tit_product'}).getText()
            description = details.find('dd', {'class': 'txt_story'}).getText()
            rating_em = details.find('em', {'class': 'emph_grade'})
            rating = rating_em.getText() if rating_em else rating

        return {
            "description": description,
            'rating': rating,
            'title': title
        }

    def get_episode(self, soup, no):
        pass

    def get_lastest_episode(self, soup):
        """
        This function will retrieve lastest episode which is top episode on page 
        :param soup: Beautifulsoup
        :return: 
        """
        latest_episode_li = soup.find("ul", {"class": "list_update"}).find('li', {"class": ""})
        uploaded_at = latest_episode_li.div.span.getText().split(' ')[1]

        return {
            "episode_title": latest_episode_li.a.img['alt'],
            "uploaded_at": self._format_daum_data(uploaded_at),
            "no": latest_episode_li.a['data-id'],
            "thumbnail_url": latest_episode_li.a.img['src']
        }

    def get_episode_list(self, soup):
        """
        This function will be used to initialize and update episode list on a webtoon
        :param soup: BeautifulSoup
        :return: Dict Episode details in dictionary type
        """
        episode_list = []
        li_list = soup.find("ul", {"class": "list_update"}).findAll('li', {"class": ""})

        for li in li_list:
            uploaded_at = li.div.span.getText().split(' ')[1]
            episode_list.append({
                "uploaded_at": self._format_daum_data(uploaded_at),
                "no": li.a['data-id'],
                "thumbnail_url": li.a.img['src'],
                "episode_title": li.a.img['alt'],
            })

        return episode_list

    def get_soup_for_episodes(self, soup, latest):
        episode_li_list = soup.find("ul", {"class": "list_update"}).findAll('li', {"class": ""})
        if episode_li_list:
            return episode_li_list[:1] if latest else episode_li_list
        return []

    def get_episode_soup(self, toon_id, page):
        print(self._get_url_queries(toon_id, page))
        return self._get_soup(self._get_url_queries(toon_id, page))

    def _get_soup(self, request_url):
        return self.get_soup(request_url)

    def _get_url_queries(self, toon_id, page):
        return urljoin(self.base_url, toon_id)

    def _format_daum_data(self, date):
        if date:
            return date.replace('.', '-')

        return datetime.datetime.now()