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
def fetch_menus(request, year, month, day):
    location_map = {
        1: 'Worcester Commons',
        2: 'Franklin Dining Commons',
        3: 'Hampshire Dining Commons',
        4: 'Berkshire Dining Commons',
    }
    date = datetime.date(year, month, day)
    for location in range(1,5):
        menu = dining.get_menu(location, date)
        if menu:
            for dish in menu:
                dish['location'] = location_map[location]
                dish['date'] = date
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
    weight = request.data['profile'].pop('weight')
    request.data['profile']['starting_weight'] = weight
    request.data['profile']['weights'] = [{'weight': weight, 'date': datetime.date.today()}]
    print(request.data)
    user_serializer = UserSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    user.profile.calorie_goal = calculate_calorie_goal(user)
    user.profile.save()
    user.set_password(user.password)
    user.save()
    return Response(user_serializer.validated_data, status=status.HTTP_201_CREATED)

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

@api_view(['GET'])
def is_username_available(request, username):
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_profile(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def log_weight(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    weight = request.data['weight']
    date = request.data['date']
    request.user.profile.weights.filter(date=date).delete()
    request.user.profile.weights.create(weight=weight, date=date)
    if request.user.profile.weights.filter(date__gt=date).count() == 0:
        request.user.profile.calorie_goal = calculate_calorie_goal(request.user)
        request.user.profile.save()
    return Response(status=status.HTTP_200_OK)

katch_mcardle_multiplier = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'heavy': 1.725,
    'extreme': 1.9
}

def calculate_calorie_goal(user):
    # mifflin-st jeor formula * katch-mcardle multiplier
    weight = user.profile.weights.latest('date').weight * 0.453592
    height = user.profile.height * 2.54
    age = user.profile.age
    sex = user.profile.sex
    activity_level = user.profile.activity_level
    lbs_per_week = float(user.profile.lbs_per_week)
    bmr = 10 * weight + 6.25 * height - 5 * age
    if sex == 'male':
        bmr += 5
    else:
        bmr -= 161
    return int(float(bmr * katch_mcardle_multiplier[activity_level]) - float(500 * lbs_per_week))
    
@api_view(["POST"])
def update_goals(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    user.profile.lbs_per_week = request.data['lbs_per_week']
    user.profile.activity_level = request.data['activity_level']
    user.profile.goal_weight = request.data['goal_weight']
    user.profile.calorie_goal = calculate_calorie_goal(user)
    user.profile.save()
    return Response(status=status.HTTP_200_OK)
