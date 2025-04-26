from django.urls import path

from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.ProdutosView.as_view(), name='produtos'),
]