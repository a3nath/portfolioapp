from django.test import TestCase
from portfolioapp.models import Asset

#creating an instance of model
#checking unique constraint

class TestModel(TestCase):

    def test_should_create_asset(self):
        asset = Asset.objects.create(
            ticker='msft',
            closing_price=1000,
            purchase_price = 100,
            purchase_quantity = 10,
            session = 'testSession123'
        )
        asset.save()

        self.assertEquals(str(asset), 'msft 1000')