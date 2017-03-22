from rest_framework.views import APIView
from rest_framework.response import Response
from ..webtoon_parser.naver_toon_image_scraper import NaverToonImageScraper


class WebtoonToonImageView(APIView):
    def get(self, request, toon_id=None, episode_num=None):
        # if webtoon marked as favorite save it into db

        toon_scraper = NaverToonImageScraper()
        soup = toon_scraper.get_toon_image_soup(toon_id, episode_num)
        toon_img_list = toon_scraper.scrap_images(soup)
        data = {
            'image_list': toon_img_list,
            'length': len(toon_img_list)
        }
        return Response(data)
