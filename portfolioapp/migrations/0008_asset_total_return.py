# Generated by Django 4.0.3 on 2022-03-16 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioapp', '0007_asset_net_return'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='total_return',
            field=models.FloatField(default=0, max_length=20, null=True),
        ),
    ]
