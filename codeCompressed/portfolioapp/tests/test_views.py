from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.db import IntegrityError, transaction
from portfolioapp.models import Asset
import json


class TestViews(TestCase):

    #setup run before every test scenario
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('starting-page')
        self.portfolio_url = reverse('portfolio-page')
        self.update_url = reverse('update-portfolio', args=['msft'])
        self.msft = Asset.objects.create(
            ticker = 'msft', 
            session = "testSession123"
        )

    def test_home_ticker_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolioapp/index.html')

    def test_portfolio_GET(self):
        response = self.client.get(self.portfolio_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolioapp/portfolio.html')

    # # Post to search ticker
    def test_home_search_ticker_POST(self):
        #search
        response = self.client.post(self.home_url, {
            'searchticker': 'Search', 
            'ticker': 'fb', 
            'session': 'sessionTest123'}
            ,follow=True
        )
        self.assertEquals(response.status_code, 200)

    # Post to update holding
    def test_update_POST(self):
        response = self.client.post(self.update_url, {'ticker': 'fb', 'closing_price': 200, 'purchase_quantity': 10, 'purchase_price': 150, 'session': 'testSession123'})
        self.assertEquals(response.status_code, 302)


   # # Post to add ticker
    # def test_home_add_ticker_POST(self):
    #     try:
    #         with transaction.atomic():
    #             print(self.home_url)
    #             # response = self.client.post(self.home_url, {
    #             #     'addasset': 'Add'
    #                 # 'ticker': 'msft', 
    #                 # 'session': 'sessionTest123'  
    #             #})
            
    #     except IntegrityError:
    #         print("err")
    #         pass

        # add
        # self.assertEquals(response.status_code, 302)

#  def test_update_GET(self):
#         response = self.client.get(self.update_url)
#         print(Asset.objects.all())
#         print(self.update_url)
#         print(response)
#         # self.assertEquals(response.status_code)
#         # self.assertTemplateUsed(response, 'portfolioapp/update-holding.html')


# class TestAddAssetView(TransactionTestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.home_url = reverse('starting-page')
#         self.portfolio_url = reverse('portfolio-page')
#         self.update_url = reverse('update-portfolio', args=['msft'])
#         self.msft = Asset.objects.create(
#             ticker = 'msft', 
#             session = "testSession123"
#         )

#     def test_home_add_ticker_POST(self):
#         try:
#             with transaction.atomic():
#                 #print(self.home_url)
#                 response = self.client.post(self.home_url, {
#                     'addasset': 'Add',
#                     'ticker': 'msft', 
#                     'session': 'sessionTest123'  
#                 })
            
#         except IntegrityError:
#             print("err")
#             pass
#         except Exception as e:
#             print('unknown exception')
#             print(e)



