import React, { useState } from 'react';

const LessonContent = ({ lesson, userId }) => {
  const [completed, setCompleted] = useState(false);

  const markAsCompleted = () => {
    setCompleted(true);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-8 text-white shadow-2xl">
        <p className="text-purple-200 text-sm font-semibold mb-2 uppercase tracking-wide">
          Lección {lesson.order}
        </p>
        <h1 className="text-4xl font-bold mb-3">{lesson.title}</h1>
        <p className="text-purple-100 text-lg mb-6">{lesson.description}</p>
        
        <div className="flex items-center gap-4 mt-8 pt-8 border-t border-white/20">
          <span className={`px-4 py-2 rounded-full font-semibold ${
            lesson.difficulty === 'BEGINNER' ? 'bg-green-500/30 text-green-100' :
            lesson.difficulty === 'INTERMEDIATE' ? 'bg-yellow-500/30 text-yellow-100' :
            'bg-red-500/30 text-red-100'
          }`}>
            {lesson.difficulty === 'BEGINNER' ? '🌱 Principiante' :
             lesson.difficulty === 'INTERMEDIATE' ? '🌿 Intermedio' :
             '🚀 Avanzado'}
          </span>
          {lesson.video_url && (
            <span className="px-4 py-2 bg-white/20 rounded-full text-white">
              📹 Incluye video
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-8 text-white">
            <div className="prose prose-invert max-w-none">
              {lesson.content.split('\n\n').map((paragraph, idx) => {
                // Check if it's a heading (starts with ##, ###, etc)
                if (paragraph.startsWith('###')) {
                  return (
                    <h3 key={idx} className="text-xl font-bold mt-6 mb-3 text-blue-300">
                      {paragraph.replace(/^#+\s/, '')}
                    </h3>
                  );
                }
                if (paragraph.startsWith('##')) {
                  return (
                    <h2 key={idx} className="text-2xl font-bold mt-6 mb-3 text-blue-400">
                      {paragraph.replace(/^#+\s/, '')}
                    </h2>
                  );
                }
                // Check if it's a list
                if (paragraph.startsWith('-') || paragraph.startsWith('•')) {
                  return (
                    <ul key={idx} className="list-disc list-inside space-y-2 text-slate-300">
                      {paragraph.split('\n').map((item, itemIdx) => (
                        <li key={itemIdx}>{item.replace(/^[-•]\s/, '')}</li>
                      ))}
                    </ul>
                  );
                }
                // Regular paragraph
                return (
                  <p key={idx} className="text-slate-300 leading-relaxed mb-4">
                    {paragraph}
                  </p>
                );
              })}
            </div>
          </div>

          {/* Video Section */}
          {lesson.video_url && (
            <div className="mt-8 bg-slate-800 border border-slate-700 rounded-xl p-8 overflow-hidden">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>📹</span> Video Educativo
              </h3>
              <div className="aspect-video bg-slate-900 rounded-lg overflow-hidden">
                <iframe
                  width="100%"
                  height="100%"
                  src={lesson.video_url}
                  title="Lesson Video"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                ></iframe>
              </div>
            </div>
          )}

          {/* Image Section */}
          {lesson.image_url && (
            <div className="mt-8 bg-slate-800 border border-slate-700 rounded-xl p-8 overflow-hidden">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>🖼️</span> Diagrama Educativo
              </h3>
              <img
                src={lesson.image_url}
                alt={lesson.title}
                className="w-full rounded-lg"
              />
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Lesson Info */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 sticky top-24">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <span>📚</span> Información
            </h3>

            <div className="space-y-4 text-sm">
              <div className="p-4 bg-slate-700 rounded-lg">
                <p className="text-slate-400 text-xs uppercase tracking-wide mb-1">
                  Dificultad
                </p>
                <p className="text-white font-semibold">
                  {lesson.difficulty === 'BEGINNER' ? '🌱 Principiante' :
                   lesson.difficulty === 'INTERMEDIATE' ? '🌿 Intermedio' :
                   '🚀 Avanzado'}
                </p>
              </div>

              <div className="p-4 bg-slate-700 rounded-lg">
                <p className="text-slate-400 text-xs uppercase tracking-wide mb-1">
                  Orden de Lección
                </p>
                <p className="text-white font-semibold">Lección {lesson.order}</p>
              </div>
            </div>

            {/* Completion Button */}
            {!completed && (
              <button
                onClick={markAsCompleted}
                className="w-full mt-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition duration-200"
              >
                ✓ Marcar como completada
              </button>
            )}

            {completed && (
              <div className="w-full mt-6 py-3 bg-green-600/30 border border-green-500 text-green-300 font-bold rounded-lg text-center">
                ✓ Lección completada
              </div>
            )}
          </div>

          {/* Key Takeaways */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <span>🎯</span> Puntos Clave
            </h3>

            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-3">
                <span className="text-yellow-400 font-bold mt-1">•</span>
                <p className="text-slate-300">
                  Comprende los fundamentos de las vulnerabilidades de seguridad
                </p>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-yellow-400 font-bold mt-1">•</span>
                <p className="text-slate-300">
                  Aprende las mejores prácticas para escribir código seguro
                </p>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-yellow-400 font-bold mt-1">•</span>
                <p className="text-slate-300">
                  Practica con ejercicios interactivos basados en esto
                </p>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 border border-blue-500 rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <span>💡</span> Próximos Pasos
            </h3>

            <ol className="space-y-3 text-sm text-blue-50">
              <li className="flex gap-3">
                <span className="font-bold">1.</span>
                <span>Lee esta lección completa</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">2.</span>
                <span>Ve el video si está disponible</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">3.</span>
                <span>Practica con los desafíos relacionados</span>
              </li>
              <li className="flex gap-3">
                <span className="font-bold">4.</span>
                <span>Revisa el código usado por otros</span>
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LessonContent;
