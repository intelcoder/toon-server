from rest_framework.generics import ListAPIView
from rest_framework import permissions
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
