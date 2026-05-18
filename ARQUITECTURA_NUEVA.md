# 🏗️ Arquitectura - Secure Coding Dojo v2.0

## Visión General

Secure Coding Dojo v2.0 es una plataforma educativa modular basada en una arquitectura de **cliente-servidor** con separación clara de responsabilidades.

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIO                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
    ┌──────────────────────────────────────────┐
    │         FRONTEND (React + Vite)          │
    ├──────────────────────────────────────────┤
    │ • Dashboard Educativo                    │
    │ • Galería de Ejercicios                  │
    │ • Visor de Ejercicios Avanzado          │
    │ • Simulador Interactivo                  │
    │ • Gestión de Progreso (localStorage)     │
    └──────────────────┬───────────────────────┘
                       │ HTTP REST API
                       ▼
    ┌──────────────────────────────────────────┐
    │       BACKEND (FastAPI + Python)         │
    ├──────────────────────────────────────────┤
    │ • API Routes (CRUD)                      │
    │ • Simulador de Ataques                   │
    │ • Lógica de Negocio                      │
    │ • Validación de Payloads                 │
    └──────────────────┬───────────────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │    DATA (SQLite / PostgreSQL)            │
    ├──────────────────────────────────────────┤
    │ • Ejercicios                             │
    │ • Progreso del Usuario                   │
    │ • Lecciones                              │
    │ • Estadísticas                           │
    └──────────────────────────────────────────┘
```

## Stack Tecnológico

### Backend

```
FastAPI 0.104.1          # Framework web moderno
├─ Uvicorn              # Servidor ASGI
├─ SQLAlchemy 2.0       # ORM
├─ Pydantic 2.5         # Validación de datos
└─ Python 3.10+         # Lenguaje
```

### Frontend

```
React 18+              # Library UI
├─ Vite                # Build tool
├─ React Router        # Navegación
├─ Recharts            # Gráficos
├─ Lucide Icons        # Iconos
├─ react-hot-toast     # Notificaciones
└─ TailwindCSS         # CSS Framework
```

### Base de Datos

```
SQLite (Desarrollo)     # Rápido para desarrollo
PostgreSQL (Producción) # Escalable
```

## Estructura de Carpetas

### Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada
│   ├── core/
│   │   └── config.py                   # Configuración
│   ├── db/
│   │   ├── base.py                     # Base SQLAlchemy
│   │   └── session.py                  # Sesión DB
│   ├── models/
│   │   ├── challenge.py                # Modelos desafíos
│   │   └── finding.py                  # Modelos hallazgos
│   ├── schemas/
│   │   └── challenge.py                # Schemas Pydantic
│   ├── api/
│   │   └── routes/
│   │       ├── interactive_exercises.py  # Ejercicios (NUEVO)
│   │       ├── challenges_new.py         # Desafíos
│   │       ├── ingestion.py              # Ingesta datos
│   │       └── metrics.py                # Métricas
│   ├── services/
│   │   └── (servicios lógica negocio)
│   └── exercises/
│       ├── __init__.py
│       └── exercises_data.py            # Base datos ejercicios (NUEVO)
├── scripts/
│   ├── load_challenges.py
│   └── manage.py
├── Dockerfile
└── requirements.txt
```

### Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── EnhancedDashboard.jsx         # Dashboard (NUEVO)
│   │   ├── EnhancedDashboard.css
│   │   ├── EnhancedChallengeGallery.jsx  # Galería (NUEVO)
│   │   ├── EnhancedChallengeGallery.css
│   │   ├── AdvancedExerciseViewer.jsx    # Visor ejercicios (NUEVO)
│   │   ├── AdvancedExerciseViewer.css
│   │   ├── ChallengeGallery.jsx          # (Legacy)
│   │   ├── InteractiveExercise.jsx       # (Legacy)
│   │   └── ...
│   ├── api/
│   │   └── client.js                    # Cliente HTTP
│   ├── App.jsx                          # Componente raíz (ACTUALIZADO)
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── Dockerfile
├── package.json
├── vite.config.js
└── index.html
```

## Flujos de Datos

### 1. Cargar Lista de Ejercicios

```
Usuario abre app
    ↓
Frontend carga (EnhancedDashboard)
    ↓
GET /api/exercises/all
    ↓
Backend retorna lista JSON
    ↓
Frontend renderiza tarjetas
    ↓
