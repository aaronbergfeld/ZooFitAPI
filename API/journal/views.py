from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .models import *
from umass_toolkit import dining
from django.shortcuts import get_list_or_404
import datetime

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
        menu = dining.get_menu(location)
        if menu:
            for dish in menu:
                dish['location'] = location_map[location]
                if dish['total-fat'] is not None:
                    dish['total-fat'] = dish['total-fat'].magnitude
                if dish['sat-fat'] is not None:
                    dish['sat-fat'] = dish['sat-fat'].magnitude
                if dish['trans-fat'] is not None:
                    dish['trans-fat'] = dish['trans-fat'].magnitude
                if dish['cholesterol'] is not None:
                    dish['cholesterol'] = dish['cholesterol'].magnitude
                if dish['sodium'] is not None:
                    dish['sodium'] = dish['sodium'].magnitude
                if dish['total-carb'] is not None:
                    dish['total-carb'] = dish['total-carb'].magnitude
                if dish['dietary-fiber'] is not None:
                    dish['dietary-fiber'] = dish['dietary-fiber'].magnitude
                if dish['sugars'] is not None:
                    dish['sugars'] = dish['sugars'].magnitude
                if dish['protein'] is not None:
                    dish['protein'] = dish['protein'].magnitude
                if dish['ingredient-list'] is not None:
                    dish['ingredient-list'] = str(dish['ingredient-list'])
                if dish['allergens'] is not None:
                    dish['allergens'] = str(dish['allergens'])
                if dish['serving-size'] is not None:
                    dish['serving-size'] = dish['serving-size'].lower()
                dish_serializer = DishSerializer(data=dish)
                if dish_serializer.is_valid():
                    dish_serializer.save()
                else:
                    return Response(dish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_menu(request, meal, location, year, month, day):
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

@api_view(['POST', 'GET', 'DELETE'])
def journal(request, year, month, day):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        date = datetime.date(year, month, day)
        journal = Journal.objects.get(user=request.user, date=date)
        for id in request.data:
            dish = Dish.objects.get(id=id)
            jdi, created = Journal_Dish_Intermediary.objects.get_or_create(journal=journal, dish=dish) 
            quantity = request.data[id]
            jdi.quantity += quantity
            jdi.save()
            journal.calories += dish.calories * quantity
            journal.calories_from_fat += dish.calories_from_fat * quantity
            journal.total_fat += dish.total_fat * quantity
            journal.sat_fat += dish.sat_fat * quantity
            journal.trans_fat += dish.trans_fat * quantity
            journal.cholesterol += dish.cholesterol * quantity
            journal.sodium += dish.sodium * quantity
            journal.total_carb += dish.total_carb * quantity
            journal.dietary_fiber += dish.dietary_fiber * quantity
            journal.sugars += dish.sugars * quantity
            journal.protein += dish.protein * quantity
            journal.save() 
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'GET':
        date = datetime.date(year, month, day)
        journal, created = Journal.objects.get_or_create(user=request.user, date=date)
        journal_serializer = JournalSerializer(journal)
        return Response(journal_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        date = datetime.date(year, month, day)
        journal = Journal.objects.get(user=request.user, date=date)
        id = request.data['id']
        dish = Dish.objects.get(id=id)
        jdi = Journal_Dish_Intermediary.objects.get(journal=journal, dish=dish)
        quantity = 1
        jdi.quantity -= 1
        if jdi.quantity == 0:
            jdi.delete()
        else:
            jdi.save()
        journal.calories -= dish.calories * quantity
        journal.calories_from_fat -= dish.calories_from_fat * quantity
        journal.total_fat -= dish.total_fat * quantity
        journal.sat_fat -= dish.sat_fat * quantity
        journal.trans_fat -= dish.trans_fat * quantity
        journal.cholesterol -= dish.cholesterol * quantity
        journal.sodium -= dish.sodium * quantity
        journal.total_carb -= dish.total_carb * quantity
        journal.dietary_fiber -= dish.dietary_fiber * quantity
        journal.sugars -= dish.sugars * quantity
        journal.protein -= dish.protein * quantity
        journal.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)