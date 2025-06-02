from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from clientes.models import Cliente
from django import forms
from utils.django_forms import *
import uuid

class ClienteForm(forms.ModelForm):
    # Criando novos atributos para o formulário de Cliente
    first_name = forms.CharField()
    last_name = forms.CharField()
    data_nascimento = forms.DateField()
    email = forms.EmailField()
    endereco_cep = forms.CharField()
    endereco_logradouro = forms.CharField()
    endereco_numero = forms.CharField()
    endereco_complemento = forms.CharField(required=False)
    endereco_bairro = forms.CharField()
    endereco_municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
    )
    endereco_uf = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.all(),
    )

    class Meta:
        model = Cliente
        fields = ['imagem','cpf', 'rg', 'telefone', 'email', 'data_nascimento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar form-control a todos os campos do formulário
        add_form_control(self)

        # Configurar auto_id para remover o prefixo 'id_'
        # self.auto_id = '%s'

        # Adicionar placeholders e atributos aos campos do formulário
        # Campos de User
        rename_label(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        
        rename_label(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')

        # Os campos de Cliente
        rename_label(self.fields['cpf'], 'CPF')
        add_placeholder(self.fields['cpf'], 'Digite seu CPF')

        rename_label(self.fields['rg'], 'RG')
        add_placeholder(self.fields['rg'], 'Digite seu RG')

        rename_label(self.fields['telefone'], 'Telefone')
        add_placeholder(self.fields['telefone'], '(00) 00000-0000')

        rename_label(self.fields['email'], 'Email')
        add_placeholder(self.fields['email'], 'exemplo@dominio.com')
        
        rename_label(self.fields['data_nascimento'], 'Data de Nascimento')
        add_placeholder(self.fields['data_nascimento'], '01/01/2000')

        # Os campos de Endereço
        rename_label(self.fields['endereco_logradouro'], 'Logradouro')
        add_placeholder(self.fields['endereco_logradouro'], 'Digite o logradouro')

        rename_label(self.fields['endereco_numero'], 'Número')
        add_placeholder(self.fields['endereco_numero'], 'Digite o número')

        rename_label(self.fields['endereco_complemento'], 'Complemento')
        add_placeholder(self.fields['endereco_complemento'], 'Digite o complemento')

        rename_label(self.fields['endereco_bairro'], 'Bairro')
        add_placeholder(self.fields['endereco_bairro'], 'Digite o bairro')

        rename_label(self.fields['endereco_cep'], 'CEP')
        add_placeholder(self.fields['endereco_cep'], '00000-000')

        rename_label(self.fields['endereco_municipio'], 'Município')
        add_attr(self.fields['endereco_municipio'], 'class', 'form-control')

        rename_label(self.fields['endereco_uf'], 'UF')

    def save(self, commit=True):
        # Criar o usuário
        user = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=f"{self.cleaned_data['email']}-{uuid.uuid4().hex[:8]}"  # Gerar username único
        )
        user.set_password(make_password(None))  # Gerar senha aleatória corretamente
        if commit:
            user.save()

        # Criar o cliente associado ao usuário
        cliente = super().save(commit=False)
        cliente.usuario = user
        cliente.email = self.cleaned_data['email']  # Salvar o email do formulário no cliente
        cliente.data_nascimento = self.cleaned_data['data_nascimento']  # Adicionar data de nascimento
        cliente.status = 'ativo'  # Definir como cliente ativo

        # Criar o endereço associado ao cliente
        endereco = Endereco(
            logradouro=self.cleaned_data['endereco_logradouro'],
            numero=self.cleaned_data['endereco_numero'],
            complemento=self.cleaned_data['endereco_complemento'],
            bairro=self.cleaned_data['endereco_bairro'],
            municipio=self.cleaned_data['endereco_municipio'],
            uf=self.cleaned_data['endereco_uf'],
            cep=self.cleaned_data['endereco_cep']
        )

        if commit:
            endereco.save()
            cliente.endereco = endereco  # Associar o endereço ao cliente
            cliente.save()

        # Garantir que a imagem escolhida seja salva antes de salvar o cliente
        if 'imagem' in self.cleaned_data:
            cliente.imagem = self.cleaned_data['imagem']

        # Criar o perfil associado ao usuário
        perfil = Perfil(
            usuario=user,
            tipo='cliente'  # Definir o tipo como cliente
        )
        if commit:
            perfil.save()

        return cliente
