from rest_framework import permissions, status

from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework.exceptions import NotFound
from ..models import Webtoon, WebtoonEpisodes
from ..serializer import WebtoonEpisodeListSerializer, WebtoonSerializer


class WebtoonEpisodeList(APIView):
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope)

    def get(self, request, toon_id=None):

        episode = WebtoonEpisodes.objects.filter(
            webtoon_id=toon_id).order_by('-no', '-uploaded_at')

        if episode.exists():
            webtoon = Webtoon.objects.get(toon_id=toon_id)
            serialized_webtoon = WebtoonSerializer(webtoon)
            serialized_episodes = WebtoonEpisodeListSerializer(
                episode, many=True)
            data = {
                'webtoon': serialized_webtoon.data,
                'episodes': serialized_episodes.data
            }
            return Response(data)
        else:
            content = {'webtoon/episode does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
