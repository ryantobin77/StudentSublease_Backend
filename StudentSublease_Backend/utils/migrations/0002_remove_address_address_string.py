# Generated by Django 3.2.8 on 2021-12-05 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_string',
        ),
    ]
