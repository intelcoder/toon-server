from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.daum_toon_list_scraper import DaumToonListScraper
from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper
from ..models import Webtoon, WebtoonEpisodes
from ..models import Site

weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class DaumInit(APIView):
    def get(self, request):
        # update_or_create_webtoon()
        # update_toon_detail()
        get_latest_episode()
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

    toon_list_scraper.close_driver()

def update_toon_detail():
    daum_webtoons = Webtoon.objects.filter(site__name='daum').only("toon_id")
    episode_scraper = DaumEpisodeScraper()
    if daum_webtoons:
        for webtoon in daum_webtoons:
            # Somehow selenium throws illegal url error for iammother
            if not webtoon.toon_id == 'iammother':
                try:
                    episode_soup = episode_scraper.get_episode_soup(webtoon.toon_id, 1)
                    detail = episode_scraper.get_webtoon_detail(episode_soup)
                    Webtoon.objects.filter(toon_id=webtoon.toon_id).update(**detail)
                    # Once error occurs close selenium driver
                except:
                    print("error occured")
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
                print("error occured")

    episode_scraper.close_driver()


def get_latest_episode():
    daum_webtoons = Webtoon.objects.filter(site__name='daum').only("toon_id")
    episode_scraper = DaumEpisodeScraper()
    episode_soup = episode_scraper.get_episode_soup('TechUniv', 1)
    lastest_episode = episode_scraper.get_lastest_episode(episode_soup)
    new_episode = WebtoonEpisodes(**lastest_episode)
    new_episode.save()
    print(lastest_episode)


