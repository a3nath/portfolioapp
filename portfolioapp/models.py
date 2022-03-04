from django.db import models

# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(max_length=50, blank=False, null=False)
    closing_price = models.FloatField(max_length=20, blank=True, null=True)
    purchase_price = models.FloatField(max_length=20, blank=False, null=True, default=0)
    purchase_quantity = models.FloatField(max_length=20, blank=False, null=True, default=0)
    session = models.CharField(max_length=200, blank=False, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['ticker', 'session'], name='ticker session unique constraint')]

    def __str__(self):
        return f"{self.ticker} {self.closing_price}"