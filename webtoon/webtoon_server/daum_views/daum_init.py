from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.daum_toon_list_scraper import DaumToonListScraper
from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper
from ..models import Webtoon, WebtoonEpisodes
from ..models import Site
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions

weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class DaumInit(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        """
        This api create list of webtoon or update and update webtoon detail after
        :param request:
        :return:
        """
        update_or_create_webtoon()
        update_toon_detail()
        return Response('daum toon updated or created')

class DaumInitEpisode(APIView):
    def get(self, request):
        get_latest_episodes()
        return Response('daum toon updated or created')

def update_or_create_webtoon():
    if not Site.objects.filter(name='daum').exists():
        site_daum = Site.objects.create(name='daum')
        site_daum.save()

    daum = Site.objects.get(name='daum')
    toon_list_scraper = DaumToonListScraper()

    for weekday in weekday_list:
        toon_list_soup = toon_list_scraper.get_toonlist_soup(weekday)
        toon_list = toon_list_scraper.get_toon_list(toon_list_soup, weekday)
        for toon in toon_list:
            toon['site'] = daum
            new_webtoon = Webtoon(**toon)
            new_webtoon.save()
            print(new_webtoon.toon_id)

    toon_list_scraper.close_driver()

def update_toon_detail():
    daum_webtoons = Webtoon.objects.filter(site__name='daum').only("toon_id")
    episode_scraper = DaumEpisodeScraper()
    length = len(daum_webtoons)
    count = 0
    if daum_webtoons:
        for webtoon in daum_webtoons:
            # Somehow selenium throws illegal url error for iammother
            if not webtoon.toon_id == 'iammother':
                try:
                    episode_soup = episode_scraper.get_episode_soup(webtoon.toon_id, 1)
                    detail = episode_scraper.get_webtoon_detail(episode_soup)
                    Webtoon.objects.filter(toon_id=webtoon.toon_id).update(**detail)
                    count += 1
                    print('done', webtoon.title, webtoon.toon_id, count, '/', length)
                    # Once error occurs close selenium driver
                except:
                    print("update_toon_detail error occured")
                    episode_scraper.close_driver()
        episode_scraper.close_driver()


def update_or_get_episode_list():
    daum_webtoons = Webtoon.objects.filter(site__name='daum').only("toon_id")
    episode_scraper = DaumEpisodeScraper()

    if daum_webtoons:
        for webtoon in daum_webtoons:
            try:
                episode_soup = episode_scraper.get_episode_soup(webtoon.toon_id, 1)
                latest_episode = episode_scraper.get_lastest_episode(episode_soup)
                new_episode = WebtoonEpisodes(**latest_episode)
                new_episode['webtoon'] = webtoon
                new_episode.save()
            except:
                episode_scraper.close_driver()
                print("update_or_get_episode_list error occured")

    episode_scraper.close_driver()


def get_latest_episodes():
    """
    Get All the lastest episode for all daum webtoon
    :return:
    """
    daum_webtoons = Webtoon.objects.filter(site__name='daum', description__isnull=False).only("toon_id")
    episode_scraper = DaumEpisodeScraper()

    for webtoon in daum_webtoons:
        episode_exist = WebtoonEpisodes.objects.filter(webtoon_id=webtoon.toon_id).exists()
        if not episode_exist:
            episode_soup = episode_scraper.get_episode_soup(webtoon.toon_id, 1)
            lastest_episode = episode_scraper.get_lastest_episode(episode_soup)
            if lastest_episode and webtoon.description and webtoon.description != "":
                lastest_episode["webtoon"] = webtoon
                WebtoonEpisodes.objects.update_or_create(**lastest_episode)
            # print(lastest_episode)
        # try:
        #
        # except:
        #     print("error occured")
        #     episode_scraper.close_driver()


