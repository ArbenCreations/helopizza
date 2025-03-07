from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('menu/',menu,name='menu'),
    path('reservation/',reservation,name='reservation'),
    path('contact/',contact,name='contact'),
]
