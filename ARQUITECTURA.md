# 🏗️ Arquitectura - Secure Coding Dojo

## 📐 Diagrama de Arqueología General

```
┌─────────────────────────────────────────────────────────────┐
│                     Usuario Final                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                  🌐 FRONTEND (React + Vite)                 │
│         ┌────────────────────────────────────────┐          │
│         │  Dashboard Educativo                   │          │
│         │  - Ruta de Aprendizaje                 │          │
│         │  - Estadísticas Globales               │          │
│         │  - Desafíos por Dificultad             │          │
│         └────────────────────────────────────────┘          │
│                       │                                       │
│         ┌────────────────────────────────────────┐          │
│         │  Challenge Editor                      │          │
│         │  - Código Vulnerable                   │          │
│         │  - Código Seguro                       │          │
│         │  - Sistema de Pistas                   │          │
│         │  - Input de Respuestas                 │          │
│         └────────────────────────────────────────┘          │
│                       │                                       │
│                    Axios / REST                              │
│                       │                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                🐍 BACKEND (FastAPI)                          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              API Routes                             │  │
│  │  ├─ /api/challenges/                               │  │
│  │  ├─ /api/challenges/{id}                           │  │
│  │  ├─ /api/challenges/user/{userId}/progress         │  │
│  │  ├─ /api/challenges/user/{userId}/challenge/{id}/  │  │
│  │  │   start                                          │  │
│  │  ├─ /api/challenges/user/{userId}/challenge/{id}/  │  │
│  │  │   submit                                         │  │
│  │  ├─ /api/challenges/stats/dashboard                │  │
│  │  └─ /api/challenges/lessons/                       │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Services Layer                        │  │
│  │  ├─ Challenge Service                             │  │
│  │  ├─ Progress Service                              │  │
│  │  ├─ Hint Service                                  │  │
│  │  └─ Stats Service                                 │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              ORM Models (SQLAlchemy)               │  │
│  │  ├─ Challenge                                     │  │
│  │  ├─ UserProgress                                  │  │
│  │  ├─ Hint                                          │  │
│  │  ├─ Lesson                                        │  │
│  │  └─ Finding                                       │  │
│  └─────────────────────────────────────────────────────┘  │
│                       │                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│            🗄️ DATABASE (PostgreSQL)                         │
│                                                              │
│  Tablas:                                                   │
│  ├─ challenges       - Ejercicios educativos              │
│  ├─ user_progress    - Progreso del usuario               │
│  ├─ hints            - Sistema de pistas                 │
│  ├─ lessons          - Lecciones educativas              │
│  └─ findings         - Hallazgos de seguridad            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Componentes Principales

### Frontend

#### DashboardEducativo.jsx
- **Responsabilidad**: Panel principal de la aplicación
- **Funciones**:
  - Mostrar estadísticas globales
  - Listar desafíos por nivel
  - Mostrar distribución de vulnerabilidades
  - Enlace a lecciones

#### ChallengeDetail.jsx
- **Responsabilidad**: Vista detallada de un desafío
- **Funciones**:
  - Mostrar explicaciones
  - Sistema de tabs (Vulnerabilidad, Ataque, Código, Defensa)
  - Formulario de envío de respuestas
  - Sistema de pistas
  - Progreso del usuario

#### CodeComparison.jsx
- **Responsabilidad**: Comparación visual de código
- **Funciones**:
  - Mostrar código vulnerable con colores
  - Mostrar código seguro con colores
  - Vista lado a lado o apilada
  - Resaltado sintáctico

#### HintSystem.jsx
- **Responsabilidad**: Gestionar sistema de pistas
- **Funciones**:
  - Solicitar pistas progresivas
  - Mostrar contenido de pistas
  - Rastrear uso de pistas

#### LessonContent.jsx
- **Responsabilidad**: Mostrar contenido educativo
- **Funciones**:
  - Mostrar lecciones estructuradas
  - Incrustación de videos
  - Mostrar imágenes/diagramas
  - Marcar completadas

### Backend

#### Models/challenge.py
```
Challenge
├─ id: UUID
├─ title: str
├─ description: str
├─ difficulty: DifficultyLevel
├─ vulnerability_type: VulnerabilityType
├─ attack_type: AttackType
├─ vulnerability_explanation: str
├─ attack_explanation: str
├─ countermeasures: str
├─ vulnerable_code: str
├─ vulnerable_code_language: str
├─ secure_code: str
├─ secure_code_language: str
├─ cvss_score: float
├─ owasp_top_10: str
├─ cwe_id: str
└─ test_payload: str

UserProgress
├─ id: UUID
├─ user_id: str
├─ challenge_id: UUID (FK)
├─ is_completed: bool
├─ attempts: int
├─ hints_requested: int
├─ user_answer: str
├─ is_correct: bool
└─ time_spent_seconds: int

Hint
├─ id: UUID
├─ challenge_id: UUID (FK)
├─ title: str
├─ content: str
├─ level: int (1, 2, 3...)
└─ created_at: datetime

