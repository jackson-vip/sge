from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from estoque.models import MovimentacaoEstoque
from produtos.models import Produto

# Create your views here.

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': reverse('dashboard:dashboard')},
        ]
        # Estoque atual
        context['produtos'] = Produto.objects.all()

        # Movimentações recentes
        context['movimentacoes'] = MovimentacaoEstoque.objects.order_by('-data_movimentacao')[:10]

        # Estoque crítico (quantidade menor que 10)
        context['estoque_critico'] = Produto.objects.filter(quantidade__lt=10)


        return context