from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from funcionarios.models import Funcionario
from django import forms
from utils.django_forms import *
from utils.validates_inputs import *
import uuid


class FuncionarioForm(forms.ModelForm):
    # Criando novos atributos para o formulário de Funcionario
    first_name = forms.CharField()
    last_name = forms.CharField()
    data_nascimento = forms.DateField()
    email_profissional = forms.EmailField()
    endereco_cep = forms.CharField()
    endereco_logradouro = forms.CharField()
    endereco_numero = forms.CharField()
    endereco_complemento = forms.CharField(required=False)
    endereco_bairro = forms.CharField()
    endereco_municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.all(),
    )
    endereco_sigla = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.all(),
    )

    class Meta:
        model = Funcionario
        fields = ['imagem', 'cpf', 'rg', 'telefone', 'email_profissional', 'data_nascimento', 'cargo', 'departamento', 'data_contratacao', 'salario', 'status', 'observacoes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar form-control a todos os campos do formulário
        add_form_control(self)

        # Adicionar placeholders e atributos aos campos do formulário
        # Campos de User
        rename_label(self.fields['first_name'], 'Nome')
        add_placeholder(self.fields['first_name'], 'Digite seu nome')
        
        rename_label(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')

        # Os campos de Funcionario
        add_placeholder(self.fields['cpf'], 'Digite seu CPF')
        add_placeholder(self.fields['rg'], 'Digite seu RG')
        add_placeholder(self.fields['data_nascimento'], '01/01/2000')
        add_placeholder(self.fields['telefone'], '(00) 00000-0000')
        rename_label(self.fields['email_profissional'], 'Email')
        add_placeholder(self.fields['email_profissional'], 'exemplo@dominio.com')
        add_placeholder(self.fields['observacoes'], 'Adicione observações sobre o funcionário')
        add_placeholder(self.fields['cargo'], 'Digite o cargo do funcionário') # Exemplo: Gerente, Analista, Caixa, etc.
        add_placeholder(self.fields['departamento'], 'Digite o departamento do funcionário') # Exemplo: Vendas, TI, RH, etc.
        add_placeholder(self.fields['data_contratacao'], '01/01/2020')

        # Os campos de Endereço
        rename_label(self.fields['endereco_cep'], 'CEP')
        add_placeholder(self.fields['endereco_cep'], '00000-000')

        rename_label(self.fields['endereco_logradouro'], 'Logradouro')
        add_placeholder(self.fields['endereco_logradouro'], 'Digite o logradouro')

        rename_label(self.fields['endereco_numero'], 'Número')
        add_placeholder(self.fields['endereco_numero'], 'Digite o número')

        rename_label(self.fields['endereco_complemento'], 'Complemento')
        add_placeholder(self.fields['endereco_complemento'], 'Digite o complemento')

        rename_label(self.fields['endereco_bairro'], 'Bairro')
        add_placeholder(self.fields['endereco_bairro'], 'Digite o bairro')

        rename_label(self.fields['endereco_municipio'], 'Município')
        add_attr(self.fields['endereco_municipio'], 'class', 'custom-select')

        rename_label(self.fields['endereco_sigla'], 'UF')
        add_attr(self.fields['endereco_sigla'], 'class', 'custom-select')

    # Validando os campos do formulário
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not validate_cpf(cpf):
            raise forms.ValidationError("CPF inválido.")
        return cpf

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        if not validate_rg(rg):
            raise forms.ValidationError("RG inválido.")
        return rg
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not validate_phone(telefone):
            raise forms.ValidationError("Telefone inválido.")
        return telefone

    def clean_endereco_cep(self):
        cep = self.cleaned_data['endereco_cep']
        if not validate_cep(cep):
            raise forms.ValidationError("CEP inválido.")
        return cep