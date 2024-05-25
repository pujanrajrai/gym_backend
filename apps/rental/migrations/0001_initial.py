# Generated by Django 4.2 on 2024-05-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("is_hidden", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                (
                    "secondary_phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["-created_date"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomerDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("is_hidden", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                ("file", models.FileField(upload_to="customer/document/")),
            ],
            options={
                "ordering": ["-created_date"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=100)),
                ("price_per_month", models.FloatField()),
                ("garbage_cost_per_month", models.FloatField()),
                ("electricity_per_unit_price", models.FloatField()),
                ("water_per_unit_price", models.FloatField()),
            ],
        ),
    ]
