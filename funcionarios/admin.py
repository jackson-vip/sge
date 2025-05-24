from django.contrib import admin
from .models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cargo', 'departamento', 'cpf', 'matricula', 'telefone', 'email_profissional']
    search_fields = ['usuario__username', 'cargo', 'departamento', 'cpf', 'matricula', 'telefone', 'email_profissional']
    list_filter = ['departamento']
    ordering = ['usuario', 'cargo']
    list_per_page = 20
