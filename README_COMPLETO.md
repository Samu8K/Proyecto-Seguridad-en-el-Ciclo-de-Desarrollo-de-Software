# 🛡️ Secure Coding Dojo - Plataforma Educativa Interactiva

Una **réplica profesional del Secure Coding Dojo** completamente funcional para aprender seguridad en la programación a través de ejercicios prácticos e interactivos.

## ✨ Características Principales

### 📚 Contenido Educativo Completo
- **6 desafíos completos** con vulnerabilidades reales:
  - SQL Injection (Inyección SQL)
  - Cross-Site Scripting (XSS)
  - Cross-Site Request Forgery (CSRF)
  - Broken Authentication (Autenticación Rota)
  - Insecure Direct Object Reference (IDOR)
  - Insecure Deserialization (Deserialización Insegura)

- **Explicaciones paso a paso** de cada vulnerabilidad
- **Código vulnerable vs seguro** lado a lado
- **Tipos de ataque** detallados con ejemplos reales
- **Contramedidas** y mejores prácticas

### 🎮 Simuladores Interactivos
- **Modo Vulnerable**: Explota vulnerabilidades reales
- **Modo Seguro**: Demuestra defensa contra ataques
- **Salida en terminal**: Simula ejecución real de exploits
- **Feedback inmediato**: Resultados en tiempo real

### 🎯 Sistema de Progreso
- **Rango del cinturón**: Desde Cinturón Blanco hasta Negro
- **Puntuaciones dinámicas**: Basadas en intentos y tiempo
- **Progreso visual**: Barra de progreso animada
- **Estadísticas globales**: Seguimiento de competencias

### 🎨 Interfaz Profesional
- **Diseño moderno y responsivo**: Funciona en móvil, tablet y desktop
- **Tema oscuro elegante**: Gradientes y animaciones suaves
- **Navegación intuitiva**: Experiencia de usuario fluida
- **Componentes visuales atractivos**: Iconos y badges

### 📱 Responsive Design
- **100% responsivo**: Se adapta a cualquier pantalla
- **Mobile-first**: Optimizado para dispositivos móviles
- **Breakpoints profesionales**: 480px, 768px, 1024px+

## 🏗️ Arquitectura del Proyecto

```
├── backend/
│   ├── app/
│   │   ├── main.py              # Aplicación FastAPI
│   │   ├── api/routes/
│   │   │   └── challenges_new.py # Endpoints de desafíos
│   │   ├── models/
│   │   │   └── challenge.py     # Modelos de BD
│   │   ├── schemas/
│   │   ├── services/
│   │   └── core/config.py
│   ├── scripts/
│   │   └── load_challenges_data.py # Datos educativos
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DashboardEducativo.jsx # Dashboard principal
│   │   │   ├── DashboardEducativo.css
│   │   │   ├── InteractiveExercise.jsx # Simulador interactivo
│   │   │   ├── InteractiveExercise.css
│   │   │   ├── ChallengeGallery.jsx
│   │   │   └── ChallengeGallery.css
│   │   ├── App.jsx              # Aplicación principal
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml           # Orquestación de contenedores
└── README.md
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Docker y Docker Compose
- Node.js 16+ (si ejecutas sin Docker)
- Python 3.9+ (si ejecutas sin Docker)

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/Samu8K/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software.git
cd Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software

# Ejecutar con Docker Compose
docker-compose up

# La aplicación estará disponible en:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Ejecución Local

#### Backend (FastAPI)
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos y cargar datos
python scripts/manage.py

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (React + Vite)
```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar desarrollo
npm run dev

