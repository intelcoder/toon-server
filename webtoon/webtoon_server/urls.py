from django.conf.urls import url

from .naver_views.naver_episode import NaverEpisodeView, NaverEpisodeList
from .naver_views.naver_init import NaverInit, NaverInitEpisode
from .naver_views.naver_toon_list import NaverToonList
from .naver_views.naver_toon_view import NaverToonView

from .daum_views.daum_toon_list_view import DaumToonListView
from .daum_views.daum_episode_view import DaumEpisodeView
from .daum_views.daum_init import DaumInit, DaumInitEpisode

urlpatterns = [

    url(r'^naver$', NaverToonList.as_view()),
    url(r'^naver/init$', NaverInit.as_view()),
    url(r'^naver/init/episode$', NaverInitEpisode.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode$', NaverEpisodeList.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)$', NaverEpisodeView.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)/toon', NaverToonView.as_view()),

    # Daum
    url(r'^daum$', DaumToonListView.as_view()),
    url(r'^daum/init$', DaumInit.as_view()),
    url(r'^daum/init/episode$', DaumInitEpisode.as_view()),
    url(r'^daum/(?P<toon_id>[a-zA-Z]+)/episode$', DaumEpisodeView.as_view()),
    # url(r'^daum/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)', NaverEpisodeView.as_view()),
    # url(r'^daum/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)/toon', NaverToonView.as_view()),

]
