from django.contrib.auth.models import User
from django.db import models


class UnidadeFederativa(models.Model):
    uf = models.CharField(verbose_name='UF', max_length=100)
    sigla = models.CharField(verbose_name='Sigla', max_length=2, unique=True)

    class Meta:
       db_table = 'sge_unidade_federativa'
       ordering = ['sigla']
       verbose_name = 'Unidade Federativa'
       verbose_name_plural = 'Unidades Federativas'

    def __str__(self):
        return self.sigla
    
class Municipio(models.Model):
    id_uf = models.ForeignKey(UnidadeFederativa, on_delete=models.RESTRICT, related_name='uf_municipios', db_column='id_uf')
    municipio = models.CharField(verbose_name="Municipio", max_length=150)
    codigo_ibge = models.CharField(verbose_name='Código IBGE', max_length=10, unique=True)
    uf = models.CharField(verbose_name='UF', max_length=2)
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14, unique=True)
    codigo_siafi = models.CharField(verbose_name='Código SIAFI', max_length=7, unique=True)

    class Meta:
        db_table = 'sge_municipio'
        ordering = ['municipio']
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'
    
    def __str__(self):
        return f"{self.municipio} - {self.uf}"

class Endereco(models.Model):
    TIPO_ENDERECO = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial')
    ]

    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='enderecos', verbose_name='Município')
    uf = models.CharField(max_length=20, verbose_name='UF')
    sigla = models.CharField(max_length=2, verbose_name='Sigla')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    tipo_endereco = models.CharField(max_length=50, choices=TIPO_ENDERECO, default='residencial')

    class Meta:
        db_table = 'sge_endereco'
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ['logradouro', 'numero']

    def __str__(self):
        return f"{self.logradouro}, {self.numero}"

        
class Perfil(models.Model):
    TIPOS_PERFIL = [
        ('administrador', 'Administrador'),
        ('fornecedor', 'Fornecedor'),
        ('funcionario', 'Funcionário'),
        ('cliente', 'Cliente')
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_PERFIL)

    class Meta:
        db_table = 'sge_perfil'
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"

