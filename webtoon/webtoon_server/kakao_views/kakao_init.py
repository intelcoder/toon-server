from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Webtoon, Site, WebtoonEpisodes
from ..webtoon_parser.kakao_toon_list_scraper import KakaoToonListScraper
from ..webtoon_parser.kakao_episode_scraper import KakaoEpisodeScraper
from ..webtoon_parser.kakao_image_scraper import KakaoImageScraper
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions

dayWeekList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class KakaoInitView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, format=None):

        site = Site.objects.get(name='kakao')
        Webtoon.objects.filter(site__name='kakao').delete()
        kakao_scraper = KakaoToonListScraper()

        dayWeekList = ['mon', 'tue',
                       'wed', 'thu', 'fri', 'sat', 'sun']
        weekday_lookup = {
            i + 1: dayWeekList[i] for i in range(len(dayWeekList))}

        for index, weekday in weekday_lookup.items():
            thumbs = kakao_scraper.get_toonlist_soup(index)
            for thumb in thumbs:

                id = thumb.a['href'].split('?')[0].split('/')[2]
                author = thumb.dl.find('dd', {'class': 'info'}).getText().split('•')[
                    1].strip()
                new_webtoon_data = {
                    "toon_id": id,
                    "title": thumb.dl.h3.getText(),
                    "thumbnail_url": thumb.findAll('img')[1]['src'],
                    "description": thumb.dl.find('dd', {'class': 'summary'}).getText(),
                    "weekday": weekday_lookup.get(index),
                    "author": author,
                    "site": site
                }

                try:
                    obj = Webtoon.objects.get(toon_id=id)
                except Webtoon.DoesNotExist:
                    new_webtoon = Webtoon.objects.create(**new_webtoon_data)
                    new_webtoon.save()

        kakao_scraper.close_driver()

        return Response("webtoon naver")
#
# http://page.kakao.com/home/46599532?categoryUid=10&subCategoryUid=115&orderby=desc


class KakaoEpisodeView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, format=None):
        scraper = KakaoEpisodeScraper()
        soup = scraper.get_episode_soup('46599532')
        episode_list = scraper.get_episode_list(soup)
        episode = scraper.get_latest_episode(episode_list)
        webtoon = Webtoon.objects.get(toon_id='46599532')
        episode['webtoon'] = webtoon
        new_episode = WebtoonEpisodes.objects.create(**episode)
        new_episode.save()
        return Response("webtoon naver")


class KakaoImageView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, format=None):
        print("KakaoImageView")
        scraper = KakaoImageScraper()
        soup = scraper.get_toon_image_soup("49388862")
        images = scraper.scrap_images(soup)

        print([{'image_url': img, "order": index}
               for index,  img in enumerate(images)])

        return Response("webtoon naver")
