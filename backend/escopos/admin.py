from django.contrib import admin
from .models import Escopo, LogAcesso


@admin.register(Escopo)
class EscopoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)


@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'metodo', 'url', 'criado_em')
    list_filter = ('metodo',)
    search_fields = ('url', 'permissao', 'usuario__username')
