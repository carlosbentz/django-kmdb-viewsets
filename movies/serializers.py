from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Movie
        fields = '__all__' # Todos os campos da model
        
        extra_kwargs = {
            "id": {"read_only": True},
        }


class MovieSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer()
    customer_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__' # Todos os campos da model
        # fields = ['documentNumber', 'balance']
        
        
        extra_kwargs = {
            "id": {"read_only": True},
        }
        
        depth = 1