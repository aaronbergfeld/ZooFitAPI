# Generated by Django 3.2.16 on 2023-04-01 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0021_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='sodium',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=8, null=True),
        ),
    ]
