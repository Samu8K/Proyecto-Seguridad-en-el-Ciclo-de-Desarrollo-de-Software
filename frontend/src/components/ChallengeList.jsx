import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const ChallengeList = ({ onSelectChallenge, userId }) => {
  const [challenges, setChallenges] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterDifficulty, setFilterDifficulty] = useState('ALL');
  const [filterType, setFilterType] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/challenges/');
      setChallenges(res.data);
      setFiltered(res.data);
    } catch (err) {
      toast.error('Error cargando desafíos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let result = challenges;

    if (filterDifficulty !== 'ALL') {
      result = result.filter(c => c.difficulty === filterDifficulty);
    }

    if (filterType !== 'ALL') {
      result = result.filter(c => c.vulnerability_type === filterType);
    }

    if (searchTerm) {
      result = result.filter(c =>
        c.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFiltered(result);
  }, [challenges, filterDifficulty, filterType, searchTerm]);

  const getDifficultyIcon = (difficulty) => {
    const icons = {
      BEGINNER: '🌱',
      INTERMEDIATE: '🌿',
      ADVANCED: '🚀'
    };
    return icons[difficulty] || '❓';
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      BEGINNER: 'from-green-600 to-green-700',
      INTERMEDIATE: 'from-yellow-600 to-yellow-700',
      ADVANCED: 'from-red-600 to-red-700'
    };
    return colors[difficulty] || 'from-slate-600 to-slate-700';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-white">Cargando desafíos...</p>
        </div>
      </div>
    );
  }

  const vulnerabilityTypes = [...new Set(challenges.map(c => c.vulnerability_type))];

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
        <h2 className="text-2xl font-bold text-white">🔍 Filtrar Desafíos</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Buscar
            </label>
            <input
              type="text"
              placeholder="Ingresa palabras clave..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Difficulty Filter */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Dificultad
            </label>
            <select
              value={filterDifficulty}
              onChange={(e) => setFilterDifficulty(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="ALL">Todos</option>
              <option value="BEGINNER">Principiante</option>
              <option value="INTERMEDIATE">Intermedio</option>
              <option value="ADVANCED">Avanzado</option>
            </select>
          </div>

          {/* Type Filter */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Tipo de Vulnerabilidad
            </label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
            >
              <option value="ALL">Todos</option>
              {vulnerabilityTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Results */}
      <div>
        <p className="text-slate-300 mb-4">
          Se encontraron <span className="font-bold text-white">{filtered.length}</span> desafíos
        </p>

        {filtered.length === 0 ? (
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-12 text-center">
            <p className="text-slate-400 text-lg">
              No se encontraron desafíos que coincidan con los filtros
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map(challenge => (
              <div
                key={challenge.id}
                onClick={() => onSelectChallenge(challenge)}
                className={`bg-gradient-to-br ${getDifficultyColor(challenge.difficulty)} rounded-xl p-6 cursor-pointer hover:shadow-2xl hover:-translate-y-2 transition-all duration-200 group border border-opacity-50`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <p className="text-sm text-white/70 mb-2 flex items-center gap-2">
                      <span>{getDifficultyIcon(challenge.difficulty)}</span>
                      {challenge.difficulty === 'BEGINNER' ? 'Principiante' :
                        challenge.difficulty === 'INTERMEDIATE' ? 'Intermedio' : 'Avanzado'}
                    </p>
                    <h3 className="text-lg font-bold text-white group-hover:text-yellow-200 transition">
                      {challenge.title}
                    </h3>
                  </div>
                  <div className="text-3xl font-bold text-white/80">
                    {challenge.cvss_score}
                  </div>
                </div>

                <p className="text-white/80 text-sm mb-4 line-clamp-2">
                  {challenge.description}
                </p>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center justify-between text-xs text-white/70">
                    <span>Vulnerabilidad:</span>
                    <span className="font-semibold">{challenge.vulnerability_type}</span>
                  </div>
                  <div className="flex items-center justify-between text-xs text-white/70">
                    <span>Clasificación:</span>
                    <span className="font-semibold">{challenge.owasp_top_10}</span>
                  </div>
                </div>

                <button className="w-full mt-4 py-3 bg-white/20 hover:bg-white/30 text-white font-bold rounded-lg transition backdrop-blur">
                  Empezar Desafío →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChallengeList;
