from django.urls import path
from .views import ( FuncionarioListView )

app_name = 'funcionario'

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario_list_view'),
]