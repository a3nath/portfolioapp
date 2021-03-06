# Generated by Django 3.2.9 on 2022-03-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioapp', '0003_auto_20220301_1827'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='asset',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='asset',
            constraint=models.UniqueConstraint(fields=('ticker', 'session'), name='ticker session unique constraint'),
        ),
    ]
