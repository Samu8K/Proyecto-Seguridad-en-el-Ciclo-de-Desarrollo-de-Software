import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import CodeComparison from './CodeComparison';
import HintSystem from './HintSystem';

const ChallengeDetail = ({ challenge, userId }) => {
  const [progress, setProgress] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [activeTab, setActiveTab] = useState('vulnerability');
  const [hints, setHints] = useState([]);
  const [loadingHints, setLoadingHints] = useState(false);

  useEffect(() => {
    initializeChallenge();
    fetchHints();
  }, [challenge.id, userId]);

  const initializeChallenge = async () => {
    try {
      const res = await axios.post(
        `/api/challenges/user/${userId}/challenge/${challenge.id}/start`
      );
      setProgress(res.data);
    } catch (err) {
      console.error('Error initializing challenge:', err);
    }
  };

  const fetchHints = async () => {
    try {
      setLoadingHints(true);
      const res = await axios.get(`/api/challenges/${challenge.id}/hints`);
      setHints(res.data);
    } catch (err) {
      console.error('Error fetching hints:', err);
    } finally {
      setLoadingHints(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userAnswer.trim()) {
      toast.error('Por favor ingresa una respuesta');
      return;
    }

    try {
      const res = await axios.post(
        `/api/challenges/user/${userId}/challenge/${challenge.id}/submit`,
        { answer: userAnswer }
      );

      setProgress(res.data.progress);
      setSubmitted(true);

      if (res.data.is_correct) {
        toast.success(res.data.message);
      } else {
        toast.error(res.data.message);
      }
    } catch (err) {
      toast.error('Error enviando respuesta');
    }
  };

  const getCVSSColor = (score) => {
    if (score >= 9.0) return 'text-red-500';
    if (score >= 7.0) return 'text-orange-500';
    if (score >= 4.0) return 'text-yellow-500';
    return 'text-green-500';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-700 rounded-2xl p-8 shadow-xl">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">{challenge.title}</h1>
            <p className="text-slate-300 text-lg">{challenge.description}</p>
          </div>
          <div className="text-right">
            <div className={`text-4xl font-bold ${getCVSSColor(challenge.cvss_score)}`}>
              {challenge.cvss_score}
            </div>
            <div className="text-xs text-slate-400">CVSS Score</div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-700">
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-wide">Tipo de Vulnerabilidad</div>
            <div className="text-sm font-semibold text-blue-400 mt-1">{challenge.vulnerability_type}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-wide">Tipo de Ataque</div>
            <div className="text-sm font-semibold text-purple-400 mt-1">{challenge.attack_type}</div>
          </div>
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-wide">Clasificación</div>
            <div className="text-sm font-semibold text-green-400 mt-1">
              {challenge.owasp_top_10} | {challenge.cwe_id}
            </div>
          </div>
          <div>
            <div className="text-xs text-slate-400 uppercase tracking-wide">Progreso</div>
            <div className="text-sm font-semibold text-yellow-400 mt-1">
              {progress?.attempts || 0} intentos
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-700 overflow-x-auto pb-4">
        {[
          { id: 'vulnerability', label: '🔍 Vulnerabilidad', icon: '🔍' },
          { id: 'attack', label: '⚔️ Tipo de Ataque', icon: '⚔️' },
          { id: 'code', label: '💻 Código', icon: '💻' },
          { id: 'defense', label: '🛡️ Contramedidas', icon: '🛡️' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 font-semibold text-sm whitespace-nowrap transition-colors ${
              activeTab === tab.id
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2">
          {activeTab === 'vulnerability' && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span>🔍</span> Explicación de la Vulnerabilidad
              </h3>
              <div className="prose prose-invert max-w-none">
                <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                  {challenge.vulnerability_explanation}
                </p>
              </div>
            </div>
          )}

          {activeTab === 'attack' && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span>⚔️</span> Explicación del Ataque
              </h3>
              <div className="prose prose-invert max-w-none">
                <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                  {challenge.attack_explanation}
                </p>
              </div>
            </div>
          )}

          {activeTab === 'code' && (
            <CodeComparison challenge={challenge} />
          )}

          {activeTab === 'defense' && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
              <h3 className="text-xl font-bold text-white flex items-center gap-2">
                <span>🛡️</span> Contramedidas y Soluciones
              </h3>
              <div className="prose prose-invert max-w-none">
                <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                  {challenge.countermeasures}
                </p>
              </div>
              {challenge.references && (
                <div className="mt-6 pt-6 border-t border-slate-700">
                  <h4 className="text-sm font-semibold text-slate-400 mb-3">📚 Referencias</h4>
                  <p className="text-slate-300 text-sm">{challenge.references}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Sidebar - Hints and Challenge */}
        <div className="space-y-6">
          <HintSystem 
            challengeId={challenge.id}
            userId={userId}
            hints={hints}
            hintsRequested={progress?.hints_requested || 0}
            loading={loadingHints}
          />

          {/* Challenge Form */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
              <span>✏️</span> Tu Respuesta
            </h3>

            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Escribe tu respuesta aquí..."
                disabled={submitted && progress?.is_completed}
                className="w-full bg-slate-700 border border-slate-600 rounded-lg p-3 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 disabled:opacity-50 h-32"
              />

              <button
                type="submit"
                disabled={submitted && progress?.is_completed}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition duration-200"
              >
                {submitted && progress?.is_completed ? '✓ Completado' : 'Enviar Respuesta'}
              </button>

              {submitted && (
                <div className={`p-4 rounded-lg ${
                  progress?.is_correct
                    ? 'bg-green-500/20 border border-green-500/50'
                    : 'bg-red-500/20 border border-red-500/50'
                }`}>
                  <p className={progress?.is_correct ? 'text-green-300' : 'text-red-300'}>
                    {progress?.is_correct
                      ? '¡Excelente! Respondiste correctamente.'
                      : 'Intenta de nuevo. Revisa las pistas para obtener ayuda.'}
                  </p>
                </div>
              )}
            </form>

            <button
              onClick={() => setShowAnswer(!showAnswer)}
              className="mt-4 text-sm text-slate-400 hover:text-white transition"
            >
              {showAnswer ? '🙈 Ocultar solución' : '👁️ Ver solución'}
            </button>

            {showAnswer && (
              <div className="mt-4 p-4 bg-slate-700 rounded-lg border-l-4 border-yellow-500">
                <p className="text-sm text-yellow-300 mb-2">⚠️ Spoiler - Solución:</p>
                <p className="text-slate-300 text-sm">{challenge.expected_result}</p>
              </div>
            )}
          </div>

          {/* Challenge Info */}
          {progress && (
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">
                📊 Mi Progreso
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-400">Intentos:</span>
                  <span className="text-white font-semibold">{progress.attempts}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Pistas usadas:</span>
                  <span className="text-white font-semibold">{progress.hints_requested}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Estado:</span>
                  <span className={progress.is_completed ? 'text-green-400' : 'text-orange-400'}>
                    {progress.is_completed ? '✓ Completo' : 'En progreso'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChallengeDetail;
