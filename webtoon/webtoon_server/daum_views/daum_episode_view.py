from rest_framework.views import APIView
from rest_framework.response import Response

from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper

class DaumEpisodeView(APIView):

    def get(self, request):
        return Response('test')