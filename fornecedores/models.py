from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.utils import timezone
from authentication.models import Endereco
from django.db import models


# Atualização no modelo Fornecedor
class Fornecedor(models.Model):
    DEFAULT_IMAGE = 'fornecedores/user_default.jpeg'
    TIPO_PESSOA = [
        ('juridica', 'Jurídica'),
        ('fisica', 'Física')
    ]
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('bloqueado', 'Bloqueado'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    imagem = models.ImageField(upload_to='fornecedores/', blank=True, null=True, default=DEFAULT_IMAGE)
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social") # blank=True, null=True,
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nome Fantasia")
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True, verbose_name="CNPJ")
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name="CPF")
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    site = models.URLField(max_length=100, blank=True, null=True)
    tipo_pessoa = models.CharField(max_length=10, choices=TIPO_PESSOA, default='juridica')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name="Status")

    class Meta:
        db_table = 'sge_fornecedor'
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['usuario__username', 'razao_social']

    def __str__(self):
        return self.usuario.username

    @property
    def imagem_url(self):
        if self.imagem and self.imagem.name and self.imagem.storage.exists(self.imagem.name):
            return self.imagem.url
        return static('global/assets/img/user.jpeg')

    def _delete_old_image_if_replaced(self):
        if not self.pk:
            return
        try:
            old = Fornecedor.objects.get(pk=self.pk)
        except Fornecedor.DoesNotExist:
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

    def clean(self):
        if self.tipo_pessoa == 'fisica' and not self.cpf:
            raise ValidationError("CPF é obrigatório para pessoa física.")
        if self.tipo_pessoa == 'juridica' and not self.cnpj:
            raise ValidationError("CNPJ é obrigatório para pessoa jurídica.")