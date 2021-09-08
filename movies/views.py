from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView, DestroyAPIView
from .serializers import MovieSerializer, MovieReviewSerializer
from .models import Movie
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsAdmin, IsCritic
from rest_framework import viewsets


class MovieModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "id"


    def get_queryset(self):
        title = self.request.data.get("title")
        if title:
            self.queryset = self.queryset.filter(title__icontains=title)

        return super().get_queryset()


    def get_serializer_class(self):
        if self.request.method == "GET" and self.request.user.is_authenticated:
            return MovieReviewSerializer
        
        return MovieSerializer
