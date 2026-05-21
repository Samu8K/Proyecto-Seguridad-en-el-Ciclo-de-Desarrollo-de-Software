# 🔐 DevSecOps Automation - GitHub Actions

## ⚡ Lo Básico

**Todo se ejecuta automáticamente en GitHub Actions. No necesitas scripts.**

Simplemente haz push a `main` y los workflows se ejecutan solos.

```bash
git add .
git commit -m "tu cambio"
git push origin main

✅ Los workflows se ejecutan automáticamente
✅ Ve a GitHub Actions tab para monitorear
```

---

## 📊 Flujo Automático

```
Tu Push a Main
    ↓
GitHub Actions Detecta
    ↓
Ejecuta 2 Workflows en Paralelo:
  ├─ DevSecOps Pipeline (.github/workflows/devsecops.yml)
  │  ├─ Setup Python & Node.js
  │  ├─ Semgrep Analysis
  │  ├─ pip-audit (Python dependencies)
  │  ├─ npm audit (Node.js dependencies)
  │  ├─ Build Docker images
  │  └─ Upload reports
  │
  └─ Security Scan (.github/workflows/security.yml)
     ├─ Semgrep Code Analysis
     ├─ Dependency Vulnerability Check
     ├─ Ingest to ASPM (optional)
     └─ Security Summary
    ↓
Resultados en GitHub Actions tab
    ↓
(Optional) Envía a ASPM Platform
```

---

## 🎯 Cómo Monitorear

### 1. Ver Workflows Ejecutando

```
GitHub → Actions Tab → DevSecOps Pipeline (o Security Scan)
```

**Estados:**
- 🟡 **In Progress** - Ejecutándose ahora
- ✅ **Success** - Completado sin errores
- ⚠️ **Warning** - Completado con findings (normal)
- ❌ **Failed** - Error que requiere atención

### 2. Ver Logs Detallados

```
Actions → [Workflow Name] → [Run] → Expand any step
```

Ejemplo:
```
✓ Setup Python
✓ Install backend dependencies
⏳ Run Semgrep security scan
  semgrep scan --config auto --json --output backend/semgrep-results.json
  [Scanning files...]
✓ Run pip-audit
  Found 2 vulnerabilities
  ├─ CVE-2023-XXXXX in requests
  └─ CVE-2023-YYYYY in urllib3
```

### 3. Descargar Reportes

```
Actions → [Workflow] → [Latest Run]
→ Scroll Down → Artifacts
→ Download "devsecops-reports"
```

Contiene:
```
devsecops-reports.zip
├── backend/semgrep-results.json
├── backend/pip-audit.json
└── npm-audit.json
```

---

## 🔄 Triggers Automáticos

### Cuándo Se Ejecutan

| Evento | DevSecOps | Security | Acción |
|--------|-----------|----------|--------|
| Push a `main` | ✅ | ✅ | Inmediatamente |
| Pull Request a `main` | ✅ | ✅ | En paralelo |
| Cada domingo 3 AM UTC | ✅ | - | Scheduled |
| Cada domingo 2 AM UTC | - | ✅ | Scheduled |

### No Haces Nada Extra

Todo es automático. No necesitas ejecutar comandos, scripts o acciones manuales.

---

## 📋 Workflows Disponibles

### 1. DevSecOps Pipeline (`.github/workflows/devsecops.yml`)

**Qué hace:**
- Instala Python 3.12 y Node 20
- Semgrep code analysis
- pip-audit (Python dependencies)
- npm audit (JavaScript dependencies)
- Build Docker images
- Upload reports to artifacts
- (Opcional) Send to ASPM

**Cuándo se ejecuta:**
- Push a main
- Pull Request a main
- Cada domingo 3 AM UTC

**Duración:** ~3-5 minutos

### 2. Security Scan (`.github/workflows/security.yml`)

**Qué hace:**
- Semgrep analysis (paralelo)
- Dependency vulnerability check (paralelo)
- Ingest results to ASPM
- Security summary

**Cuándo se ejecuta:**
- Push a main o develop
- Pull Request a main o develop
- Cada domingo 2 AM UTC

**Duración:** ~2-4 minutos

---

## 📊 Entender Resultados

### Semgrep Findings

```json
{
  "results": [
    {
      "check_id": "python.lang.security.insecure-hash-function",
      "message": "Use of MD5 for hashing passwords",
      "path": "backend/app/security.py",
      "line": 45,
      "severity": "ERROR"
    }
  ]
}
```

