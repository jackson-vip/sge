from django.urls import path
from .views import ( FuncionarioListView, FuncionarioCreateView )

app_name = 'funcionario'

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario_list_view'),
    path('novo_funcionario/', FuncionarioCreateView.as_view(), name='funcionario_create_view'),
]