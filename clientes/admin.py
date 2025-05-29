from django.contrib import admin
from .models import Cliente

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cpf', 'rg', 'email', 'telefone']
    search_fields = ['usuario__username', 'cpf', 'rg', 'email', 'telefone']
    list_filter = ['status']
    ordering = ['usuario__username']
    list_per_page = 20
