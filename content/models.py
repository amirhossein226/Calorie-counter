from django.db import models
from content.constants import MEAL_CATEGORY
from accounts.models import Profile, User

# Create your models here.


class Article(models.Model):
    headline = models.CharField(max_length=200)
    short_description = models.CharField(max_length=250, default=" ")
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.headline} by ({self.author})"


class NutritionalValue(models.Model):
    name = models.CharField(unique=True, max_length=255)

    calorie = models.PositiveIntegerField()
    protein = models.PositiveIntegerField()
    carbs = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class FoodEaten(models.Model):
    name = models.ForeignKey(
        NutritionalValue, on_delete=models.CASCADE, related_name="food")
    amount_of_food_eaten = models.PositiveIntegerField(blank=False, null=False)

    def total_calorie(self):
        return self.amount_of_food_eaten * self.name.calorie

    def __str__(self):
        return f"{self.name} ({self.total_calorie()})"


class Meal(models.Model):
    person_name = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="meals")
    category = models.IntegerField(choices=MEAL_CATEGORY)
    foods = models.ManyToManyField(FoodEaten, related_name="meals")

    def __str__(self):
        return f"{self.person_name.name} for {self.category} ate the {self.foods}"
