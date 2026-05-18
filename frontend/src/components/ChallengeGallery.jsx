import React, { useState, useEffect } from 'react';
import { Zap, Shield, Trophy, Filter } from 'lucide-react';
import './ChallengeGallery.css';

export default function ChallengeGallery({ challenges, onSelectChallenge }) {
  const [filteredChallenges, setFilteredChallenges] = useState(challenges);
  const [selectedDifficulty, setSelectedDifficulty] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    let filtered = challenges;

    if (selectedDifficulty) {
      filtered = filtered.filter(c => c.difficulty === selectedDifficulty);
    }

    if (searchTerm) {
      filtered = filtered.filter(c =>
        c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.short_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredChallenges(filtered);
  }, [challenges, selectedDifficulty, searchTerm]);

  const getDifficultyColor = (difficulty) => {
    const colors = {
      'BEGINNER': { bg: '#10b981', text: '#d1fae5' },
      'INTERMEDIATE': { bg: '#f59e0b', text: '#fffbeb' },
      'ADVANCED': { bg: '#ef4444', text: '#fee2e2' }
    };
    return colors[difficulty] || colors.BEGINNER;
  };

  const getDifficultyLabel = (difficulty) => {
    const labels = {
      'BEGINNER': 'Principiante',
      'INTERMEDIATE': 'Intermedio',
      'ADVANCED': 'Avanzado'
    };
    return labels[difficulty] || difficulty;
  };

  return (
    <div className="challenge-gallery">
      {/* Filters Header */}
      <div className="gallery-header">
        <h1>🎯 Desafíos de Seguridad</h1>
        <p>Aprende sobre vulnerabilidades reales con ejercicios interactivos</p>
      </div>

      {/* Filters Bar */}
      <div className="filters-bar">
        <div className="search-box">
          <input
            type="text"
            placeholder="🔍 Buscar desafío..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="difficulty-filters">
          <button
            className={`filter-btn ${!selectedDifficulty ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty(null)}
          >
            <Filter size={16} />
            Todos
          </button>
          <button
            className={`filter-btn ${selectedDifficulty === 'BEGINNER' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('BEGINNER')}
            style={{
              borderColor: getDifficultyColor('BEGINNER').bg
            }}
          >
            <Trophy size={16} />
            Principiante
          </button>
          <button
            className={`filter-btn ${selectedDifficulty === 'INTERMEDIATE' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('INTERMEDIATE')}
            style={{
              borderColor: getDifficultyColor('INTERMEDIATE').bg
            }}
          >
            <Zap size={16} />
            Intermedio
          </button>
          <button
            className={`filter-btn ${selectedDifficulty === 'ADVANCED' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('ADVANCED')}
            style={{
              borderColor: getDifficultyColor('ADVANCED').bg
            }}
          >
            <Shield size={16} />
            Avanzado
          </button>
        </div>
      </div>

      {/* Challenges Grid */}
      <div className="challenges-grid">
        {filteredChallenges.map((challenge) => (
          <div
            key={challenge.id}
            className="challenge-card"
            onClick={() => onSelectChallenge(challenge)}
          >
            {/* Card Header */}
            <div className="card-header">
              <span className="challenge-icon">{challenge.icon}</span>
              <span
                className="difficulty-badge"
                style={{
                  backgroundColor: getDifficultyColor(challenge.difficulty).bg,
                  color: getDifficultyColor(challenge.difficulty).text
                }}
              >
                {getDifficultyLabel(challenge.difficulty)}
              </span>
            </div>

            {/* Card Body */}
            <div className="card-body">
              <h3>{challenge.title}</h3>
              <p className="card-description">{challenge.description}</p>

              {/* Stats */}
              <div className="card-stats">
                <div className="stat-item">
                  <Zap size={14} />
                  <span>CVSS {challenge.cvss_score}/10</span>
                </div>
                <div className="stat-item">
                  <Shield size={14} />
                  <span>{challenge.owasp_top_10}</span>
                </div>
              </div>

              {/* Tags */}
              <div className="card-tags">
                <span className="tag">{challenge.vulnerability_type}</span>
                <span className="tag">{challenge.attack_type}</span>
              </div>
            </div>

            {/* Card Footer */}
            <div className="card-footer">
              <button className="btn-start">
                Iniciar Desafío →
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredChallenges.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h2>No se encontraron desafíos</h2>
          <p>Intenta con diferentes filtros o términos de búsqueda</p>
        </div>
      )}

      {/* Stats Footer */}
      <div className="stats-footer">
        <div className="stat-box">
          <span className="stat-number">{challenges.length}</span>
          <span className="stat-label">Desafíos Totales</span>
        </div>
        <div className="stat-box">
          <span className="stat-number">{challenges.filter(c => c.difficulty === 'BEGINNER').length}</span>
          <span className="stat-label">Para Principiantes</span>
        </div>
        <div className="stat-box">
          <span className="stat-number">{challenges.filter(c => c.difficulty === 'INTERMEDIATE').length}</span>
          <span className="stat-label">Nivel Intermedio</span>
        </div>
        <div className="stat-box">
          <span className="stat-number">{challenges.filter(c => c.difficulty === 'ADVANCED').length}</span>
          <span className="stat-label">Nivel Avanzado</span>
        </div>
      </div>
    </div>
  );
}
