# Generated by Django 3.2.16 on 2023-03-14 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0016_alter_profile_weights'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weight',
            name='profile',
        ),
    ]
