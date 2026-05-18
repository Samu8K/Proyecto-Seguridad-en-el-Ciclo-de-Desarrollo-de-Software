import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const HintSystem = ({ challengeId, userId, hints, hintsRequested, loading }) => {
  const [displayedHints, setDisplayedHints] = useState([]);
  const [requesting, setRequesting] = useState(false);

  const requestHint = async () => {
    try {
      setRequesting(true);
      const res = await axios.post(
        `/api/challenges/user/${userId}/challenge/${challengeId}/request-hint`
      );

      if (res.data.hint) {
        setDisplayedHints([...displayedHints, res.data.hint]);
        toast.success(res.data.message);
      } else {
        toast.info(res.data.message);
      }
    } catch (err) {
      toast.error('Error solicitando pista');
    } finally {
      setRequesting(false);
    }
  };

  const totalHints = hints.length;
  const hasMoreHints = hintsRequested < totalHints;

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
      <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <span>💡</span> Pistas Disponibles
      </h3>

      {loading ? (
        <div className="text-center py-4">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-yellow-500"></div>
          <p className="text-slate-400 text-sm mt-2">Cargando pistas...</p>
        </div>
      ) : (
        <div className="space-y-3">
          {displayedHints.length > 0 && (
            <div className="space-y-3 mb-4">
              {displayedHints.map((hint, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-yellow-500/10 border-l-4 border-yellow-500 rounded-lg"
                >
                  <h4 className="text-sm font-bold text-yellow-300 mb-2">
                    {hint.title}
                  </h4>
                  <p className="text-sm text-slate-300 whitespace-pre-wrap">
                    {hint.content}
                  </p>
                </div>
              ))}
            </div>
          )}

          {hasMoreHints ? (
            <button
              onClick={requestHint}
              disabled={requesting}
              className="w-full py-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition duration-200 flex items-center justify-center gap-2"
            >
              {requesting ? (
                <>
                  <span className="animate-spin">⏳</span>
                  Cargando pista...
                </>
              ) : (
                <>
                  <span>💡</span>
                  Solicitar Pista ({hintsRequested}/{totalHints})
                </>
              )}
            </button>
          ) : (
            <div className="p-3 bg-slate-700 rounded-lg text-center">
              <p className="text-sm text-slate-400">
                Se acabaron las pistas disponibles
              </p>
            </div>
          )}

          {totalHints === 0 && (
            <div className="p-4 bg-slate-700 rounded-lg text-center">
              <p className="text-sm text-slate-400">
                No hay pistas disponibles para este desafío
              </p>
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-slate-700">
            <p className="text-xs text-slate-400 text-center">
              💭 Cada pista proporciona orientación progresiva hacia la solución
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default HintSystem;
