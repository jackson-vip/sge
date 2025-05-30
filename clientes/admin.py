from django.contrib import admin
from .models import Cliente
from utils.filters import ClienteFilter

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cpf', 'rg', 'email', 'telefone', 'status']
    list_display_links = ['usuario', 'email']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'cpf', 'rg', 'email', 'telefone']
    list_filter = ['status']
    ordering = ['usuario__username']
    list_per_page = 20
    readonly_fields = ['cpf', 'rg']
    list_select_related = ['usuario']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        cliente_filter = ClienteFilter(request.GET, queryset=queryset)
        return cliente_filter.qs

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('usuario', 'cpf', 'rg', 'email', 'telefone', 'status')
        }),
    )