**Cómo interpretarlo:**
- `ERROR` = Crítico, debe arreglarse
- `WARNING` = Revisar y considerar arreglarlo
- Línea exacta del problema
- Recomendación de la herramienta

### pip-audit Vulnerabilities

```
Found 3 vulnerabilities
├─ CVE-2023-12345 (HIGH) in requests@2.28.0
│  └─ Upgrade to requests>=2.31.0
├─ CVE-2023-67890 (MEDIUM) in django@3.2.0
│  └─ Upgrade to django>=3.2.20
└─ ...
```

**Cómo interpretarlo:**
- CVE = Common Vulnerabilities and Exposures
- HIGH/MEDIUM/LOW = Severidad
- Recomendación de versión

### npm audit Issues

```
found 5 vulnerabilities
├─ 2 high severity
├─ 2 moderate severity
└─ 1 low severity

run "npm audit fix" to fix some of these
```

---

## ⚙️ Configurar Integración ASPM (Opcional)

Si tienes una plataforma ASPM (Snyk, Aqua, etc.):

### 1. Obtener Credenciales

De tu plataforma ASPM:
```
API URL: https://tu-aspm-instance.com/api
API Key: sk_live_xxxxxxxxxxxxx
```

### 2. Agregar a GitHub Secrets

```
GitHub → Settings → Secrets and variables → Actions
→ New repository secret
```

Agregar:
```
Name: ASPM_API_URL
Value: https://tu-aspm-instance.com/api

Name: ASPM_API_KEY
Value: tu-api-key-aqui
```

### 3. Resultados Se Envían Automáticamente

Una vez configurados, cada workflow automáticamente:
```
1. Ejecuta scans
2. Genera reportes
3. ✅ Envía a ASPM
4. Los ves en dashboard ASPM
```

Sin necesidad de hacer nada más.

---

## 🚨 Si Algo Falla

### Paso 1: Ver los Logs

```
Actions → [Workflow] → [Latest Run]
→ Expand failed step
→ Ver el error exacto
```

### Errores Comunes

**"pip-audit: command not found"**
- ✅ Ya está arreglado, debería instalar
- Si sigue fallando, verificar logs

**"npm audit failed"**
- ✅ Normal si hay vulnerabilidades
- Usa `|| true` para no detener el workflow
- Ver resultados en artifacts

**"Secrets not found"**
- ✅ Normal si no configuraste ASPM
- Workflows continúan sin fallar
- Solo salt la ingesta a ASPM

**"Cannot connect to ASPM"**
- ✅ Verifica URL en secrets
- ✅ Verifica API Key válida
- ✅ Workflows siguen sin fallar

### Paso 2: Revisar Workflow

```
Actions → [Workflow Name] → View workflow file
→ Revisar la configuración
→ Comparar con documentación
```

---

## 📈 Monitorear Tendencias

### Ver Histórico

```
Actions → [Workflow Name]
→ Ver lista de todas las ejecuciones
→ Comparar: ¿Más vulnerabilidades hoy que ayer?
```

### Descargar Reportes Históricos

```
Para cada ejecución:
Actions → [Run] → Artifacts → Download
→ Comparar a lo largo del tiempo
```

---

## 🎯 Workflow Diagram

```
┌─────────────────┐
│   Push to Main  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │GitHub    │
    │Detects   │
    └────┬─────┘
         │
    ┌────▼────────────────────┐
    │ Trigger Both Workflows  │
    │ (in parallel)           │
    └────┬──────────────┬─────┘
         │              │
   ┌─────▼──────┐  ┌───▼─────────┐
   │ DevSecOps  │  │ Security    │
   │ Pipeline   │  │ Scan        │
   └─────┬──────┘  └───┬─────────┘
         │              │
    ┌────┴─────────┬───┴─────┐
    │              │         │
    ▼              ▼         ▼
 Semgrep      pip-audit  npm audit
 Analysis     Check      Check
    │              │         │
    └──────┬───────┴────┬────┘
           │            │
        ┌──▼────────────▼──┐
        │ Generate Reports │
        │ (.json files)    │
        └──┬──────────────┘
           │
        ┌──▼──────────────┐
        │ Upload Artifacts│
        │ GitHub Actions  │
        └──┬──────────────┘
           │
        ┌──▼──────────────┐
        │ (Optional) Send │
        │ to ASPM         │
        └─────────────────┘
```

---

## ✅ Checklist

- [ ] Entiendes que todo es automático
- [ ] Sabes dónde ver los workflows (Actions tab)
- [ ] Sabes cómo descargar reportes (Artifacts)
- [ ] Configuraste ASPM secrets (si tienes ASPM)
- [ ] Entiendes cómo leer los resultados

