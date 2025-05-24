from django.contrib import admin
from .models import (UnidadeFederativa, Municipio, Endereco, Perfil)

# Register your models here.

# unidade_federativa
@admin.register(UnidadeFederativa)
class UnidadeFederativaAdmin(admin.ModelAdmin):
    list_display = ['uf', 'sigla']
    search_fields = ['uf', 'sigla']
    list_filter = ['uf']
    ordering = ['uf']
    list_per_page = 20

# Municipio
@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['municipio', 'uf', 'codigo_ibge', 'cnpj', 'codigo_siafi']
    search_fields = ['municipio', 'uf', 'codigo_ibge', 'cnpj', 'codigo_siafi']
    list_filter = ['uf']
    ordering = ['municipio']
    list_per_page = 20

# Endereco
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    # list_display todos
    list_display = ['logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'uf', 'cep', 'tipo_endereco']
    search_fields = ['logradouro', 'complemento', 'bairro', 'municipio', 'uf', 'cep']
    list_filter = ['tipo_endereco']
    ordering = ['logradouro']
    list_per_page = 20

# Perfil
@admin.action(description='Alterar para Funcionário')
def alterar_para_funcionario(modeladmin, request, queryset):
    queryset.update(tipo='funcionario')

@admin.action(description='Resetar senha para padrão')
def resetar_senha(modeladmin, request, queryset):
    for obj in queryset:
        obj.set_password('mudar123')
        obj.save()

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo']
    search_fields = ['usuario__username']
    list_filter = ['tipo']
    autocomplete_fields = ['usuario']
    actions = [alterar_para_funcionario, resetar_senha]