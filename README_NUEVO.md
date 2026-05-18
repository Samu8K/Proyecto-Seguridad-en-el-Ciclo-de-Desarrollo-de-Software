# 🛡️ Secure Coding Dojo - Plataforma Educativa Interactiva v2.0

Una plataforma moderna y completamente funcional para aprender **ciberseguridad y seguridad en la codificación** mediante ejercicios prácticos, simuladores de ataques y explicaciones detalladas. Replicando la metodología educativa de Secure Coding Dojo con un enfoque completamente interactivo.

## 🎯 Características Principales

### 📚 Sistema Completo de Ejercicios Educativos

#### 5+ Ejercicios Funcionales Detallados
1. **SQL Injection en Sistema de Login** (Principiante)
   - Explicación completa de la vulnerabilidad
   - Simulador de ataque interactivo
   - Código vulnerable vs seguro lado a lado
   - Pistas progresivas
   - Impacto en mundo real

2. **Cross-Site Scripting (XSS)** (Principiante)
   - Explicación de inyección de código JavaScript
   - Tipos de XSS (Reflejado, Almacenado)
   - Simulador funcional
   - Contramedidas con ejemplos

3. **Broken Authentication - Sesiones Débiles** (Intermedio)
   - Tokens de sesión predecibles
   - Session fixation attacks
   - Implementación de JWT seguro
   - Rate limiting

4. **Deserialización Insegura** (Avanzado)
   - Gadget chains
   - Remote Code Execution (RCE)
   - Validación segura de datos
   - Firmas HMAC

5. **Criptografía Débil** (Avanzado)
   - Algoritmos inseguros (MD5, SHA-1, DES)
   - Rainbow tables
   - Implementations seguras (bcrypt, argon2, AES-256-GCM)
   - Gestión de claves

### 🎨 Interfaz Moderna y Atractiva

#### Dashboard Educativo
- **Estadísticas en Tiempo Real**: Visualización de ejercicios, dificultades, vulnerabilidades
- **Gráficos Interactivos**: Distribución por nivel, tipos de vulnerabilidades
- **Ruta de Aprendizaje**: Progresión visual de niveles

#### Visor de Ejercicios Avanzado
- **Múltiples Pestañas Educativas**:
  - 📖 Explicación de Vulnerabilidad
  - ⚔️ Tipo de Ataque y Funcionamiento
  - 💻 Comparación Lado a Lado: Código Vulnerable vs Seguro
  - ⚡ Simulador Interactivo de Ataques
  - 🛡️ Contramedidas y Mejores Prácticas

- **Simulador de Ataques Funcional**:
  - Prueba payloads en entorno seguro
  - Retroalimentación educativa inmediata
  - Explicación de por qué funcionan/no funcionan

- **Sistema de Pistas Progresivas**:
  - Pista 1: Concepto general
  - Pista 2: Acercándose a la solución
  - Pista 3: Casi la respuesta
  - Sin spoilers innecesarios

#### Galería de Ejercicios
- **Búsqueda y Filtrado**:
  - Por dificultad (Principiante, Intermedio, Avanzado)
  - Por vulnerabilidad
  - Búsqueda por nombre
  
- **Tarjetas Informativas**:
  - CVSS Score visual
  - OWASP Top 10 classification
  - CWE references
  - Estado de dificultad con código de colores

### 🔬 Simulador Educativo Interactivo

Cada ejercicio incluye un simulador funcional que:
- ✅ Acepta payloads del usuario
- ✅ Evalúa si explotan la vulnerabilidad
- ✅ Proporciona retroalimentación educativa
- ✅ Explica por qué funcionan los ataques
- ✅ Enseña cómo prevenirlos

### 📊 Análisis de Seguridad OWASP

Cada ejercicio incluye:
- 🔐 **CVSS Score** (Common Vulnerability Scoring System)
- 🏆 **OWASP Top 10** Classification
- 🔍 **CWE ID** (Common Weakness Enumeration)
- 📚 **Referencias Técnicas** (OWASP, PortSwigger, CVE)

