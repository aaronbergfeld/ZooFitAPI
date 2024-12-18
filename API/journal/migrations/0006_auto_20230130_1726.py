# Generated by Django 3.2.16 on 2023-01-30 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_alter_journal_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='calories_from_fat',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='cholesterol',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='dietary_fiber',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='protein',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='sat_fat',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='sodium',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='sugars',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='total_carb',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='total_fat',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='trans_fat',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=6, null=True),
        ),
    ]
