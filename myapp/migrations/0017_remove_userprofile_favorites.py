# Generated by Django 3.1.3 on 2020-12-07 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_auto_20201207_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='favorites',
        ),
    ]
