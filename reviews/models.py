from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    stars = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
