from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


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
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='enderecos')
    uf = models.CharField(max_length=20)
    sigla = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    tipo_endereco = models.CharField(max_length=50, choices=TIPO_ENDERECO, default='residencial')

    class Meta:
        db_table = 'sge_endereco'
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ['logradouro', 'numero']

    def __str__(self):
        return f"{self.logradouro}, {self.numero}"
    
# Atualização no modelo Usuario
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    imagem = models.ImageField(upload_to='clientes/', blank=True, null=True, default='clientes/default.png')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    status = models.CharField(max_length=20, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo'), ('bloqueado', 'Bloqueado')], default='ativo', verbose_name="Status")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        db_table = 'sge_cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['usuario__username']

    def __str__(self):
        return self.usuario.username

# Atualização no modelo Fornecedor
class Fornecedor(models.Model):
    TIPO_PESSOA = [
        ('fisica', 'Pessoa Física'),
        ('juridica', 'Pessoa Jurídica')
    ]

    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='fornecedores/', blank=True, null=True, default='fornecedores/default.png')
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome Fantasia")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name="CNPJ")
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name="CPF")
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    site = models.URLField(max_length=100, blank=True, null=True)
    tipo_pessoa = models.CharField(max_length=10, choices=TIPO_PESSOA, default='juridica')

    class Meta:
        db_table = 'sge_fornecedor'
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['usuario__username', 'razao_social']

    def __str__(self):
        return self.usuario.username

    def clean(self):
        if self.tipo_pessoa == 'fisica' and not self.cpf:
            raise ValidationError("CPF é obrigatório para pessoa física.")
        if self.tipo_pessoa == 'juridica' and not self.cnpj:
            raise ValidationError("CNPJ é obrigatório para pessoa jurídica.")

# Atualização no modelo Funcionario
class Funcionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='funcionarios/', blank=True, null=True, default='funcionarios/default.png')
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    data_contratacao = models.DateField()
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=12, unique=True, blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    email_profissional = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = 'sge_funcionario'
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['usuario__username']

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"

class Perfil(models.Model):
    TIPOS_PERFIL = [
        ('administrador', 'Administrador'),
        ('fornecedor', 'Fornecedor'),
        ('funcionario', 'Funcionário')
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_PERFIL)

    class Meta:
        db_table = 'sge_perfil'
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"

