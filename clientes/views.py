from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView

from utils.filters import ClienteFilter

# Importação dos modelos
from .models import Cliente

# Create your views here.

PRE_PAGES = 12

class ClienteListView(LoginRequiredMixin, FilterView):
    model = Cliente
    template_name = 'cliente/cliente_list_view.html'
    context_object_name = 'clientes'
    paginate_by = PRE_PAGES
    filterset_class = ClienteFilter

    def get(self, request, *args, **kwargs):
        if request.GET.get('opcao'):
            self.paginate_by = request.GET.get('opcao')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['action_url'] = reverse('cliente:cliente_list_view')
        context['qnt_clientes'] = Cliente.objects.filter(status='ativo').count()
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
    
class ClienteDetailView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'cliente/cliente_detail_view.html'
    context_object_name = 'cliente'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Cliente.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.get_queryset().first()
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Detalhes do Cliente', 'url': reverse('cliente:cliente_detail_view', kwargs={'pk': self.kwargs['pk']})},
        ]
        return context

class ClienteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente/cliente_modal/modal_cliente_delete_view.html'
    success_url = reverse_lazy('cliente:cliente_list_view')
    success_message = "Cliente %(cliente_nome)s removido com sucesso!"
    
    def get_success_message(self, cleaned_data):
        cliente = self.object if hasattr(self, 'object') else self.get_object()
        return self.success_message % {'cliente_nome': cliente.usuario.get_full_name()}

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'cliente/cliente_update_view.html'
    fields = ['usuario', 'imagem']  # Substitua pelos campos do modelo Cliente
    success_url = reverse_lazy('cliente:cliente_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Atualizar Cliente'
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Atualizar Cliente', 'url': reverse('cliente:cliente_update_view', kwargs={'pk': self.kwargs['pk']})},
        ]
        return context