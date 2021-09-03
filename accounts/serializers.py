from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", 
            "password", "is_staff", "is_superuser"
        ]
                
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "is_superuser": {"default": False},
            "is_staff": {"default": True}
        }


class CriticSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
