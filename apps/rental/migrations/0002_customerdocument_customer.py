# Generated by Django 4.2 on 2024-05-28 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rental", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerdocument",
            name="customer",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="rental.customer",
            ),
            preserve_default=False,
        ),
    ]
