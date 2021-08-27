from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    duration = models.CharField(max_length=50)
    premiere = models.CharField(max_length=50)
    classification = models.IntegerField()
    synopsis = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="movies")
