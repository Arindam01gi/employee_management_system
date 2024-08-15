# Generated by Django 5.0.6 on 2024-08-15 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_post_options_alter_post_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostDoc',
            fields=[
                ('post_doc_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('post_doc_name', models.CharField(max_length=256, null=True)),
                ('post_doc_path', models.CharField(max_length=256, null=True)),
                ('doc_type', models.CharField(max_length=50, null=True)),
                ('created_on', models.DateTimeField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='user.post')),
            ],
            options={
                'db_table': 'post_doc',
                'managed': True,
            },
        ),
    ]