# Generated by Django 2.2.4 on 2019-08-23 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share_calculator', '0009_position_is_shortterm'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='net_capital_gains_after_sale',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='sale',
            name='target',
            field=models.DecimalField(decimal_places=2, default=1000000.0, max_digits=14),
        ),
    ]