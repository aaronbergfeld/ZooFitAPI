from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

class ProfileSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Profile
        fields = ['age', 'weight', 'height', 'lbs_per_week', 'calorie_goal']

class UserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'groups', 'profile')