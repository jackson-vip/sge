from django.db import models
from django.contrib.auth.models import User

class LogSistema(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    acao = models.CharField(max_length=255, verbose_name="Ação")
    tabela_afetada = models.CharField(max_length=255, verbose_name="Tabela Afetada", blank=True, null=True)
    registro_id = models.CharField(max_length=255, verbose_name="ID do Registro Afetado", blank=True, null=True)
    detalhes = models.TextField(verbose_name="Detalhes", blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")

    class Meta:
        db_table = 'sge_log_sistema'
        verbose_name = "Log do Sistema"
        verbose_name_plural = "Logs do Sistema"
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.data_hora} - {self.acao}"