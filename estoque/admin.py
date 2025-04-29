from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import (MovimentacaoEstoque,)

# Register your models here.

# MovimentacaoEstoque

@admin.action(description='Exportar para CSV')
def exportar_para_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimentacao_estoque.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Produto', 'Tipo', 'Quantidade', 'Data Movimentacao', 'Observacoes'])
    for movimentacao in queryset:
        writer.writerow([movimentacao.id, movimentacao.produto.nome, movimentacao.tipo, movimentacao.quantidade, movimentacao.data_movimentacao, movimentacao.observacoes])
    return response

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data_movimentacao', 'observacoes']
    search_fields = ['produto__nome', 'tipo', 'quantidade', 'data_movimentacao', 'observacoes']
    list_filter = ['tipo']
    ordering = ['-data_movimentacao']
    list_per_page = 20
    actions = ['exportar_para_csv']
    list_display_links = ['produto', 'data_movimentacao']
    list_editable = ['tipo', 'quantidade', 'observacoes']