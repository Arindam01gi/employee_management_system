# Generated by Django 5.0.6 on 2024-07-31 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='post',
            table='post',
        ),
    ]
