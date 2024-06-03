
from base.models import BaseModel
from django.db import models
from rental.models import Customer, Property
from django.utils import timezone
from django.core.exceptions import ValidationError


class UnconfirmInvoice(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )
    myproperty = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        verbose_name="property"
    )
    month_name = models.CharField(
        max_length=100,
    )
    property_rent = models.FloatField()
    total_electricity_unit = models.FloatField()
    total_electricity_amount = models.FloatField()
    total_water_unit = models.FloatField()
    total_water_amount = models.FloatField()
    total_garbage_amount = models.FloatField()
    miscellaneous_amount = models.FloatField()
    total_price = models.FloatField()
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = (self.property_rent +
                            self.total_electricity_amount +
                            self.total_water_amount +
                            self.total_garbage_amount +
                            self.miscellaneous_amount)
        super(UnconfirmInvoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} {self.myproperty.name}"


class Invoice(BaseModel):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )
    myproperty = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        verbose_name="property"
    )
    month_name = models.CharField(
        max_length=100,
    )
    property_rent = models.FloatField()
    total_electricity_unit = models.FloatField()
    total_electricity_amount = models.FloatField()
    total_water_unit = models.FloatField()
    total_water_amount = models.FloatField()
    total_garbage_amount = models.FloatField()
    miscellaneous_amount = models.FloatField()
    total_price = models.FloatField()
    remarks = models.TextField()
    is_cancelled = models.FloatField()

    def save(self, *args, **kwargs):
        if self.pk:  # Check if it's an update
            old_invoice = Invoice.objects.get(pk=self.pk)
            if not old_invoice.is_cancelled and self.is_cancelled:
                if not self.can_be_cancelled():
                    raise ValidationError(
                        "Invoice can only be cancelled within 24 hours of creation.")
            elif old_invoice.is_cancelled and self.is_cancelled:
                raise ValidationError("Invoice is already cancelled.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} {self.myproperty.name}"

    def can_be_cancelled(self):
        # 24 hours in seconds
        return (timezone.now() - self.created_date).total_seconds() <= 86400
