"""
API Routes Mejoradas para Ejercicios Interactivos
Replicando la metodología de Secure Coding Dojo
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.exercises.exercises_data import COMPLETE_EXERCISES, PROGRESSION
from datetime import datetime
from typing import List, Dict, Any
from uuid import uuid4

router = APIRouter(prefix="/api/exercises", tags=["interactive_exercises"])

# ==================== EJERCICIOS INTERACTIVOS ====================

@router.get("/all")
async def get_all_exercises():
    """Obtiene todos los ejercicios disponibles"""
    exercises_list = []
    for key, exercise in COMPLETE_EXERCISES.items():
        exercises_list.append({
            "id": exercise["id"],
            "title": exercise["title"],
            "short_title": exercise["short_title"],
            "description": exercise["description"],
            "difficulty": exercise["difficulty"],
            "vulnerability_type": exercise["vulnerability_type"],
            "icon": exercise["icon"],
            "color": exercise["color"],
            "cvss_score": exercise["cvss_score"],
            "owasp_top_10": exercise["owasp_top_10"],
        })
    return {
        "total": len(exercises_list),
        "exercises": sorted(exercises_list, key=lambda x: x["cvss_score"], reverse=True)
    }

@router.get("/exercise/{exercise_id}")
async def get_exercise_details(exercise_id: str):
    """Obtiene detalles completos de un ejercicio"""
    if exercise_id not in COMPLETE_EXERCISES:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise = COMPLETE_EXERCISES[exercise_id]
    return {
        "id": exercise["id"],
        "title": exercise["title"],
        "short_title": exercise["short_title"],
        "description": exercise["description"],
        "difficulty": exercise["difficulty"],
        "vulnerability_type": exercise["vulnerability_type"],
        "attack_type": exercise["attack_type"],
        "icon": exercise["icon"],
        "color": exercise["color"],
        "cvss_score": exercise["cvss_score"],
        "owasp_top_10": exercise["owasp_top_10"],
        "cwe_id": exercise["cwe_id"],
        "cwe_description": exercise["cwe_description"],
        "vulnerability_explanation": exercise["vulnerability_explanation"],
        "attack_explanation": exercise["attack_explanation"],
        "real_world_impact": exercise["real_world_impact"],
        "countermeasures": exercise["countermeasures"],
        "best_practices": exercise["best_practices"],
        "learning_objectives": exercise["learning_objectives"],
    }

@router.get("/exercise/{exercise_id}/code")
async def get_exercise_code(exercise_id: str):
    """Obtiene código vulnerable y seguro"""
    if exercise_id not in COMPLETE_EXERCISES:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise = COMPLETE_EXERCISES[exercise_id]
    return {
        "id": exercise["id"],
        "vulnerable": {
            "code": exercise["vulnerable_code"],
            "language": exercise["vulnerable_code_language"],
            "explanation": exercise["vulnerable_code_explanation"]
        },
        "secure": {
            "code": exercise["secure_code"],
            "language": exercise["secure_code_language"],
            "explanation": exercise["secure_code_explanation"]
        }
    }

@router.get("/exercise/{exercise_id}/hints")
async def get_exercise_hints(exercise_id: str, hints_used: int = Query(0)):
    """Obtiene pistas progresivas del ejercicio"""
    if exercise_id not in COMPLETE_EXERCISES:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise = COMPLETE_EXERCISES[exercise_id]
    hints = []
    
    if hints_used >= 0:
        hints.append({"level": 1, "hint": exercise["hint_1"]})
    if hints_used >= 1:
        hints.append({"level": 2, "hint": exercise["hint_2"]})
    if hints_used >= 2:
        hints.append({"level": 3, "hint": exercise["hint_3"]})
    
    return {
        "id": exercise["id"],
        "total_hints": 3,
        "hints": hints,
        "next_hint_level": min(hints_used + 1, 3)
    }

@router.get("/exercise/{exercise_id}/references")
async def get_exercise_references(exercise_id: str):
    """Obtiene referencias y recursos adicionales"""
    if exercise_id not in COMPLETE_EXERCISES:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise = COMPLETE_EXERCISES[exercise_id]
    return {
        "id": exercise["id"],
        "references": exercise["references"],
        "learning_objectives": exercise["learning_objectives"]
    }

# ==================== SIMULADOR DE ATAQUES ====================

@router.post("/exercise/{exercise_id}/test-attack")
async def test_attack(exercise_id: str, payload: Dict[str, Any]):
    """Simula un ataque en el ejercicio"""
    if exercise_id not in COMPLETE_EXERCISES:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    exercise = COMPLETE_EXERCISES[exercise_id]
    user_input = payload.get("input", "")
    
    # Simular diferentes tipos de ataque según el ejercicio
    result = simulate_attack(exercise_id, user_input, exercise)
    
    return {
        "exercise_id": exercise_id,
        "vulnerability_type": exercise["vulnerability_type"],
        "success": result["success"],
        "message": result["message"],
        "details": result["details"],
        "educational_insight": result["educational_insight"]
    }

def simulate_attack(exercise_id: str, payload: str, exercise: Dict) -> Dict:
    """Simula el ataque y proporciona retroalimentación educativa"""
    
    if exercise_id == "1_sql_injection_login":
        # SQL Injection detection
        dangerous_patterns = ["' --", "' OR", "'; DROP", "UNION SELECT", "1'='1"]
        
        if any(pattern in payload for pattern in dangerous_patterns):
            return {
                "success": True,
                "message": "✅ ¡ATAQUE EXITOSO! SQL Injection detectado.",
                "details": f"El payload '{payload}' contiene un patrón de SQL Injection válido.",
                "educational_insight": """
                Este payload explota la vulnerabilidad porque:
                1. Cierra la cadena de la query con '
                2. Comenta el resto con --
                3. Permite login sin contraseña
                
                En código seguro, esto sería imposible porque los parámetros están separados de la query.
                """
            }
        else:
            return {
                "success": False,
                "message": "❌ Ataque bloqueado o inefectivo.",
                "details": "El payload no contiene patrones válidos de SQL Injection.",
                "educational_insight": "Intenta usar caracteres especiales SQL como ', --, OR"
            }
    
    elif exercise_id == "2_xss_comment_section":
        # XSS detection
        xss_patterns = ["<script", "<img", "onerror", "onload", "onclick", "javascript:"]
        
        if any(pattern in payload.lower() for pattern in xss_patterns):
            return {
                "success": True,
                "message": "✅ ¡ATAQUE EXITOSO! Cross-Site Scripting detectado.",
                "details": f"El payload '{payload}' contiene código JavaScript inyectable.",
                "educational_insight": """
                Este payload ejecutaría JavaScript porque:
                1. Se renderiza directamente en HTML
                2. El navegador interpreta las etiquetas
                3. Se ejecutan los event handlers (onerror, onload, etc.)
                
                Con protección XSS, esta entrada sería escapada y tratada como texto.
                """
            }
        else:
            return {
                "success": False,
                "message": "❌ Ataque bloqueado o inefectivo.",
                "details": "El payload no contiene código inyectable.",
                "educational_insight": "Intenta usar <img>, <script>, onerror, onload"
            }
    
    elif exercise_id == "3_broken_authentication_weak_session":
        # Session prediction
        if payload.startswith("user_") and payload.count("_") == 2:
            parts = payload.split("_")
            try:
                user_id = int(parts[1])
                sequence = int(parts[2])
                
                return {
                    "success": True,
                    "message": "✅ ¡ATAQUE EXITOSO! Token de sesión predecible.",
                    "details": f"El token '{payload}' sigue un patrón predecible: user_{{id}}_{{sequence}}",
                    "educational_insight": """
                    Este token es predecible porque:
                    1. Sigue un patrón matemático simple
                    2. Se puede enumerar fácilmente
                    3. No tiene entropía criptográfica
                    
                    En código seguro, se usarían tokens generados con secrets.token_urlsafe()
                    o JWT firmados que son imposibles de predecir.
                    """
                }
            except ValueError:
                pass
        
        return {
            "success": False,
            "message": "❌ Token inválido o impredecible.",
            "details": "El formato no coincide con el patrón vulnerable.",
            "educational_insight": "Intenta el formato: user_{{user_id}}_{{secuencia}}"
        }
    
    elif exercise_id == "4_insecure_deserialization":
        # Deserialization attack detection
        pickle_patterns = ["cos", "system", "__reduce__", "os.system"]
        
        if any(pattern in payload.lower() for pattern in pickle_patterns):
            return {
                "success": True,
                "message": "✅ ¡ATAQUE EXITOSO! Deserialización Insegura detectada.",
                "details": f"El payload contiene una cadena de gadgets para RCE.",
                "educational_insight": """
                Este payload permite RCE porque:
                1. pickle.loads() ejecuta código automáticamente
                2. La clase Exploit tiene __reduce__() que ejecuta comandos
                3. Se pueden usar gadget chains existentes
                
                En código seguro, se usaría JSON que no ejecuta código.
                """
            }
        else:
            return {
                "success": False,
                "message": "❌ Payload inválido para deserialización.",
                "details": "El payload no contiene gadgets válidos.",
                "educational_insight": "Intenta crear una clase Python con __reduce__() que ejecute un comando"
            }
    
    elif exercise_id == "5_weak_encryption":
        # Weak cryptography detection
        weak_patterns = ["md5", "sha1", "des", "ecb", "no_salt"]
        
        if any(pattern in payload.lower() for pattern in weak_patterns):
            return {
                "success": True,
                "message": "✅ ¡VULNERABILIDAD IDENTIFICADA! Criptografía Débil detectada.",
                "details": f"El algoritmo '{payload}' es vulnerable a ataques modernos.",
                "educational_insight": """
                Por qué esto es vulnerable:
                - MD5: Colisiones demostradas, vulnerable a rainbow tables
                - SHA-1: Debilitado, colisiones teóricas
                - DES: Solo 56 bits, se rompe en minutos con GPU
                - ECB: Revela patrones en el ciphertext
                - Sin salt: Rainbow tables funcionan perfectamente
                
                En código seguro, se usaría bcrypt/argon2 para contraseñas y AES-256-GCM para datos.
                """
            }
        else:
            return {
                "success": False,
                "message": "❌ Algoritmo no reconocido.",
                "details": "Intenta identificar un algoritmo débil específico.",
                "educational_insight": "Prueba con: md5, sha1, des, ecb"
            }
    
    return {
        "success": False,
        "message": "Ejercicio no reconocido.",
        "details": "",
        "educational_insight": ""
    }

# ==================== PROGRESIÓN Y LOGROS ====================

@router.get("/progression")
async def get_progression():
    """Obtiene la estructura de progresión"""
    return PROGRESSION

@router.get("/progression/{level}")
async def get_level_details(level: str):
    """Obtiene detalles de un nivel específico"""
    if level not in PROGRESSION:
        raise HTTPException(status_code=404, detail="Level not found")
    
    level_data = PROGRESSION[level]
    challenges = []
    
    for challenge_id in level_data["challenges"]:
        if challenge_id in COMPLETE_EXERCISES:
            challenge = COMPLETE_EXERCISES[challenge_id]
            challenges.append({
                "id": challenge["id"],
                "title": challenge["title"],
                "difficulty": challenge["difficulty"],
                "cvss_score": challenge["cvss_score"]
            })
    
    return {
        "level": level,
        "title": level_data["title"],
        "challenges": challenges,
        "rewards": level_data["rewards"],
        "unlocks": level_data["unlocks"]
    }

# ==================== ESTADÍSTICAS ====================

@router.get("/statistics")
async def get_statistics():
    """Obtiene estadísticas globales"""
    total_exercises = len(COMPLETE_EXERCISES)
    difficulties = {"BEGINNER": 0, "INTERMEDIATE": 0, "ADVANCED": 0}
    vulnerabilities = {}
    
    for exercise in COMPLETE_EXERCISES.values():
        difficulties[exercise["difficulty"]] += 1
        vuln_type = exercise["vulnerability_type"]
        vulnerabilities[vuln_type] = vulnerabilities.get(vuln_type, 0) + 1
    
    return {
        "total_exercises": total_exercises,
        "by_difficulty": difficulties,
        "by_vulnerability": vulnerabilities,
        "average_cvss": sum(e["cvss_score"] for e in COMPLETE_EXERCISES.values()) / total_exercises
    }
