from django.db import models
from produtos.models import Produto

# Removida a classe Fornecedor deste arquivo, pois foi movida para o app authentication.

class Pedido(models.Model):
    STATUS_PEDIDO = [
        ('pendente', 'Pendente'),
        ('em processamento', 'Em Processamento'),
        ('aguardando pagamento', 'Aguardando Pagamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('entregue', 'Entregue')
    ]

    fornecedor = models.ForeignKey('authentication.Fornecedor', on_delete=models.CASCADE)
    cliente = models.ForeignKey('authentication.Cliente', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_PEDIDO, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Total")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        db_table = 'sge_pedido'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']

    def __str__(self):
        return f"Pedido {self.id} - {self.status.capitalize()}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sge_item_pedido'
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"
