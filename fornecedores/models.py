from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from authentication.models import Endereco
from django.db import models


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