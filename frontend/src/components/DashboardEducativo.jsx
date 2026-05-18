import React, { useState, useEffect } from 'react';
import { Lock, Unlock, Shield, TrendingUp, Award, BookOpen, Code, Terminal, Zap, Star, CheckCircle, AlertCircle } from 'lucide-react';
import './DashboardEducativo.css';

const DashboardEducativo = ({ challenges = [], userProgress = {}, onSelectChallenge = () => {} }) => {
  const [stats, setStats] = useState({
    completedChallenges: 0,
    totalScore: 0,
    completionPercentage: 0,
    currentBelt: 'Cinturón Blanco'
  });

  useEffect(() => {
    if (userProgress) {
      setStats({
        completedChallenges: userProgress.completed_challenges || 0,
        totalScore: userProgress.total_score || 0,
        completionPercentage: userProgress.completion_percentage || 0,
        currentBelt: getBeltRank(userProgress.completion_percentage || 0)
      });
    }
  }, [userProgress]);

  const getBeltRank = (percentage) => {
    if (percentage === 0) return 'Cinturón Blanco';
    if (percentage < 20) return 'Cinturón Amarillo';
    if (percentage < 40) return 'Cinturón Naranja';
    if (percentage < 60) return 'Cinturón Verde';
    if (percentage < 80) return 'Cinturón Azul';
    if (percentage < 100) return 'Cinturón Marrón';
    return 'Cinturón Negro';
  };

  const getChallengesByDifficulty = (difficulty) => {
    return challenges.filter(c => c.difficulty === difficulty);
  };

  return (
    <div className="dashboard-educativo">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="hero-blob"></div>
          <div className="hero-blob"></div>
        </div>
        <div className="hero-content">
          <div className="hero-icon">🛡️</div>
          <h1>Secure Coding Dojo</h1>
          <p className="hero-subtitle">Aprende seguridad en la programación dominando vulnerabilidades reales</p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-grid">
          <div className="stat-card stat-card-primary">
            <div className="stat-icon">🥋</div>
            <div className="stat-content">
              <p className="stat-label">Rango Actual</p>
              <p className="stat-value">{stats.currentBelt}</p>
            </div>
          </div>

          <div className="stat-card stat-card-success">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <p className="stat-label">Desafíos Completados</p>
              <p className="stat-value">{stats.completedChallenges}/{challenges.length}</p>
            </div>
          </div>

          <div className="stat-card stat-card-info">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <p className="stat-label">Puntuación Total</p>
              <p className="stat-value">{stats.totalScore}</p>
            </div>
          </div>

          <div className="stat-card stat-card-warning">
            <div className="stat-icon">🎯</div>
            <div className="stat-content">
              <p className="stat-label">Progreso General</p>
              <p className="stat-value">{stats.completionPercentage.toFixed(1)}%</p>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="progress-container">
          <div className="progress-label">
            <span>Progreso del Viaje de Aprendizaje</span>
            <span className="progress-percentage">{stats.completionPercentage.toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${stats.completionPercentage}%` }}
            >
              {stats.completionPercentage > 10 && <span className="progress-text">Avanzando...</span>}
            </div>
          </div>
          <div className="progress-milestones">
            <div className="milestone" style={{ left: '0%' }}>0%</div>
            <div className="milestone" style={{ left: '25%' }}>25%</div>
            <div className="milestone" style={{ left: '50%' }}>50%</div>
            <div className="milestone" style={{ left: '75%' }}>75%</div>
            <div className="milestone" style={{ left: '100%' }}>100%</div>
          </div>
        </div>
      </section>

      {/* Challenges by Difficulty */}
      <section className="challenges-section">
        {/* Beginner */}
        {getChallengesByDifficulty('BEGINNER').length > 0 && (
          <div className="difficulty-group">
            <div className="difficulty-header">
              <div className="difficulty-icon green">🟢</div>
              <div className="difficulty-info">
                <h2>Principiante</h2>
                <p>Fundamentos de seguridad y vulnerabilidades comunes</p>
              </div>
              <span className="difficulty-count">
                {getChallengesByDifficulty('BEGINNER').length} Desafíos
              </span>
            </div>
            <div className="challenges-grid">
              {getChallengesByDifficulty('BEGINNER').map(challenge => (
                <ChallengeCard 
                  key={challenge.id} 
                  challenge={challenge} 
                  onSelect={onSelectChallenge}
                />
              ))}
            </div>
          </div>
        )}

        {/* Intermediate */}
        {getChallengesByDifficulty('INTERMEDIATE').length > 0 && (
          <div className="difficulty-group">
            <div className="difficulty-header">
              <div className="difficulty-icon yellow">🟡</div>
              <div className="difficulty-info">
                <h2>Intermedio</h2>
                <p>Vulnerabilidades avanzadas y ataques complejos</p>
              </div>
              <span className="difficulty-count">
                {getChallengesByDifficulty('INTERMEDIATE').length} Desafíos
              </span>
            </div>
            <div className="challenges-grid">
              {getChallengesByDifficulty('INTERMEDIATE').map(challenge => (
                <ChallengeCard 
                  key={challenge.id} 
                  challenge={challenge} 
                  onSelect={onSelectChallenge}
                />
              ))}
            </div>
          </div>
        )}

        {/* Advanced */}
        {getChallengesByDifficulty('ADVANCED').length > 0 && (
          <div className="difficulty-group">
            <div className="difficulty-header">
              <div className="difficulty-icon red">🔴</div>
              <div className="difficulty-info">
                <h2>Avanzado</h2>
                <p>Casos extremos, cadenas de ataques y seguridad en profundidad</p>
              </div>
              <span className="difficulty-count">
                {getChallengesByDifficulty('ADVANCED').length} Desafíos
              </span>
            </div>
            <div className="challenges-grid">
              {getChallengesByDifficulty('ADVANCED').map(challenge => (
                <ChallengeCard 
                  key={challenge.id} 
                  challenge={challenge} 
                  onSelect={onSelectChallenge}
                />
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Learning Path Info */}
      <section className="learning-path-section">
        <div className="learning-path-card">
          <div className="learning-icon">📚</div>
          <div className="learning-content">
            <h3>🥋 Tu Camino en Secure Coding Dojo</h3>
            <p>
              Comienza con desafíos de principiante para aprender los fundamentos de las vulnerabilidades web más comunes. 
              Progresa a través de niveles intermedios dominando técnicas de ataque y defensa más sofisticadas. 
              Finalmente, alcanza el nivel avanzado donde enfrentarás escenarios complejos del mundo real. 
              ¡Cada desafío completado te acerca a convertirte en un experto en ciberseguridad!
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

function ChallengeCard({ challenge, onSelect }) {
  const getGradientClass = (vulnerability) => {
    const colors = {
      'SQL_INJECTION': 'gradient-red',
      'XSS': 'gradient-orange',
      'CSRF': 'gradient-purple',
      'BROKEN_AUTH': 'gradient-yellow',
      'IDOR': 'gradient-blue',
      'INSECURE_DESERIALIZE': 'gradient-pink'
    };
    return colors[vulnerability] || 'gradient-default';
  };

  return (
    <div 
      className={`challenge-card ${getGradientClass(challenge.vulnerability_type)}`}
      onClick={() => onSelect(challenge)}
    >
      <div className="card-header">
        <span className="card-icon">{challenge.icon}</span>
        <div className="card-badges">
          <span className="badge badge-difficulty">
            {challenge.difficulty === 'BEGINNER' ? '🟢' : 
             challenge.difficulty === 'INTERMEDIATE' ? '🟡' : 
             '🔴'}
          </span>
        </div>
      </div>

      <div className="card-body">
        <h3>{challenge.short_title}</h3>
        <p className="card-description">{challenge.description}</p>

        <div className="card-meta">
          <div className="meta-item">
            <span className="meta-label">CVSS</span>
            <span className="meta-value">{challenge.cvss_score}/10</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">OWASP</span>
            <span className="meta-value">{challenge.owasp_top_10}</span>
          </div>
        </div>

        <div className="card-tags">
          <span className="tag">{challenge.vulnerability_type}</span>
          <span className="tag">{challenge.attack_type}</span>
        </div>
      </div>

      <div className="card-footer">
        <button className="btn-challenge">
          🎯 Iniciar Desafío
        </button>
      </div>
    </div>
  );
}

export default DashboardEducativo;
