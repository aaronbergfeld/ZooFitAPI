# Generated by Django 3.2.16 on 2023-03-13 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0010_auto_20230313_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='profile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='journal.profile'),
        ),
    ]
