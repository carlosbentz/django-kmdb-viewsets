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


        
    # def create(self, validated_data):
    #     # ipdb.set_trace()
    #     get_object_or_404(Customer, id=validated_data["customer_id"])
    #     # if not Customer.objects.filter(id=validated_data["customer_id"]).exists():
    #         # raise Exception
            
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
