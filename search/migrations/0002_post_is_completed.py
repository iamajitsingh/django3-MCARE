# Generated by Django 3.1.4 on 2021-05-07 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
