from base.models import BaseModel
from django.db import models


class Customer(BaseModel):
    name = models.CharField(
        max_length=100
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True
    )
    secondary_phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class CustomerDocument(BaseModel):
    name = models.CharField(
        max_length=100
    )
    file = models.FileField(
        upload_to='customer/document/',
    )

    def __str__(self):
        return self.name
