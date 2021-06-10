import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
import django
django.setup()
import pandas as pd
from core.models import Linha, Empresa, Carro, ViagemDePassageiro, Cartao , TipoCartao, Trecho, Partida, Ponto, PontoPorEmpresa, ViagemDePassageiro
from escopos.models import Escopo
import warnings
warnings.filterwarnings('ignore')

escopo, _ = Escopo.objects.get_or_create(
    nome='Imperatriz-00-7YhfYgclÇs'
)

#Lendo os dataframes

#janeiro = pd.read_excel('Janeiro de 2020.xlsx')

#Passando para pickle

#janeiro.to_pickle('pass_jan.zip' , compression = 'zip')

#Lendo as informações do dataframe geral

df = pd.read_pickle('pass.zip', compression='zip')


#Lendo as informações do dataframe com informações de janeiro de 2020

janeiro = pd.read_pickle('pass_jan.zip', compression='zip')


#Efetuando a mescla de dataframes (apenas os comuns)

mescla = df.merge(janeiro[['TurnoID', 'Prefixo']].drop_duplicates(), how='inner', on='TurnoID')
mescla['Linha'] = mescla['Linha'].astype(str).str.replace('.0', '')


#Adição da ida/volta

mescla = mescla.merge(janeiro[['TurnoID', 'Sentido']].dropna().drop_duplicates(), how='inner', on='TurnoID')
mescla['Sentido'][mescla['Sentido'] == 'I'] = 'ida'
mescla['Sentido'][mescla['Sentido'] == 'V'] = 'volta'

#mescla['Prefixo'] = mescla['Prefixo'].astype(str)


#Arredondamento latitude e Longitude

for i in ['latitude', 'Longitude', 'Latitude9', 'longitude10']:
    mescla[i] = mescla[i]/10000000
    mescla[i] = mescla[i].round(4)
    
mescla['HoraEmbarque'] = mescla['InicioTurno'].dt.date.astype('str') + ' ' + mescla['HoraEmbarque']
mescla['HoraDesembarque'] = mescla['InicioTurno'].dt.date.astype('str') + ' ' + mescla['HoraDesembarque']


# Criando empresa

empresa, _ = Empresa.objects.get_or_create(
    nome_oficial='Imperatriz',
    nome_cittamobi='Imperatriz',
    nome_report='Imperatriz',
    lote='000',
    abreviacao='IMP',
    ativa=True,
    valor_km=0,
    escopo=escopo
)

numeros_da_linhas = mescla['Linha'].astype(str).str.replace('.0', '').unique()

numeros_carros = mescla['Prefixo'].astype(str).unique()


# Criando Linhas

linhas_a_criar = []
for n_linha in numeros_da_linhas:
    linha = Linha(
        numero=n_linha,
        nome=n_linha,
        empresa=empresa,
        escopo=escopo
    )
    linhas_a_criar.append(linha)
Linha.objects.bulk_create(linhas_a_criar)


#Adicionando os carro no banco de dados

carros = []
for carro in numeros_carros:
    prefixo = Carro(
        empresa=empresa,
        numero=carro,
    )
    carros.append(prefixo)
Carro.objects.bulk_create(carros)


#Junção das informações - Trecho

trechos_df = mescla['Descricao2'].append(mescla['Descricao8']).unique()


#Salvando os trechos

trecho_saving=[]

for i in trechos_df:
    trechos = Trecho(
        nome=i
    )
    trecho_saving.append(trechos)
Trecho.objects.bulk_create(trecho_saving)


# Criando tipo de cartão
tipo_cartao, _ = TipoCartao.objects.get_or_create(
    tipo='Comum',
    valor='3,00',
)


#Adição dos cartões dos passageiros

cartoes_list = []

for cartao in mescla['NumSerie'].unique():
    cartoes = Cartao(
        numero=cartao,
        tipo=tipo_cartao,
    )
    cartoes_list.append(cartoes)
Cartao.objects.bulk_create(cartoes_list)

partidas_df = mescla.groupby(['TurnoID','InicioTurno','Linha','servico','Prefixo','Sentido'], as_index = False).min()[['TurnoID','InicioTurno','Linha','servico','Prefixo','HoraEmbarque','Sentido']]
partidas_df['Linha'] = partidas_df['Linha'].astype(str).str.replace('.0', '')


