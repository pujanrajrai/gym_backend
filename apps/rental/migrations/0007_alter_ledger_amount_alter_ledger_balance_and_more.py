# Generated by Django 4.2 on 2024-06-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rental", "0006_alter_unconfirminvoice_remarks_ledger"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ledger",
            name="amount",
            field=models.FloatField(editable=False),
        ),
        migrations.AlterField(
            model_name="ledger",
            name="balance",
            field=models.FloatField(editable=False),
        ),
        migrations.AlterField(
            model_name="ledger",
            name="company_balance",
            field=models.FloatField(editable=False),
        ),
    ]
