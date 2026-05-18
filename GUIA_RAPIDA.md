# ⚡ Guía Rápida de Inicio - Secure Coding Dojo v2.0

## 🚀 Inicio en 5 Minutos

### Opción 1: Docker (Recomendado - La Más Rápida)

```bash
# 1. Asegúrate de tener Docker instalado
docker --version
docker-compose --version

# 2. Clona o descarga el proyecto
cd tu-proyecto

# 3. Levanta los contenedores
docker-compose up -d

# 4. Espera 30 segundos a que se inicialice

# 5. Accede a:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Docs API: http://localhost:8000/docs

# 6. ¡Comienza a usar!
```

### Opción 2: Instalación Local Manual

#### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

#### Backend

```bash
# Terminal 1: Backend

cd backend

# Crear entorno virtual
python -m venv venv

# Activar
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000

# Listo en: http://localhost:8000
```

#### Frontend

```bash
# Terminal 2: Frontend

cd frontend

# Instalar dependencias
npm install

# Ejecutar desarrollo
npm run dev

# Listo en: http://localhost:3000
```

## 🎯 Uso Básico

### Como Estudiante

1. **Abre el navegador**: http://localhost:3000
2. **Verás el Dashboard** con:
   - Estadísticas de ejercicios
   - Ruta de aprendizaje
   - Botón "Comenzar Ejercicios"

3. **Haz clic en "Comenzar"** para ver:
   - Galería de 5+ ejercicios
   - Filtros por dificultad
   - Búsqueda
   - Tarjetas informativas

4. **Selecciona un ejercicio** (ej: SQL Injection)
   - Verás explicación completa
   - Código vulnerable vs seguro
   - Simulador interactivo
   - Pistas progresivas

5. **Prueba un ataque**:
   - En simulador, ingresa: `admin' --`
   - Haz clic "Probar Ataque"
   - Verás si funcionó + explicación

6. **Aprende contramedidas**:
   - Estudia código seguro
   - Lee mejores prácticas
   - Entiende defensa

### Como Educador

#### Agregar Nuevo Ejercicio

1. Abre: `backend/app/exercises/exercises_data.py`

2. Agreg al diccionario `COMPLETE_EXERCISES`:

```python
"6_mi_ejercicio": {
    "id": "6_mi_ejercicio",
    "title": "Mi Título",
    "short_title": "Corto",
    "description": "Descripción",
    "difficulty": "BEGINNER",  # o INTERMEDIATE, ADVANCED
    "vulnerability_type": "SQL_INJECTION",  # Ver opciones abajo
    "attack_type": "INJECTION",  # Ver opciones abajo
    "icon": "🔓",
    "color": "red",
    "cvss_score": 7.5,
    "owasp_top_10": "A03:2021",
    "cwe_id": "CWE-89",
    "cwe_description": "Description from CWE",
    
    "vulnerability_explanation": "Explicación completa...",
    "attack_explanation": "Cómo funciona el ataque...",
    "real_world_impact": "Casos históricos...",
    "countermeasures": "Cómo defenderse...",
    "best_practices": "Mejores prácticas...",
    "learning_objectives": ["Objetivo 1", "Objetivo 2"],
    
    "vulnerable_code": "# código vulnerable aquí",
    "vulnerable_code_language": "python",
    "vulnerable_code_explanation": "Qué está mal...",
    
    "secure_code": "# código seguro aquí",
    "secure_code_language": "python",
    "secure_code_explanation": "Qué se mejoró...",
    
    "hint_1": "Pista básica",
    "hint_2": "Pista intermedia",
    "hint_3": "Pista avanzada",
    
    "test_endpoint": "/api/test",
    "test_payload": "ejemplo",
    "expected_result": "resultado esperado",
    
    "references": [
        "URL1",
        "URL2"
    ]
}
```

3. Agrega lógica en simulador:

Abre: `backend/app/api/routes/interactive_exercises.py`

Busca función `simulate_attack()` y agrega:

```python
elif exercise_id == "6_mi_ejercicio":
    # Tu lógica de detección
    if "patron" in payload:
        return {
            "success": True,
            "message": "✅ ¡Ataque exitoso!",
            "details": "Detalles aquí",
            "educational_insight": "Lección educativa aquí"
        }
    return {
        "success": False,
        "message": "❌ Inténtalo de nuevo",
        "details": "Detalles",
        "educational_insight": "Intenta con..."
    }
```

4. ¡Reinicia el servidor y prueba!

#### Opciones de Enums

**VulnerabilityType:**
- SQL_INJECTION
- XSS
- CSRF
- BROKEN_AUTH
- IDOR
- INSECURE_DESERIALIZE
- COMMAND_INJECTION
- XXE
- INSECURE_CRYPTOGRAPHY
- PATH_TRAVERSAL

