from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer, CriticSerializer


class ReviewSerializer(serializers.ModelSerializer):    
    critic = CriticSerializer(read_only=True)
    critic_id = serializers.IntegerField(write_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        exclude = ["movie"]

        depth = 1
