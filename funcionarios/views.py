from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UnidadeFederativa
from funcionarios.forms import FuncionarioForm
from utils.filters import FuncionarioFilter
from utils.messages import msg_criado, msg_atualizado, msg_erro_criar, msg_erro_atualizar
from django_filters.views import FilterView
from .models import Funcionario
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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
    
class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/funcionario_create_view.html'
    success_url = reverse_lazy('funcionario:funcionario_list_view')

    def form_valid(self, form):
        messages.success(self.request, msg_criado("Funcionário"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, msg_erro_criar("Funcionário"))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Funcionário'
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse('funcionario:funcionario_list_view')},
            {'name': 'Novo Funcionário', 'url': reverse('funcionario:funcionario_create_view')},
        ]
        return context
    
class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario/funcionario_create_view.html'
    success_url = reverse_lazy('funcionario:funcionario_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Funcionário'
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse_lazy('funcionario:funcionario_list_view')},
            {'name': 'Editar Funcionário', 'url': self.request.path},
        ]
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        funcionario = self.get_object()
        user = funcionario.usuario
        endereco = funcionario.endereco
        
        if user:
            initial.update({
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        
        if endereco:
            uf = UnidadeFederativa.objects.filter(sigla=endereco.sigla).first() if endereco.sigla else None
            initial.update({
                'endereco_cep': endereco.cep,
                'endereco_logradouro': endereco.logradouro,
                'endereco_numero': endereco.numero,
                'endereco_complemento': endereco.complemento,
                'endereco_bairro': endereco.bairro,
                'endereco_municipio': endereco.municipio,
                'endereco_sigla': uf
            })
        return initial

    def form_valid(self, form):
        messages.success(self.request, msg_atualizado("Funcionário"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, msg_erro_atualizar("Funcionário"))
        return super().form_invalid(form)

class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    model = Funcionario
    template_name = 'funcionario/funcionario_detail_view.html'
    context_object_name = 'funcionario'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Funcionario.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalhes do Funcionário'
        context['funcionario'] = self.get_queryset().first()
        context['breadcrumbs'] = [
            {'name': 'Funcionários', 'url': reverse_lazy('funcionario:funcionario_list_view')},
            {'name': 'Detalhes do Funcionário', 'url': self.request.path},
        ]
        return context

class FuncionarioDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario/funcionario_modal/modal_funcionario_delete_view.html'
    success_url = reverse_lazy('funcionario:funcionario_list_view')
    success_message = "Funcionario %(funcionario_nome)s removido com sucesso!"

    def get_success_message(self, cleaned_data):
        funcionario = self.object if hasattr(self, 'object') else self.get_object()
        return self.success_message % {'funcionario_nome': funcionario.usuario.get_full_name()}
