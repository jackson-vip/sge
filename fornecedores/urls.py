from django.urls import path
from .views import (
    FornecedorListView, FornecedorCreateView,
)

app_name = 'fornecedor'

urlpatterns = [
    path('', FornecedorListView.as_view(), name='fornecedor_list_view'),
    path('novo/', FornecedorCreateView.as_view(), name='fornecedor_create_view'),
]
