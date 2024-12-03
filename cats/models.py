from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=63)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=63)
    salary = models.IntegerField()
