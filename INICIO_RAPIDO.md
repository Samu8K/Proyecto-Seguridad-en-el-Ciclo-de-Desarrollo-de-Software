# 🚀 Guía de Inicio Rápido - Secure Coding Dojo

## ⚡ Automatización DevSecOps (Automático)

**NO necesitas hacer nada.** Todo se ejecuta automáticamente en GitHub Actions:

```bash
# Solo haz push normal
git add .
git commit -m "tu cambio"
git push origin main

✅ Los workflows se ejecutan automáticamente
✅ Ve a GitHub → Actions para ver progreso
✅ Descarga reportes en Artifacts
```

**Documentación completa:** Ver [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)

---

## 🌐 Desarrollo Local (Opcional)

Si quieres desarrollar sin Docker:

### Backend Setup

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (otra terminal)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

**Accede a:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🐳 Con Docker (Recomendado)

```bash
# Opción 1: docker-compose
docker-compose up --build

# Opción 2: docker compose (plugin moderno)
docker compose up --build
```

**Accede a:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎮 Primer Uso

1. **Abre http://localhost:3000 en tu navegador**
2. **Verás el Dashboard** con:
   - 📊 Estadísticas globales
   - 🌱 Desafíos por dificultad
   - 📚 Lecciones disponibles

3. **Selecciona un desafío** (comienza con Principiante)
4. **Lee las explicaciones**:
   - 🔍 Vulnerabilidad
   - ⚔️ Ataque real
   - 💻 Código vulnerable vs seguro
   - 🛡️ Contramedidas

5. **Resuelve el desafío**:
   - Escribe respuesta
   - Solicita pistas si necesitas
   - Envía respuesta

6. **Recibe feedback** y continúa aprendiendo

---

## 🔌 Endpoints Útiles

```bash
# Ver todos los desafíos
curl http://localhost:8000/api/exercises/all

# Ver documentación interactiva
open http://localhost:8000/docs

# Health check
curl http://localhost:8000/health
```

---

## 📝 Configuración (Opcional)

### Secrets para ASPM

Si tienes plataforma ASPM (Snyk, Aqua, etc.):

```
GitHub Settings → Secrets → Actions

ASPM_API_URL=https://tu-aspm.com/api
ASPM_API_KEY=tu-api-key
```

Los resultados se enviarán automáticamente.

---

## 📚 Documentación Completa

- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Cómo funciona la automatización
- **[WORKFLOW_FIXES.md](WORKFLOW_FIXES.md)** - Qué se corrigió
- **[DEVSECOPS_FIXES.md](DEVSECOPS_FIXES.md)** - Correcciones generales
- **[ARQUITECTURA_NUEVA.md](ARQUITECTURA_NUEVA.md)** - Arquitectura del proyecto
- **[DESAFIOS.md](DESAFIOS.md)** - Desafíos disponibles

---

## 🆘 Problemas Comunes

### No puedo ver Frontend en http://localhost:3000

```
- Verifica que npm run dev esté ejecutándose
- Verifica que no hay otro proceso en puerto 3000
- Revisa los logs en la terminal de frontend
```

### Backend no responde

```
- Verifica que uvicorn esté corriendo
- Verifica http://localhost:8000/health
- Revisa los logs en la terminal de backend
```

### Docker no funciona

```
- Verifica que Docker está instalado: docker --version
- Verifica que Docker Daemon esté corriendo
- Intenta: docker-compose up --build
```

### Workflows no se ejecutan en GitHub

```
- Verifica que los cambios están en la rama main
- Ve a Actions tab y espera 1-2 minutos
- Revisa si hay `.github/workflows/*.yml`
```

---

¡Listo! 🎉 Ahora puedes empezar a usar Secure Coding Dojo

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
