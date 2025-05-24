from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View

# Importação dos modelos
from .models import Cliente


# Create your views here.

class ClienteListView(LoginRequiredMixin, View):
    template_name = 'cliente/cliente_list_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Lista de Clientes'
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
        ]
        context['clientes'] = Cliente.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class ClienteCreateView(LoginRequiredMixin, View):
    template_name = 'cliente/cliente_create_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Criar Cliente'
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('authentication:cliente_list')},
            {'name': 'Criar Cliente', 'url': reverse('authentication:cliente_create')},
        ]
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
