from base.models import BaseModel
from django.db import models


class Property(models.Model):
    name = models.CharField(
        max_length=100
    )
    address = models.CharField(
        max_length=100
    )
    price_per_month = models.FloatField()
    garbage_cost_per_month = models.FloatField()
    electricity_per_unit_price = models.FloatField()
    water_per_unit_price = models.FloatField()

    def __str__(self):
        return self.name
