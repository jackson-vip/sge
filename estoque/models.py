from django.db import models
from django.core.exceptions import ValidationError
from produtos.models import Produto
from django.contrib.auth.models import User

class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída')
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário Responsável")

    class Meta:
        db_table = 'sge_movimentacao_estoque'
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        if self.tipo == 'saida':
            estoque_atual = self.produto.quantidade
            if self.quantidade > estoque_atual:
                raise ValidationError(f"Estoque insuficiente para o produto {self.produto.nome}. Quantidade disponível: {estoque_atual}.")
            self.produto.quantidade -= self.quantidade
        elif self.tipo == 'entrada':
            self.produto.quantidade += self.quantidade
        self.produto.save()
        super().save(*args, **kwargs)
