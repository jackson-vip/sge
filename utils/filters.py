import django_filters
from django.db.models import Q
from clientes.models import Cliente

class ClienteFilter(django_filters.FilterSet):
    qs = django_filters.CharFilter(method='filter_qs', label='Busca')
    status = django_filters.ChoiceFilter(
        choices=[
            ('ativo', 'Ativo'),
            ('inativo', 'Inativo'),
            ('bloqueado', 'Bloqueado'),
        ],
        empty_label='Todos',
        label='Status',
    )

    class Meta:
        model = Cliente
        fields = {
            'usuario__first_name': ['icontains'],
            'usuario__last_name': ['icontains'],
            'cpf': ['exact'],
            'email': ['icontains'],
            'telefone': ['icontains'],
            'status': ['exact'],
        }

    def filter_qs(self, queryset, name, value):
        if not value:
            return queryset  # Retorna todos os resultados se o valor estiver vazio
        
        return queryset.filter(
            Q(usuario__first_name__icontains=value) |
            Q(usuario__last_name__icontains=value) |
            Q(cpf__icontains=value) |
            Q(email__icontains=value) |
            Q(telefone__icontains=value) 
        )