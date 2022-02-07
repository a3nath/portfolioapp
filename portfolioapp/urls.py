from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.starting_Page, name='starting-page'),
    path('portfolio/', views.portfolio, name='portfolio-page')
]