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



class WebtoonEpisodeToon(serializers.ModelSerializer):
    class Meta:
        model = WebtoonEpisodeToon
        fields = (
            'image_url',
            'order',
            'webtoon_episode'
        )
