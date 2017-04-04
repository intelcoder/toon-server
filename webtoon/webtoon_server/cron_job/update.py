from django_cron import CronJobBase, Schedule
from ..models import Webtoon
from ..webtoon_parser.naver_episode_scraper import NaverEpisodeScraper
from ..webtoon_parser.naver_toon_image_scraper import NaverToonImageScraper
from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper
from ..webtoon_views.webtoon_toon_image_view import bulk_toon_list
from ..models import WebtoonEpisodes, WebtoonEpisodeToon
from django.db import Error


class EpisodeToonUpdate(CronJobBase):
    RUN_AT_TIMES = ['10:10', '17:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'webtoon.test'

    def do(self):
        favorites = Webtoon.objects.filter(favorite=True)
        if favorites.exists():
            for webtoon in favorites:
                if webtoon.site.name == 'naver':
                    scraper = get_episode_scraper(webtoon.site.name)
                    soup = scraper.get_page_soup(webtoon.toon_id)
                    lastest = scraper.get_lastest_episode(soup)
                    lastest['webtoon'] = webtoon
                    try:
                        result, _ = WebtoonEpisodes.objects.update_or_create(**lastest)
                        toon_list = bulk_toon_list(webtoon.toon_id, result.no)
                        WebtoonEpisodeToon.objects.bulk_create(toon_list)
                    except Error:
                        # @todo use Logger to save error
                        print(Error)


def get_episode_scraper(site):
    if site == 'naver':
        return NaverEpisodeScraper()
    elif site == 'daum':
        return DaumEpisodeScraper()
