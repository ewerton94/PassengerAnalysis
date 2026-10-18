# Frontend - Análise de dados de passageiros

SPA **Vue 3 + Quasar 2 (Vite) + Pinia**.

Requer **Node.js ≥ 20**.

## Install

```bash
cd frontend
npm install
```

Copie `.env.example` para `.env` e, se for usar mapa de calor, preencha `GoogleMapsKey`.

## Dev

```bash
npm run dev
```

Abre em `http://localhost:8080/`. A API esperada é `http://localhost:8000/` (veja `src/config/constants.js`).

Use o usuário criado com `createsuperuser` no backend.

## Build

```bash
npm run build
```

Saída em `dist/spa/`.

## Lint

```bash
npm run lint
```
