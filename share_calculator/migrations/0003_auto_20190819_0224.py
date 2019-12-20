# Generated by Django 2.2.4 on 2019-08-19 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_calculator', '0002_account_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['acquired']},
        ),
        migrations.AlterField(
            model_name='account',
            name='capital_gains',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='account',
            name='capital_losses',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='account',
            name='cash',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='position',
            name='cost_basis',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
    ]