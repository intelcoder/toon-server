from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import WebtoonEpisodes
from ..serializer import WebtoonEpisodeSerializer
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from ..webtoon_parser.daum_episode_scraper import DaumEpisodeScraper


class DaumEpisodeView(APIView):
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)
    def get(self, request, toon_id=None):
        webtoons = WebtoonEpisodes.objects.all()
        serialized_data = WebtoonEpisodeSerializer(webtoons).data
        return Response(serialized_data)