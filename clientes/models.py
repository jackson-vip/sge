from django.db import models

# Importando o modelo User do Django
from django.contrib.auth.models import User
from authentication.models import Endereco

# Create your models here.

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