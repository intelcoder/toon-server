from django.conf.urls import url


from .naver_views.naver_episode import NaverEpisodeView, NaverEpisodeList
from .naver_views.naver_init import NaverInit, NaverInitEpisode
from .naver_views.naver_toon_list import NaverToonList, NaverListDetail
from .naver_views.naver_toon_view import NaverToonView

from .daum_views.daum_toon_list_view import DaumToonListView
from .daum_views.daum_episode_view import DaumEpisodeView
from .daum_views.daum_init import DaumInit, DaumInitEpisode

from .kakao_views.kakao_init import KakaoInitView, KakaoEpisodeView, KakaoImageView

from .webtoon_views.webtoon_episode_view import WebtoonEpisodeList
from .webtoon_views.webtoon_view import WebtoonListView, WebtoonDetail, WebtoonFavorite
from .webtoon_views.webtoon_toon_image_view import WebtoonToonImageView


urlpatterns = [
    url(r'^$', WebtoonListView.as_view()),
    url(r'^favorite$', WebtoonFavorite.as_view()),
    url(r'^(?P<toon_id>[0-9a-zA-Z]+)/$', WebtoonDetail.as_view()),
    url(r'^^(?P<toon_id>[0-9a-zA-Z]+)/episode/$',
        WebtoonEpisodeList.as_view()),
    url(r'^^(?P<toon_id>[0-9a-zA-Z]+)/episode/(?P<episode_num>[0-9]+)/$',
        WebtoonEpisodeList.as_view()),
    url(r'^^(?P<toon_id>[0-9a-zA-Z]+)/episode/(?P<episode_num>[0-9]+)/toon/$',
        WebtoonToonImageView.as_view()),

    url(r'^naver$', NaverToonList.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)$', NaverListDetail.as_view()),
    url(r'^naver/init$', NaverInit.as_view()),
    url(r'^naver/init/episode$', NaverInitEpisode.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode$', NaverEpisodeList.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)$',
        NaverEpisodeView.as_view()),
    url(r'^naver/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)/toon',
        NaverToonView.as_view()),

    # Daum
    url(r'^daum$', DaumToonListView.as_view()),
    url(r'^daum/init$', DaumInit.as_view()),
    url(r'^daum/init/episode$', DaumInitEpisode.as_view()),
    url(r'^daum/(?P<toon_id>[a-zA-Z]+)/episode$', DaumEpisodeView.as_view()),
    # url(r'^daum/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)', NaverEpisodeView.as_view()),
    # url(r'^daum/(?P<toon_id>[0-9]+)/episode/(?P<episode_num>[0-9]+)/toon', NaverToonView.as_view()),
    url(r'^kakao$', KakaoInitView.as_view()),
    url(r'^kakao/episode$', KakaoEpisodeView.as_view()),
    url(r'^kakao/images$', KakaoImageView.as_view()),

]
