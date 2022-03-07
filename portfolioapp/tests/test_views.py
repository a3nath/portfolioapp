from django.test import TestCase, Client
from django.urls import reverse
from portfolioapp.models import Asset
import json


class TestViews(TestCase):

    #runs before every test scenario
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('starting-page')
        self.portfolio_url = reverse('portfolio-page')
        self.update_url = reverse('update-holding', args=['msft'])
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

    def test_update_GET(self):
        response = self.client.get(self.update_url)
        print(response)

        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'portfolioapp/update-holding.html')

    # # Post to search ticker
    def test_home_search_ticker_POST(self):

        #search
        response = self.client.post(self.home_url, {
            'searchticker': 'Search', 
            'ticker': 'fb', 
            'session': 'sessionTest456'}
            ,follow=True
        )

        self.assertEquals(response.status_code, 200)

    # # Post to add ticker
    def test_home_add_ticker_POST(self):
        response = self.client.post(self.home_url, {
            'addasset': 'Add', 
            'ticker': 'msft', 
            'session': 'sessionTest123'}
            , follow=True
        )

        # add
        print(response)
    #     self.assertEquals(response.status_code, 302)

    # def test_update_add_ticker_POST(self):
    #     response = self.client.post(self.home_url, {'addasset': 'Add'}, follow=True)

    #     # add
    #     self.assertEquals(response.status_code, 302)
        
    # # Non duplicate

    # # Post to update holding
    # def test_update_POST(self):
    #     response = self.client.post(self.update_url, {'ticker': 'testTicker2', 'closing_price': 100, 'purchase_quantity': 10, 'purchase_price': 150, 'session': 'testSession'})

    #     tickerTest = Asset.objects.get(ticker='testTicker2')
    #     self.assertEquals(tickerTest.closing_price, 100)



