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
