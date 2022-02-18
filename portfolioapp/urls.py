from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.StartingPageView.as_view(), name='starting-page'),
    path('portfolio/', views.PortfolioPageView.as_view(), name='portfolio-page'),
    path('holdings/<str:ticker>', views.HoldingUpdateView.as_view(), name='update_holding')
    # path('holdings/<str:ticker>', views.holdings, name='update_holding')
    #   dateHoldingView.as_view(), name='update_holding')

]