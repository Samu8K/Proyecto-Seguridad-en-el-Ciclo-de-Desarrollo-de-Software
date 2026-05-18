import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import toast from 'react-hot-toast';
import EnhancedDashboard from './components/EnhancedDashboard';
import EnhancedChallengeGallery from './components/EnhancedChallengeGallery';
import AdvancedExerciseViewer from './components/AdvancedExerciseViewer';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedExerciseId, setSelectedExerciseId] = useState(null);
  
  const [userId, setUserId] = useState(() => {
    const stored = localStorage.getItem('secure_dojo_user_id');
    if (stored) return stored;
    const newId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('secure_dojo_user_id', newId);
    return newId;
  });

  const handleNavigateToGallery = () => {
    setCurrentView('gallery');
  };

  const handleSelectChallenge = (exerciseId) => {
    setSelectedExerciseId(exerciseId);
    setCurrentView('exercise');
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
    setSelectedExerciseId(null);
  };

  const handleBackToGallery = () => {
    setCurrentView('gallery');
    setSelectedExerciseId(null);
  };

  return (
    <div className="app">
      <Toaster position="top-right" />
      
      {currentView === 'dashboard' && (
        <EnhancedDashboard onNavigateToExercises={handleNavigateToGallery} />
      )}
      
      {currentView === 'gallery' && (
        <EnhancedChallengeGallery onSelectChallenge={handleSelectChallenge} />
      )}
      
      {currentView === 'exercise' && selectedExerciseId && (
        <AdvancedExerciseViewer 
          exerciseId={selectedExerciseId} 
          onBack={handleBackToGallery}
        />
      )}
    </div>
  );
}

export default App;
        const data = await response.json();
        setUserProgress(data);
      } catch (error) {
        console.error('Error loading progress:', error);
      }
    };

    loadProgress();
  }, [userId]);

  const handleSelectChallenge = async (challenge) => {
    try {
      // Cargar detalles completos del desafío
      const response = await fetch(`http://localhost:8000/api/challenges/${challenge.id}`);
      const fullChallenge = await response.json();
      
      setSelectedChallenge(fullChallenge);
      
      // Registrar que el usuario inició el desafío
      await fetch('http://localhost:8000/api/challenges/progress/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ challenge_id: challenge.id, user_id: userId })
      });
      
      setCurrentView('exercise');
    } catch (error) {
      console.error('Error loading challenge details:', error);
      toast.error('Error cargando detalles del desafío');
    }
  };

  const handleCompleteChallenge = async (data) => {
    try {
      const response = await fetch('http://localhost:8000/api/challenges/progress/submit-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          challenge_id: selectedChallenge.id,
          user_id: userId,
          answer: 'completed',
          time_spent: data.timeSpent
        })
      });
      
      const result = await response.json();
      
      toast.success('¡Desafío completado! 🎉');
      setCurrentView('dashboard');
      setSelectedChallenge(null);
      
      // Reload progress
      const progressResponse = await fetch(`http://localhost:8000/api/challenges/progress/${userId}`);
      const progressData = await progressResponse.json();
      setUserProgress(progressData);
    } catch (error) {
      console.error('Error completing challenge:', error);
      toast.error('Error completando desafío');
    }
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
    setSelectedChallenge(null);
  };

  return (
    <div className="app-container">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1e293b',
            color: '#e2e8f0',
            border: '1px solid #334155',
            borderRadius: '8px',
            backdropFilter: 'blur(10px)',
          },
        }}
      />
      
      {/* Header Navigation */}
      {currentView !== 'exercise' && (
        <header className="app-header">
          <div className="header-content">
            <div className="logo-section">
              <span className="logo-icon">🛡️</span>
              <div className="logo-text">
                <h1>Secure Coding Dojo</h1>
                <p>Plataforma Educativa Interactiva</p>
              </div>
            </div>
            
            <div className="header-stats">
              <div className="stat">
                <span className="stat-label">Desafíos Completados</span>
                <span className="stat-value">{userProgress.completed_challenges || 0}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Puntuación Total</span>
                <span className="stat-value">{userProgress.total_score || 0}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Progreso</span>
                <span className="stat-value">{userProgress.completion_percentage || 0}%</span>
              </div>
            </div>
          </div>
        </header>
      )}

      {/* Main Content */}
      <main className="app-main">
        {loading && (
          <div className="loading-container">
            <div className="loading-spinner">⚙️</div>
            <p>Cargando desafíos educativos...</p>
          </div>
        )}

        {!loading && currentView === 'dashboard' && (
          <DashboardEducativo 
            challenges={challenges}
            onSelectChallenge={handleSelectChallenge}
            userProgress={userProgress}
          />
        )}

        {!loading && currentView === 'gallery' && (
          <ChallengeGallery 
            challenges={challenges}
            onSelectChallenge={handleSelectChallenge}
          />
        )}

        {currentView === 'exercise' && selectedChallenge && (
          <InteractiveExercise 
            challenge={selectedChallenge}
            onComplete={handleCompleteChallenge}
            onBack={handleBackToDashboard}
          />
        )}
      </main>

      {/* Footer */}
      {currentView !== 'exercise' && (
        <footer className="app-footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Sobre Secure Coding Dojo</h3>
              <p>Plataforma educativa de seguridad en la programación con ejercicios prácticos basados en vulnerabilidades reales.</p>
            </div>
            <div className="footer-section">
              <h3>Contenido</h3>
              <ul>
                <li>6+ Desafíos de Seguridad</li>
                <li>Explicaciones Detalladas</li>
                <li>Código Vulnerable vs Seguro</li>
                <li>Pistas Progresivas</li>
              </ul>
            </div>
            <div className="footer-section">
              <h3>Recursos</h3>
              <ul>
                <li>OWASP Top 10</li>
                <li>CWE/CVSS Scores</li>
                <li>Mejores Prácticas</li>
                <li>Referencias</li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Secure Coding Dojo - Plataforma Educativa de Ciberseguridad</p>
          </div>
        </footer>
      )}
    </div>
  );
}

export default App;
