# Generated by Django 3.2.16 on 2023-03-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0020_auto_20230314_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(max_length=6),
        ),
    ]
