# Generated by Django 5.0.6 on 2024-05-31 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userdetails_active_userdetails_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='joining_data',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='salary',
            field=models.BigIntegerField(null=True),
        ),
    ]