Usuario ve 5+ ejercicios
```

### 2. Ver Detalles de Ejercicio

```
Usuario hace clic en ejercicio
    ↓
GET /api/exercises/exercise/{id}
    ↓
Backend retorna:
  - Explicación completa
  - Tipo de ataque
  - CVSS, OWASP, CWE
  - Objetivos de aprendizaje
    ↓
Frontend renderiza en tabs:
  - Explanation
  - Attack
  - Code
  - Simulator
  - Countermeasures
```

### 3. Probar Ataque (Simulador)

```
Usuario ingresa payload
    ↓
POST /api/exercises/exercise/{id}/test-attack
    ↓
Backend:
  1. Valida formato del payload
  2. Detecta patrones de ataque
  3. Crea retroalimentación educativa
  4. Retorna resultado
    ↓
Frontend muestra:
  - ✅ Éxito o ❌ Fallo
  - Explicación técnica
  - Por qué funcionó
  - Lección educativa
```

### 4. Obtener Pistas Progresivas

```
Usuario hace clic "Get Hint"
    ↓
GET /api/exercises/exercise/{id}/hints?hints_used=1
    ↓
Backend retorna:
  - Pista nivel 1
  - Pista nivel 2
  - Pista nivel 3 (si disponible)
    ↓
Frontend renderiza pistas con
número creciente de información
```

## Modelos de Datos

### Exercise (Ejercicio)

```python
{
  "id": UUID,
  "title": str,                    # "SQL Injection en Login"
  "short_title": str,              # "SQL Injection"
  "description": str,              # Descripción corta
  "difficulty": "BEGINNER|INTERMEDIATE|ADVANCED",
  "vulnerability_type": "SQL_INJECTION|XSS|...",
  "attack_type": "INJECTION|CROSS_SITE|...",
  
  # Contenido educativo
  "vulnerability_explanation": str,
  "attack_explanation": str,
  "real_world_impact": str,
  "countermeasures": str,
  "best_practices": str,
  "learning_objectives": [str],
  
  # Código
  "vulnerable_code": str,
  "vulnerable_code_language": "python|javascript|...",
  "vulnerable_code_explanation": str,
  
  "secure_code": str,
  "secure_code_language": "python|javascript|...",
  "secure_code_explanation": str,
  
  # Seguridad
  "cvss_score": float,  # 0-10
  "owasp_top_10": str,  # "A03:2021"
  "cwe_id": str,        # "CWE-89"
  "cwe_description": str,
  
  # Pistas
  "hint_1": str,
  "hint_2": str,
  "hint_3": str,
  
  # Metadatos
  "icon": str,          # "🔓"
  "color": str,         # "red"
  "difficulty_order": int,
  "is_active": bool,
  
  # Timestamps
  "created_at": datetime,
  "updated_at": datetime
}
```

### UserProgress (Progreso Usuario)

```python
{
  "id": UUID,
  "user_id": str,           # Identificador único del usuario
  "challenge_id": UUID,     # Referencia al ejercicio
  "is_completed": bool,
  "attempts": int,          # Número de intentos
  "hints_used": int,        # Pistas utilizadas
  "user_answer": str,       # Respuesta del usuario
  "is_correct": bool,
  "score": int,             # Puntuación 0-100
  "started_at": datetime,
  "completed_at": datetime,
  "time_spent_seconds": int,
}
```

## Componentes React

### EnhancedDashboard
**Ubicación:** `frontend/src/components/EnhancedDashboard.jsx`

Responsabilidades:
- Mostrar estadísticas globales
- Visualizar gráficos (Pie, Bar)
- Mostrar ruta de aprendizaje
- Features de la plataforma
- Call-to-action a ejercicios

Props:
- `onNavigateToExercises`: Callback para navegar

### EnhancedChallengeGallery
**Ubicación:** `frontend/src/components/EnhancedChallengeGallery.jsx`

Responsabilidades:
- Listar todos los ejercicios
- Filtrar por dificultad
- Búsqueda de ejercicios
- Mostrar estadísticas
- Manejo de clic en ejercicio

Props:
- `onSelectChallenge`: Callback con ID del ejercicio

### AdvancedExerciseViewer
**Ubicación:** `frontend/src/components/AdvancedExerciseViewer.jsx`

Responsabilidades:
- Mostrar detalles completos del ejercicio
- 5 tabs educativos
- Simulador interactivo
- Sistema de pistas
- Temporizador y contador de intentos

Props:
- `exerciseId`: ID del ejercicio
- `onBack`: Callback para volver

## API Endpoints

### GET Endpoints

```
GET /api/exercises/all
├─ Retorna: {total, exercises[]}
└─ Uso: Listar todos los ejercicios

