from django.urls import path
from .views import (
    FornecedorListView, FornecedorCreateView, FornecedorDeleteView, FornecedorDetailView, FornecedorUpdateView
)

app_name = 'fornecedor'

urlpatterns = [
    path('', FornecedorListView.as_view(), name='fornecedor_list_view'),
    path('novo_fornecedor/', FornecedorCreateView.as_view(), name='fornecedor_create_view'),
    path('deletar_fornecedor/<int:pk>/', FornecedorDeleteView.as_view(), name='fornecedor_delete_view'),
    path('detalhes_fornecedor/<int:pk>/', FornecedorDetailView.as_view(), name='fornecedor_detail_view'),
    path('editar_fornecedor/<int:pk>/', FornecedorUpdateView.as_view(), name='fornecedor_update_view'),
]
