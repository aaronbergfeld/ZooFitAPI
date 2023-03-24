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
    sex = models.CharField(max_length=6)
    activity_level = models.CharField(max_length=50)
    starting_weight = models.IntegerField()
    goal_weight = models.IntegerField()
    weights = models.ManyToManyField('Weight', related_name='weights', blank=True, null=True)
    height = models.IntegerField()
    lbs_per_week = models.DecimalField(decimal_places=1, max_digits=3)
    calorie_goal = models.IntegerField(default=2000)

class Dish(models.Model):
    dish_name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    meal_name = models.CharField(max_length=50)
    category_name = models.CharField(max_length=50)
    serving_size = models.CharField(max_length=50)
    calories = models.IntegerField(null=True, default=0)
    calories_from_fat = models.IntegerField(null=True, default=0)
    total_fat = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    sat_fat = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    trans_fat = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    cholesterol = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    sodium = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    total_carb = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    dietary_fiber = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    sugars = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    protein = models.DecimalField(null=True, decimal_places=1, max_digits=6, default=0)
    ingredient_list = models.TextField()
    allergens = models.TextField()

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    dishes = models.ManyToManyField(to=Dish, through='Journal_Dish_Intermediary', default=None)
    calorie_goal = models.IntegerField(default=2000)
    calories = models.IntegerField(default=0)
    calories_from_fat = models.IntegerField(default=0)
    total_fat = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    sat_fat = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    trans_fat = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    cholesterol = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    sodium = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    total_carb = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    dietary_fiber = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    sugars = models.DecimalField(decimal_places=1, max_digits=6, default=0)
    protein = models.DecimalField(decimal_places=1, max_digits=6, default=0)

class Journal_Dish_Intermediary(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='journal_dish_intermediary')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class Weight(models.Model):
    date = models.DateField()
    weight = models.IntegerField()   

    class Meta:
        ordering = ['date']
    
    
    
