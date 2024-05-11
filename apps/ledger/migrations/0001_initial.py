# Generated by Django 4.2 on 2024-05-10 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('_type', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], editable=False, max_length=100)),
                ('particular', models.CharField(editable=False, max_length=500)),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('remarks', models.CharField(max_length=1000)),
                ('entry_type', models.CharField(choices=[('Ledger Entry', 'Ledger Entry'), ('Invoice', 'Invoice'), ('Cancel Invoice', 'Cancel Invoice'), ('Other', 'Other')], editable=False, max_length=50)),
                ('leaserid', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_ledger', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
                'abstract': False,
            },
        ),
    ]
