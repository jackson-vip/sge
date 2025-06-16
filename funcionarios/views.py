from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.filters import FuncionarioFilter
from django_filters.views import FilterView
from .models import Funcionario

# Create your views here.

PRE_PAGES = 12

class FuncionarioListView(LoginRequiredMixin, FilterView):
    model = Funcionario
    template_name = 'funcionario/funcionario_list_view.html'
    context_object_name = 'funcionarios'
    paginate_by = PRE_PAGES
    filterset_class = FuncionarioFilter

    def get(self, request, *args, **kwargs):
        if request.GET.get('opcao'):
            self.paginate_by = request.GET.get('opcao')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Funcionários'
        context['qnt_ativos'] = Funcionario.objects.filter(status='ativo').count()
        context['qnt_inativos'] = Funcionario.objects.filter(status='inativo').count()
        context['qnt_bloqueados'] = Funcionario.objects.filter(status='bloqueado').count()
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse('funcionario:funcionario_list_view')},
        ]
        return context