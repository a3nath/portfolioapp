# Generated by Django 4.0.3 on 2022-03-31 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioapp', '0008_asset_total_return'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='net_return',
            new_name='net_val',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='total_return',
            new_name='tot_val',
        ),
    ]
