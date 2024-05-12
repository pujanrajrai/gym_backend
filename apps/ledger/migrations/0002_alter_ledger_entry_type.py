# Generated by Django 4.2 on 2024-05-12 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='entry_type',
            field=models.CharField(choices=[('Ledger Entry', 'Ledger Entry'), ('Invoice', 'Invoice'), ('Cancel Invoice', 'Cancel Invoice'), ('Salary', 'Salary'), ('Other', 'Other')], editable=False, max_length=50),
        ),
    ]
