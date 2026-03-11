from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib import messages

from authentication.models import UnidadeFederativa
from fornecedores.forms import FornecedorForm
from utils.messages import msg_criado, msg_atualizado, msg_erro_criar, msg_erro_atualizar
from .models import Fornecedor

class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedor_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedores'] = Fornecedor.objects.all()
        context['qnt_ativos'] = Fornecedor.objects.filter(status='ativo').count()
        context['qnt_inativos'] = Fornecedor.objects.filter(status='inativo').count()
        context['qnt_bloqueados'] = Fornecedor.objects.filter(status='bloqueado').count()
        context['title'] = 'Detalhes do Fornecedor'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
        ]
        return context

class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedor/fornecedor_create_view.html'
    success_url = reverse_lazy('fornecedor:fornecedor_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Fornecedor'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
            {'name': 'Novo Fornecedor', 'url': reverse('fornecedor:fornecedor_create_view')},
        ]
        return context

    def form_valid(self, form):
        messages.success(self.request, msg_criado('Fornecedor'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, msg_erro_criar('Fornecedor'))
        return super().form_invalid(form)

class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedor_modal/modal_funcionario_delete_view.html'
    success_url = reverse_lazy('fornecedor:fornecedor_list_view')

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Fornecedor.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedor'] = self.get_queryset().first()
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
            {'name': 'Detalhes do Fornecedor', 'url': reverse('fornecedor:fornecedor_detail_view', kwargs={'pk': self.kwargs['pk']})},
        ]
        return context

class FornecedorDetailView(LoginRequiredMixin, DetailView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedor_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalhes do Fornecedor'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
            {'name': 'Detalhes do Fornecedor', 'url': reverse('fornecedor:fornecedor_detail_view', args=[self.object.id])},
        ]
        return context

class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedor/fornecedor_update_view.html'
    success_url = reverse_lazy('fornecedor:fornecedor_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Fornecedor'
        context['breadcrumbs'] = [
            {'name': 'Fornecedores', 'url': reverse('fornecedor:fornecedor_list_view')},
            {'name': 'Editar Fornecedor', 'url': reverse('fornecedor:fornecedor_update_view', args=[self.object.id])},
        ]
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        fornecedor = self.get_object()
        endereco = fornecedor.endereco

        if endereco:
            initial.update({
                'endereco_cep': endereco.cep,
                'endereco_logradouro': endereco.logradouro,
                'endereco_numero': endereco.numero,
                'endereco_complemento': endereco.complemento,
                'endereco_bairro': endereco.bairro,
                'endereco_municipio': endereco.municipio, 
                'endereco_sigla': UnidadeFederativa.objects.get(sigla=endereco.sigla), # Assumindo que sigla é um campo de UnidadeFederativa
            })

        return initial
    
    def form_valid(self, form):
        messages.success(self.request, msg_atualizado('Fornecedor'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, msg_erro_atualizar('Fornecedor'))
        return super().form_invalid(form)