### 🎓 Contenido Educativo Completo

Para cada vulnerabilidad:
- ✅ Explicación técnica detallada
- ✅ Descripción del ataque paso a paso
- ✅ Casos históricos (breaches reales)
- ✅ Impacto en el mundo real
- ✅ Contramedidas efectivas
- ✅ Mejores prácticas de desarrollo
- ✅ Código vulnerable real
- ✅ Código seguro mejorado
- ✅ Comparación lado a lado

### 🏆 Sistema de Progresión

- **3 Niveles Educativos**:
  - Nivel 1: Fundamentos (SQL Injection, XSS)
  - Nivel 2: Intermedio (Autenticación)
  - Nivel 3: Avanzado (Deserialización, Criptografía)

- **Badges y Logros**:
  - 🏅 Logros por ejercicio completado
  - 🏆 Cerificados por nivel
  - 👑 Maestría en Seguridad

## 🚀 Inicio Rápido

### Requisitos Previos

- **Docker** y **Docker Compose** (Recomendado)
- O instalación local de:
  - **Python 3.10+** para el backend
  - **Node.js 18+** y **npm** para el frontend

### Opción 1: Instalación con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repositorio>
cd Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software

# Iniciar con Docker Compose
docker-compose up -d

# Esperar a que los contenedores se levanten (~30 segundos)
# Acceder a:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Instalación Local

#### Backend

```bash
# Navegar al directorio del backend
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# El backend estará en: http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

#### Frontend

```bash
# En otra terminal, navegar al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev

# El frontend estará en: http://localhost:3000
```

### Variables de Entorno

Crear `.env` en el directorio `backend/`:

```env
# Base de datos (opcional, usa SQLite por defecto)
DATABASE_URL=sqlite:///./db.sqlite3

# Configuración de la aplicación
DEBUG=True
SECRET_KEY=tu-clave-secreta-fuerte-aqui

