from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from ..models import Webtoon
from ..serializer import WebtoonSerializer
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)


class NaverToonList(ListAPIView):
    """
    This view returns webtoon list depends on url query
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['read']
    serializer_class = WebtoonSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title',)
    ordering_fields = ('title', 'rating')

    def get_queryset(self, *args):
        queryset = Webtoon.objects.filter(site__name="naver")
        query = self.request.query_params.get('weekday')
        if query:
            queryset = queryset.filter(weekday=query)
        return queryset


class NaverListDetail(RetrieveUpdateAPIView):
    queryset = Webtoon.objects.filter(site__name='naver')
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = WebtoonSerializer
    lookup_field = 'toon_id'
    lookup_url_kwarg = 'toon_id'

    def get_object(self):
        queryset = self.get_queryset()
        target_value = self.kwargs[self.lookup_field]
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
