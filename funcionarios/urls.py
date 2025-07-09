from django.urls import path
from .views import (FuncionarioListView, FuncionarioCreateView, FuncionarioUpdateView)

app_name = 'funcionario'

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario_list_view'),
    path('novo_funcionario/', FuncionarioCreateView.as_view(), name='funcionario_create_view'),
    path('editar_funcionario/<int:pk>/', FuncionarioUpdateView.as_view(), name='funcionario_update_view'),
]