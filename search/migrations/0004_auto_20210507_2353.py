# Generated by Django 3.1.4 on 2021-05-07 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20210507_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contact_phone',
            field=models.PositiveBigIntegerField(blank=True, default=8),
        ),
    ]
