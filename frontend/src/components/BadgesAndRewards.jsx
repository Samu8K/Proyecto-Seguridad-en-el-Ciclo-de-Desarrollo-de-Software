import React, { useState, useEffect } from 'react';
import { Star, Award, Zap, Shield, Lock, Trophy, Flame } from 'lucide-react';
import './BadgesAndRewards.css';

const BadgesAndRewards = ({ progress = {}, challenges = [] }) => {
  const [badges, setBadges] = useState([]);
  const [showBadgesModal, setShowBadgesModal] = useState(false);

  useEffect(() => {
    calculateBadges();
  }, [progress, challenges]);

  const calculateBadges = () => {
    const earnedBadges = [];
    const completedChallenges = progress.completed_challenges || 0;
    const totalScore = progress.total_score || 0;
    const completionPercentage = progress.completion_percentage || 0;

    // Badge: Primer Paso
    if (completedChallenges >= 1) {
      earnedBadges.push({
        id: 'first-step',
        name: 'Primer Paso',
        description: 'Completar el primer desafío',
        icon: '👣',
        color: '#3b82f6',
        earned: true
      });
    }

    // Badge: Aprendiz de Seguridad
    if (completedChallenges >= 2) {
      earnedBadges.push({
        id: 'learner',
        name: 'Aprendiz',
        description: 'Completar 2 desafíos',
        icon: '📚',
        color: '#8b5cf6',
        earned: true
      });
    }

    // Badge: Experto Iniciado
    if (completedChallenges >= 3) {
      earnedBadges.push({
        id: 'expert-beginner',
        name: 'Experto Iniciado',
        description: 'Completar 3 desafíos',
        icon: '🌟',
        color: '#ec4899',
        earned: true
      });
    }

    // Badge: Maestro del Dojo
    if (completedChallenges >= 4) {
      earnedBadges.push({
        id: 'dojo-master',
        name: 'Maestro del Dojo',
        description: 'Completar 4 desafíos',
        icon: '🥋',
        color: '#f59e0b',
        earned: true
      });
    }

    // Badge: Cinturón Negro
    if (completionPercentage === 100) {
      earnedBadges.push({
        id: 'black-belt',
        name: 'Cinturón Negro',
        description: 'Completar TODOS los desafíos',
        icon: '🎖️',
        color: '#000000',
        earned: true
      });
    }

    // Badge: Puntuación Perfecta
    if (totalScore >= 500) {
      earnedBadges.push({
        id: 'perfect-score',
        name: 'Puntuación Elite',
        description: 'Alcanzar 500+ puntos',
        icon: '💯',
        color: '#10b981',
        earned: true
      });
    }

    // Badge: Velocista
    if (completedChallenges >= 2) {
      earnedBadges.push({
        id: 'speedster',
        name: 'Rayo',
        description: 'Completar desafíos rápidamente',
        icon: '⚡',
        color: '#fbbf24',
        earned: true
      });
    }

    // Badge: Persistente
    if (totalScore > 0) {
      earnedBadges.push({
        id: 'persistent',
        name: 'Persistente',
        description: 'No rendirse en los desafíos',
        icon: '💪',
        color: '#ef4444',
        earned: true
      });
    }

    // Locked badges
    if (completedChallenges < 1) {
      earnedBadges.push({
        id: 'first-step-locked',
        name: 'Primer Paso',
        description: 'Completar el primer desafío',
        icon: '👣',
        color: '#64748b',
        earned: false
      });
    }

    setBadges(earnedBadges);
  };

  const earnedBadgesCount = badges.filter(b => b.earned).length;
  const totalBadgesCount = 8;

  return (
    <div className="badges-and-rewards">
      <div className="badges-header">
        <h3>🏆 Tu Sala de Trofeos</h3>
        <span className="badges-counter">
          {earnedBadgesCount}/{totalBadgesCount}
        </span>
      </div>

      <div className="badges-showcase">
        {badges.map(badge => (
          <div 
            key={badge.id}
            className={`badge-item ${badge.earned ? 'earned' : 'locked'}`}
            onClick={() => setShowBadgesModal(true)}
            title={badge.description}
          >
            <div className="badge-icon">{badge.icon}</div>
            <div className="badge-info">
              <p className="badge-name">{badge.name}</p>
              <p className="badge-desc">{badge.description}</p>
            </div>
            {!badge.earned && (
              <div className="badge-lock">🔒</div>
            )}
          </div>
        ))}
      </div>

      {showBadgesModal && (
        <div className="badges-modal" onClick={() => setShowBadgesModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button 
              className="modal-close"
              onClick={() => setShowBadgesModal(false)}
            >
              ✕
            </button>
            
            <h2>Tu Colección de Badges</h2>
            
            <div className="modal-badges-grid">
              {badges.filter(b => b.earned).map(badge => (
                <div key={badge.id} className="modal-badge earned">
                  <div className="modal-badge-icon" style={{ color: badge.color }}>
                    {badge.icon}
                  </div>
                  <h4>{badge.name}</h4>
                  <p>{badge.description}</p>
                </div>
              ))}
            </div>

            {badges.filter(b => !b.earned).length > 0 && (
              <>
                <h3>Próximos Badges</h3>
                <div className="modal-badges-grid">
                  {badges.filter(b => !b.earned).map(badge => (
                    <div key={badge.id} className="modal-badge locked">
                      <div className="modal-badge-icon">
                        {badge.icon}
                      </div>
                      <h4>{badge.name}</h4>
                      <p>{badge.description}</p>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default BadgesAndRewards;