# CORS (para desarrollo)
ALLOWED_ORIGINS=localhost:3000,localhost:3001
```

## 📖 Cómo Usar

### Para Estudiantes

1. **Acceder al Dashboard**
   - Vista general de estadísticas
   - Ruta de aprendizaje recomendada

2. **Seleccionar un Ejercicio**
   - Comenzar con nivel principiante
   - Leer la explicación completa
   - Estudiar el tipo de ataque

3. **Practicar con el Simulador**
   - Usar pistas progresivas si es necesario
   - Probar diferentes payloads
   - Entender por qué funcionan o no

4. **Estudiar Código Seguro**
   - Comparar vulnerable vs seguro
   - Entender contramedidas
   - Aplicar a tus proyectos

5. **Avanzar a Siguiente Nivel**
   - Completar ejercicios actuales
   - Desbloquear nivel siguiente
   - Ganar badges

### Para Educadores

#### Agregar Nuevos Ejercicios

Editar `backend/app/exercises/exercises_data.py` y agregar a `COMPLETE_EXERCISES`:

```python
"6_your_exercise_id": {
    "id": "6_your_exercise_id",
    "title": "Tu Título del Ejercicio",
    "short_title": "Versión Corta",
    "description": "Descripción corta",
    "difficulty": "BEGINNER",  # o INTERMEDIATE, ADVANCED
    "vulnerability_type": "XSS",  # Ver enum
    "attack_type": "CROSS_SITE",
    "icon": "🔐",
    "color": "blue",
    "cvss_score": 7.5,
    "owasp_top_10": "A03:2021",
    # ... resto de campos
    "vulnerable_code": "...",
    "secure_code": "...",
    # ... etc
}
```

#### Personalizar Progresión

Editar `PROGRESSION` en el mismo archivo para definir niveles y requisitos.

## 🔄 Arquitectura

### Backend (FastAPI + SQLAlchemy)

```
backend/
├── app/
│   ├── main.py                 # Aplicación principal
│   ├── exercises/
│   │   └── exercises_data.py   # Base de datos de ejercicios
│   ├── api/routes/
│   │   ├── interactive_exercises.py  # API de ejercicios
│   │   ├── challenges_new.py
│   │   └── ...
│   ├── models/
│   │   └── challenge.py         # Modelos de datos
│   └── db/
│       └── session.py           # Sesión de base de datos
```

### Frontend (React + Vite)

```
frontend/
├── src/
│   ├── components/
│   │   ├── EnhancedDashboard.jsx
│   │   ├── EnhancedChallengeGallery.jsx
│   │   ├── AdvancedExerciseViewer.jsx
│   │   └── ...
│   ├── App.jsx                 # Componente principal
│   └── api/
│       └── client.js           # Cliente API
```

## 📊 Endpoints de API

### Ejercicios

- `GET /api/exercises/all` - Obtener todos los ejercicios
- `GET /api/exercises/exercise/{id}` - Detalles de ejercicio
- `GET /api/exercises/exercise/{id}/code` - Código vulnerable/seguro
- `GET /api/exercises/exercise/{id}/hints` - Pistas progresivas
- `POST /api/exercises/exercise/{id}/test-attack` - Probar ataque
- `GET /api/exercises/statistics` - Estadísticas globales
- `GET /api/exercises/progression` - Estructura de progresión

## 🎨 Personalización

### Temas de Color

Editar CSS en `frontend/src/components/*.css`:
- Colores primarios: Cambiar `#667eea` (morado)
- Colores secundarios: Cambiar `#764ba2`
- Dificultad: BEGINNER `#10b981`, INTERMEDIATE `#f59e0b`, ADVANCED `#ef4444`

### Fuentes

Por defecto usa:
- Encabezados: Sistema de fuentes del sistema
- Código: `Monaco`, `Courier New`, `monospace`

Modificable en `frontend/src/App.css`

## 📚 Recursos Educativos

### Recursos Internos
- Código completo vulnerable y seguro
- Explicaciones paso a paso
- Pistas progresivas
- Simulador de ataques

### Recursos Externos (Referenciados)
- OWASP Top 10 & CheatSheets
- PortSwigger Web Security Academy
- CWE (Common Weakness Enumeration)
- CVE (Common Vulnerabilities and Exposures)

## 🔒 Seguridad

### La Plataforma es Educativa y Segura

- ✅ Ejercicios simulados (no código real malicioso)
- ✅ Ambiente aislado para pruebas
- ✅ Enseña tanto ataque como defensa
- ✅ Enfoque ético: aprender para defender

### Endpoints Protegidos en Producción

```python
# En producción, agregar:
# - Autenticación JWT
# - Rate limiting
# - CORS restrictivo
# - HTTPS obligatorio
# - Headers de seguridad
```

## 📈 Progreso y Estadísticas

### Métricas Disponibles
- Ejercicios completados
- Tiempo promedio por ejercicio
- Intentos fallidos/exitosos
- Distribución por dificultad
- CVSS promedio aprendido

## 🤝 Contribuir

Para agregar nuevos ejercicios o mejorar la plataforma:

1. Fork el repositorio
2. Crea rama: `git checkout -b feature/nuevo-ejercicio`
3. Commit cambios: `git commit -am 'Agregar nuevo ejercicio'`
4. Push: `git push origin feature/nuevo-ejercicio`
5. Pull Request

## 📝 Licencia

Este proyecto es con fines educativos.

## 💬 Soporte

Para problemas o sugerencias:
- Abrir un Issue en GitHub
- Contactar al equipo educativo

## 🙏 Créditos

Inspirado en:
- **Secure Coding Dojo** (OWASP)
- **PortSwigger Web Security Academy**
- **HackTheBox**
- **TryHackMe**

---

### Notas de Versión v2.0

✨ **Nuevo en esta versión:**
- 5 ejercicios completos y funcionales
- Simulador interactivo mejorado
- Interfaz moderna con React + Tailwind
- Dashboard con gráficos
- Sistema de pistas progresivas
- API completamente refactorizada
- Componentes educativos mejorados
- Mejor experiencia de usuario

---

**Hecho con ❤️ para la educación en seguridad**
