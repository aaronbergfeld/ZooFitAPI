# Generated by Django 3.2.16 on 2023-03-13 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0012_alter_weight_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journal.profile'),
        ),
    ]
