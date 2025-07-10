from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UnidadeFederativa
from funcionarios.forms import FuncionarioForm
from utils.filters import FuncionarioFilter
from django_filters.views import FilterView
from .models import Funcionario
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
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
        funcionario = self.get_object()
        user = funcionario.usuario
        endereco = funcionario.endereco
        # Atualiza os dados do usuário relacionado
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email_profissional')
        user.save()
        # Atualiza os dados do endereço relacionado
        endereco.cep = form.cleaned_data.get('endereco_cep')
        endereco.logradouro = form.cleaned_data.get('endereco_logradouro')
        endereco.numero = form.cleaned_data.get('endereco_numero')
        endereco.complemento = form.cleaned_data.get('endereco_complemento')
        endereco.bairro = form.cleaned_data.get('endereco_bairro')
        endereco.municipio = form.cleaned_data.get('endereco_municipio')
        sigla_obj = form.cleaned_data.get('endereco_sigla')
        endereco.sigla = sigla_obj.sigla if sigla_obj else ''
        endereco.save()
        # Salva o restante do formulário normalmente
        return super().form_valid(form)

class FuncionarioDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario/funcionario_modal/modal_funcionario_delete_view.html'
    success_url = reverse_lazy('funcionario:funcionario_list_view')
    success_message = "Funcionario %(funcionario_nome)s removido com sucesso!"

    def get_success_message(self, cleaned_data):
        funcionario = self.object if hasattr(self, 'object') else self.get_object()
        return self.success_message % {'funcionario_nome': funcionario.usuario.get_full_name()}