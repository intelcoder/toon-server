from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.naver_toon_image_scraper import NaverToonImageScraper
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from ..models import WebtoonEpisodes, WebtoonEpisodeToon
from ..serializer import WebtoonEpisodeToonSerializer


class WebtoonToonImageView(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, toon_id=None, episode_num=None):
        # If it is save in db get it from db otherwise use scraper
        toons = WebtoonEpisodeToon.objects.filter(webtoon_episode__no=episode_num)


        if toons.exists():
            serialized = WebtoonEpisodeToonSerializer(toons, many=True)
            return Response(serialized.data)
        else:
            bulk_toon = []
            toon_list = scrape_toon_list(toon_id, episode_num)
            episode = WebtoonEpisodes.objects.filter(webtoon__toon_id=toon_id, no=episode_num).first()

            for index, url in enumerate(toon_list):
                new_toon = create_toon(episode, index, url)
                bulk_toon.append(new_toon)

            WebtoonEpisodeToon.objects.bulk_create(bulk_toon)
            serialized = WebtoonEpisodeToonSerializer(bulk_toon, many=True)
            return Response(serialized.data)


def scrape_toon_list(toon_id, episode_num):
    toon_scraper = NaverToonImageScraper()
    soup = toon_scraper.get_toon_image_soup(toon_id, episode_num)

    return toon_scraper.scrap_images(soup)


def create_toon(episode, order, url):
    new_toon = WebtoonEpisodeToon()
    new_toon.order = order
    new_toon.image_url = url
    new_toon.webtoon_episode = episode
    return new_toon
