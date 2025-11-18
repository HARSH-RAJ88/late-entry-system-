from .views import *
from django.urls import path

urlpatterns = [
    path('',DashboardView.as_view(),name='dashboard'),
    path('warden', WardenDashBoardView.as_view(), name='warden'),
    path('guard', GuardDashBoardView.as_view(), name='guard'),
    path('student', StudentDashBoardView.as_view(), name='student'),
    path('grant', WardenGrantView.as_view(), name='grant'),
    path('granted/<int:permissionID>' , GrantedPermissionView.as_view(), name='granted'),
    path('rejected/<int:permissionID>' , RejectedPermissionView.as_view(), name='rejected'),

]