Lesson
├─ id: UUID
├─ title: str
├─ description: str
├─ content: str
├─ order: int
├─ difficulty: DifficultyLevel
├─ video_url: str (optional)
└─ image_url: str (optional)
```

#### Routes/challenges.py
Endpoints principales:
- `GET /api/challenges/` - Listar desafíos activos
- `GET /api/challenges/{id}` - Obtener detalles
- `POST /api/challenges/user/{userId}/challenge/{id}/start` - Iniciar desafío
- `POST /api/challenges/user/{userId}/challenge/{id}/submit` - Enviar respuesta
- `POST /api/challenges/user/{userId}/challenge/{id}/request-hint` - Pedir pista
- `GET /api/challenges/stats/dashboard` - Estadísticas globales

## 🔄 Flujo de Datos

### Flujo: Usuario Completa un Desafío

```
1. Usuario selecciona desafío
   └─> Frontend: ChallengeDetail carga
       └─> Backend: GET /api/challenges/{id}
           └─> DB: Obtiene Challenge + Hints

2. Usuario lee explicaciones
   └─> Frontend: Muestra tabs (Vulnerabilidad, Ataque, Código, etc)
       └─> No hay petición backend (todo local)

3. Usuario solicita pista
   └─> Frontend: HintSystem envia request
       └─> Backend: POST /request-hint
           └─> DB: UserProgress.hints_requested += 1
               └─> Retorna siguiente Hint

4. Usuario envía respuesta
   └─> Frontend: Submite formulario
       └─> Backend: POST /submit
           └─> Valida respuesta
           └─> DB: UserProgress.is_correct = True/False
               └─> Retorna feedback

5. Dashboard se actualiza
   └─> Frontend: Actualiza stats
       └─> Backend: GET /stats/dashboard
           └─> DB: Calcula estadísticas
```

## 🗂️ Estructura de Archivos Detallada

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app + inicialización
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── challenges.py      # ⭐ Rutas principales (70 endpoints)
│   │       ├── ingestion.py       # Ingesta de vulnerabilidades
│   │       └── metrics.py         # Métricas
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuración global
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                # Base ORM + importación modelos
│   │   └── session.py             # Session factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── challenge.py           # ⭐ Modelos educativos
│   │   └── finding.py             # Modelo legacy
│   └── schemas/
│       ├── __init__.py
│       └── challenge.py           # ⭐ Validaciones Pydantic
├── scripts/
│   ├── manage.py
│   └── load_challenges.py         # ⭐ Carga 6 desafíos profesionales
├── Dockerfile
└── requirements.txt

frontend/
├── src/
│   ├── App.jsx                    # ⭐ Componente raíz + nav
│   ├── App.css                    # ⭐ Estilos personalizados
│   ├── main.jsx                   # Punto de entrada
│   ├── index.css                  # Tailwind + estilos globales
│   ├── config.js                  # Configuración API_URL
│   ├── api/
│   │   └── client.js              # Cliente Axios configurado
│   └── components/
│       ├── DashboardEducativo.jsx # ⭐ Panel principal
│       ├── ChallengeDetail.jsx    # ⭐ Vista principal desafío
│       ├── ChallengeList.jsx      # ⭐ Listado con filtros
│       ├── CodeComparison.jsx     # ⭐ Comparación sintaxis
│       ├── HintSystem.jsx         # ⭐ Sistema de pistas
│       └── LessonContent.jsx      # ⭐ Lecciones educativas
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── Dockerfile

├── docker-compose.yml             # Orquestación completa
├── .env.example                   # Template de variables
└── README.md                      # Documentación
```

## 🔐 Security Features

- ✅ SQL Injection Prevention (ORM + Validated inputs)
- ✅ CORS Enabled (pero restrictivo en producción)
- ✅ Error Handling (no expone stack traces)
- ✅ Input Validation (Pydantic schemas)
- ✅ Type Safety (SQLAlchemy + Pydantic)

## 📊 Base de Datos

### Relaciones

```
Challenge (1) -----> (Many) UserProgress
    │
    └─────> (Many) Hint

Challenge (1) -----> (Many) Lesson

UserProgress -----> Challenge (FK)
```

### Índices
- `challenges.difficulty` - Para filtros rápidos
- `challenges.vulnerability_type` - Para búsquedas
- `user_progress.user_id` - Para queries por usuario
- `user_progress.challenge_id` - Para búsquedas
- `user_progress.is_completed` - Para estadísticas

## 🔌 Integration Points

### Nuevas Funcionalidades
1. GitHub Authentication
2. Leaderboards
3. Badges System
4. Certificate Generation
5. Slack Notifications

## 📈 Performance

- Frontend: Lazy loading de componentes
- Backend: Queries optimizadas con índices
- Cache: StaticDict para estadísticas

## 🧪 Testing

### Backend Testing
```bash
pytest tests/
```

### Frontend Testing
```bash
npm run test
```

---

**Documento mantenido por**: Equipo de Desarrollo
**Última actualización**: 2024
