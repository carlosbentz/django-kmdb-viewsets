from rest_framework import serializers
from .models import Movie, Genre
from reviews.serializers import ReviewSerializer


class GenreSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Genre
        fields = "__all__" # Todos os campos da model
        
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"validators": []}
        }


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    
    class Meta:
        model = Movie
        fields = "__all__"
        
        extra_kwargs = {
            "id": {"read_only": True},
            "title": {"validators": []}
        }
        
        depth = 1


    def create(self, validated_data):
        genre_list = validated_data.pop("genres")

        movie_instance = Movie.objects.filter(title=validated_data["title"])

        if Movie.objects.filter(title=validated_data["title"]).exists():
            return movie_instance[0]
 
        movie_instance = super().create(validated_data)

        for genre in genre_list:

            genre = Genre.objects.get_or_create(**genre)[0]

            movie_instance.genres.add(genre.id)

        return movie_instance


class MovieReviewSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = "__all__"
        
        depth = 1
