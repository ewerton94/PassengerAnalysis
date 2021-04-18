import os
import pandas as pd
import numpy as np
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

import django
django.setup()

from core.models import ViagemDePassageiro
from core.dataframe import ViagensVazias, get_order_trecho


def calcular_sobreposicao(self=None):
    '''
    Exemplo de cálculo de Sobreposição:
    '''
    df = self.get_df()
    df.columns = ['ponto', 'trecho', 'partida', 'sentido', 'linha', 'sc', 'eixo', 'km_ida', 'km_volta', 'custo_por_km', 'receita']
    df = df[~pd.isnull(df.ponto)]
    results = []
    for linha1, df1 in df.groupby('linha'):
        pontos_linha1 = df1.trecho.unique()
        for linha2, df2 in df.groupby('linha'):
            pontos_linha2 = df2.trecho.unique()
            total = len(np.unique(np.union1d(pontos_linha1, pontos_linha2)))
            inter = len(np.intersect1d(pontos_linha1, pontos_linha2, assume_unique=True))
            results.append((linha1, linha2, inter/total))
    df = pd.DataFrame(results, columns=['Linha 1', 'Linha 2', 'sobreposicao'])
    return df


# Liste alguns códigos de linhas
linhas = ['068', '069', '716']
# Filtrar linhas pelo código:
viagens = ViagemDePassageiro.objects.filter(
    partida_embarque__linha__numero__in=linhas
).filter(
    horario__year__gte=2020
)
# Crie uma instância da classe ViagensVazias (Ou outra classe definida)
vv = ViagensVazias(viagens)
df = calcular_sobreposicao(self=vv)
