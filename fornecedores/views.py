from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import render

from fornecedores.forms import FornecedorForm
from .models import Fornecedor

class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedor_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {}
        context['title'] = 'Lista de Fornecedores'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
        ]
        context['fornecedores'] = Fornecedor.objects.all()
        return context

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     return render(request, self.template_name, context)

class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedor/fornecedor_create_view.html'
    success_url = 'fornecedores/'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Novo Fornecedor'
        context['form'] = self.form_class()
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
            {'name': 'Novo Fornecedor', 'url': reverse('fornecedor:fornecedor_create_view')},
        ]
        return context
    
    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data()
    #     return render(request, self.template_name, context)
