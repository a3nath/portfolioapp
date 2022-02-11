from django.db import models

# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(max_length=50, blank=False)
    closing_price = models.FloatField(max_length=20, blank=True)
    purchase_price = models.FloatField(max_length=20, blank=True)
    purchase_quantity = models.FloatField(max_length=20, blank=True)
    session = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.ticker} {self.closing_price}"