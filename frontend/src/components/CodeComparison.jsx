import React, { useState } from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const CodeComparison = ({ challenge }) => {
  const [view, setView] = useState('side'); // 'side' or 'stacked'

  const getLanguage = (lang) => {
    const langMap = {
      'Python': 'python',
      'JavaScript': 'javascript',
      'Java': 'java',
      'PHP': 'php',
      'C#': 'csharp',
      'Go': 'go',
      'Rust': 'rust',
      'Python/HTML': 'python'
    };
    return langMap[lang] || 'python';
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-white">💻 Comparación de Código</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setView('side')}
            className={`px-3 py-1 text-sm rounded transition ${
              view === 'side'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Lado a Lado
          </button>
          <button
            onClick={() => setView('stacked')}
            className={`px-3 py-1 text-sm rounded transition ${
              view === 'stacked'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            Apilado
          </button>
        </div>
      </div>

      {view === 'side' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Vulnerable */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-700">
              <span className="text-red-500 text-xl">❌</span>
              <h4 className="font-bold text-red-400">Código Vulnerable</h4>
            </div>
            <SyntaxHighlighter
              language={getLanguage(challenge.vulnerable_code_language)}
              style={atomOneDark}
              className="rounded-lg text-sm !bg-slate-900"
              showLineNumbers
            >
              {challenge.vulnerable_code}
            </SyntaxHighlighter>
          </div>

          {/* Secure */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-700">
              <span className="text-green-500 text-xl">✓</span>
              <h4 className="font-bold text-green-400">Código Seguro</h4>
            </div>
            <SyntaxHighlighter
              language={getLanguage(challenge.secure_code_language)}
              style={atomOneDark}
              className="rounded-lg text-sm !bg-slate-900"
              showLineNumbers
            >
              {challenge.secure_code}
            </SyntaxHighlighter>
          </div>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Vulnerable */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-700">
              <span className="text-red-500 text-xl">❌</span>
              <h4 className="font-bold text-red-400">Código Vulnerable</h4>
            </div>
            <SyntaxHighlighter
              language={getLanguage(challenge.vulnerable_code_language)}
              style={atomOneDark}
              className="rounded-lg text-sm !bg-slate-900"
              showLineNumbers
            >
              {challenge.vulnerable_code}
            </SyntaxHighlighter>
          </div>

          {/* Secure */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-700">
              <span className="text-green-500 text-xl">✓</span>
              <h4 className="font-bold text-green-400">Código Seguro</h4>
            </div>
            <SyntaxHighlighter
              language={getLanguage(challenge.secure_code_language)}
              style={atomOneDark}
              className="rounded-lg text-sm !bg-slate-900"
              showLineNumbers
            >
              {challenge.secure_code}
            </SyntaxHighlighter>
          </div>
        </div>
      )}

      {/* Key Differences */}
      <div className="mt-8 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
        <h4 className="font-bold text-blue-300 mb-3 flex items-center gap-2">
          <span>💡</span> Diferencias Clave
        </h4>
        <ul className="text-sm text-slate-300 space-y-2">
          <li className="flex items-start gap-3">
            <span className="text-red-500 font-bold mt-1">✗</span>
            <span>El código vulnerable confía en entrada del usuario sin validación</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-green-500 font-bold mt-1">✓</span>
            <span>El código seguro valida, sanitiza y usa métodos seguros como prepared statements</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="text-blue-500 font-bold mt-1">📌</span>
            <span>Aplica el principio de "no confiar" - valida SIEMPRE entrada externa</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default CodeComparison;
