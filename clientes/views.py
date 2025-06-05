from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django_filters.views import FilterView

from authentication.models import UnidadeFederativa
from utils.filters import ClienteFilter
from .forms import ClienteForm

# Importação dos modelos
from .models import Cliente

# Create your views here.

PRE_PAGES = 12

class ClienteListView(LoginRequiredMixin, FilterView):
    model = Cliente
    template_name = 'cliente/cliente_list_view.html'
    context_object_name = 'clientes'
    paginate_by = PRE_PAGES
    filterset_class = ClienteFilter

    def get(self, request, *args, **kwargs):
        if request.GET.get('opcao'):
            self.paginate_by = request.GET.get('opcao')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['action_url'] = reverse('cliente:cliente_list_view')
        context['qnt_ativos'] = Cliente.objects.filter(status='ativo').count()
        context['qnt_inativos'] = Cliente.objects.filter(status='inativo').count()
        context['qnt_bloqueados'] = Cliente.objects.filter(status='bloqueado').count()
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
        ]
        return context
    
class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/cliente_create_view.html'
    success_url = reverse_lazy('cliente:cliente_list_view')

    def form_valid(self, form):
        messages.success(self.request, "Cliente criado com sucesso!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Cliente'
        context['form'] = self.get_form()
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Criar Cliente', 'url': reverse('cliente:cliente_create_view')},
        ]
        return context
    
class ClienteDetailView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'cliente/cliente_detail_view.html'
    context_object_name = 'cliente'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Cliente.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.get_queryset().first()
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Detalhes do Cliente', 'url': reverse('cliente:cliente_detail_view', kwargs={'pk': self.kwargs['pk']})},
        ]
        return context

class ClienteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cliente/cliente_modal/modal_cliente_delete_view.html'
    success_url = reverse_lazy('cliente:cliente_list_view')
    success_message = "Cliente %(cliente_nome)s removido com sucesso!"
    
    def get_success_message(self, cleaned_data):
        cliente = self.object if hasattr(self, 'object') else self.get_object()
        return self.success_message % {'cliente_nome': cliente.usuario.get_full_name()}

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/cliente_update_view.html'
    success_url = reverse_lazy('cliente:cliente_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse('cliente:cliente_list_view')},
            {'name': 'Editar Cliente', 'url': reverse('cliente:cliente_update_view', kwargs={'pk': self.kwargs['pk']})},
        ]
        return context

    def get_initial(self):
        initial = super().get_initial()
        cliente = self.object
        user = cliente.usuario
        endereco = cliente.endereco

        # Adicionar dados do User
        if user:
            initial.update({
                'first_name': user.first_name,
                'last_name': user.last_name,
            })

# TODO: Lembrar de trasformar o atributo endereço_sigla em um campo de ForeignKey para UnidadeFederativa
        # Adicionar dados do Endereco
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
        cliente = form.save(commit=False)
        usuario = cliente.usuario

        # Atualizar os dados do usuário
        usuario.first_name = form.cleaned_data['first_name']
        usuario.last_name = form.cleaned_data['last_name']
        usuario.save()  # Salvar o usuário antes de salvar o cliente

        if 'imagem' in self.request.FILES:
            cliente.imagem = self.request.FILES['imagem']
        cliente.save()

        messages.success(self.request, "Cliente atualizado com sucesso!")
        return super().form_valid(form)