# Acceder en http://localhost:5173
```

## 📖 Uso de la Plataforma

### 1. **Dashboard Principal**
- Visualiza tu rango actual (Cinturón Blanco → Negro)
- Revisa estadísticas personales
- Navega por desafíos organizados por dificultad

### 2. **Seleccionar Desafío**
- Elige por dificultad: Principiante, Intermedio, Avanzado
- Lee descripción y metadatos (CVSS, OWASP, CWE)
- Accede a través de tarjetas interactivas

### 3. **Ejercicio Interactivo**
Tabs disponibles:

- **📖 Explicación**: Conceptos de la vulnerabilidad
- **⚡ Tipo de Ataque**: Cómo funciona el ataque
- **💻 Código**: Comparación vulnerable vs seguro
- **🎮 Simulador**: Ejecuta ataques interactivamente
- **🛡️ Protección**: Contramedidas y mejores prácticas

### 4. **Simulador Interactivo**
- **Modo Vulnerable**: Ataca la aplicación insegura
- **Modo Seguro**: Comprueba que las defensas funcionan
- **Terminal**: Ve la salida del exploit en tiempo real
- **Feedback**: Mensajes sobre éxito/fallo del ataque

### 5. **Sistema de Pistas**
- 3 pistas progresivas por desafío
- Desbloquéalas a medida que avances
- Diseñadas para guiarte sin revelar la solución

### 6. **Progreso y Badges**
- Puntuaciones dinámicas (100 - intentos×10)
- Progreso visual en tiempo real
- Cambio automático de rango según progreso

## 🔧 Configuración y Personalización

### Modificar Datos de Desafíos
Edita `/backend/scripts/load_challenges_data.py`:
```python
# Agregar nuevo desafío
challenges = [
    Challenge(
        title="Tu Desafío",
        short_title="Título Corto",
        description="Descripción...",
        # ... más campos
    ),
]
```

### Personalizar Colores
En `/frontend/src/components/DashboardEducativo.css`:
```css
.hero-section h1 {
  background: linear-gradient(135deg, #tu-color-1 0%, #tu-color-2 100%);
}
```

### Ajustar Puntuación
En `/frontend/src/components/InteractiveExercise.jsx`:
```javascript
const score = Math.max(10, 100 - attempts * 10); // Modificar fórmula
```

## 📊 API Endpoints

### Desafíos
- `GET /api/challenges/` - Obtener todos los desafíos
- `GET /api/challenges/{id}` - Obtener desafío específico
- `GET /api/challenges/difficulty/{difficulty}` - Filtrar por dificultad

### Progreso
- `POST /api/challenges/progress/start` - Iniciar desafío
- `POST /api/challenges/progress/submit-answer` - Enviar respuesta
- `GET /api/challenges/progress/{user_id}` - Obtener progreso

### Estadísticas
- `GET /api/challenges/stats/dashboard` - Estadísticas globales
- `GET /api/challenges/stats/global-statistics` - Datos agregados

## 🎓 Estructura de Datos de Desafío

```python
{
  "id": "uuid",
  "title": "SQL Injection Básico",
  "short_title": "SQL Injection",
  "description": "Aprende cómo explotar vulnerabilidades de inyección SQL...",
  "difficulty": "BEGINNER",
  "vulnerability_type": "SQL_INJECTION",
  "attack_type": "SQL Injection",
  "cvss_score": 9.8,
  "owasp_top_10": "A03:2021 Injection",
  "cwe_id": "CWE-89",
  "vulnerability_explanation": "...",
  "attack_explanation": "...",
  "real_world_impact": "...",
  "countermeasures": "...",
  "best_practices": "...",
  "vulnerable_code": "...",
  "secure_code": "...",
  "hint_1": "Intenta...",
  "hint_2": "Considera...",
  "hint_3": "La solución...",
  "icon": "💉",
  "color": "#ef4444"
}
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm run test
```

## 🤝 Contribuciones

¡Contribuciones bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para detalles.

## 🙋 Soporte

¿Dudas o problemas?

- 📧 Email: [Tu email]
- 💬 Issues: [GitHub Issues]
- 📚 Documentación: Ver `ARQUITECTURA.md`

## 🎯 Hoja de Ruta

- [ ] Agregar más desafíos (AAAA Vulnerabilidades comunes)
- [ ] Integración de video educativos
- [ ] Sistema de competencias/leaderboard
- [ ] Exportar certificados
- [ ] Desafíos personalizados
- [ ] Integraciones con plataformas externas

## 👥 Autores

**Proyecto Educativo de Seguridad en el Ciclo de Desarrollo de Software**

Inspirado en [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) y [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

**¡Que disfrutes aprendiendo seguridad en la programación!** 🛡️

Recuerda: *Un código seguro es un código responsable.*
