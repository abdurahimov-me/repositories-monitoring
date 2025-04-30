from django.urls import path

from apps.users.views import RegisterRequestView,RegisterVerifyView

urlpatterns = [
    path('register/', RegisterRequestView.as_view(), name='register'),
    path('verify/', RegisterVerifyView.as_view(), name='verify'),
]