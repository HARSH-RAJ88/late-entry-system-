from .views import *
from django.urls import path

urlpatterns = [
    path('', ViewPreviousData.as_view(), name='viewPrevData'),
    path('roll',ViewPreviousDataRoll.as_view(),name='viewPrevDataRoll'),
    path('date',ViewPreviousDataDate.as_view(),name='viewPrevDataDate'),
    path('permissionView',PermissionView.as_view(),name='permissionView')
]
