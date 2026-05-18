# 🛡️ Secure Coding Dojo - Plataforma Educativa Interactiva

Una plataforma educativa moderna y completamente interactiva para aprender ciberseguridad y seguridad en la codificación mediante ejercicios prácticos, desafíos y lecciones basadas en vulnerabilidades reales del mundo.

## 🎯 Características Principales

### 📚 Sistema de Desafíos Educativos
- **6+ Ejercicios de Seguridad** cubriendo las vulnerabilidades más críticas
- **Niveles Progresivos**: Principiante → Intermedio → Avanzado
- **Puntuación CVSS**: Cada desafío incluye su puntuación de severidad
- **Explicaciones Detalladas** de vulnerabilidades y ataques

### 🎨 Interfaz Educativa Completa
- **Comparación Lado a Lado**: Código vulnerable vs código seguro
- **Sistema de Pistas Progresivas**: Ayuda gradual sin spoilers
- **Pestañas Educativas**:
  - 🔍 Explicación de la Vulnerabilidad
  - ⚔️ Explicación del Tipo de Ataque
  - 💻 Comparación de Código
  - 🛡️ Contramedidas y Soluciones

### 📖 Lecciones Interactivas
- Contenido educativo estructurado
- Soporte para videos educativos
- Diagrama y visualizaciones
- Marcado de lecciones completadas

### 📊 Panel de Control
- Estadísticas en tiempo real
- Progreso del usuario
- Distribución de vulnerabilidades
- Tasas de éxito global

### 🔐 Vulnerabilidades Cubiertas
1. **SQL Injection** - La vulnerabilidad más común
2. **Cross-Site Scripting (XSS)** - Inyección de scripts
3. **Broken Authentication** - Fallos en autenticación
4. **CSRF** - Falsificación de solicitudes entre sitios
5. **IDOR** - Referencias directas inseguras a objetos
6. **Serialización Insegura** - Deserialización de datos no seguros

Cada una con:
- Explicación clara del problema
- Cómo funciona el ataque
- Código vulnerable real
- Código seguro con mejores prácticas
- Contramedidas y soluciones
- Pistas progresivas

## 🚀 Inicio Rápido

### Requisitos
- Docker y Docker Compose
- Node.js 18+ (si ejecutas sin docker)
- Python 3.9+ (si ejecutas sin docker)

### Con Docker Compose (Recomendado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/secure-coding-dojo.git
cd secure-coding-dojo

# 2. Construir y ejecutar los contenedores
docker-compose up --build

# 3. La aplicación estará disponible en:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Swagger API: http://localhost:8000/docs
```

### Instalación Manual

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Cargar ejercicios iniciales
python scripts/load_challenges.py

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

## 📁 Estructura del Proyecto

```
secure-coding-dojo/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── challenges.py      # Rutas principales de desafíos
│   │   │       ├── ingestion.py       # Ingesta de datos
│   │   │       └── metrics.py         # Métricas
│   │   ├── models/
│   │   │   ├── challenge.py           # Modelos de desafíos
│   │   │   └── finding.py             # Modelos de hallazgos
│   │   ├── schemas/
│   │   │   └── challenge.py           # Esquemas Pydantic
│   │   ├── db/
│   │   │   ├── base.py                # Base ORM
│   │   │   └── session.py             # Sesiones DB
│   │   ├── core/
│   │   │   └── config.py              # Configuración
│   │   └── main.py                    # Aplicación principal
│   │
│   ├── scripts/
│   │   ├── load_challenges.py         # Cargar ejercicios educativos
│   │   └── manage.py                  # Utilidades
│   │
│   ├── requirements.txt               # Dependencias Python
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DashboardEducativo.jsx    # Panel principal
│   │   │   ├── ChallengeDetail.jsx       # Detalles del desafío
│   │   │   ├── ChallengeList.jsx         # Lista de desafíos
│   │   │   ├── CodeComparison.jsx        # Comparación de código
│   │   │   ├── HintSystem.jsx            # Sistema de pistas
│   │   │   └── LessonContent.jsx         # Contenido de lecciones
│   │   ├── App.jsx                      # Componente raíz
│   │   ├── App.css                      # Estilos personalizados
│   │   ├── main.jsx                     # Punto de entrada
│   │   └── index.css                    # Estilos globales
│   │
│   ├── package.json                  # Dependencias Node
│   ├── tailwind.config.js            # Configuración Tailwind
│   ├── postcss.config.js             # PostCSS config
│   ├── vite.config.js                # Configuración Vite
│   ├── Dockerfile
│   └── index.html
│
├── docker-compose.yml                # Orquestación de servicios
└── README.md                         # Este archivo
```

## 🔌 Endpoints API Principales

### Desafíos
```
GET    /api/challenges/                          # Listar desafíos
GET    /api/challenges/{id}                      # Obtener desafío
GET    /api/challenges/by-difficulty             # Desafíos por dificultad
POST   /api/challenges/                          # Crear desafío
```

### Progreso del Usuario
```
GET    /api/challenges/user/{userId}/progress              # Progreso general
POST   /api/challenges/user/{userId}/challenge/{id}/start  # Iniciar desafío
POST   /api/challenges/user/{userId}/challenge/{id}/submit # Enviar respuesta
POST   /api/challenges/user/{userId}/challenge/{id}/request-hint # Pedir pista
```

### Estadísticas
```
GET    /api/challenges/stats/dashboard      # Estadísticas globales
GET    /api/challenges/stats/user/{userId}  # Estadísticas del usuario
```

Ver documentación completa en: http://localhost:8000/docs

## 📚 Contenido Educativo Incluido

### Desafío 1: SQL Injection
- **Nivel**: Principiante
- **CVSS**: 9.8 / 10
- Aprende cómo prevenir la inyección de SQL

### Desafío 2: Cross-Site Scripting (XSS)
- **Nivel**: Principiante
- **CVSS**: 7.1 / 10
- Domina la prevención de ataques XSS

### Desafío 3: Broken Authentication
- **Nivel**: Principiante
- **CVSS**: 9.1 / 10
- Construye autenticación segura

### Desafío 4: CSRF
- **Nivel**: Intermedio
- **CVSS**: 8.1 / 10
- Protege contra falsificación de solicitudes

### Desafío 5: IDOR
- **Nivel**: Intermedio
- **CVSS**: 8.2 / 10
- Implementa control de acceso adecuado

### Desafío 6: Serialización Insegura
- **Nivel**: Avanzado
- **CVSS**: 10.0 / 10
- Serializa datos de forma segura

## 🎓 Cómo Usar la Plataforma

### Para Estudiantes

1. **Explora el Dashboard** - Ve todos los desafíos disponibles
2. **Selecciona un Desafío** - Comienza con nivel Principiante
3. **Aprende el Concepto** - Lee explicaciones y analiza código
4. **Practica** - Intenta resolver, solicita pistas si es necesario
5. **Avanza** - Progresa al siguiente nivel

### Para Educadores

1. **Crea Nuevos Desafíos** - Usa la API para agregar contenido
2. **Monitorea el Progreso** - Usa el panel de estadísticas
3. **Personaliza Contenido** - Añade lecciones y pistas adicionales

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **PostgreSQL/SQLite** - Base de datos
- **Uvicorn** - Servidor ASGI

### Frontend
- **React 18** - Librería de interfaz
- **Vite** - Build tool moderno
- **Tailwind CSS** - Estilos utilitarios
- **Axios** - Cliente HTTP
- **React Syntax Highlighter** - Resaltado de código

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- Seguridad en el Ciclo de Desarrollo de Software

---

**Hecho con ❤️ para la educación en ciberseguridad**

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

