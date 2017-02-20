from rest_framework.views import APIView
from rest_framework.response import Response
from ..thumbnail.naverThumbDownloader import NaverThumbnailDownloader
from ..models import Webtoon, Site, WebtoonEpisodes
from ..webtoon_parser.naver_episode_scraper import NaverEpisodeScraper


# This function add description, author, no, which is not in thumbnail page
def add_webtoon_detail():
    webtoons = Webtoon.objects.all()
    naver_scraper = NaverEpisodeScraper()
    length = len(webtoons)
    count = 0
    for webtoon in webtoons:
        toon_id = webtoon.toon_id
        soup = naver_scraper.get_page_soup(toon_id)
        webtoon_detail = naver_scraper.get_webtoon_detail(soup)
        # update webtoon with detail info
        webtoon.description = webtoon_detail['description']
        webtoon.lastest_no = webtoon_detail['no']
        webtoon.author = webtoon_detail['author']
        webtoon.save()
        count += 1
        print('done', webtoon.title, webtoon.toon_id, count, '/', length )
    print('Adding finished!')


class NaverInit(APIView):
    def get(self, request, format=None):
        init_webtoon_list()
        add_webtoon_detail()
        return Response("webtoon naver")


class NaverInitEpisode(APIView):
    def get(self, request, format=None):
        init_webtoon_episode()
        return Response("naver episode init")

def is_webtoon_exist(toonInfo):
    is_webtoon_exist = Webtoon.objects.filter(toon_id=toonInfo['id']).exists()
    if is_webtoon_exist:
        return True
    else:
        return False


def init_webtoon_list():
    if not Site.objects.filter(name='naver').exists():
        site_naver = Site.objects.create(name='naver');
        site_naver.save()

    naver = Site.objects.get(name='naver')

    naver_downloader = NaverThumbnailDownloader()
    weekday_list = naver_downloader.get_weekday_list()

    for dayOfWeek in weekday_list:
        # get thumbnail url with webtoon basic info for day of week
        webtoons = naver_downloader.get_thumbnail(dayOfWeek)
        for webtoon in webtoons['webtoons']:
            if not is_webtoon_exist(webtoon):
                newWebtoon = Webtoon.objects.create(
                    toon_id=str(webtoon['id']),
                    title=webtoon['alt'],
                    thumbnail_url=webtoon['src'],
                    weekday=dayOfWeek,
                    rating=webtoon['rating'],
                    site=naver,
                )
                # create new webtoon info
                newWebtoon.save()
    naver_downloader.close_driver()


# get episode lists from page 1 for all webtoons
def init_webtoon_episode():
    webtoons = Webtoon.objects.filter(site__name='naver')
    naver_scraper = NaverEpisodeScraper()
    for webtoon in webtoons:
        toon_id = webtoon.toon_id

        soup = naver_scraper.get_page_soup(toon_id)
        episode_detail = naver_scraper.get_lastest_episode(soup)
        episode_detail['webtoon'] = webtoon
        WebtoonEpisodes.objects.update_or_create(**episode_detail)

        print("done", toon_id, webtoon.title)
