from django.db import models
import datetime


class WebtoonInit(models.Model):
    initialized = models.BooleanField(default=False)
    # class Meta:
    #     db_table = "webtoon_init"


class Site(models.Model):
    name = models.CharField(max_length=20)

    # class Meta:
    #     db_table = "site"

    def __str__(self):
        return self.name


# Create your models here.
class Webtoon(models.Model):
    toon_id = models.CharField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    thumbnail_url = models.URLField(null=True)
    weekday = models.CharField(max_length=10)
    lastest_no = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    uploaded_at = models.DateTimeField(default=datetime.datetime.now)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)
    favorite = models.BooleanField(default=False)
    site = models.ForeignKey(Site)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class WebtoonEpisodes(models.Model):
    episode_title = models.CharField(max_length=50)
    no = models.IntegerField()
    uploaded_at = models.DateTimeField(default=datetime.datetime.now)
    thumbnail_url = models.URLField(null=True)
    rating = models.FloatField(null=True)
    webtoon = models.ForeignKey(Webtoon)

    def __str__(self):
        return self.episode_title

    class Meta:
        get_latest_by = "uploaded_at"


class WebtoonThumbnail(models.Model):
    path = models.CharField(max_length=225)
    url = models.CharField(max_length=225)
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)


# this table will contains toon image url for each episodes
# might need image order in case that image name is random
class WebtoonEpisodeToon(models.Model):
    image_url = models.URLField()
    order = models.IntegerField()
    webtoon_episode = models.ForeignKey(WebtoonEpisodes)

