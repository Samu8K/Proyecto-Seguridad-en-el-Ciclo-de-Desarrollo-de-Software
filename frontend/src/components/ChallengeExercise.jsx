import React, { useState, useEffect } from 'react';
import { ChevronRight, Zap, Shield, AlertCircle, CheckCircle, BookOpen, Code } from 'lucide-react';
import './ChallengeExercise.css';

export default function ChallengeExercise({ challenge, onComplete, onBack }) {
  const [activeTab, setActiveTab] = useState('explanation');
  const [currentHintLevel, setCurrentHintLevel] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [showCode, setShowCode] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [attempts, setAttempts] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleRequestHint = () => {
    if (currentHintLevel < 3) {
      setCurrentHintLevel(prev => prev + 1);
      setShowHint(true);
    }
  };

  const handleComplete = () => {
    setAttempts(prev => prev + 1);
    onComplete({
      challengeId: challenge.id,
      attempts,
      timeSpent,
      hintsUsed: currentHintLevel
    });
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      'BEGINNER': 'bg-green-500/20 text-green-700',
      'INTERMEDIATE': 'bg-yellow-500/20 text-yellow-700',
      'ADVANCED': 'bg-red-500/20 text-red-700'
    };
    return colors[difficulty] || 'bg-gray-500/20 text-gray-700';
  };

  const getVulnIcon = (vuln) => {
    const icons = {
      'SQL_INJECTION': '💉',
      'XSS': '🔤',
      'CSRF': '🔗',
      'BROKEN_AUTH': '🔑',
      'IDOR': '🚪',
      'INSECURE_DESERIALIZE': '⚙️'
    };
    return icons[vuln] || '🔓';
  };

  return (
    <div className="challenge-exercise-container">
      {/* Header */}
      <div className="challenge-header">
        <button onClick={onBack} className="btn-back">
          ← Volver
        </button>
        
        <div className="challenge-title-section">
          <span className="challenge-icon">{getVulnIcon(challenge.vulnerability_type)}</span>
          <div>
            <h1>{challenge.title}</h1>
            <p className="challenge-subtitle">{challenge.description}</p>
          </div>
        </div>

        <div className="challenge-stats">
          <div className="stat">
            <span className="stat-label">Tiempo</span>
            <span className="stat-value">{formatTime(timeSpent)}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Intentos</span>
            <span className="stat-value">{attempts}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Pistas</span>
            <span className="stat-value">{currentHintLevel}/3</span>
          </div>
        </div>
      </div>

      {/* Info Bar */}
      <div className="info-bar">
        <div className="info-item">
          <Zap size={18} className="text-yellow-500" />
          <span>CVSS: {challenge.cvss_score}/10</span>
        </div>
        <div className="info-item">
          <Shield size={18} className="text-blue-500" />
          <span>{challenge.owasp_top_10}</span>
        </div>
        <div className={`badge ${getDifficultyColor(challenge.difficulty)}`}>
          {challenge.difficulty}
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="tabs-nav">
        <button 
          className={`tab-btn ${activeTab === 'explanation' ? 'active' : ''}`}
          onClick={() => setActiveTab('explanation')}
        >
          <AlertCircle size={18} />
          <span>Explicación</span>
        </button>
        <button 
          className={`tab-btn ${activeTab === 'attack' ? 'active' : ''}`}
          onClick={() => setActiveTab('attack')}
        >
          <Zap size={18} />
          <span>Cómo Ataca</span>
        </button>
        <button 
          className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          <Code size={18} />
          <span>Comparar Código</span>
        </button>
        <button 
          className={`tab-btn ${activeTab === 'protection' ? 'active' : ''}`}
          onClick={() => setActiveTab('protection')}
        >
          <Shield size={18} />
          <span>Cómo Protegerse</span>
        </button>
        <button 
          className={`tab-btn ${activeTab === 'impact' ? 'active' : ''}`}
          onClick={() => setActiveTab('impact')}
        >
          <AlertCircle size={18} />
          <span>Impacto Real</span>
        </button>
      </div>

      {/* Content Area */}
      <div className="challenge-content">
        {activeTab === 'explanation' && (
          <div className="content-section">
            <div className="content-header">
              <h2>¿Qué es {challenge.short_title}?</h2>
              <p className="text-sm text-gray-400">CWE-{challenge.cwe_id}</p>
            </div>
            <div className="content-body">
              <p>{challenge.vulnerability_explanation}</p>
              <div className="key-points">
                <h3>Puntos Clave:</h3>
                {challenge.learning_objectives.split('\n').map((line, i) => (
                  line.trim() && <div key={i} className="key-point">{line.trim()}</div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'attack' && (
          <div className="content-section">
            <div className="content-header">
              <h2>Cómo Funciona el Ataque</h2>
              <span className="badge-info">Tipo: {challenge.attack_type}</span>
            </div>
            <div className="content-body">
              <p>{challenge.attack_explanation}</p>
              <div className="alert-box alert-danger">
                <AlertCircle size={20} />
                <div>
                  <h3>Impacto Potencial</h3>
                  <p>{challenge.real_world_impact.split('\n')[1]}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'code' && (
          <div className="content-section">
            <div className="content-header">
              <h2>Comparación de Código</h2>
              <button className="btn-small" onClick={() => setShowCode(!showCode)}>
                {showCode ? 'Ocultar' : 'Ver'} Código
              </button>
            </div>
            
            {showCode && (
              <div className="code-comparison">
                <div className="code-block vulnerable">
                  <div className="code-header">
                    ❌ CÓDIGO VULNERABLE
                    <span className="lang-badge">{challenge.vulnerable_code_language}</span>
                  </div>
                  <pre><code>{challenge.vulnerable_code}</code></pre>
                  <div className="code-explanation">
                    <h4>¿Por qué es vulnerable?</h4>
                    <p>{challenge.vulnerable_code_explanation}</p>
                  </div>
                </div>

                <div className="code-block secure">
                  <div className="code-header">
                    ✅ CÓDIGO SEGURO
                    <span className="lang-badge">{challenge.secure_code_language}</span>
                  </div>
                  <pre><code>{challenge.secure_code}</code></pre>
                  <div className="code-explanation">
                    <h4>¿Por qué es seguro?</h4>
                    <p>{challenge.secure_code_explanation}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'protection' && (
          <div className="content-section">
            <div className="content-header">
              <h2>Cómo Protegerse</h2>
            </div>
            <div className="content-body">
              <div className="countermeasures-section">
                <h3>Contramedidas Recomendadas:</h3>
                <div className="countermeasures-list">
                  {challenge.countermeasures.split('\n').map((line, i) => (
                    line.trim() && <div key={i} className="countermeasure-item">{line.trim()}</div>
                  ))}
                </div>
              </div>

              <div className="best-practices-section">
                <h3>Mejores Prácticas:</h3>
                <div className="practices-grid">
                  {challenge.best_practices.split('\n').map((line, i) => (
                    line.trim() && (
                      <div key={i} className="practice-item">
                        <CheckCircle size={16} />
                        <span>{line.replace(/^✓\s*/, '')}</span>
                      </div>
                    )
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'impact' && (
          <div className="content-section">
            <div className="content-header">
              <h2>Impacto en el Mundo Real</h2>
            </div>
            <div className="content-body">
              <p>{challenge.real_world_impact}</p>
              <div className="references-section">
                <h3>Referencias y Recursos:</h3>
                <div className="references-list">
                  {challenge.references.split('\n').map((line, i) => (
                    line.trim() && <div key={i} className="reference-item">{line.trim()}</div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Hints Section */}
      <div className="hints-section">
        <h3>Sistema de Pistas Progresivas</h3>
        <div className="hints-container">
          {[1, 2, 3].map((level) => (
            <div key={level} className={`hint-card ${currentHintLevel >= level ? 'unlocked' : 'locked'}`}>
              <div className="hint-level">Pista {level}</div>
              {currentHintLevel >= level && (
                <div className="hint-content">
                  {level === 1 && <p>{challenge.hints.level_1}</p>}
                  {level === 2 && <p>{challenge.hints.level_2}</p>}
                  {level === 3 && <p>{challenge.hints.level_3}</p>}
                </div>
              )}
              {currentHintLevel < level && (
                <button 
                  className="btn-unlock"
                  onClick={handleRequestHint}
                  disabled={currentHintLevel !== level - 1}
                >
                  Desbloquear
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="btn btn-primary" onClick={handleComplete}>
          <CheckCircle size={20} />
          He Completado Este Desafío
        </button>
        <button className="btn btn-secondary" onClick={() => setActiveTab('code')}>
          <Code size={20} />
          Ver Solución
        </button>
      </div>
    </div>
  );
}
