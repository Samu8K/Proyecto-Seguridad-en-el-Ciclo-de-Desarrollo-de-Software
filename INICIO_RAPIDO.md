# 🚀 Guía de Inicio Rápido - Secure Coding Dojo

## Opción 1: Con Docker Compose (Recomendado - ⭐ MÁS FÁCIL)

### Pasos:

1. **Abre una terminal en la carpeta del proyecto**
```bash
cd /workspaces/Proyecto-Seguridad-en-el-Ciclo-de-Desarrollo-de-Software
```

2. **Copia el archivo de ejemplo de configuración**
```bash
cp .env.example .env
```

3. **Levanta los servicios con Docker Compose**
```bash
docker-compose up --build
```

4. **Espera a que se complete la inicialización**
   - Verás mensajes de carga de ejercicios
   - El backend iniciará en puerto 8000
   - El frontend iniciará en puerto 5173

5. **Accede a la aplicación**
   - 🌐 **Frontend**: http://localhost:5173
   - 📚 **Backend API Docs**: http://localhost:8000/docs
   - 📊 **API Health**: http://localhost:8000/health

## Opción 2: Instalación Manual (Desarrollo)

### Backend Setup

```bash
# 1. Navega al directorio del backend
cd backend

# 2. Crear entorno virtual Python
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Cargar ejercicios iniciales
python scripts/load_challenges.py

# 6. Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (en otra terminal)

```bash
# 1. Navega al directorio del frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar servidor de desarrollo
npm run dev

# 4. Accede a http://localhost:5173
```

## 🎮 Primer Uso

1. **Abre http://localhost:5173 en tu navegador**
2. **Verás el Dashboard principal** con:
   - 📊 Estadísticas globales
   - 🌱 Desafíos por nivel de dificultad
   - 📚 Lecciones disponibles

3. **Selecciona un desafío** (comienza con Principiante)
4. **Lee las explicaciones**:
   - 🔍 Comprende la vulnerabilidad
   - ⚔️ Aprende cómo funciona el ataque
   - 💻 Compara el código vulnerable vs seguro
   - 🛡️ Estudia las contramedidas

5. **Intenta resolver** el desafío:
   - Escribe tu respuesta
   - Solicita pistas si es necesario
   - Envía tu respuesta

6. **Recibe feedback** y continúa aprendiendo

## 🔌 Endpoints Rápidos

```bash
# Ver todos los desafíos
curl http://localhost:8000/api/challenges/

# Ver documentación interactiva
open http://localhost:8000/docs

# Verificar salud del servidor
curl http://localhost:8000/health
```

## 📱 Características Principales

✅ 6+ Desafíos educativos interactivos
✅ Sistema de pistas progresivas
✅ Comparación de código color-realizado
✅ Explicaciones educativas detalladas
✅ Panel de control con estadísticas
✅ Interfaz responsiva y atractiva
✅ Soporte para videos educativos

## 🎯 Desafíos Disponibles

1. **SQL Injection** - Principiante
2. **XSS (Cross-Site Scripting)** - Principiante
3. **Broken Authentication** - Principiante
4. **CSRF** - Intermedio
5. **IDOR** - Intermedio
6. **Serialización Insegura** - Avanzado

## ⚙️ Configuración

### Rutas Disponibles

```
🌐 http://localhost:5173/        # Frontend
📊 http://localhost:8000/docs    # API Documentation
🏥 http://localhost:8000/health  # Health Check
```

### Variables de Entorno

Ver archivo `.env.example` para todas las variables disponibles.

## 🐛 Solución de Problemas

### "Connection refused" en el frontend
- Asegurate de que el backend esté corriendo en puerto 8000
- Verifica que Docker esté iniciado

### "Permission denied" con Docker
- Intenta con `sudo docker-compose up --build`

### Puerto en uso
```bash
# Encuentra qué proceso está usando el puerto
lsof -i :8000   # Para backend
lsof -i :5173   # Para frontend

# Mata el proceso
kill -9 <PID>
```

## 📖 Documentación Adicional

- [README.md](README.md) - Documentación completa
- [API Docs](http://localhost:8000/docs) - Documentación interactiva
- [Estructtura del Proyecto](#structure) - Organización de carpetas

## ✨ Próximos Pasos

1. ✅ Configura la aplicación
2. ✅ Accede al dashboard
3. ✅ Completa un desafío
4. ✅ Estudia el código seguro
5. ✅ Practica más ejercicios
6. 🎯 Domina la seguridad en codificación

¡Diviértete aprendiendo ciberseguridad! 🛡️

---

**¿Problemas?** Revisa los logs o crea un issue en GitHub.
