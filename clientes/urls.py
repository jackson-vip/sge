from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteDeleteView,
)

app_name = 'cliente'

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list_view'),
    path('novo/', ClienteCreateView.as_view(), name='cliente_create_view'),
    # path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='update'),
    path('cliente_deletar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete_view'),
    # path('<int:pk>/', ClienteDetailView.as_view(), name='detail'),
]