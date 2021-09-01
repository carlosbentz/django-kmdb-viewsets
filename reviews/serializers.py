from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Review
from rest_framework.response import Response
from rest_framework import status


class ReviewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Review
        fields = ["id", "stars", "review", "spoilers"]
        
        
        extra_kwargs = {
            "id": {"read_only": True}
        }
        
        depth = 1