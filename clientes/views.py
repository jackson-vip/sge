from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.urls import reverse, reverse_lazy

# Importação dos modelos
from .models import Cliente


# Create your views here.

PRE_PAGES = 12

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'cliente/cliente_list_view.html'
    context_object_name = 'clientes'
    paginate_by = PRE_PAGES

    def get(self, request, *args, **kwargs):
        if request.GET.get('opcao'):
            self.paginate_by = request.GET.get('opcao')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        qs = self.request.GET.get('qs', '').strip()  # Use strip para remover espaços em branco

        if qs:
            queryset = queryset.filter(
                Q(usuario__first_name__icontains=qs) |
                Q(usuario__last_name__icontains=qs) |
                Q(usuario__username__icontains=qs) |
                Q(cpf__icontains=qs) |
                Q(email__icontains=qs)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        qs = self.request.GET.get('qs', '').strip()
        context['qs'] = qs
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
        ]
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'cliente/cliente_create_view.html'
    fields = ['usuario', 'imagem']  # Substitua pelos campos do modelo Cliente
    success_url = reverse_lazy('cliente:cliente_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Cliente'
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Criar Cliente', 'url': reverse('cliente:cliente_create_view')},
        ]
        return context
