from django.contrib import admin
from .models import (UnidadeFederativa, Municipio, Endereco, Fornecedor, Funcionario, Perfil)
import csv
from django.http import HttpResponse

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

# Fornecedor
@admin.action(description='Ativar fornecedores selecionados')
def ativar_fornecedores(modeladmin, request, queryset):
    queryset.update(ativo=True)

@admin.action(description='Desativar fornecedores selecionados')
def desativar_fornecedores(modeladmin, request, queryset):
    queryset.update(ativo=False)

@admin.action(description='Exportar para CSV')
def exportar_para_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dados.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nome', 'Email'])  # Cabeçalhos
    for obj in queryset:
        writer.writerow([obj.id, obj.nome, obj.email])  # Dados
    return response

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'razao_social', 'cnpj', 'cpf', 'telefone', 'email']
    search_fields = ['usuario__username', 'razao_social', 'cnpj', 'cpf', 'telefone', 'email']
    list_filter = ['tipo_pessoa']
    ordering = ['razao_social', 'telefone', 'email', 'cnpj']
    list_per_page = 20
    actions = [ativar_fornecedores, desativar_fornecedores, exportar_para_csv]

# Funcionario
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cargo', 'departamento', 'cpf', 'matricula', 'telefone', 'email_profissional']
    search_fields = ['usuario__username', 'cargo', 'departamento', 'cpf', 'matricula', 'telefone', 'email_profissional']
    list_filter = ['departamento']
    ordering = ['usuario', 'cargo']
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