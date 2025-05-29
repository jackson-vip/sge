from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteDeleteView, ClienteDetailView, ClienteUpdateView
)

app_name = 'cliente'

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list_view'),
    path('novo_cliente/', ClienteCreateView.as_view(), name='cliente_create_view'),
    path('deletar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete_view'),
    path('detalhes_cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail_view'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update_view'),
]