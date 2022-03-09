from django.urls import path
from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting-page'),
    path('portfolio/', views.PortfolioPageView.as_view(), name='portfolio-page'),
    # path('portfolio/', views.portfolioPage, name='portfolio-page'),
    path('portfolio/<str:ticker>', views.PortfolioUpdate, name='update-portfolio')
    # path('holdings/<str:ticker>', views.HoldingUpdate, name='update-holding')
    # path('holdings/<str:ticker>', views.holdings, name='update_holding')
    #   dateHoldingView.as_view(), name='update_holding')
] 