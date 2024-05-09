# Generated by Django 4.2 on 2024-05-07 07:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_staffprofile'),
        ('plan', '0002_userplan_userplandetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnConfirmUserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('starting_date', models.DateField()),
                ('end_date', models.DateField()),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'ordering': ['-created_date'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='userplan',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterModelOptions(
            name='userplandetail',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='userplan',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userplan',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userplan',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userplan',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userplandetail',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userplandetail',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userplandetail',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userplandetail',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='UnConfirmUserPlanDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('userplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.unconfirmuserplan')),
            ],
            options={
                'ordering': ['-created_date'],
                'abstract': False,
            },
        ),
    ]
