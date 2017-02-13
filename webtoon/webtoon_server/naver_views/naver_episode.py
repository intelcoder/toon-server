from rest_framework.views import APIView
from rest_framework.response import Response
from webtoon_server.models import Webtoon, WebtoonEpisodes
from webtoon_server.serializer import WebtoonSerializer, WebtoonEpisodeSerializer, WebtoonEpisodeListSerializer
from rest_framework.exceptions import NotFound

# /naver/22323/episode/no?page=1&sort_by=name
class NaverEpisodeView(APIView):
     def get(self, request,toon_id=None, episode_num=None):
         episode = WebtoonEpisodes.objects.filter(webtoon_id=toon_id, no=episode_num)
         if episode.exists():
             serialized_episode = WebtoonEpisodeSerializer(episode[0])
             return Response(serialized_episode.data)
         else: 
             raise NotFound('episode does not exist')

         

class NaverEpisodeList(APIView):
    def get(self, request, toon_id=None, format=None):
        episode = WebtoonEpisodes.objects.filter(webtoon_id=toon_id)
      
        if episode.exists():
             webtoon = Webtoon.objects.get(toon_id=toon_id)
             serialized_webtoon = WebtoonSerializer(webtoon)
             serialized_episodes = WebtoonEpisodeListSerializer(episode, many=True)
             data = {
                 'webtoon': serialized_webtoon.data,
                 'episodes': serialized_episodes.data
             }
             return Response(data)
        else: 
             raise NotFound('webtoon/episode does not exist')

