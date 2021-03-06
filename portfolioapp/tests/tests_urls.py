from django.test import SimpleTestCase
from django.urls import reverse, resolve
from portfolioapp.views import StartingPageView, PortfolioPageView, PortfolioUpdate


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('starting-page')
        self.assertEquals(resolve(url).func.view_class, StartingPageView)

    def test_portfolio_url_is_resolved(self):
        url = reverse('portfolio-page')
        self.assertEquals(resolve(url).func.view_class, PortfolioPageView)

    def test_update_portfolio_url_is_resolved(self):
        url = reverse('update-portfolio', args=['some-ticker'])
        self.assertEquals(resolve(url).func, PortfolioUpdate)

    

        