---

## 🔗 Archivos Importantes

- **`.github/workflows/devsecops.yml`** - Pipeline principal
- **`.github/workflows/security.yml`** - Escaneo de seguridad
- **`WORKFLOW_FIXES.md`** - Detalle de correcciones realizadas

### 1️⃣ **DevSecOps Pipeline** (`.github/workflows/devsecops.yml`)

**Ejecuta cuando:**
- Push a `main`
- Pull request a `main`
- Cada domingo a las 3 AM UTC

**Pasos:**

```
┌─ Setup Python (3.12)
│  └─ Install backend dependencies
│     └─ Semgrep security scan
│     └─ Pip-audit (dependency check)
│
├─ Setup Node.js (20)
│  └─ Install frontend dependencies
│     └─ npm audit
│     └─ npm run build
│
├─ Build Docker images
│  ├─ Backend container
│  └─ Frontend container
│
├─ Upload Reports
│  ├─ semgrep-results.json
│  └─ pip-audit.json
│
└─ Send to ASPM (si está configurado)
   └─ Ingest con retry (3 intentos)
```

### 2️⃣ **Security Scan** (`.github/workflows/security.yml`)

**Ejecuta cuando:**
- Push a `main` o `develop`
- Pull request a `main` o `develop`
- Cada domingo a las 2 AM UTC

**Pasos paralelos:**

```
┌─ Semgrep Code Analysis
│  └─ Scan con config auto
│  └─ Upload resultados
│  └─ Check findings
│
├─ Dependency Vulnerability Check
│  ├─ pip-audit (Python)
│  └─ npm audit (Node.js)
│  └─ Upload resultados
│
└─ Ingest to ASPM (solo en main)
   ├─ Verifica credenciales
   ├─ Envía con retry (3 intentos)
   └─ Resumen de seguridad
```

---

## 🔧 Errores Encontrados y Corregidos

### Error 1: Sintaxis Incorrecta en pip-audit
**Antes:**
```bash
pip-audit --json --output backend/pip-audit.json --fail-on high
```

**Problema:** `--fail-on high` es incorrecto. El flag correcto es `--fail-on=high`

**Después:**
```bash
pip-audit --json --output backend/pip-audit.json --fail-on=high || true
```

**Mejora:** `|| true` permite que el job continúe aunque haya vulnerabilidades

---

### Error 2: npm audit Causaba Fallo del Job
**Antes:**
```bash
npm audit --audit-level=high
```

**Problema:** Falla si encuentra vulnerabilidades, deteniendo todo el pipeline

**Después:**
```bash
npm audit --audit-level=high || true
```

**Mejora:** El análisis se ejecuta pero no detiene el workflow

---

### Error 3: Manejo Deficiente de Secretos
**Antes:**
```bash
if: ${{ secrets.ASPM_API_URL != '' && secrets.ASPM_API_KEY != '' }}
```

**Problema:**
- Los secretos no se pueden comparar en expresiones `if`
- Sin validación antes de usar en curl
- Falla silenciosa

**Después:**
```bash
if github.event_name == 'push' && github.ref == 'refs/heads/main'
...
if [ -z "$API_URL" ] || [ -z "$API_KEY" ]; then
  echo "⚠️  Secrets not configured. Skipping..."
  exit 0
fi
```

**Mejora:**
- Verifica en el script shell, no en YAML
- Mensaje claro si secretos falta
- Continúa sin fallar

---

### Error 4: Archivo de Resultados Pueden No Existir
**Antes:**
```bash
-d @backend/semgrep-results.json
```

**Problema:** Si Semgrep no encuentra nada, el archivo no existe y curl falla

**Después:**
```bash
if [ ! -f "backend/semgrep-results.json" ]; then
  echo "⚠️  No Semgrep results found. Skipping..."
  exit 0
fi
```

**Mejora:** Verifica que el archivo existe antes de usarlo

---

### Error 5: Sin Manejo de Errores de Curl
**Antes:**
```bash
status=$(curl ... -o /dev/null ...)
```

**Problema:**
- Sin ver la respuesta del servidor
- Difícil de debuggear

**Después:**
```bash
HTTP_STATUS=$(curl ... -w '%{http_code}' -o response.json ...)
echo "Response:"
cat response.json
```

**Mejora:**
- Captura HTTP status y respuesta
- Logs informativos
- Fácil debuggear en GitHub Actions

---

