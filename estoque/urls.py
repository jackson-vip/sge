from django.urls import path

from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.EstoqueView.as_view(), name='estoque'),
]