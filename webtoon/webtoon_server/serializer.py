from rest_framework import serializers
from webtoon_server.models import Webtoon, Site, WebtoonEpisodeToon, WebtoonEpisodes


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'id',
            'name'
        )


class WebtoonSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = Webtoon
        fields = (
            'toon_id',
            'title',
            'weekday',
            'rating',
            'description',
            'author',
            'thumbnail_url',
            'lastest_no',
            'created_at',
            'updated_at',
            'favorite',
            'site'
        )


class SimpleSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['name']


class WebtoonFavSerizlizer(serializers.ModelSerializer):
    site = serializers.CharField(source='site.name', read_only=True)

    class Meta:
        model = Webtoon
        fields = (
            'toon_id',
            'site'
        )


class WebtoonEpisodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebtoonEpisodes
        fields = (
            'episode_title',
            'no',
            'uploaded_at',
            'thumbnail_url',
            'rating',
        )


class WebtoonEpisodeSerializer(WebtoonEpisodeListSerializer):
    webtoon = WebtoonSerializer(read_only=True)

    class Meta:
        model = WebtoonEpisodes
        fields = '__all__'


class WebtoonEpisodeToonSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebtoonEpisodeToon
        fields = (
            'image_url',
            'order',
        )
