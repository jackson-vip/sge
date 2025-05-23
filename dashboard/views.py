from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse

# Importando os modelos necessários
from estoque.models import MovimentacaoEstoque
from produtos.models import Produto

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
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