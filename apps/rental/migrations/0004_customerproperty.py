# Generated by Django 4.2 on 2024-05-30 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rental", "0003_customer_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerProperty",
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
                ("is_terminated", models.BooleanField(default=False)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rental.customer",
                    ),
                ),
                (
                    "myproperty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rental.property",
                        verbose_name="Property",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_date"],
                "abstract": False,
            },
        ),
    ]
