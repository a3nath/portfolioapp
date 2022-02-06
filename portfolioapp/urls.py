from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='starting-page'),
    path('portfolio/', views.portfolio, name='portfolio-page')
]