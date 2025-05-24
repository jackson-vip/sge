from django.contrib import admin
from .models import Fornecedor

# Register your models here.

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'cpf', 'telefone', 'email']
    search_fields = ['nome', 'cnpj', 'cpf', 'telefone', 'email']
    list_filter = ['tipo_pessoa']
    ordering = ['razao_social']
    list_per_page = 20
