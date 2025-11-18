from .views import DeleteDataView
from django.urls import path

urlpatterns = [
    path('', DeleteDataView.as_view(), name='delete'),

]
