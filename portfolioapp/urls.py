from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.StartingPageView.as_view(), name='starting-page'),
    path('portfolio/', views.StartingPageView.as_view(), name='portfolio-page')
]