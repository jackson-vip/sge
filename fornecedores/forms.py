from datetime import timezone
import uuid
from django.utils.crypto import get_random_string
from authentication.models import Endereco, UnidadeFederativa, Municipio, Perfil
from django.contrib.auth.models import User
from fornecedores.models import Fornecedor
from django import forms

from utils.django_forms import *
from utils.validates_inputs import validate_cep, validate_cnpj, validate_cpf, validate_phone

class FornecedorForm(forms.ModelForm):
    # Criando novos atributos para o formulário de Fornecedor
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
        model = Fornecedor
        fields = [
            'imagem',
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'cpf',
            'telefone',
            'email',
            'site',
            'tipo_pessoa',
            'observacoes',
        ]
        # widgets = {
        #     'tipo_pessoa': forms.RadioSelect
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar form-control a todos os campos do formulário
        add_form_control(self)

        # Adicionar placeholders e atributos aos campos do formulário
        add_placeholder(self.fields['razao_social'], 'Digite a Razão Social')
        add_placeholder(self.fields['nome_fantasia'], 'Digite o Nome Fantasia')
        add_placeholder(self.fields['cpf'], 'Digite o CPF')
        add_placeholder(self.fields['cnpj'], 'Digite o CNPJ')
        add_placeholder(self.fields['email'], 'Digite o Email')
        add_placeholder(self.fields['site'], 'Digite o Site')
        add_placeholder(self.fields['telefone'], 'Digite o Telefone')
        add_placeholder(self.fields['observacoes'], 'Adicione observações sobre o fornecedor')
        add_placeholder(self.fields['endereco_cep'], 'Digite o CEP')
        add_placeholder(self.fields['endereco_logradouro'], 'Digite o Logradouro')
        add_placeholder(self.fields['endereco_numero'], 'Digite o Número')
        add_placeholder(self.fields['endereco_complemento'], 'Digite o Complemento')
        add_placeholder(self.fields['endereco_bairro'], 'Digite o Bairro')

        # Adicionar atributos específicos aos campos do formulário
        add_attr(self.fields['imagem'], 'class', 'form-control')
        # add_attr(self.fields['tipo_pessoa'], 'class', 'd-flex justify-content-around') # custom-select
        add_attr(self.fields['tipo_pessoa'], 'class', 'custom-select')
        # add_attr(self.fields['tipo_pessoa'], 'required', 'true')
        add_attr(self.fields['endereco_municipio'], 'class', 'custom-select')
        add_attr(self.fields['endereco_sigla'], 'class', 'custom-select')

        # Alterar o label dos campos de endereço
        rename_label(self.fields['endereco_cep'], 'CEP')
        rename_label(self.fields['endereco_logradouro'], 'Logradouro')
        rename_label(self.fields['endereco_numero'], 'Número')
        rename_label(self.fields['endereco_complemento'], 'Complemento')
        rename_label(self.fields['endereco_bairro'], 'Bairro')
        rename_label(self.fields['endereco_municipio'], 'Município')
        rename_label(self.fields['endereco_sigla'], 'UF')

    # Métodos de validação para os campos

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

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj and not validate_cnpj(cnpj):
            raise forms.ValidationError("CNPJ inválido.")
        return cnpj

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and not validate_cpf(cpf):
            raise forms.ValidationError("CPF inválido.")
        return cpf

    # Método de limpeza geral do formulário
    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get('tipo_pessoa')
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')

        if tipo_pessoa == 'fisica':
            if not cpf:
                self.add_error('cpf', 'CPF é obrigatório para pessoa física.')
            cleaned_data['cnpj'] = None  # Ignora CNPJ
        elif tipo_pessoa == 'juridica':
            if not cnpj:
                self.add_error('cnpj', 'CNPJ é obrigatório para pessoa jurídica.')
            cleaned_data['cpf'] = None  # Ignora CPF
        return cleaned_data

    def save(self, commit=True):
        is_create = self.instance.pk is None
        uf_obj = self.cleaned_data['endereco_sigla']
        imagem_upload = self.cleaned_data.get('imagem')

        fornecedor = super().save(commit=False)
        fornecedor.tipo_pessoa = self.cleaned_data['tipo_pessoa']
        fornecedor.cnpj = self.cleaned_data['cnpj']
        fornecedor.cpf = self.cleaned_data['cpf']
        fornecedor.razao_social = self.cleaned_data['razao_social']
        fornecedor.nome_fantasia = self.cleaned_data['nome_fantasia']
        fornecedor.email = self.cleaned_data['email']
        fornecedor.telefone = self.cleaned_data['telefone']
        fornecedor.site = self.cleaned_data['site']
        fornecedor.observacoes = self.cleaned_data['observacoes']

        if imagem_upload:
            fornecedor.imagem = imagem_upload

        if is_create:
            # Criar usuário e perfil apenas no create
            usuario = User(
                username=f"{self.cleaned_data['email']}-{uuid.uuid4().hex[:8]}"
            )
            usuario.set_password(get_random_string(8))
            fornecedor.status = 'ativo'
            fornecedor.usuario = usuario

            endereco = Endereco(
                cep=self.cleaned_data['endereco_cep'],
                logradouro=self.cleaned_data['endereco_logradouro'],
                numero=self.cleaned_data['endereco_numero'],
                complemento=self.cleaned_data['endereco_complemento'],
                bairro=self.cleaned_data['endereco_bairro'],
                municipio=self.cleaned_data['endereco_municipio'],
                uf=uf_obj.uf,
                sigla=uf_obj.sigla,
            )

            if commit:
                usuario.save()
                endereco.save()
                fornecedor.endereco = endereco
                fornecedor.save()
                Perfil.objects.create(usuario=usuario, tipo='fornecedor')
        else:
            # Atualizar endereço existente no update — não toca em User nem Perfil
            endereco = fornecedor.endereco
            endereco.cep = self.cleaned_data['endereco_cep']
            endereco.logradouro = self.cleaned_data['endereco_logradouro']
            endereco.numero = self.cleaned_data['endereco_numero']
            endereco.complemento = self.cleaned_data['endereco_complemento']
            endereco.bairro = self.cleaned_data['endereco_bairro']
            endereco.municipio = self.cleaned_data['endereco_municipio']
            endereco.uf = uf_obj.uf
            endereco.sigla = uf_obj.sigla

            if commit:
                endereco.save()
                fornecedor.save()

        return fornecedor
