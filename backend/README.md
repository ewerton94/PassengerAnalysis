## Backend - Análises de dados de passageiros

API Django REST Framework com PostgreSQL. Stack alvo: **Python 3.12** + **Django 5.2 LTS**.

### Testando localmente

```powershell
cd backend
```

#### Primeira vez

1. Crie um venv com Python 3.12 na raiz do repositório (se ainda não existir):

```powershell
cd ..
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
```

2. Instale/configure o PostgreSQL e crie o banco `passenger_analysis`.

3. Copie `conf/secret.example.py` para `conf/secret.py` e ajuste `SECRET_KEY`, usuário e senha do Postgres.

4. Aplique migrations:

```powershell
python manage.py migrate
```

5. Crie um superusuário:

```powershell
python manage.py createsuperuser
```

6. No admin (`http://127.0.0.1:8000/admin/`), crie um **Escopo** e um **Usuario** (`core.Usuario`) associado ao seu user Django.

#### Rodar o servidor

```powershell
python manage.py runserver
```

- API / Swagger UI: `http://127.0.0.1:8000/`
- OpenAPI schema: `http://127.0.0.1:8000/schema/`
- Login: `POST /entrar/` com `{ "username", "password" }` → retorna `token` DRF
