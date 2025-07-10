from django.urls import path
from .views import (FuncionarioDeleteView, FuncionarioListView, FuncionarioCreateView, FuncionarioUpdateView)

app_name = 'funcionario'

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario_list_view'),
    path('novo_funcionario/', FuncionarioCreateView.as_view(), name='funcionario_create_view'),
    path('editar_funcionario/<int:pk>/', FuncionarioUpdateView.as_view(), name='funcionario_update_view'),
    path('deletar_funcionario/<int:pk>/', FuncionarioDeleteView.as_view(), name='funcionario_delete_view'),
]