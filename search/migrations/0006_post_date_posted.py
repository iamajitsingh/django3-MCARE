# Generated by Django 3.1.4 on 2021-05-07 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20210507_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date_posted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
