# 🛡️ ASPM - Vulnerability Management

## Ejecución paso a paso

### Opción 1: Con Docker Compose (recomendado)

1. Abre una terminal en la raíz del proyecto:

```bash
cd /workspaces/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software
docker-compose up --build
```

2. Accede a la aplicación en:

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

---

### Opción 2: Ejecución local manual

#### 1. Preparar el backend

```bash
cd /workspaces/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software/backend
cp .env.example .env
python3 -m pip install -r requirements.txt
```

#### 2. Iniciar PostgreSQL y Redis

```bash
cd /workspaces/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software
docker compose up -d db redis
```

#### 3. Inicializar base de datos y datos de prueba

```bash
cd backend
python3 scripts/manage.py init-db
python3 scripts/manage.py seed
```

#### 4. Ejecutar el backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 5. Ejecutar el frontend

En otra terminal:

```bash
cd /workspaces/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software/frontend
npm install
npm run dev
```

6. Abrir en el navegador:

- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

En el frontend puedes cambiar el estado de cada hallazgo directamente desde la tabla.

---

### Atajos útiles

- Inicializar base de datos:
  ```bash
  cd backend
  python3 scripts/manage.py init-db
  ```
- Agregar datos de prueba:
  ```bash
  cd backend
  python3 scripts/manage.py seed
  ```

