from django.contrib import admin
from .models import Pedido, ItemPedido

# Register your models here.

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['fornecedor', 'data_pedido', 'status']
    search_fields = ['fornecedor__usuario__username', 'data_pedido', 'status']
    list_filter = ['status']
    ordering = ['-data_pedido']
    list_per_page = 20
    list_display_links = ['fornecedor', 'data_pedido']
    list_editable = ['status']


@admin.register(ItemPedido)
class PedidoProdutoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'produto', 'quantidade', 'preco_unitario']
    search_fields = ['pedido__fornecedor__usuario__username', 'produto__nome', 'quantidade', 'preco_unitario']
    list_filter = ['pedido']
    ordering = ['pedido']
    list_per_page = 20
    list_display_links = ['pedido', 'produto']
    list_editable = ['quantidade', 'preco_unitario']