from urllib.parse import urlparse, parse_qs, urlencode

from .episode_scraper_base import EpisodeScraperBase


class NaverEpisodeScraper(EpisodeScraperBase):
    def __init__(self):
        self.baseUrl = "http://comic.naver.com/webtoon/list.nhn"

        super().__init__()

    # Get webtoon detail and author to update webtoon
    def get_webtoon_detail(self, soup):

        detail_conatiner = soup.find('div', {'class': 'comicinfo'}).find('div', {'class': 'detail'})
        author = detail_conatiner.find('span', {'class': 'wrt_nm'}).getText()
        description = detail_conatiner.p.getText()
        no = self.get_lastest_no(soup)
        # remove whitespace
        return {
            'no': no,
            'description': description.strip(),
            'author': author.strip()
        }

    def get_lastest_no(self, soup):
        lastest_episode_link = self.get_episode_list(soup)[0].find('a')
        return self._get_episode_no(lastest_episode_link)

    def _get_episode_no(self, episode_a_tag):
        return parse_qs(urlparse(episode_a_tag['href']).query)['no'][0]

    # extract necessary info from episode tr html source
    def _extract_episode_detail(self, episode_tr_source):
        a_tag = episode_tr_source.find('a')
        no = self._get_episode_no(a_tag)
        img_src = a_tag.img['src']
        title = episode_tr_source.find('td', {'class': 'title'}).a.getText()
        rating = episode_tr_source.find('strong').getText()
        uploaded_at = episode_tr_source.find('td', {'class': 'num'}).getText()
        formated_uploaded_at = uploaded_at.replace('.', '-')

        return {
            'no': no,
            'thumbnail_url': img_src,
            'episode_title': title,
            'rating': rating,
            'uploaded_at': formated_uploaded_at
        }

    def get_episode(self, soup, no):
        pass

    def get_episode_list(self, soup):

        toon_list_container = soup.find('table', {'class': 'viewList'}).findAll('tr', {'class': ''})
        return list(filter(lambda x: x.a, toon_list_container))

        # get episodes in first page( lastest )

    def get_lastest_list(self, soup):
        episode_details = []
        episode_list = self.get_episode_list(soup)
        for episode in episode_list:
            episode_detail = self._extract_episode_detail(episode)
            episode_details.append(episode_detail)
        return episode_details


    def get_lastest_episode(self, soup):
        episode_list = self.get_episode_list(soup)
        return self._extract_episode_detail(episode_list[0])



    def get_all_list(self):
        pass

    def get_page_soup(self, toon_id, page=1):
        requestUrl = self._get_url_queries(toon_id, page)
        return self._get_soup(requestUrl)

    def _get_url_queries(self, toon_id, page):
        params = {'titleId': toon_id, 'page': page}
        query = urlencode(params)
        return self.baseUrl + '?' + query

    def _get_soup(self, request_url):
        if request_url:
            return self.get_soup(request_url, 3)
        else:
            print('please set query')
