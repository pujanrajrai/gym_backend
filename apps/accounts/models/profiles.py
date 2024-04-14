from django.db import models
from django.conf import settings
from base.models import BaseModel
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]


class StaffProfile(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_profile"
    )
    fullname = models.CharField(
        max_length=255,
        verbose_name='Full Name',
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Gender',
    )
    address = models.CharField(
        max_length=100,
    )
    photo = models.ImageField(
        upload_to="staff/photo/",
        blank=True,
        null=True
    )
    id_document = models.FileField(
        upload_to='document/staff/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.fullname}'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class UserProfile(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_profile"
    )
    fullname = models.CharField(
        max_length=255,
        verbose_name='Full Name',
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Gender',
    )
    address = models.CharField(
        max_length=100,
    )
    photo = models.ImageField(
        upload_to="staff/photo/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.fullname}'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
