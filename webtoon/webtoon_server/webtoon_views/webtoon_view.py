from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import permissions
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from ..models import Webtoon
from ..serializer import WebtoonSerializer, WebtoonFavSerizlizer
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from django.core.serializers import serialize


class WebtoonListView(ListAPIView, RetrieveUpdateAPIView):
    """
    This view returns webtoon list depends on url query
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['read']
    serializer_class = WebtoonSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('favorite',)
    search_fields = ('title',)
    ordering_fields = ('favorite', 'title', 'rating')

    def get_queryset(self, *args):
        queryset = Webtoon.objects.all()
        query = self.request.query_params.get('weekday')
        site = self.request.query_params.get('site')
        if site:
            queryset = queryset.filter(site__name=site)
        if query:
            queryset = queryset.filter(weekday=query)

        return queryset.order_by('favorite', 'title')


class WebtoonDetail(RetrieveUpdateAPIView):
    queryset = Webtoon.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = WebtoonSerializer
    lookup_field = 'toon_id'
    lookup_url_kwarg = 'toon_id'

    def get_object(self):
        queryset = self.get_queryset()
        target_value = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_404(queryset, **{self.lookup_field: target_value})
        return obj

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serialized = serializer(self.get_object())
        return Response(serialized.data)

    def put(self, request, *args, **kwargs):
        '''
        Only allow to update favorite field for now
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        webtoon = self.get_object()

        new_favorite = request.data['favorite']
        if new_favorite == True or new_favorite == False:
            webtoon.favorite = new_favorite
            webtoon.save()
            return Response(True)

        return Response(False)


class WebtoonFavorite(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        weekday = self.request.query_params.get('weekday')
        fav = Webtoon.objects.filter(
            favorite=True, weekday=weekday).only('toon_id', 'site__name')
        result = WebtoonFavSerizlizer(fav, many=True)
        return Response(result.data)

    def put(self, request):
        toon_ids = request.data.get("favorite_list")
        try:
            webtoons = Webtoon.objects.filter(toon_id__in=toon_ids)
            for webtoon in webtoons:
                webtoon.favorite = True
                webtoon.save()
            return Response(True)
        except:
            return Response(False)
