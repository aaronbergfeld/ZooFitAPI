from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .serializers import *
from umass_toolkit import dining
from django.shortcuts import get_list_or_404

# Create your views here.
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def fetch_menus(request):
    location_map = {
        1: 'Worcester Commons',
        2: 'Franklin Dining Commons',
        3: 'Hampshire Dining Commons',
        4: 'Berkshire Dining Commons',
    }
    for location in range(1,5):
        menu = dining.get_menu(1)
        if menu:
            for dish in menu:
                dish['location'] = location_map[location]
                dish['total-fat'] = dish['total-fat'].magnitude
                dish['sat-fat'] = dish['sat-fat'].magnitude
                dish['trans-fat'] = dish['trans-fat'].magnitude
                dish['cholesterol'] = dish['cholesterol'].magnitude
                dish['sodium'] = dish['sodium'].magnitude
                dish['total-carb'] = dish['total-carb'].magnitude
                dish['dietary-fiber'] = dish['dietary-fiber'].magnitude
                dish['sugars'] = dish['sugars'].magnitude
                dish['protein'] = dish['protein'].magnitude
                dish['ingredient-list'] = str(dish['ingredient-list'])
                dish['allergens'] = str(dish['allergens'])
                dish_serializer = DishSerializer(data=dish)
                if dish_serializer.is_valid():
                    dish_serializer.save()
                else:
                    return Response(dish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_menu(request, meal, location, day, month, year):
    dishes = get_list_or_404(Dish, meal_name=meal, location=location, date__year=year, date__month=month, date__day=day)
    dish_serializer = DishSerializer(dishes, many=True)
    return Response(dish_serializer.data, status=status.HTTP_200_OK)


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
