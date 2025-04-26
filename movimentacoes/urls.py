from django.urls import path

from . import views

app_name = 'movimentacoes'

urlpatterns = [
    path('', views.MovimentacoesView.as_view(), name='movimentacoes'),
]