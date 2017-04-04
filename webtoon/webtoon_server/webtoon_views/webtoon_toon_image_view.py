from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.naver_toon_image_scraper import NaverToonImageScraper
from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from ..models import WebtoonEpisodes, WebtoonEpisodeToon, Webtoon
from ..serializer import WebtoonEpisodeToonSerializer
from ..webtoon_parser.daum_toon_image_scraper import DaumToonImageScraper
from rest_framework import status


class WebtoonToonImageView(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, toon_id=None, episode_num=None):
        # If it is save in db get it from db otherwise use scraper
        episode = WebtoonEpisodes.objects.filter(webtoon__toon_id=toon_id, no=episode_num).first()

        if not episode:
            return Response({"message": "Webtoon or Episode Not Foundd"}, status=status.HTTP_404_NOT_FOUND)

        toons = WebtoonEpisodeToon.objects.filter(webtoon_episode__webtoon__toon_id=toon_id,
                                                  webtoon_episode__no=episode_num)

        if toons.exists():
            serialized = WebtoonEpisodeToonSerializer(toons, many=True)
            return Response(serialized.data)
        else:
            bulk_toon = []
            site = episode.webtoon.site.name
            episode = WebtoonEpisodes.objects.filter(webtoon__toon_id=toon_id, no=episode_num).first()
            toon_list = scrape_toon_list(toon_id, episode_num, site)

            for index, url in enumerate(toon_list):
                new_toon = create_toon(episode, index, url)
                bulk_toon.append(new_toon)

            WebtoonEpisodeToon.objects.bulk_create(bulk_toon)
            serialized = WebtoonEpisodeToonSerializer(bulk_toon, many=True)
            return Response(serialized.data)

def scrape_toon_list(toon_id, episode_num, site):
    toon_scraper = NaverToonImageScraper() if site == 'naver' else DaumToonImageScraper()
    soup = toon_scraper.get_toon_image_soup(toon_id, episode_num)
    return toon_scraper.scrap_images(soup)


def create_toon(episode, order, url):
    new_toon = WebtoonEpisodeToon()
    new_toon.order = order
    new_toon.image_url = url
    new_toon.webtoon_episode = episode
    return new_toon


def get_toon_image_scraper(site):
    if site == 'naver':
        return NaverToonImageScraper()
    elif site == 'daum':
        return NaverToonImageScraper()
