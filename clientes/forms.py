from django import forms
from clientes.models import Cliente
from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password
import uuid


class UnidadeFederativaForm(forms.ModelForm):
    class Meta:
        model = UnidadeFederativa
        fields = ['uf', 'sigla']
        widgets = {
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['id_uf', 'municipio', 'codigo_ibge', 'uf', 'cnpj', 'codigo_siafi']
        widgets = {
            'id_uf': forms.Select(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_ibge': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_siafi': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'numero', 'complemento', 'bairro', 'municipio', 'uf', 'sigla', 'cep', 'tipo_endereco'
        ]
        widgets = {
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'uf': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_endereco': forms.Select(attrs={'class': 'form-control'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['usuario', 'tipo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nome"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Sobrenome"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    endereco_logradouro = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Logradouro"
    )
    endereco_numero = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Número"
    )
    endereco_complemento = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Complemento",
        required=False
    )
    endereco_bairro = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Bairro"
    )
    endereco_municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Município"
    )
    endereco_uf = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="UF"
    )
    endereco_cep = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="CEP"
    )
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Data de Nascimento"
    )

    class Meta:
        model = Cliente
        fields = ['imagem', 'cpf', 'rg', 'telefone']
        widgets = {
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

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
