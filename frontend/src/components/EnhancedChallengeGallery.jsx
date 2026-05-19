import React, { useState, useEffect } from 'react';
import { Zap, Target, Lock, AlertTriangle, TrendingUp, Award } from 'lucide-react';
import API_URL from '../config';
import './EnhancedChallengeGallery.css';

const EnhancedChallengeGallery = ({ onSelectChallenge }) => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterDifficulty, setFilterDifficulty] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [statistics, setStatistics] = useState(null);

  // Cargar ejercicios y estadísticas
  useEffect(() => {
    const loadData = async () => {
      try {
        const [exercisesRes, statsRes] = await Promise.all([
          fetch(`${API_URL}/api/exercises/all`),
          fetch(`${API_URL}/api/exercises/statistics`)
        ]);

        const exercisesData = await exercisesRes.json();
        const statsData = await statsRes.json();

        setExercises(exercisesData.exercises || []);
        setStatistics(statsData);
        setLoading(false);
      } catch (error) {
        console.error('Error loading exercises:', error);
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filtrar ejercicios
  const filteredExercises = exercises.filter(ex => {
    const matchesDifficulty = filterDifficulty === 'ALL' || ex.difficulty === filterDifficulty;
    const matchesSearch = ex.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          ex.vulnerability_type.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesDifficulty && matchesSearch;
  });

  if (loading) {
    return <div className="gallery-loading">Cargando ejercicios...</div>;
  }

  return (
    <div className="enhanced-gallery">
      {/* Header */}
      <div className="gallery-header">
        <div className="header-content">
          <h1>🛡️ Ejercicios Educativos de Seguridad</h1>
          <p>Aprende seguridad en la codificación mediante ejercicios prácticos y simulaciones reales</p>
        </div>
      </div>

      {/* Estadísticas */}
      {statistics && (
        <div className="statistics-container">
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <span className="stat-label">Total de Ejercicios</span>
              <span className="stat-value">{statistics.total_exercises}</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🟢</div>
            <div className="stat-content">
              <span className="stat-label">Principiante</span>
              <span className="stat-value">{statistics.by_difficulty.BEGINNER}</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🟡</div>
            <div className="stat-content">
              <span className="stat-label">Intermedio</span>
              <span className="stat-value">{statistics.by_difficulty.INTERMEDIATE}</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔴</div>
            <div className="stat-content">
              <span className="stat-label">Avanzado</span>
              <span className="stat-value">{statistics.by_difficulty.ADVANCED}</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <span className="stat-label">CVSS Promedio</span>
              <span className="stat-value">{statistics.average_cvss.toFixed(1)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Filtros y Búsqueda */}
      <div className="filters-section">
        <div className="search-container">
          <input
            type="text"
            placeholder="🔍 Buscar ejercicio..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="difficulty-filters">
          {['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'].map(difficulty => (
            <button
              key={difficulty}
              className={`filter-btn ${filterDifficulty === difficulty ? 'active' : ''}`}
              onClick={() => setFilterDifficulty(difficulty)}
            >
              {difficulty === 'ALL' && 'Todos'}
              {difficulty === 'BEGINNER' && '🟢 Principiante'}
              {difficulty === 'INTERMEDIATE' && '🟡 Intermedio'}
              {difficulty === 'ADVANCED' && '🔴 Avanzado'}
            </button>
          ))}
        </div>
      </div>

      {/* Galería de Ejercicios */}
      <div className="exercises-grid">
        {filteredExercises.length > 0 ? (
          filteredExercises.map(exercise => (
            <div key={exercise.id} className="exercise-card" onClick={() => onSelectChallenge(exercise.id)}>
              <div className="card-header" style={{ borderTopColor: getDifficultyColor(exercise.difficulty) }}>
                <div className="card-icon">{exercise.icon}</div>
                <div className="card-title-section">
                  <h3>{exercise.title}</h3>
                  <p>{exercise.vulnerability_type.replace(/_/g, ' ')}</p>
                </div>
              </div>

              <div className="card-body">
                <p className="card-description">{exercise.description}</p>

                <div className="card-metrics">
                  <div className="metric">
                    <span className="metric-icon">📋</span>
                    <span className="metric-label">OWASP</span>
                    <span className="metric-value">{exercise.owasp_top_10}</span>
                  </div>
                  <div className="metric">
                    <span className="metric-icon">⚠️</span>
                    <span className="metric-label">CVSS</span>
                    <span className={`metric-value cvss-${getCVSSLevel(exercise.cvss_score)}`}>
                      {exercise.cvss_score}
                    </span>
                  </div>
                </div>

                <div className="card-difficulty">
                  <span
                    className="difficulty-badge"
                    style={{ backgroundColor: getDifficultyColor(exercise.difficulty) }}
                  >
                    {getDifficultyLabel(exercise.difficulty)}
                  </span>
                </div>
              </div>

              <div className="card-footer">
                <button className="start-btn">
                  Comenzar Ejercicio <Zap size={16} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">
            <p>No se encontraron ejercicios que coincidan con tus criterios.</p>
          </div>
        )}
      </div>

      {/* Sección de Consejos */}
      <div className="tips-section">
        <h3>💡 Consejos para Aprovechar al Máximo</h3>
        <div className="tips-grid">
          <div className="tip-card">
            <div className="tip-icon">📚</div>
            <h4>Lee la Explicación</h4>
            <p>Comprende a fondo cómo funciona la vulnerabilidad antes de intentar explotarla.</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">🔬</div>
            <h4>Experimenta</h4>
            <p>Prueba diferentes payloads en el simulador para entender qué funciona y por qué.</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">🛡️</div>
            <h4>Aprende la Defensa</h4>
            <p>Estudia el código seguro y las contramedidas para saber cómo proteger tus aplicaciones.</p>
          </div>
          <div className="tip-card">
            <div className="tip-icon">📈</div>
            <h4>Progresa Gradualmente</h4>
            <p>Comienza con ejercicios de principiante y avanza a niveles más difíciles.</p>
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

function getDifficultyLabel(difficulty) {
  const labels = {
    'BEGINNER': 'Principiante',
    'INTERMEDIATE': 'Intermedio',
    'ADVANCED': 'Avanzado'
  };
  return labels[difficulty] || difficulty;
}

function getCVSSLevel(score) {
  if (score >= 9) return 'critical';
  if (score >= 7) return 'high';
  if (score >= 4) return 'medium';
  return 'low';
}

export default EnhancedChallengeGallery;
