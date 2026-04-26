# Ejemplos de Uso - ASPM Vulnerability Management

## 🎯 Objetivo del Sistema

Este sistema está diseñado para **gestión integral de vulnerabilidades** con capacidades avanzadas de:

- **Recepción**: Integración con múltiples herramientas de seguridad (SAST, DAST, SCA, IAST)
- **Clasificación**: Categorización por CWE, OWASP Top 10, y tipos de vulnerabilidad
- **Priorización Inteligente**: Score calculado basado en múltiples factores de riesgo
- **Seguimiento**: Estados, asignación, y gestión del ciclo de vida

## 📥 Formato de Entrada Completo

El sistema recibe vulnerabilidades con metadata completa para priorización inteligente:

```json
{
  "tenant_id": "string",
  "project_id": "string",
  "scan_id": "string",           // ID único del escaneo
  "tool_info": {                 // Información global de herramienta
    "name": "semgrep",
    "version": "1.50.0",
    "type": "SAST"              // SAST, DAST, SCA, IAST
  },
  "context": {                   // Contexto global del escaneo
    "commit_hash": "a1b2c3d...",
    "branch": "main",
    "author": "dev@company.com",
    "repository_url": "https://...",
    "scan_date": "2026-04-26T10:30:00Z"
  },
  "findings": [
    {
      // Información básica
      "title": "string",
      "description": "string",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",

      // Clasificación
      "cwe_id": "CWE-XXX",
      "owasp_top_10": "A01:2021-...",
      "category": "Injection|XSS|Auth|etc.",

      // Ubicación precisa
      "file_path": "string",
      "line_number": number,
      "code_snippet": "string",
      "function_name": "string",
      "class_name": "string",

      // Priorización avanzada
      "cvss": {
        "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "base_score": number,
        "temporal_score": number,
        "environmental_score": number
      },
      "confidence": number,      // 0.0 - 1.0
      "impact": "HIGH|MEDIUM|LOW",
      "exploitability": "HIGH|MEDIUM|LOW",

      // Metadatos
      "tags": ["array", "of", "tags"],
      "references": ["array", "of", "urls"],
      "custom_fields": {"key": "value"},

      // Información específica de herramienta
      "tool": {
        "name": "string",
        "version": "string",
        "type": "SAST|DAST|SCA|IAST"
      },

      // Contexto específico
      "context": {
        "commit_hash": "string",
        "branch": "string",
        "author": "string",
        "repository_url": "string",
        "scan_date": "datetime"
      }
    }
  ]
}
```

## 🧠 Sistema de Priorización Inteligente

El sistema calcula un **Priority Score** basado en múltiples factores:

### Factores Considerados:
- **40%**: Severidad/CVSS Score
- **20%**: Impacto potencial
- **20%**: Explotabilidad
- **10%**: Confianza de la herramienta
- **10%**: Confianza en la detección

### Pesos por Tipo de Herramienta:
- **IAST**: 100% (máxima confianza - testing en runtime)
- **DAST**: 90% (alta confianza - testing dinámico)
- **SAST**: 80% (buena confianza - análisis estático)
- **SCA**: 70% (confianza moderada - dependencias)

### Ejemplo de Cálculo:
```
Vulnerabilidad SQL Injection:
- CVSS: 9.8 (40% = 3.92)
- Impact: HIGH (20% = 2.0)
- Exploitability: HIGH (20% = 2.0)
- Tool: SAST (10% = 0.8)
- Confidence: 0.95 (10% = 0.95)
- **Priority Score: 9.67**
```

## 🔄 Estados de Vulnerabilidades

- `OPEN`: Nueva vulnerabilidad detectada
- `IN_PROGRESS`: En proceso de resolución
- `RESOLVED`: Solucionada
- `FALSE_POSITIVE`: Detectada automáticamente como falso positivo
- `ACCEPTED_RISK`: Riesgo aceptado por la organización

## 🤖 Detección Automática de Falsos Positivos

Reglas inteligentes basadas en:
- **Ubicación**: Archivos de test, mock, dev
- **Severidad**: Vulnerabilidades "INFO"
- **Tipo de herramienta**: SCA en entornos dev
- **Contexto**: Configuraciones específicas

## 📊 Reportes Disponibles

### 1. Dashboard de Métricas
- Conteo por estado y severidad
- Tendencias de vulnerabilidades
- Distribución por categorías

### 2. Listado Detallado
- Filtros por estado, severidad, herramienta
- Información completa de priorización
- Historial de cambios

### 3. Reportes de Equipos
- Agrupación por proyecto/tenant
- Métricas de rendimiento del equipo
- SLA de resolución

## 🚀 Integración con Herramientas

### Herramientas Soportadas:
- **SAST**: Semgrep, SonarQube, ESLint Security
- **DAST**: OWASP ZAP, Burp Suite, Acunetix
- **SCA**: OWASP Dependency Check, Snyk, WhiteSource
- **IAST**: Contrast Security, Seeker

### Formatos de Salida Esperados:
Cada herramienta debe mapear su salida al schema estándar del sistema.

## 📈 Beneficios del Nuevo Formato

✅ **Priorización Inteligente**: No solo severidad, sino riesgo real
✅ **Contexto Completo**: Información de commit, autor, repositorio
✅ **Trazabilidad**: Referencias CWE, OWASP, CVSS vectors
✅ **Flexibilidad**: Campos customizables para necesidades específicas
✅ **Integración**: Soporte nativo para múltiples tipos de herramientas