from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .custom.fields import SeparatedValuesField

# Create your models here.
class Journal(models.Model):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    lbs_per_week = models.FloatField()
    calorie_goal = models.IntegerField(default=2000)

class Dish(models.Model):
    dish_name = models.CharField(max_length=100, primary_key=True)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=100)
    meal_name = models.CharField(max_length=50)
    category_name = models.CharField(max_length=50)
    serving_size = models.CharField(max_length=50)
    calories = models.IntegerField()
    calories_from_fat = models.IntegerField()
    total_fat = models.FloatField()
    sat_fat = models.FloatField()
    trans_fat = models.FloatField()
    cholesterol = models.FloatField()
    sodium = models.FloatField()
    total_carb = models.FloatField()
    dietary_fiber = models.FloatField()
    sugars = models.FloatField()
    protein = models.FloatField()
    ingredient_list = SeparatedValuesField()
    allergens = SeparatedValuesField()

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    dishes = models.ManyToManyField(to=Dish, through='Journal_Dish_Intermediary')
    calorie_goal = models.IntegerField()
    calories = models.IntegerField()
    calories_from_fat = models.IntegerField()
    total_fat = models.FloatField()
    sat_fat = models.FloatField()
    trans_fat = models.FloatField()
    cholesterol = models.FloatField()
    sodium = models.FloatField()
    total_carb = models.FloatField()
    dietary_fiber = models.FloatField()
    sugars = models.FloatField()
    protein = models.FloatField()

class Journal_Dish_Intermediary(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    
    