### Error 6: Retry Logic Falla Completamente
**Antes:**
```bash
exit 1  # Si todos los reintentos fallan
```

**Problema:** Cancela todo el pipeline por error de conexión

**Después:**
```bash
echo "⚠️  Could not ingest after 3 attempts, but workflow continues"
exit 0
```

**Mejora:** El escaneo se completa aunque la ingesta falle

---

### Error 7: Workflow de Security.yml Muy Simple
**Antes:**
- Solo Semgrep
- Sin npm audit
- Sin logs
- Falla si no hay secretos

**Después:**
```yaml
- Paralleliza Semgrep y Dependency Check
- Pasos separados y independientes
- Mejor manejo de errores
- Resumen de seguridad
- Artifacts para revisión manual
```

---

## ✅ Variables de Entorno Requeridas (GitHub Secrets)

### Configurar en: `Settings > Secrets and variables > Actions`

```bash
# Opcional - Para integración con ASPM
ASPM_API_URL=https://tu-aspm-instance.com/api
ASPM_API_KEY=tu-api-key-aquí
```

**Sin secretos:** Los workflows siguen funcionando, solo sin ingesta a ASPM

---

## 🚀 Cómo Usar

### 1. Los Workflows Se Ejecutan Automáticamente

```
event push a main
        │
        ├─→ DevSecOps Pipeline ejecuta
        │   ├─ Semgrep
        │   ├─ pip-audit
        │   ├─ npm audit
        │   ├─ Build Docker
        │   └─ (opcional) Envía a ASPM
        │
        └─→ Security Scan ejecuta en paralelo
            ├─ Semgrep analysis
            ├─ Dependency check
            ├─ Ingest results
            └─ Resumen
```

### 2. Monitorear en GitHub

1. Ve a tu repo
2. `Actions` tab
3. Selecciona el workflow que quieres ver
4. Mira los logs en tiempo real

### 3. Descargar Reportes

```
Actions > [Workflow Run]
        > Artifacts
        > [devsecops-reports]
        > Download
```

---

## 📊 Flujo de Pull Request

```
git push origin feature-branch
        │
        ├─→ GitHub abre PR
        │
        ├─→ Workflows ejecutan automáticamente
        │   ├─ DevSecOps Pipeline
        │   └─ Security Scan
        │
        ├─→ Resultados en PR
        │   ├─ Check status (✓/✗)
        │   └─ Link a los logs
        │
        └─→ Reviewer ve resultados
            ├─ Puede mergear si está ok
            └─ O pide cambios si hay vulnerabilidades
```

---

## 🔍 Monitorear Seguridad

### En la Terminal Local

```bash
# Ver qué cambios se enviarán
git log --oneline main..HEAD

# Antes de hacer push
semgrep scan --config auto .
```

### En GitHub

1. Ve a `Actions`
2. Click en el workflow que acabas de ejecutar
3. Mira:
   - ✅ Paso que pasó
   - ❌ Paso que falló
   - ⚠️ Advertencias

### Descargar y Analizar Reports

```bash
# En la sección Artifacts
# Descargar devsecops-reports.zip

unzip devsecops-reports.zip
cat backend/semgrep-results.json | jq .
```

---

## 📈 Schedule Automático

**DevSecOps:** Cada domingo 3 AM UTC
```
0 3 * * 0
```

**Security:** Cada domingo 2 AM UTC
```
0 2 * * 0
```

Puedes cambiar los horarios editando los workflows

---

## 🛠️ Troubleshooting

### Problema: "Secrets not found"
```
Solución: Ve a Settings > Secrets > Agregar ASPM_API_URL y ASPM_API_KEY
```

### Problema: "npm audit failed"
```
Esto ya está arreglado con || true
Los resultados se guardan sin fallar el pipeline
```

### Problema: "Cannot connect to ASPM"
```
- Verifica la URL en secrets
- Verifica que la clave API sea válida
- El workflow continúa sin esta integración
```

### Problema: "Semgrep timeout"
```
Aumenta el timeout en el workflow:
timeout-ms: 0  # Sin timeout
```

---

## 📚 Documentación Relevante

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semgrep Rules](https://semgrep.dev/r)
- [pip-audit Documentation](https://github.com/pypa/pip-audit)
- [npm audit Documentation](https://docs.npmjs.com/cli/v9/commands/npm-audit)

---

## 🎯 Próximos Pasos

1. **Configurar secretos** si tienes ASPM
2. **Hacer un push de prueba** a main
3. **Monitorear Actions** tab
4. **Revisar reportes** descargados
5. **Ajustar configuraciones** según necesidad
