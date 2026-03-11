from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import models
from django.templatetags.static import static
from django.utils import timezone

# Importando o modelo User do Django
from django.contrib.auth.models import User
from authentication.models import Endereco

# Create your models here.

# Atualização no modelo Usuario
class Cliente(models.Model):
    DEFAULT_IMAGE = 'clientes/user.jpeg'

    usuario = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    imagem = models.ImageField(upload_to='clientes/', blank=True, null=True, default=DEFAULT_IMAGE)
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
    def imagem_url(self):
        if self.imagem and self.imagem.name and self.imagem.storage.exists(self.imagem.name):
            return self.imagem.url
        return static('global/assets/img/user.jpeg')

    def _delete_old_image_if_replaced(self):
        if not self.pk:
            return
        try:
            old = Cliente.objects.get(pk=self.pk)
        except Cliente.DoesNotExist:
            return

        old_name = old.imagem.name if old.imagem else ''
        new_name = self.imagem.name if self.imagem else ''
        if old_name and old_name != new_name and old_name != self.DEFAULT_IMAGE:
            storage = old.imagem.storage
            if storage.exists(old_name):
                storage.delete(old_name)

    def save(self, *args, **kwargs):
        if self.data_cadastro and timezone.is_naive(self.data_cadastro):
            self.data_cadastro = timezone.make_aware(
                self.data_cadastro,
                timezone.get_current_timezone(),
            )
        self._delete_old_image_if_replaced()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.imagem and self.imagem.name and self.imagem.name != self.DEFAULT_IMAGE:
            storage = self.imagem.storage
            if storage.exists(self.imagem.name):
                storage.delete(self.imagem.name)
        super().delete(*args, **kwargs)

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
        total_dias = delta.days
        
        # Flag: aniversário é hoje
        is_hoje = (hoje.month == self.data_nascimento.month and 
                   hoje.day == self.data_nascimento.day)
        
        # Total de horas até meia-noite do próximo aniversário
        total_horas = total_dias * 24
        
        # Semanas completas e dias restantes
        semanas = total_dias // 7
        dias_semana = total_dias % 7
        
        # Meses e dias restantes usando relativedelta
        rd = relativedelta(proximo, hoje)
        meses = rd.months
        dias_mes = rd.days

        return {
            'total_dias': total_dias,
            'total_horas': total_horas,
            'semanas': semanas,
            'dias_semana': dias_semana,
            'meses': meses,
            'dias_mes': dias_mes,
            'is_hoje': is_hoje,
            'data': proximo,
        }