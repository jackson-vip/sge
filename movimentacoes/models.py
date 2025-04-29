from django.db import models
from produtos.models import Produto

# Removida a classe Fornecedor deste arquivo, pois foi movida para o app authentication.

class Pedido(models.Model):
    STATUS_PEDIDO = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado')
    ]

    fornecedor = models.ForeignKey('authentication.Fornecedor', on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='PedidoProduto')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO, default='pendente')

    class Meta:
        db_table = 'sge_pedido'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']

    def __str__(self):
        return f"Pedido {self.id} - {self.status.capitalize()}"

class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sge_pedido_produto'
        verbose_name = "Produto do Pedido"
        verbose_name_plural = "Produtos dos Pedidos"

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"
