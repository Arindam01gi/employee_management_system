# Generated by Django 5.0.6 on 2024-06-10 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_joining_data_userdetails_joining_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='designation',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