**AttackType:**
- INJECTION
- CROSS_SITE
- AUTHENTICATION
- AUTHORIZATION
- SERIALIZATION
- CRYPTO
- TRAVERSAL

## 🔧 Troubleshooting

### Puerto 3000 ya está en uso

```bash
# Cambiar puerto frontend
cd frontend
npm run dev -- --port 3001
```

### Puerto 8000 ya está en uso

```bash
# Cambiar puerto backend
uvicorn app.main:app --reload --port 8001
```

### Errores de conexión API

Edita `frontend/src/components/AdvancedExerciseViewer.jsx`:

```javascript
// Busca:
const response = await fetch(`http://localhost:8000/api/exercises/exercise/${exerciseId}`);

// Cambia a tu URL:
const response = await fetch(`http://tu-ip:8000/api/exercises/exercise/${exerciseId}`);
```

### Base de datos corrupta

```bash
# Elimina y recrea
rm backend/db.sqlite3
python backend/app/scripts/manage.py init_db
```

## 📊 Monitoreo

### Ver API Docs

Abre: http://localhost:8000/docs

Verás:
- Todos los endpoints
- Parámetros esperados
- Respuestas
- Prueba directo en el navegador

### Ver Logs del Backend

```bash
# Ya está en --reload, ver terminal donde ejecutaste uvicorn
# Verás todas las peticiones y errores
```

### Ver Logs del Frontend

```bash
# Abre browser DevTools (F12)
# Consola: verás logs y errores
```

## 📈 Estadísticas

Accede a: http://localhost:8000/api/exercises/statistics

Verás JSON con:
- Total de ejercicios
- Por dificultad
- Por vulnerabilidad
- CVSS promedio

## 🎨 Personalización Rápida

### Cambiar Tema Principal

Abre: `frontend/src/components/EnhancedDashboard.css`

Busca colores:
```css
/* Cambiar de morado a otro color */
#667eea  → #tu-color

/* Cambiar a azul */
#667eea  → #3b82f6
```

### Cambiar Logo/Título

Abre: `frontend/src/components/EnhancedDashboard.jsx`

```jsx
<h1>🛡️ Secure Coding Dojo</h1>

// Cambia a:
<h1>🎓 Mi Academia de Seguridad</h1>
```

### Agregar tu Logo

1. Copia imagen a: `frontend/public/logo.png`
2. En componente:
```jsx
<img src="/logo.png" alt="Logo" style={{height: '50px'}} />
```

## 🚀 Deploy en Producción

### Opción 1: Heroku

```bash
# Instala Heroku CLI
brew install heroku-cli  # Mac
# o descarga desde heroku.com

# Login
heroku login

# Crea app
heroku create mi-app

# Deploy
git push heroku main

# Abre
heroku open
```

### Opción 2: Docker Hub + VPS

```bash
# Build imagen
docker build -t mi-usuario/secure-dojo:1.0 .

# Push a Docker Hub
docker push mi-usuario/secure-dojo:1.0

# En tu VPS:
docker pull mi-usuario/secure-dojo:1.0
docker run -p 80:3000 -p 8000:8000 mi-usuario/secure-dojo:1.0
```

### Opción 3: AWS / Google Cloud / Azure

Usa Docker Compose en instancia cloud

## 📞 Soporte

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Cannot GET /" | Backend no está corriendo, inicia en terminal 1 |
| API 404 errors | URL de API incorrecta, verifica ports |
| Ejercicios vacíos | exercises_data.py no está siendo cargado |
| Estilos extraños | Limpia caché del navegador (Ctrl+Shift+R) |

### Ver Logs Completos

```bash
# Backend
cd backend
tail -f app.log  # Si lo tienes configurado

# O en terminal donde ejecutaste uvicorn
# Verás todos los logs en tiempo real
```

## ✅ Checklist de Instalación

- [ ] Docker instalado y running
- [ ] Proyecto clonado
- [ ] docker-compose up -d ejecutado
- [ ] Esperar 30 segundos
- [ ] Frontend accesible en :3000
- [ ] Backend accesible en :8000
- [ ] API Docs en :8000/docs
- [ ] Dashboard muestra estadísticas
- [ ] Galería muestra ejercicios
- [ ] Simulador funciona

## 🎓 Próximos Pasos

1. **Estudia** el primer ejercicio (SQL Injection)
2. **Practica** con el simulador
3. **Lee** código seguro vs vulnerable
4. **Aprende** contramedidas
5. **Avanza** a siguientes ejercicios
6. **Enseña** a otros lo que aprendiste

---

**¡Listo para aprender seguridad? ¡Comienza ahora!** 🚀
