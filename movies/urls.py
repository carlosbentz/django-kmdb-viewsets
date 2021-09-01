from django.urls import path
from .views import MovieView, MovieDetailView

urlpatterns = [
    path('movies', MovieView.as_view()),
    path('movies/<int:id>', MovieDetailView.as_view())
]