GET /api/exercises/exercise/{id}
├─ Retorna: Detalles completos del ejercicio
└─ Uso: Ver detalles antes de empezar

GET /api/exercises/exercise/{id}/code
├─ Retorna: {vulnerable{}, secure{}}
└─ Uso: Mostrar comparación de código

GET /api/exercises/exercise/{id}/hints?hints_used={n}
├─ Retorna: {hints[], next_hint_level}
└─ Uso: Obtener pistas progresivas

GET /api/exercises/statistics
├─ Retorna: {total, by_difficulty{}, by_vulnerability{}, average_cvss}
└─ Uso: Datos para dashboard

GET /api/exercises/progression
├─ Retorna: {levels}
└─ Uso: Estructura de progresión
```

### POST Endpoints

```
POST /api/exercises/exercise/{id}/test-attack
├─ Body: {input: "payload"}
├─ Retorna: {success, message, details, educational_insight}
└─ Uso: Probar ataque en simulador
```

## Simulador de Ataques

### Algoritmo de Validación

```python
def simulate_attack(exercise_id, payload, exercise):
    if exercise_id == "1_sql_injection_login":
        dangerous_patterns = ["' --", "' OR", "UNION SELECT", ...]
        if matches_pattern(payload, dangerous_patterns):
            return SUCCESS
        return FAIL
    
    elif exercise_id == "2_xss_comment_section":
        xss_patterns = ["<script", "onerror", "onload", ...]
        if matches_pattern(payload.lower(), xss_patterns):
            return SUCCESS
        return FAIL
    
    # ... más ejercicios
```

### Retroalimentación Educativa

Cada resultado incluye:

1. **Mensaje**: ✅ Éxito o ❌ Fallo
2. **Detalles**: Por qué funcionó/no funcionó
3. **Lección**: Explicación educativa
4. **Contexto**: Relación con defensa

Ejemplo:
```json
{
  "success": true,
  "message": "✅ ¡ATAQUE EXITOSO! SQL Injection detectado.",
  "details": "El payload 'admin' --' contiene un patrón válido",
  "educational_insight": "Este payload exploita porque..."
}
```

## Seguridad

### En Desarrollo

```python
# frontend/.env
VITE_API_URL=http://localhost:8000

# backend/.env
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

### En Producción

```python
# Recomendaciones:
DEBUG=False
CORS_ORIGINS=["https://tu-dominio.com"]

# Agregar:
- Autenticación JWT
- Rate limiting (slowapi)
- HTTPS obligatorio
- Headers de seguridad (CORSMiddleware)
- Validación de entrada robusta
- Logging de intentos
```

## Performance

### Frontend

- **Code Splitting**: Componentes cargados on-demand
- **Lazy Loading**: Imágenes y gráficos
- **Caché**: localStorage para datos estáticos
- **Optimización**: Memoization de componentes

### Backend

- **Caching**: Redis para datos frecuentes
- **Indexación**: DB con índices en búsquedas
- **Async**: Todas las rutas son async
- **Connection Pooling**: SQLAlchemy

## Escalabilidad Futura

### Fase 2
- [ ] Autenticación de usuarios
- [ ] Persistencia de progreso en BD
- [ ] Sistema de badges y certificados
- [ ] Leaderboard (opcional)
- [ ] Comentarios en ejercicios

### Fase 3
- [ ] Más ejercicios (10+)
- [ ] Videos educativos integrados
- [ ] Quizzes y evaluaciones
- [ ] API de terceros (CVSS)

### Fase 4
- [ ] Machine Learning para recomendaciones
- [ ] Análisis de dificultad dinámica
- [ ] Reportes personalizados
- [ ] Integración con LMS

## Testing

### Propuesto

```bash
# Backend
pytest backend/tests/

# Frontend
npm run test

# E2E
npm run test:e2e
```

## Deployment

### Docker

```dockerfile
# Backend
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

# Frontend
FROM node:18-slim
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

**Diseño modular, educativo y escalable** ✨
