import React, { useState, useEffect } from 'react';
import { ChevronRight, Shield, AlertTriangle, CheckCircle, Book, Code, Target, Zap, Lock, Globe } from 'lucide-react';
import './AdvancedExerciseViewer.css';

const AdvancedExerciseViewer = ({ exerciseId, onBack }) => {
  const [exercise, setExercise] = useState(null);
  const [activeTab, setActiveTab] = useState('explanation');
  const [codeTab, setCodeTab] = useState('vulnerable');
  const [hintsUsed, setHintsUsed] = useState(0);
  const [hints, setHints] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [testResult, setTestResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeSpent, setTimeSpent] = useState(0);
  const [attempts, setAttempts] = useState(0);

  // Cargar ejercicio
  useEffect(() => {
    const loadExercise = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/exercises/exercise/${exerciseId}`);
        const data = await response.json();
        setExercise(data);
        setLoading(false);
      } catch (error) {
        console.error('Error loading exercise:', error);
        setLoading(false);
      }
    };
    loadExercise();
  }, [exerciseId]);

  // Temporizador
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Obtener pistas
  const loadHints = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/exercises/exercise/${exerciseId}/hints?hints_used=${hintsUsed}`
      );
      const data = await response.json();
      setHints(data.hints);
    } catch (error) {
      console.error('Error loading hints:', error);
    }
  };

  useEffect(() => {
    loadHints();
  }, [hintsUsed]);

  // Probar ataque
  const handleTestAttack = async () => {
    setAttempts(prev => prev + 1);
    try {
      const response = await fetch(
        `http://localhost:8000/api/exercises/exercise/${exerciseId}/test-attack`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input: userInput })
        }
      );
      const data = await response.json();
      setTestResult(data);
    } catch (error) {
      console.error('Error testing attack:', error);
      setTestResult({
        success: false,
        message: 'Error en la prueba',
        details: error.message
      });
    }
  };

  // Formato de tiempo
  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) return `${hours}h ${minutes}m`;
    if (minutes > 0) return `${minutes}m ${secs}s`;
    return `${secs}s`;
  };

  if (loading) {
    return <div className="loading-container">Cargando ejercicio...</div>;
  }

  if (!exercise) {
    return <div className="error-container">Ejercicio no encontrado</div>;
  }

  return (
    <div className="advanced-exercise-viewer">
      {/* Header */}
      <div className="exercise-header">
        <button className="back-btn" onClick={onBack}>
          ← Volver
        </button>
        <div className="header-content">
          <h1>{exercise.title}</h1>
          <div className="header-badges">
            <span className="badge difficulty" style={{ backgroundColor: getDifficultyColor(exercise.difficulty) }}>
              {exercise.difficulty}
            </span>
            <span className="badge cvss" title="CVSS Score">
              <AlertTriangle size={16} /> {exercise.cvss_score}
            </span>
            <span className="badge owasp">OWASP {exercise.owasp_top_10}</span>
            <span className="badge cwe">CWE-{exercise.cwe_id}</span>
          </div>
        </div>
        <div className="header-stats">
          <div className="stat">
            <span className="stat-label">Tiempo</span>
            <span className="stat-value">{formatTime(timeSpent)}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Intentos</span>
            <span className="stat-value">{attempts}</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="exercise-content">
        {/* Tabs */}
        <div className="tabs-container">
          <div className="tabs-header">
            <button
              className={`tab ${activeTab === 'explanation' ? 'active' : ''}`}
              onClick={() => setActiveTab('explanation')}
            >
              <Book size={18} /> Explicación
            </button>
            <button
              className={`tab ${activeTab === 'attack' ? 'active' : ''}`}
              onClick={() => setActiveTab('attack')}
            >
              <Target size={18} /> Tipo de Ataque
            </button>
            <button
              className={`tab ${activeTab === 'code' ? 'active' : ''}`}
              onClick={() => setActiveTab('code')}
            >
              <Code size={18} /> Código
            </button>
            <button
              className={`tab ${activeTab === 'simulator' ? 'active' : ''}`}
              onClick={() => setActiveTab('simulator')}
            >
              <Zap size={18} /> Simulador
            </button>
            <button
              className={`tab ${activeTab === 'countermeasures' ? 'active' : ''}`}
              onClick={() => setActiveTab('countermeasures')}
            >
              <Shield size={18} /> Protección
            </button>
          </div>

          {/* Tab Contents */}
          <div className="tabs-content">
            {/* Explicación de Vulnerabilidad */}
            {activeTab === 'explanation' && (
              <div className="tab-content">
                <div className="content-section">
                  <h3>¿Qué es esta vulnerabilidad?</h3>
                  <div className="content-text">
                    {exercise.vulnerability_explanation}
                  </div>
                </div>
                
                <div className="content-section">
                  <h3>Información Técnica</h3>
                  <div className="tech-info">
                    <div className="info-item">
                      <span className="label">CWE ID:</span>
                      <span className="value">{exercise.cwe_id}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Descripción CWE:</span>
                      <span className="value">{exercise.cwe_description}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Tipo de Ataque:</span>
                      <span className="value">{exercise.attack_type}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Puntuación CVSS:</span>
                      <span className="value" style={{ color: getCVSSColor(exercise.cvss_score) }}>
                        {exercise.cvss_score}/10 - {getCVSSSeverity(exercise.cvss_score)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="content-section">
                  <h3>Objetivos de Aprendizaje</h3>
                  <ul className="learning-objectives">
                    {exercise.learning_objectives.map((obj, idx) => (
                      <li key={idx}>{obj}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Explicación del Ataque */}
            {activeTab === 'attack' && (
              <div className="tab-content">
                <div className="content-section">
                  <h3>¿Cómo Funciona el Ataque?</h3>
                  <div className="content-text">
                    {exercise.attack_explanation}
                  </div>
                </div>

                <div className="content-section">
                  <h3>Impacto en el Mundo Real</h3>
                  <div className="impact-box">
                    {exercise.real_world_impact}
                  </div>
                </div>
              </div>
            )}

            {/* Comparación de Código */}
            {activeTab === 'code' && (
              <div className="tab-content">
                <div className="code-tabs">
                  <button
                    className={`code-tab ${codeTab === 'vulnerable' ? 'active' : ''}`}
                    onClick={() => setCodeTab('vulnerable')}
                  >
                    ❌ Código Vulnerable
                  </button>
                  <button
                    className={`code-tab ${codeTab === 'secure' ? 'active' : ''}`}
                    onClick={() => setCodeTab('secure')}
                  >
                    ✅ Código Seguro
                  </button>
                </div>

                {codeTab === 'vulnerable' && (
                  <div className="code-section vulnerable">
                    <div className="code-explanation">
                      {/* Vulnerable code explanation */}
                    </div>
                    <pre className="code-block">
                      <code>{exercise.vulnerable_code}</code>
                    </pre>
                    <div className="code-insights">
                      <p><strong>Problemas:</strong></p>
                      <p>{exercise.vulnerable_code_explanation}</p>
                    </div>
                  </div>
                )}

                {codeTab === 'secure' && (
                  <div className="code-section secure">
                    <pre className="code-block">
                      <code>{exercise.secure_code}</code>
                    </pre>
                    <div className="code-insights">
                      <p><strong>Mejoras de Seguridad:</strong></p>
                      <p>{exercise.secure_code_explanation}</p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Simulador de Ataque */}
            {activeTab === 'simulator' && (
              <div className="tab-content">
                <div className="simulator-section">
                  <h3>Prueba el Ataque Aquí</h3>
                  <p className="simulator-instruction">
                    Intenta explotar la vulnerabilidad ingresando un payload de ataque.
                  </p>

                  <div className="simulator-input">
                    <textarea
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      placeholder="Ingresa tu payload aquí... (ejemplo: admin' --)"
                      rows="4"
                    />
                    <button
                      className="test-btn"
                      onClick={handleTestAttack}
                      disabled={!userInput.trim()}
                    >
                      <Zap size={18} /> Probar Ataque
                    </button>
                  </div>

                  {testResult && (
                    <div className={`test-result ${testResult.success ? 'success' : 'failed'}`}>
                      <div className="result-header">
                        {testResult.success ? (
                          <>
                            <CheckCircle size={24} /> {testResult.message}
                          </>
                        ) : (
                          <>
                            <AlertTriangle size={24} /> {testResult.message}
                          </>
                        )}
                      </div>
                      <div className="result-details">
                        <p><strong>Detalles:</strong> {testResult.details}</p>
                        {testResult.educational_insight && (
                          <div className="educational-insight">
                            <p><strong>📚 Lección Educativa:</strong></p>
                            <p>{testResult.educational_insight}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Pistas */}
                  <div className="hints-section">
                    <h4>Pistas Progresivas</h4>
                    {hints.length > 0 ? (
                      <div className="hints-list">
                        {hints.map((hint, idx) => (
                          <div key={idx} className="hint-item">
                            <span className="hint-level">💡 Pista {hint.level}:</span>
                            <p>{hint.hint}</p>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="no-hints">No hay más pistas disponibles</p>
                    )}
                    {hintsUsed < 3 && (
                      <button
                        className="next-hint-btn"
                        onClick={() => setHintsUsed(prev => prev + 1)}
                      >
                        Obtener Siguiente Pista
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Contramedidas */}
            {activeTab === 'countermeasures' && (
              <div className="tab-content">
                <div className="content-section">
                  <h3>Contramedidas Efectivas</h3>
                  <div className="content-text">
                    {exercise.countermeasures}
                  </div>
                </div>

                <div className="content-section">
                  <h3>Mejores Prácticas</h3>
                  <div className="content-text">
                    {exercise.best_practices}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Funciones auxiliares
function getDifficultyColor(difficulty) {
  const colors = {
    'BEGINNER': '#10b981',
    'INTERMEDIATE': '#f59e0b',
    'ADVANCED': '#ef4444'
  };
  return colors[difficulty] || '#6b7280';
}

function getCVSSColor(score) {
  if (score >= 9) return '#dc2626';
  if (score >= 7) return '#ea580c';
  if (score >= 4) return '#f59e0b';
  return '#10b981';
}

function getCVSSSeverity(score) {
  if (score >= 9) return 'Crítico';
  if (score >= 7) return 'Alto';
  if (score >= 4) return 'Medio';
  return 'Bajo';
}

export default AdvancedExerciseViewer;
