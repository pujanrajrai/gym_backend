# In your app's models.py file

from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    default_month = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
