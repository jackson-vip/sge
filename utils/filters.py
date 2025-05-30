import django_filters
from django.db.models import Q
from clientes.models import Cliente

class ClienteFilter(django_filters.FilterSet):
    qs = django_filters.CharFilter(method='filter_qs', label='Busca')

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
        return queryset.filter(
            Q(usuario__first_name__icontains=value) |
            Q(usuario__last_name__icontains=value) |
            Q(cpf__icontains=value) |
            Q(email__icontains=value) |
            Q(telefone__icontains=value) |
            Q(status__icontains=value)
        )