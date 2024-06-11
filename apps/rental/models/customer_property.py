from base.models import BaseModel
from django.db import models
from rental.models import Customer, Property
from django.core.exceptions import ValidationError


class CustomerProperty(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    myproperty = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        verbose_name="Property"
    )
    electricity_unit_reading = models.FloatField(
        null=True,
        blank=True,
    )
    is_terminated = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new instance
            existing_link = CustomerProperty.objects.filter(
                myproperty=self.myproperty, is_terminated=False).first()
            if existing_link:
                raise ValidationError(
                    'This property is already linked to another customer.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} {self.myproperty.name}"
