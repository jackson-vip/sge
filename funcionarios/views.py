from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Funcionario

# Create your views here.

class FuncionarioListView(LoginRequiredMixin, View):
    template = 'funcionario/funcionario_list_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Lista de Funcionários'
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse('funcionario:funcionario_list_view')},
        ]
        context['funcionarios'] = Funcionario.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template, context)
    
class FuncionarioCreateView(LoginRequiredMixin, View):
    template = 'funcionario/funcionario_create_view.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'Criar Funcionário'
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse('funcionario:funcionario_list_view')},
            {'name': 'Criar Funcionário', 'url': reverse('funcionario:funcionario_create_view')},
        ]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template, context)