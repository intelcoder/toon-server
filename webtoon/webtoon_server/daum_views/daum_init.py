from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.daum_toon_list_scraper import DaumToonListScraper
from ..models import Webtoon
from ..models import Site

weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class DaumInit(APIView):
    def get(self, request):
        update_or_create_webtoon()
        return Response('daum toon updated or created')


def update_or_create_webtoon():
    if not Site.objects.filter(name='daum').exists():
        site_daum = Site.objects.create(name='daum')
        site_daum.save()

    daum = Site.objects.get(name='daum')
    toon_list_scraper = DaumToonListScraper()
    try:
        for weekday in weekday_list:
            toon_list_soup = toon_list_scraper.get_toonlist_soup(weekday)
            toon_list = toon_list_scraper.get_toon_list(toon_list_soup, weekday)
            for toon in toon_list:
                toon['site'] = daum
                new_webtoon = Webtoon(**toon)
                new_webtoon.save()
                print(new_webtoon.title)
    except:
        toon_list_scraper.close_driver()

def update_toon_detail():
    pass