#Criação dos dicionários

linha_dict = {l.numero: l for l in Linha.objects.all()}
carro_dict = {l.numero: l for l in Carro.objects.all()}

# for linha, df_linha in partidas_df.groupby('Linha'):
#Adição de Partida

partida_saving = []

for viagem in partidas_df.index.values:
    partidas = Partida(
        linha=linha_dict[partidas_df.loc[viagem, ('Linha')]],
        carro=carro_dict[partidas_df.loc[viagem, ('Prefixo')].astype('str')],
        #horario_prevista_terminal = partidas_df.loc[viagem,('InicioTurno')],
        horario_realizada_terminal=partidas_df.loc[viagem, ('InicioTurno')],
        sentido=partidas_df.loc[viagem, ('Sentido')],
    )
    partida_saving.append(partidas)
Partida.objects.bulk_create(partida_saving)


#Correção das latlon

pontos_df = mescla[['Descricao2', 'latitude', 'Longitude']]

pontos_df_2 = mescla[['Descricao8', 'Latitude9', 'longitude10']]

pontos_df_2.columns = ['Descricao2', 'latitude', 'Longitude']

pontos_df = pontos_df.append(pontos_df_2)

pontos_df = pontos_df.drop_duplicates().reset_index(drop=True)


#Adição dos pontos

pontos_saving=[]
trecho_dict = {l.nome: l for l in Trecho.objects.all()}

for i in pontos_df.index.values:
    pontos = Ponto(
    lat=pontos_df.loc[i, 'latitude'],
    lon=pontos_df.loc[i, 'Longitude'],
    trecho=trecho_dict[pontos_df.loc[i, 'Descricao2']],
    )
    pontos_saving.append(pontos)
pontos = Ponto.objects.bulk_create(pontos_saving)


#Ponto por empresa

ponto_empresa_sav = []
pontos_dict = {(l.lat, l.lon): l for l in pontos}

for i in pontos_df.index.values:
    pontos = PontoPorEmpresa(
        ponto=pontos_dict[(pontos_df.loc[i, 'latitude'], pontos_df.loc[i, 'Longitude'])],
        empresa=Empresa.objects.all()[0],
    )
    ponto_empresa_sav.append(pontos)
PontoPorEmpresa.objects.bulk_create(ponto_empresa_sav)   


#Adição de viagem por passageiro

linha_dict = {l.nome: l for l in Linha.objects.all()}
cartao_dict = {l.numero: l for l in Cartao.objects.all()}
ponto_dict = {(l.ponto.lat, l.ponto.lon): l for l in PontoPorEmpresa.objects.select_related().all()}
partida_dict = {(l.carro.numero, pd.to_datetime(l.horario_realizada_terminal, utc=False)): l for l in Partida.objects.all()}


#Adição das viagens por passageiro

passageiros_saving = []

for i in mescla.index.values:
    pontos = ViagemDePassageiro(
        linha=linha_dict[mescla.loc[i, 'Linha']],
        cartao=cartao_dict[mescla.loc[i, 'NumSerie'].astype('str')],
        ponto_embarque=ponto_dict[mescla.loc[i, 'latitude'],mescla.loc[i, 'Longitude']],
        ponto_desembarque=ponto_dict[mescla.loc[i, 'Latitude9'], mescla.loc[i, 'longitude10']],
        partida_embarque=partida_dict[(mescla.loc[i,'Prefixo'].astype('str'), pd.to_datetime(mescla.loc[i, 'InicioTurno'], utc=True))],
        partida_desembarque=partida_dict[(mescla.loc[i,'Prefixo'].astype('str'),pd.to_datetime(mescla.loc[i, 'InicioTurno'], utc=True))],
        horario=mescla.loc[i, 'HoraEmbarque'],
        horario_desembarque=mescla.loc[i, 'HoraDesembarque']
    )
    passageiros_saving.append(pontos)
print('Sanvando viagens no banco...')
ViagemDePassageiro.objects.bulk_create(passageiros_saving)

print('Finalizado!')
