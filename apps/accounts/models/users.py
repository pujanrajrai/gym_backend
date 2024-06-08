from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        # email,
        phone_number,
        password=None,
        role='user',
        is_blocked=False,
        **extra_fields
    ):
        user = self.model(
            # email=email,
            phone_number=phone_number,
            role=role,
            is_blocked=is_blocked,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        # email,
        phone_number,
        password=None,
        role='admin',
        is_blocked=False,
        **extra_fields
    ):
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, role, is_blocked, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'admin'),
            ('staff', 'staff'),
            ('user', 'user'),
            ('company', 'company')
        ],
        default='user'
    )
    is_blocked = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_rental_user = models.BooleanField(
        default=False,
        blank=True,
        null=True
    )
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        role = self.role
        if role == "user":
            return f"{self.user_profile.fullname} {self.phone_number}"
        elif role == "staff":
            return f"{self.staff_profile.fullname} {self.phone_number} "
        else:
            return f"{self.phone_number}"
