# Generated by Django 4.2 on 2024-05-20 08:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ledger", "0002_alter_ledger_entry_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="ledger",
            name="expenses_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
