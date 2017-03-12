from rest_framework.generics import ListAPIView
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from ..models import Webtoon
from ..serializer import WebtoonSerializer

weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class DaumToonListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = WebtoonSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title',)
    ordering_fields = ('title', 'rating')

    def get_queryset(self, *args):
        queryset = Webtoon.objects.filter(site__name='daum')
        query = self.request.query_params.get('weekday')
        if query:
            queryset = queryset.filter(weekday=query)
        return queryset
