from django.db import models
from django.contrib.auth.models import User


class Escopo(models.Model):
    nome = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.nome


class LogAcesso(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='logs_acesso',
        null=True,
        blank=True,
    )
    url = models.TextField()
    permissao = models.CharField(max_length=500, blank=True, default='')
    metodo = models.CharField(max_length=20, blank=True, default='')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.metodo} {self.url}'
