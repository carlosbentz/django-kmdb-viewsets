from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from .serializers import MovieSerializer, MovieReviewSerializer
from .models import Movie, Genre
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsAdmin, IsCritic

class MovieView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
 
    def get(self, request, *args, **kwargs):
        title = request.data.get("title")
        if title:
            self.queryset = self.queryset.filter(title__icontains=title)

        return self.list(request, *args, **kwargs)


class MovieDetailView(RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]


    queryset = Movie.objects.all()
    
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.user.is_authenticated:
            return MovieReviewSerializer
        
        return MovieSerializer