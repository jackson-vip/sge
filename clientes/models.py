from datetime import date
from django.db import models

# Importando o modelo User do Django
from django.contrib.auth.models import User
from authentication.models import Endereco

# Create your models here.

# Atualização no modelo Usuario
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    imagem = models.ImageField(upload_to='clientes/', blank=True, null=True, default='clientes/user.jpeg')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
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
        return f"{self.usuario.first_name} {self.usuario.last_name}".strip()

    @property
    def idade(self):
        if self.data_nascimento:
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None
    
    @property
    def tempo_para_aniversario(self):
        if not self.data_nascimento:
            return None

        hoje = date.today()
        # Próximo aniversário neste ano
        proximo = self.data_nascimento.replace(year=hoje.year)
        # Se já passou, pega do ano seguinte
        if proximo < hoje:
            proximo = proximo.replace(year=hoje.year + 1)
        delta = proximo - hoje

        # Calcula meses e dias restantes
        meses = (proximo.year - hoje.year) * 12 + proximo.month - hoje.month
        if proximo.day < hoje.day:
            meses -= 1
            dias = (proximo - proximo.replace(day=1)).days + proximo.day - hoje.day
        else:
            dias = proximo.day - hoje.day

        return {'meses': meses, 'dias': dias, 'total_dias': delta.days}