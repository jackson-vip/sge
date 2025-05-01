from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'sge_categoria'
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    UNIDADE_MEDIDA = [
        ('un', 'Unidade'),
        ('kg', 'Quilograma'),
        ('g', 'Grama'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('mm', 'Milímetro'),
        ('pacote', 'Pacote'),
        ('caixa', 'Caixa'),
        ('saco', 'Saco'),
        ('outro', 'Outro')
    ]

    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=0)
    quantidade_minima = models.PositiveIntegerField(default=0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20, choices=UNIDADE_MEDIDA, default='unidade')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    fornecedor_id = models.ForeignKey('authentication.Fornecedor', on_delete=models.SET_NULL, null=True, blank=True, name='fornecedor')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sge_produto'
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.codigo}) - R$ {self.preco_venda:.2f}"

    def clean(self):
        if self.preco_venda < self.preco_custo:
            raise ValidationError('O preço de venda não pode ser inferior ao preço de custo.')

    def verificar_estoque_minimo(self):
        if self.quantidade < self.quantidade_minima:
            return f"Atenção: O estoque do produto {self.nome} está abaixo do mínimo ({self.quantidade_minima})."
        return None

    def save(self, *args, **kwargs):
        alerta_estoque = self.verificar_estoque_minimo()
        if alerta_estoque:
            # Aqui você pode implementar lógica para enviar notificações ou logs
            print(alerta_estoque)
        super().save(*args, **kwargs)