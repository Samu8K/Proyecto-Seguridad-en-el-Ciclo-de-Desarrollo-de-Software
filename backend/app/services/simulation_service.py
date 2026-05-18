"""
Servicio de Simulación de Ataques - Simula vulnerabilidades de forma segura
Ejecuta ataques educativos sin peligro real en aplicaciones vulnerables demo
"""

from typing import Dict, Any, Tuple
import json
import re
import html
from urllib.parse import quote, unquote


class SimulationService:
    """Simula ataques educativos de forma segura para demostración"""
    
    # Patrones para detectar intentos de exploit
    INJECTION_PATTERNS = {
        'sql': [r"'\s*OR\s*'", r"--", r";.*DROP", r"UNION.*SELECT", r"\*\/", r"\/\*"],
        'xss': [r"<script", r"javascript:", r"onerror=", r"onclick=", r"img.*src="],
        'command': [r";\s*ls", r";\s*cat", r"&&", r"\|\|", r"`"],
    }
    
    @staticmethod
    def simulate_sql_injection(payload: str) -> Dict[str, Any]:
        """
        Simula SQL Injection y muestra el resultado
        Demuestra cómo el payload alter la query
        """
        
        # Simulación de base de datos
        users_db = {
            "admin": {"password": "hashed_password_123", "role": "admin", "email": "admin@example.com"},
            "user": {"password": "hashed_password_456", "role": "user", "email": "user@example.com"},
            "guest": {"password": "hashed_password_789", "role": "guest", "email": "guest@example.com"},
        }
        
        # Query vulnerable original
        original_query = f"SELECT * FROM users WHERE username='{payload}' AND password='{payload}'"
        
        # Análisis del payload
        is_injection = any(re.search(pattern, payload, re.IGNORECASE) for pattern in SimulationService.INJECTION_PATTERNS['sql'])
        
        detected_techniques = []
        if "' OR" in payload or "' or" in payload:
            detected_techniques.append("Bypassing authentication with OR clause")
        if "--" in payload:
            detected_techniques.append("Comment-based query truncation")
        if "UNION" in payload.upper():
            detected_techniques.append("UNION-based data extraction")
        if ";" in payload:
            detected_techniques.append("Multiple statement injection")
        
        # Simular ejecución
        if is_injection:
            if "' OR '1'='1" in payload or "' OR 1=1" in payload.lower():
                result_query = f"SELECT * FROM users WHERE username='' OR '1'='1' AND password=''"
                result_data = list(users_db.items())  # Retorna todos los usuarios
                status = "ATTACK_SUCCESSFUL"
                message = "⚠️ SQL Injection successful! Query was modified to return all users."
            elif "--" in payload:
                result_query = f"SELECT * FROM users WHERE username='{payload}' --' AND password='..."
                username = payload.replace("' --", "")
                result_data = [(username, users_db.get(username, {}))] if username in users_db else []
                status = "ATTACK_SUCCESSFUL"
                message = "⚠️ SQL Injection successful! Comment clause bypassed password check."
            else:
                result_query = original_query
                result_data = []
                status = "INJECTION_DETECTED"
                message = "✓ Injection pattern detected but query structure unclear."
        else:
            result_query = original_query
            result_data = []
            status = "NO_INJECTION"
            message = "✓ No injection detected. Normal query execution."
        
        return {
            "simulation_type": "SQL_INJECTION",
            "payload": payload,
            "original_query": original_query,
            "executed_query": result_query,
            "status": status,
            "message": message,
            "detected_techniques": detected_techniques,
            "results": result_data,
            "vulnerability_severity": "CRITICAL" if status == "ATTACK_SUCCESSFUL" else "LOW",
            "explanation": SimulationService._get_sql_injection_explanation(payload, status)
        }
    
    @staticmethod
    def simulate_xss_attack(payload: str, context: str = "html") -> Dict[str, Any]:
        """
        Simula Cross-Site Scripting (XSS)
        Demuestra cómo se ejecutaría JavaScript malicioso
        """
        
        # Patrones de XSS
        is_xss = any(re.search(pattern, payload, re.IGNORECASE) for pattern in SimulationService.INJECTION_PATTERNS['xss'])
        
        detected_techniques = []
        if "<script" in payload.lower():
            detected_techniques.append("Script tag injection")
        if "javascript:" in payload.lower():
            detected_techniques.append("JavaScript protocol injection")
        if "onerror=" in payload.lower():
            detected_techniques.append("Event handler exploitation")
        if "<img" in payload.lower() or "onclick=" in payload.lower():
            detected_techniques.append("Stored XSS vulnerability")
        
        # Simular contexto vulnerable
        if context == "html":
            vulnerable_html = f"<p>User comment: {payload}</p>"
            safe_html = f"<p>User comment: {html.escape(payload)}</p>"
        elif context == "attribute":
            vulnerable_html = f'<input value="{payload}">'
            # Escapar comillas también
            safe_html = f'<input value="{html.escape(payload)}">'
        else:
            vulnerable_html = f"<div>{payload}</div>"
            safe_html = f"<div>{html.escape(payload)}</div>"
        
        status = "ATTACK_SUCCESSFUL" if is_xss else "NO_INJECTION"
        
        return {
            "simulation_type": "XSS",
            "payload": payload,
            "context": context,
            "status": status,
            "vulnerable_html": vulnerable_html,
            "safe_html": safe_html,
            "detected_techniques": detected_techniques,
            "vulnerability_severity": "HIGH" if is_xss else "LOW",
            "message": "⚠️ XSS Attack successful!" if is_xss else "✓ Payload properly escaped",
            "explanation": SimulationService._get_xss_explanation(payload, status)
        }
    
    @staticmethod
    def simulate_command_injection(command: str) -> Dict[str, Any]:
        """
        Simula Command Injection
        Demuestra cómo se podría ejecutar comandos del sistema
        """
        
        is_injection = any(re.search(pattern, command, re.IGNORECASE) for pattern in SimulationService.INJECTION_PATTERNS['command'])
        
        detected_techniques = []
        if ";" in command:
            detected_techniques.append("Command chaining with semicolon")
        if "&&" in command:
            detected_techniques.append("Conditional command execution (AND)")
        if "||" in command:
            detected_techniques.append("Conditional command execution (OR)")
        if "|" in command:
            detected_techniques.append("Pipe to another command")
        if "`" in command or "$(" in command:
            detected_techniques.append("Command substitution")
        
        # Simular ejecución segura vs vulnerable
        safe_execution = f"search({repr(command)})"
        vulnerable_execution = command
        
        return {
            "simulation_type": "COMMAND_INJECTION",
            "payload": command,
            "status": "ATTACK_SUCCESSFUL" if is_injection else "NO_INJECTION",
            "detected_techniques": detected_techniques,
            "vulnerability_severity": "CRITICAL" if is_injection else "LOW",
            "safe_execution": safe_execution,
            "message": "⚠️ Command Injection successful!" if is_injection else "✓ Command properly sanitized",
            "explanation": SimulationService._get_command_injection_explanation(command, is_injection)
        }
    
    @staticmethod
    def validate_solution(
        exercise_type: str,
        user_code: str,
        test_payload: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Valida la solución del usuario verificando si es segura
        """
        
        checks = {
            "uses_prepared_statements": False,
            "input_validation": False,
            "output_encoding": False,
            "error_handling": False,
            "security_headers": False,
        }
        
        # Análisis del código
        code_lower = user_code.lower()
        
        if exercise_type == "SQL_INJECTION":
            checks["uses_prepared_statements"] = any(
                pattern in code_lower for pattern in 
                ['prepared', 'parameterized', 'execute(', '?', '%s']
            )
            checks["input_validation"] = any(
                pattern in code_lower for pattern in
                ['validate', 'check', 'sanitize', 'strip']
            )
        
        elif exercise_type == "XSS":
            checks["output_encoding"] = any(
                pattern in code_lower for pattern in
                ['escape', 'htmlescape', 'sanitize', 'quote']
            )
            checks["input_validation"] = 'validate' in code_lower
        
        elif exercise_type == "COMMAND_INJECTION":
            checks["input_validation"] = any(
                pattern in code_lower for pattern in
                ['validate', 'whitelist', 'safe']
            )
        
        passed_checks = sum(1 for v in checks.values() if v)
        total_checks = len(checks)
        score = int((passed_checks / total_checks) * 100)
        is_correct = score >= 60
        
        return is_correct, {
            "score": score,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "checks_detail": checks,
            "feedback": SimulationService._get_validation_feedback(checks, exercise_type)
        }
    
    @staticmethod
    def _get_sql_injection_explanation(payload: str, status: str) -> str:
        """Explicación de lo que sucedió en la simulación de SQL Injection"""
        if status == "ATTACK_SUCCESSFUL":
            return f"""
            ⚠️ **ATTACK ANALYSIS**
            
            Your payload successfully modified the SQL query behavior:
            
            **Original Intent**: Search for user with matching username and password
            **What Happened**: The query was bypassed
            
            **Key Points**:
            - The single quote (') closed the string prematurely
            - Your additional SQL code was interpreted as part of the query
            - The database executed unintended commands
            - In a real scenario, this could lead to data breach
            
            **Why This Is Dangerous**:
            - Attackers can extract entire databases
            - User credentials can be compromised
            - Data can be modified or deleted
            """
        else:
            return "No successful SQL Injection detected in this payload."
    
    @staticmethod
    def _get_xss_explanation(payload: str, status: str) -> str:
        """Explicación de lo que sucedió en la simulación de XSS"""
        if status == "ATTACK_SUCCESSFUL":
            return f"""
            ⚠️ **ATTACK ANALYSIS**
            
            Your payload would execute JavaScript code in the victim's browser:
            
            **What Could Happen**:
            - Steal session cookies
            - Redirect to phishing site
            - Capture keyboard input
            - Deface the website
            - Spread malware
            
            **Why This Is Dangerous**:
            - Affects all users who view the content
            - No server-side detection possible
            - User data can be compromised
            """
        else:
            return "No XSS vulnerability detected. Payload was properly encoded."
    
    @staticmethod
    def _get_command_injection_explanation(command: str, is_injection: bool) -> str:
        """Explicación de lo que sucedió en la simulación de Command Injection"""
        if is_injection:
            return f"""
            ⚠️ **ATTACK ANALYSIS**
            
            Your payload would execute arbitrary system commands:
            
            **What Could Happen**:
            - Read sensitive system files
            - Execute malware
            - Create backdoors
            - Compromise entire server
            - Access other applications
            
            **Why This Is Dangerous**:
            - Full system compromise possible
            - No recovery possible without reinstall
            - Can affect all users of the system
            """
        else:
            return "No command injection detected. Input was properly sanitized."
    
    @staticmethod
    def _get_validation_feedback(checks: Dict[str, bool], exercise_type: str) -> str:
        """Genera feedback de validación de la solución"""
        feedback = []
        
        if exercise_type == "SQL_INJECTION":
            if not checks["uses_prepared_statements"]:
                feedback.append("❌ Use prepared statements or parameterized queries")
            if not checks["input_validation"]:
                feedback.append("❌ Add input validation and sanitization")
            if checks["uses_prepared_statements"]:
                feedback.append("✓ Good! Prepared statements prevent SQL Injection")
        
        elif exercise_type == "XSS":
            if not checks["output_encoding"]:
                feedback.append("❌ Encode output to prevent XSS")
            if not checks["input_validation"]:
                feedback.append("❌ Validate and sanitize user input")
            if checks["output_encoding"]:
                feedback.append("✓ Good! Output encoding prevents XSS")
        
        if not feedback:
            feedback.append("✓ Solution looks secure!")
        
        return " | ".join(feedback)
