from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, CustomLogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]