from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import *

# Create your views here.

@api_view(['POST'])
@csrf_exempt
def create_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(user.password)
        user.save()
        return Response(user_serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)