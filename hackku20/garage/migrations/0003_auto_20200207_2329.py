# Generated by Django 3.0.3 on 2020-02-08 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0002_auto_20200207_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garagepass',
            name='passID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
