from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from clientes.models import Cliente
from django import forms
from utils.django_forms import *
import uuid

# class UnidadeFederativaForm(forms.ModelForm):
#     class Meta:
#         model = UnidadeFederativa
#         fields = ['uf', 'sigla']
#         widgets = {
#             'uf': forms.TextInput(attrs={'class': 'form-control'}),
#             'sigla': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class MunicipioForm(forms.ModelForm):
#     class Meta:
#         model = Municipio
#         fields = ['id_uf', 'municipio', 'codigo_ibge', 'uf', 'cnpj', 'codigo_siafi']
#         widgets = {
#             'id_uf': forms.Select(attrs={'class': 'form-control'}),
#             'municipio': forms.TextInput(attrs={'class': 'form-control'}),
#             'codigo_ibge': forms.TextInput(attrs={'class': 'form-control'}),
#             'uf': forms.TextInput(attrs={'class': 'form-control'}),
#             'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
#             'codigo_siafi': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class EnderecoForm(forms.ModelForm):
#     class Meta:
#         model = Endereco
#         fields = ['logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'uf', 'sigla', 'cep', 'tipo_endereco'
#         ]
#         widgets = {
#             'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
#             'numero': forms.TextInput(attrs={'class': 'form-control'}),
#             'complemento': forms.TextInput(attrs={'class': 'form-control'}),
#             'bairro': forms.TextInput(attrs={'class': 'form-control'}),
#             'municipio': forms.Select(attrs={'class': 'form-control'}),
#             'uf': forms.TextInput(attrs={'class': 'form-control'}),
#             'sigla': forms.TextInput(attrs={'class': 'form-control'}),
#             'cep': forms.TextInput(attrs={'class': 'form-control'}),
#             'tipo_endereco': forms.Select(attrs={'class': 'form-control'}),
#         }
        
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             # Adicionar placeholders
#             add_placeholder(self.fields['logradouro'], 'Logradouro')
#             add_placeholder(self.fields['numero'], 'Número')
#             add_placeholder(self.fields['complemento'], 'Complemento')
#             add_placeholder(self.fields['bairro'], 'Bairro')
#             add_placeholder(self.fields['cep'], 'CEP')

# class PerfilForm(forms.ModelForm):
#     class Meta:
#         model = Perfil
#         fields = ['usuario', 'tipo']
#         widgets = {
#             'usuario': forms.Select(attrs={'class': 'form-control'}),
#             'tipo': forms.Select(attrs={'class': 'form-control'}),
#         }

class ClienteForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    endereco_logradouro = forms.CharField()
    endereco_numero = forms.CharField()
    endereco_complemento = forms.CharField(
        required=False,
    )
    endereco_bairro = forms.CharField()
    endereco_municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
    )
    endereco_uf = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.all(),
    )
    endereco_cep = forms.CharField()
    data_nascimento = forms.DateField()

    class Meta:
        model = Cliente
        fields = ['imagem', 'cpf', 'rg', 'telefone', 'email']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar form-control a todos os campos do formulário
        add_form_control(self)

        # Configurar auto_id para remover o prefixo 'id_'
        # self.auto_id = '%s'

        # Adicionar placeholders e atributos aos campos do formulário
        # Campos de User
        rename_label(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['first_name'], 'Ex.: João')
        
        rename_label(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['last_name'], 'Ex.: da Silva')

        # Os campos de Cliente
        rename_label(self.fields['cpf'], 'CPF')
        add_placeholder(self.fields['cpf'], 'Ex.: 000.000.000-00')

        rename_label(self.fields['rg'], 'RG')
        add_placeholder(self.fields['rg'], 'Ex.: 00.000.000-0')

        rename_label(self.fields['telefone'], 'Telefone')
        add_placeholder(self.fields['telefone'], 'Ex.: (00) 00000-0000')

        rename_label(self.fields['email'], 'Email')
        add_placeholder(self.fields['email'], 'Ex.: exemplo@dominio.com')
        
        rename_label(self.fields['data_nascimento'], 'Data de Nascimento')
        add_placeholder(self.fields['data_nascimento'], 'Ex.: 01/01/2000')

        # Os campos de Endereço
        rename_label(self.fields['endereco_logradouro'], 'Logradouro')
        add_placeholder(self.fields['endereco_logradouro'], 'Ex.: Rua Exemplo')

        rename_label(self.fields['endereco_numero'], 'Número')
        add_placeholder(self.fields['endereco_numero'], 'Ex.: 123')

        rename_label(self.fields['endereco_complemento'], 'Complemento')
        add_placeholder(self.fields['endereco_complemento'], 'Ex.: Apartamento 45')

        rename_label(self.fields['endereco_bairro'], 'Bairro')
        add_placeholder(self.fields['endereco_bairro'], 'Ex.: Centro')

        rename_label(self.fields['endereco_cep'], 'CEP')
        add_placeholder(self.fields['endereco_cep'], 'Ex.: 00000-000')

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
