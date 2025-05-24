from django.db import models
from django.contrib.auth.models import User
from authentication.models import Endereco

# Create your models here.


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