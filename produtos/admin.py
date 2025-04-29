from django.contrib import admin
from .models import Categoria, Produto

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    list_filter = ['nome']
    ordering = ['nome']
    list_per_page = 20

    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'quantidade', 'quantidade_minima', 'preco_custo', 'preco_venda', 'categoria', 'ativo', 'criado_em', 'atualizado_em']
    search_fields = ['nome', 'codigo']
    list_filter = ['nome', 'codigo', 'categoria', 'ativo']
    ordering = ['nome', 'categoria']
    list_per_page = 20
    list_display_links = ['nome', 'codigo']
    list_editable = ['quantidade', 'quantidade_minima', 'preco_custo', 'preco_venda', 'categoria', 'ativo']
    list_select_related = True
