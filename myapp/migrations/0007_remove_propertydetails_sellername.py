# Generated by Django 3.1.3 on 2020-12-02 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_propertydetails_sellername'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertydetails',
            name='sellername',
        ),
    ]
