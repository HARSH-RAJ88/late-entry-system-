from .views import InsertView
from django.urls import path

urlpatterns = [
    path('', InsertView.as_view(), name='insert'),

]
