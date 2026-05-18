import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { Zap, Target, Lock, AlertTriangle, Award, TrendingUp, Clock, Shield } from 'lucide-react';
import './EnhancedDashboard.css';

const EnhancedDashboard = ({ onNavigateToExercises }) => {
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStatistics = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/exercises/statistics');
        const data = await response.json();
        setStatistics(data);
        setLoading(false);
      } catch (error) {
        console.error('Error loading statistics:', error);
        setLoading(false);
      }
    };
    loadStatistics();
  }, []);

  if (loading) {
    return <div className="dashboard-loading">Cargando dashboard...</div>;
  }

  const difficultyData = statistics ? [
    { name: 'Principiante', value: statistics.by_difficulty.BEGINNER, fill: '#10b981' },
    { name: 'Intermedio', value: statistics.by_difficulty.INTERMEDIATE, fill: '#f59e0b' },
    { name: 'Avanzado', value: statistics.by_difficulty.ADVANCED, fill: '#ef4444' }
  ] : [];

  const vulnerabilityData = statistics ? Object.entries(statistics.by_vulnerability).map(([key, value]) => ({
    name: key.replace(/_/g, ' '),
    value: value,
    fill: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b'][Math.floor(Math.random() * 6)]
  })) : [];

  return (
    <div className="enhanced-dashboard">
      {/* Header Principal */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>🛡️ Secure Coding Dojo</h1>
          <p>Aprende seguridad en la codificación mediante ejercicios prácticos y educación interactiva</p>
        </div>
        <button className="cta-button" onClick={onNavigateToExercises}>
          Comenzar Ejercicios <Zap size={20} />
        </button>
      </div>

      {/* Quick Stats */}
      <div className="quick-stats">
        <div className="stat-card stat-primary">
          <div className="stat-icon">📊</div>
          <div className="stat-info">
            <span className="stat-label">Total Ejercicios</span>
            <span className="stat-value">{statistics?.total_exercises || 0}</span>
          </div>
        </div>
        <div className="stat-card stat-success">
          <div className="stat-icon">🟢</div>
          <div className="stat-info">
            <span className="stat-label">Principiante</span>
            <span className="stat-value">{statistics?.by_difficulty.BEGINNER || 0}</span>
          </div>
        </div>
        <div className="stat-card stat-warning">
          <div className="stat-icon">🟡</div>
          <div className="stat-info">
            <span className="stat-label">Intermedio</span>
            <span className="stat-value">{statistics?.by_difficulty.INTERMEDIATE || 0}</span>
          </div>
        </div>
        <div className="stat-card stat-danger">
          <div className="stat-icon">🔴</div>
          <div className="stat-info">
            <span className="stat-label">Avanzado</span>
            <span className="stat-value">{statistics?.by_difficulty.ADVANCED || 0}</span>
          </div>
        </div>
        <div className="stat-card stat-critical">
          <div className="stat-icon">⚠️</div>
          <div className="stat-info">
            <span className="stat-label">CVSS Promedio</span>
            <span className="stat-value">{(statistics?.average_cvss || 0).toFixed(1)}</span>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        {/* Dificultad Distribution */}
        <div className="chart-card">
          <h3>Distribución por Nivel de Dificultad</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={difficultyData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {difficultyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Vulnerabilities */}
        <div className="chart-card">
          <h3>Vulnerabilidades Cubiertas</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vulnerabilityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h2>¿Por qué Secure Coding Dojo?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎓</div>
            <h3>Educación Completa</h3>
            <p>Explicaciones detalladas de cada vulnerabilidad, cómo funciona el ataque y cómo defenderse.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔬</div>
            <h3>Simulador de Ataques</h3>
            <p>Prueba tus ataques en un entorno seguro. Aprende cómo explotar vulnerabilidades sin riesgo.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3>Código Real</h3>
            <p>Compara código vulnerable con código seguro. Aprende las mejores prácticas de desarrollo.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>Progresión Gradual</h3>
            <p>Comienza desde cero hasta convertirte en experto. Ejercicios ordenados por dificultad.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🏆</div>
            <h3>Sistema de Logros</h3>
            <p>Desbloquea badges y certificados mientras avanzas en tu aprendizaje de seguridad.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🛡️</div>
            <h3>Prácticas Seguras</h3>
            <p>Aprende cómo prevenir vulnerabilidades en tus aplicaciones desde el diseño inicial.</p>
          </div>
        </div>
      </div>

      {/* Course Path */}
      <div className="course-path-section">
        <h2>Ruta de Aprendizaje</h2>
        <div className="course-path">
          <div className="course-level">
            <div className="level-number">1</div>
            <h4>Fundamentos</h4>
            <p>SQL Injection</p>
            <p>XSS</p>
            <span className="difficulty-badge beginner">Principiante</span>
          </div>
          <div className="path-arrow">→</div>
          <div className="course-level">
            <div className="level-number">2</div>
            <h4>Intermedio</h4>
            <p>Autenticación</p>
            <p>Control de Acceso</p>
            <span className="difficulty-badge intermediate">Intermedio</span>
          </div>
          <div className="path-arrow">→</div>
          <div className="course-level">
            <div className="level-number">3</div>
            <h4>Avanzado</h4>
            <p>Deserialización</p>
            <p>Criptografía</p>
            <span className="difficulty-badge advanced">Avanzado</span>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="cta-section">
        <h2>¿Listo para aprender?</h2>
        <p>Comienza con los ejercicios básicos y progresa hacia niveles más avanzados. Cada ejercicio es una oportunidad para mejorar tus habilidades de seguridad.</p>
        <button className="cta-large-button" onClick={onNavigateToExercises}>
          Ir a Ejercicios <ChevronRight size={24} />
        </button>
      </div>

      {/* Footer */}
      <div className="dashboard-footer">
        <p>Secure Coding Dojo © 2024 | Plataforma Educativa de Seguridad en Codificación</p>
        <p style={{ fontSize: '0.875rem', opacity: 0.7 }}>
          Diseñado para enseñar seguridad ofensiva y defensiva de forma práctica e interactiva.
        </p>
      </div>
    </div>
  );
};

export default EnhancedDashboard;
