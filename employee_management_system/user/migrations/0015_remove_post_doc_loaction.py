# Generated by Django 5.0.6 on 2024-08-15 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_postdoc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='doc_loaction',
        ),
    ]
