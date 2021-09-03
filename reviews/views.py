from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .serializers import ReviewSerializer
from .models import Review
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsCritic
from movies.models import Movie
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class ReviewView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin | IsCritic]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        if not (self.request.user.is_staff and self.request.user.is_superuser):
            self.queryset = self.queryset.filter(critic_id=self.request.user.id)
        
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            raise PermissionDenied

        return super().get_queryset()


class ReviewDetailView(CreateModelMixin, 
    UpdateModelMixin, GenericAPIView
    ):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCritic]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # lookup_field = "movie_id" -- Foi reescrevido o método get_object, 
    # então, não é mais necessário.

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            "critic_id": self.request.user.id,
            "movie_id": self.kwargs["movie_id"],
        }

        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


    def post(self, request, *args, **kwargs):
        request.data["critic_id"] = request.user.id
        request.data["movie_id"] = kwargs["movie_id"]

        if request.user.reviews.exists():
            return Response(
                {"detail": "You already made this review."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

        get_object_or_404(Movie, id=request.data["movie_id"])

        return self.create(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        request.data["critic_id"] = request.user.id
        request.data["movie_id"] = kwargs["movie_id"]

        return self.update(request, *args, **kwargs)
