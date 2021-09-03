from django.urls import path
from .views import ReviewView, ReviewDetailView

urlpatterns = [
    path('reviews/', ReviewView.as_view()),
    path('movies/<int:movie_id>/review/', ReviewDetailView.as_view())
]
