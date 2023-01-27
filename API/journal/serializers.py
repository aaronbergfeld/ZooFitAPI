from django.contrib.auth.models import User
from .models import Dish, Profile
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

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'id'
            'location',
            'dish-name',
            'date',
            'location',
            'meal-name',
            'category-name',
            'serving-size',
            'calories',
            'calories-from-fat',
            'total-fat',
            'sat-fat',
            'trans-fat',
            'cholesterol',
            'sodium',
            'total-carb',
            'dietary-fiber',
            'sugars',
            'protein',
            'ingredient-list',
            'allergens',
        ]
        extra_kwargs = {
            'dish-name': {'source': 'dish_name'},
            'meal-name': {'source': 'meal_name'},
            'category-name': {'source': 'category_name'},
            'serving-size': {'source': 'serving_size'},
            'calories-from-fat': {'source': 'calories_from_fat'},
            'total-fat': {'source': 'total_fat'},
            'sat-fat': {'source': 'sat_fat'},
            'trans-fat': {'source': 'trans_fat'},
            'total-carb': {'source': 'total_carb'},
            'dietary-fiber': {'source': 'dietary_fiber'},
            'ingredient-list': {'source': 'ingredient_list'},
        }
        