# Generated by Django 3.2.16 on 2023-02-07 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0006_auto_20230130_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='calories',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
