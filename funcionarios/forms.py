from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.models import User
from funcionarios.models import Funcionario
from django import forms
from utils.django_forms import *
from utils.validates_inputs import *
from django.utils.crypto import get_random_string
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

    CARGOS_OPCOES = [
        ('assistente', 'Assistente'),
        ('caixa', 'Caixa'),
        ('estagiario', 'Estagiário'),
        ('gerente', 'Gerente'),
        ('supervisor', 'Supervisor'),
        ('vendedor', 'Vendedor'),
        ('outro', 'Outro'),
    ]
    cargo = forms.ChoiceField(choices=CARGOS_OPCOES)

    DEPARTAMENTOS_OPCOES = [
        ('vendas', 'Vendas'),
        ('financeiro', 'Financeiro'),
        ('logistica', 'Logística'),
        ('marketing', 'Marketing'),
        ('outro', 'Outro'),
    ]
    departamento = forms.ChoiceField(choices=DEPARTAMENTOS_OPCOES, required=False)

    class Meta:
        model = Funcionario
        fields = ['imagem', 'cpf', 'rg', 'telefone', 'email_profissional', 'data_nascimento', 'cargo', 'departamento', 'data_contratacao', 'salario', 'observacoes']

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
        # add_placeholder(self.fields['cargo'], 'Digite o cargo do funcionário') # Exemplo: Gerente, Analista, Caixa, etc.
        add_attr(self.fields['cargo'], 'class', 'custom-select')
        # add_placeholder(self.fields['departamento'], 'Digite o departamento do funcionário') # Exemplo: Vendas, TI, RH, etc.
        add_attr(self.fields['departamento'], 'class', 'custom-select')
        add_placeholder(self.fields['data_contratacao'], '01/01/2020')
        add_placeholder(self.fields['salario'], 'R$ 0,00')

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
    
    def save(self, commit=True):
        # Criar o usuário
        usuario = User(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=f"{self.cleaned_data['email_profissional']}-{uuid.uuid4().hex[:8]}"  # Gerar username único
        )
        senha_aleatoria = get_random_string(8)
        usuario.set_password(senha_aleatoria)  # Gerar senha aleatória corretamente
        if commit:
            usuario.save()

        # Criar o funcionário associado ao usuário
        funcionario = super().save(commit=False)
        funcionario.usuario = usuario
        funcionario.email = self.cleaned_data['email_profissional'] # Salva o email profissional no campo email do usuário
        funcionario.data_nascimento = self.cleaned_data['data_nascimento']
        funcionario.status = 'ativo'  # Define o status como ativo por padrão

        # Criar o endereço associado ao funcionário
        endereco = Endereco(
            cep=self.cleaned_data['endereco_cep'],
            logradouro=self.cleaned_data['endereco_logradouro'],
            numero=self.cleaned_data['endereco_numero'],
            complemento=self.cleaned_data['endereco_complemento'],
            bairro=self.cleaned_data['endereco_bairro'],
            municipio=self.cleaned_data['endereco_municipio'],
            sigla=self.cleaned_data['endereco_sigla']
        )

        if commit:
            endereco.save()
            funcionario.endereco = endereco
            funcionario.save()

        # Garantir que a imagem escolhida seja salva antes de salvar o funcionário
        if 'imagem' in self.files:
            funcionario.imagem = self.files['imagem']
            funcionario.save()
        
        # Criar o perfil associado ao usuário
        perfil = Perfil(
            usuario=usuario,
            tipo='funcionario' # Definir o tipo como funcionário
            )
        if commit:
            perfil.save()
        
        return funcionario