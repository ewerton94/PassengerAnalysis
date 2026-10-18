# Análises de dados de passageiros

![Dashboard](print.png "Dashboard")

Trabalho de Conclusão de Curso de Engenharia Civil da Universidade Federal de Alagoas.

**Resumo do projeto (com prints e link do TCC):** [portfolio/RESUMO-PROJETO.md](portfolio/RESUMO-PROJETO.md)

## Estrutura

```
  ├── ArquivosEntrada
  ├── Resultados
  ├── ScriptsIniciais
  ├── backend          # Django 5.2 + DRF
  └── frontend         # Vue 3 + Quasar 2
```

## Rodar a aplicação web localmente

Pré-requisitos: **Python 3.12**, **Node.js ≥ 20**, **PostgreSQL**.

### Backend

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
copy backend\conf\secret.example.py backend\conf\secret.py
# edite secret.py com a senha do Postgres e crie o DB passenger_analysis
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Detalhes: [backend/README.md](backend/README.md).

### Frontend

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Detalhes: [frontend/README.md](frontend/README.md).

## Arquivos de entrada / scripts

[Sistema GoolSystem](https://gool.cittati.com.br/Login.aspx?ReturnUrl=%2f) e [ReportCenter](http://mrc.maceio.prodatamobility.com.br/) fornecem os dados brutos.

Os scripts em `ScriptsIniciais/` (`main.py`, `open_mrc_detail.py`, `consolidate_mrc_detail.py`, `find_local_pass.py`) cuidam da ingestão offline e são independentes do stack web atualizado.

## Contribuindo

Verifique issues abertas e envie mudanças via pull request.
