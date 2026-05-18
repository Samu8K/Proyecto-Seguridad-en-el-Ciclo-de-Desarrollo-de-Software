# 📑 ÍNDICE DE ARCHIVOS - Secure Coding Dojo v2.0

Guía completa de todos los archivos nuevos y modificados en la transformación.

## 📚 Documentación Nueva (Empieza aquí)

| Archivo | Descripción | Leer Primero |
|---------|-------------|-------------|
| **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** | Instalación en 5 min y uso básico | ✅ SÍ |
| **[README_NUEVO.md](README_NUEVO.md)** | Documentación completa del proyecto | ✅ SÍ |
| **[ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md)** | Arquitectura técnica detallada | ⭐ Para devs |
| **[RESUMEN_CAMBIOS.md](RESUMEN_CAMBIOS.md)** | Qué se cambió y por qué | ℹ️ Referencia |

---

## 🔧 Backend - Nuevos Archivos

### `backend/app/exercises/` (NUEVO - Módulo de Ejercicios)

```
backend/app/exercises/
├── __init__.py
│   └── Inicialización del módulo
│
└── exercises_data.py ⭐⭐⭐ ARCHIVO PRINCIPAL
    ├── 5 Ejercicios completos:
    │   ├── 1. SQL Injection en Login
    │   ├── 2. XSS en Comentarios
    │   ├── 3. Broken Authentication
    │   ├── 4. Deserialización Insegura
    │   └── 5. Criptografía Débil
    │
    ├── Sistema de Progresión (3 niveles)
    │
    └── ~1500 líneas de contenido educativo
```

**¿Qué contiene?**
- 5 ejercicios con explicaciones técnicas completas
- Código vulnerable y seguro para cada uno
- Pistas progresivas (3 niveles)
- Casos históricos y impacto real
- Contramedidas y mejores prácticas
- Referencias OWASP/CWE

