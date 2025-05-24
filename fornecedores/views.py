from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from .models import Fornecedor

class FornecedorListView(LoginRequiredMixin, View):
    template_name = 'fornecedor/fornecedor_list_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Lista de Fornecedores'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
        ]
        context['fornecedores'] = Fornecedor.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class FornecedorCreateView(LoginRequiredMixin, View):
    template_name = 'fornecedor/fornecedor_create_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Criar Fornecedor'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
