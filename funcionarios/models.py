from django.db import models
from django.contrib.auth.models import User
from authentication.models import Endereco
import uuid

# Create your models here.


class Funcionario(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('bloqueado', 'Bloqueado'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='funcionarios/', blank=True, null=True, default='funcionarios/default.png')
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departamento")
    data_contratacao = models.DateField(verbose_name="Data de Contratação")
    matricula = models.CharField(max_length=20, unique=True, blank=True, null=False, verbose_name="Matrícula")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=12, unique=True, blank=True, null=True, verbose_name="RG")
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salário")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")
    email_profissional = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name="Status")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        db_table = 'sge_funcionario'
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['usuario__username']

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo}"
    
    def save(self, *args, **kwargs):
        if not self.matricula:
            # Gera uma matrícula única (exemplo: 8 dígitos hexadecimais)
            self.matricula = uuid.uuid4().hex[:8].upper()
            # Garante unicidade
            while Funcionario.objects.filter(matricula=self.matricula).exists():
                self.matricula = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)