**¿Cómo editarlo?**
Ver: [GUIA_RAPIDA.md - Agregar Nuevo Ejercicio](GUIA_RAPIDA.md#agregar-nuevo-ejercicio)

---

### `backend/app/api/routes/` (ACTUALIZADO)

```
backend/app/api/routes/
├── interactive_exercises.py ⭐⭐⭐ NUEVO
│   ├── GET /api/exercises/all
│   ├── GET /api/exercises/exercise/{id}
│   ├── GET /api/exercises/exercise/{id}/code
│   ├── GET /api/exercises/exercise/{id}/hints
│   ├── POST /api/exercises/exercise/{id}/test-attack
│   ├── GET /api/exercises/statistics
│   ├── GET /api/exercises/progression
│   │
│   └── Simulador de ataques interactivo
│       ~400 líneas
│
├── challenges_new.py (EXISTENTE)
├── ingestion.py (EXISTENTE)
└── metrics.py (EXISTENTE)
```

**¿Qué hace?**
- API REST para todos los ejercicios
- Simulador que detecta patrones de ataque
- Retroalimentación educativa automática
- Endpoints de progresión y estadísticas

---

### `backend/app/main.py` (MEJORADO)

**Cambios:**
- ✅ Agregada ruta: `interactive_exercises.router`
- ✅ Mejorada descripción de la API
- ✅ Endpoint raíz mejorado

```python
from app.api.routes import interactive_exercises
app.include_router(interactive_exercises.router)
```

---

### `backend/app/models/challenge.py` (ACTUALIZADO)

**Cambios:**
- ✅ Agregados tipos de vulnerabilidad: COMMAND_INJECTION, XXE, etc.
- ✅ Mejor documentación

```python
class VulnerabilityType(str, enum.Enum):
    SQL_INJECTION = "SQL_INJECTION"
    XSS = "XSS"
    CSRF = "CSRF"
    # ... y 6 más
```

---

## 🎨 Frontend - Nuevos Archivos

### Componentes Principales

#### 1. **`frontend/src/components/EnhancedDashboard.jsx`** ⭐⭐

**Propósito**: Pantalla principal con estadísticas y bienvenida

**Características:**
- Dashboard educativo visual
- Gráficos con Recharts (Pie, Bar)
- Tarjetas de estadísticas
- Ruta de aprendizaje visual
- Features de la plataforma
- Call-to-action

**Estadísticas**: 300+ líneas

**Ubicación:** `http://localhost:3000` (Primera pantalla)

---

#### 2. **`frontend/src/components/EnhancedChallengeGallery.jsx`** ⭐⭐

**Propósito**: Galería de todos los ejercicios

**Características:**
- Lista de 5+ ejercicios
- Búsqueda por nombre/tipo
- Filtro por dificultad
- Tarjetas informativas
- CVSS scores visuales
- OWASP classification
- Tips educativos

**Estadísticas**: 250+ líneas

**Ubicación:** `http://localhost:3000` → Botón "Comenzar Ejercicios"

---

#### 3. **`frontend/src/components/AdvancedExerciseViewer.jsx`** ⭐⭐⭐

**Propósito**: Visor completo del ejercicio

**5 Tabs Educativos:**
1. 📖 **Explanation** - Explicación de la vulnerabilidad
2. ⚔️ **Attack** - Cómo funciona el ataque
3. 💻 **Code** - Comparación lado a lado
4. ⚡ **Simulator** - Prueba tu ataque
5. 🛡️ **Countermeasures** - Defensa y mejores prácticas

**Características:**
- Código con highlight
- Simulador interactivo
- Pistas progresivas (3 niveles)
- Temporizador
- Contador de intentos
- Retroalimentación educativa

**Estadísticas**: 400+ líneas

**Ubicación:** Cuando haces clic en un ejercicio

---

### Archivos de Estilos CSS

| Archivo | Líneas | Propósito |
|---------|--------|----------|
| **EnhancedDashboard.css** | 600+ | Estilos dashboard |
| **EnhancedChallengeGallery.css** | 500+ | Estilos galería |
| **AdvancedExerciseViewer.css** | 700+ | Estilos visor |

**Características CSS:**
- ✅ Responsive (mobile, tablet, desktop)
- ✅ Gradientes modernos
- ✅ Animaciones suaves
- ✅ Hover effects
- ✅ Dark mode ready
- ✅ Accesibilidad

---

### `frontend/src/App.jsx` (REDISEÑO COMPLETO)

**Antes:**
```jsx
// Navegación básica entre 2 vistas
```

**Ahora:**
```jsx
// 3 vistas principales:
// 1. Dashboard (Principal)
// 2. Gallery (Ejercicios)
// 3. ExerciseViewer (Detalles)

// Navegación fluida entre pantallas
// Estados bien manejados
```

**Estadísticas**: 55 líneas (simple y limpio)

---

## 📊 Estructura de Archivos Completa

### Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          📝 MEJORADO
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── challenge.py                 📝 MEJORADO
│   │   └── finding.py
│   │
│   ├── schemas/
│   │   └── challenge.py
│   │
│   ├── exercises/                       ✨ NUEVA CARPETA
│   │   ├── __init__.py
│   │   └── exercises_data.py            ✨ NUEVO (1500+ líneas)
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── interactive_exercises.py ✨ NUEVO (400+ líneas)
│   │       ├── challenges_new.py
│   │       ├── ingestion.py
│   │       └── metrics.py
│   │
│   └── services/
│
├── scripts/
│   ├── load_challenges.py
│   └── manage.py
│
├── Dockerfile
└── requirements.txt
```

### Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── EnhancedDashboard.jsx        ✨ NUEVO
│   │   ├── EnhancedDashboard.css        ✨ NUEVO
│   │   ├── EnhancedChallengeGallery.jsx ✨ NUEVO
│   │   ├── EnhancedChallengeGallery.css ✨ NUEVO
│   │   ├── AdvancedExerciseViewer.jsx   ✨ NUEVO
│   │   ├── AdvancedExerciseViewer.css   ✨ NUEVO
│   │   │
│   │   ├── ChallengeGallery.jsx         (legacy)
│   │   ├── InteractiveExercise.jsx      (legacy)
│   │   ├── DashboardEducativo.jsx       (legacy)
│   │   └── ...
│   │
│   ├── api/
│   │   └── client.js
│   │
│   ├── App.jsx                          📝 REDISEÑO
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── Dockerfile
├── package.json
├── vite.config.js
└── index.html
```

### Raíz del Proyecto

```
Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software/
├── README.md                            (Original)
├── README_NUEVO.md                      ✨ NUEVO
├── README_COMPLETO.md                   (Original)
├── ARQUITECTURA.md                      (Original)
├── ARQUITECTURA_NUEVA.md                ✨ NUEVO
├── DESAFIOS.md                          (Original)
├── INICIO_RAPIDO.md                     (Original)
├── GUIA_RAPIDA.md                       ✨ NUEVO
├── RESUMEN_CAMBIOS.md                   ✨ NUEVO
│
├── docker-compose.yml
│
├── backend/
├── frontend/
└── examples/
```

---

## 🔍 Cómo Navegar el Código

### Para Estudiantes

1. Abre [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
2. Sigue instrucciones de instalación
3. Abre http://localhost:3000
4. ¡Comienza a aprender!

### Para Desarrolladores (Backend)

1. Lee [ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md)
2. Explora `backend/app/exercises/exercises_data.py`
3. Revisa `backend/app/api/routes/interactive_exercises.py`
4. Entiende el simulador de ataques

### Para Desarrolladores (Frontend)

1. Lee [ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md) - Sección Frontend
2. Abre `frontend/src/App.jsx` (punto de entrada)
3. Explora componentes en `frontend/src/components/`
4. Revisa estilos CSS

### Para Educadores

1. Lee [README_NUEVO.md](README_NUEVO.md) - Sección Para Educadores
2. Abre `backend/app/exercises/exercises_data.py`
3. Copia formato de un ejercicio existente
4. Sigue [GUIA_RAPIDA.md - Agregar Nuevo Ejercicio](GUIA_RAPIDA.md)

---

## 📈 Estadísticas de Código

| Componente | Archivos | Líneas | Estado |
|-----------|----------|--------|--------|
| Ejercicios Backend | 2 | 1,500+ | ✨ NUEVO |
| API Routes | 1 | 400+ | ✨ NUEVO |
| Componentes React | 3 | 950+ | ✨ NUEVO |
| Estilos CSS | 3 | 1,800+ | ✨ NUEVO |
| Documentación | 4 | 1,500+ | ✨ NUEVO |
| **TOTAL** | **~20** | **~7,150+** | ✨ COMPLETO |

---

## 🚀 Próximos Pasos

### Para Usar Inmediatamente

1. [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Instalación
2. [README_NUEVO.md](README_NUEVO.md) - Descripción general
3. ¡Comienza!

### Para Entender la Arquitectura

1. [ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md)
2. Explora carpetas
3. Lee código comentado

### Para Agregar Funciones

1. [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Sección Educador
2. [ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md) - Sección Escalabilidad
3. Sigue patrones existentes

---

## 💡 Tips Importantes

1. **Empieza con GUIA_RAPIDA.md** - Es lo más rápido
2. **Todos los archivos tienen comentarios** - Lee el código
3. **Los ejercicios son modulares** - Fácil de agregar más
4. **El simulador es educativo** - No código malicioso real
5. **La documentación es exhaustiva** - No debería haber dudas

---

## 📞 Referencias Rápidas

| Necesito... | Archivo |
|-----------|---------|
| Instalar rápido | [GUIA_RAPIDA.md](GUIA_RAPIDA.md) |
| Entender todo | [README_NUEVO.md](README_NUEVO.md) |
| Arquitectura técnica | [ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md) |
| Ver cambios | [RESUMEN_CAMBIOS.md](RESUMEN_CAMBIOS.md) |
| Agregar ejercicio | [GUIA_RAPIDA.md](GUIA_RAPIDA.md) |
| Ver código ejercicios | `backend/app/exercises/exercises_data.py` |
| Ver API | `backend/app/api/routes/interactive_exercises.py` |
| Ver Dashboard | `frontend/src/components/EnhancedDashboard.jsx` |
| Ver Galería | `frontend/src/components/EnhancedChallengeGallery.jsx` |
| Ver Visor | `frontend/src/components/AdvancedExerciseViewer.jsx` |

---

**¡Tu proyecto está listo para aprender!** 🎓  
**¡Empieza por GUIA_RAPIDA.md!** 🚀
