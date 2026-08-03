import React from 'react';
import { X, Brain, TrendingUp, DollarSign, Target, AlertCircle } from 'lucide-react';

const AIRecommendationModal = ({ student, recommendations, onClose, isOpen }) => {
  if (!isOpen || !recommendations) return null;

  const { capaciteFinanciere, recommandationBourse, probabiliteInscription, recommandationGlobale, details } = recommendations;

  // Fonction pour déterminer la couleur en fonction du niveau
  const getCouleurCapacite = (score) => {
    if (score >= 60) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 30) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getCouleurBourse = (type) => {
    if (type === 'Complète') return 'text-green-600 bg-green-50 border-green-200';
    if (type === 'Partielle') return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getCouleurProbabilite = (niveau) => {
    if (niveau.includes('Élevée')) return 'text-green-600 bg-green-50 border-green-200';
    if (niveau.includes('Moyenne')) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getCouleurDecision = (couleur) => {
    if (couleur === 'green') return 'bg-green-600 text-white';
    if (couleur === 'yellow') return 'bg-yellow-500 text-white';
    return 'bg-red-600 text-white';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-t-lg">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-3">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <Brain size={32} />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Recommandations IA</h2>
                <p className="text-blue-100 text-sm mt-1">
                  Analyse complète pour {recommendations.nomComplet}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition"
            >
              <X size={24} />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Recommandation Globale */}
          <div className={`${getCouleurDecision(recommandationGlobale.couleur)} rounded-xl p-6 shadow-lg`}>
            <div className="flex items-start gap-4">
              <div className="bg-white bg-opacity-20 p-3 rounded-lg">
                <Target size={28} />
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">
                  {recommandationGlobale.decision}
                </h3>
                <p className="text-lg opacity-95 leading-relaxed">
                  {recommandationGlobale.justification}
                </p>
                <div className="mt-4 flex items-center gap-2">
                  <div className="bg-white bg-opacity-20 px-4 py-2 rounded-lg">
                    <span className="text-sm font-semibold">
                      Score Global: {recommandationGlobale.scoreGlobal}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Grid des 3 prédictions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Capacité Financière */}
            <div className={`border-2 rounded-lg p-5 ${getCouleurCapacite(capaciteFinanciere.score)}`}>
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-white p-2 rounded-lg shadow">
                  <TrendingUp size={24} className={getCouleurCapacite(capaciteFinanciere.score).split(' ')[0]} />
                </div>
                <h4 className="font-bold text-lg">Capacité Financière</h4>
              </div>
              <div className="space-y-2">
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-3xl font-bold text-center mb-1">
                    {capaciteFinanciere.score}/100
                  </div>
                  <div className="text-center text-sm font-semibold opacity-80">
                    {capaciteFinanciere.niveau}
                  </div>
                </div>
                <p className="text-sm leading-relaxed">
                  {capaciteFinanciere.message}
                </p>
              </div>
            </div>

            {/* Recommandation de Bourse */}
            <div className={`border-2 rounded-lg p-5 ${getCouleurBourse(recommandationBourse.type)}`}>
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-white p-2 rounded-lg shadow">
                  <DollarSign size={24} className={getCouleurBourse(recommandationBourse.type).split(' ')[0]} />
                </div>
                <h4 className="font-bold text-lg">Type de Bourse</h4>
              </div>
              <div className="space-y-2">
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-2xl font-bold text-center mb-1">
                    {recommandationBourse.type}
                  </div>
                  <div className="text-center text-lg font-semibold opacity-80">
                    {recommandationBourse.montant > 0 ? `${recommandationBourse.montant.toLocaleString()} DH` : 'N/A'}
                  </div>
                </div>
                <p className="text-sm leading-relaxed">
                  {recommandationBourse.message}
                </p>
              </div>
            </div>

            {/* Probabilité d'Inscription */}
            <div className={`border-2 rounded-lg p-5 ${getCouleurProbabilite(probabiliteInscription.niveau)}`}>
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-white p-2 rounded-lg shadow">
                  <Target size={24} className={getCouleurProbabilite(probabiliteInscription.niveau).split(' ')[0]} />
                </div>
                <h4 className="font-bold text-lg">Probabilité d'Inscription</h4>
              </div>
              <div className="space-y-2">
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-2xl font-bold text-center mb-1">
                    {probabiliteInscription.niveau}
                  </div>
                  <div className="text-center text-sm font-semibold opacity-80">
                    Confiance: {probabiliteInscription.confiance}%
                  </div>
                </div>
                <p className="text-sm leading-relaxed">
                  Probabilité que l'étudiant s'inscrive après acceptation
                </p>
              </div>
            </div>
          </div>

          {/* Détails des données */}
          <div className="bg-gray-50 rounded-lg p-5 border border-gray-200">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle size={20} className="text-gray-600" />
              <h4 className="font-bold text-gray-800">Données Utilisées pour l'Analyse</h4>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                <div className="text-xs text-gray-600 mb-1">GPA</div>
                <div className="text-lg font-bold text-gray-800">{details.gpa.toFixed(2)}</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                <div className="text-xs text-gray-600 mb-1">Note Examen</div>
                <div className="text-lg font-bold text-gray-800">{details.noteExamen}</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                <div className="text-xs text-gray-600 mb-1">Revenu</div>
                <div className="text-lg font-bold text-gray-800">{details.revenu.toLocaleString()}</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                <div className="text-xs text-gray-600 mb-1">Dépendants</div>
                <div className="text-lg font-bold text-gray-800">{details.dependants}</div>
              </div>
              <div className="bg-white rounded-lg p-3 text-center shadow-sm">
                <div className="text-xs text-gray-600 mb-1">Distance (km)</div>
                <div className="text-lg font-bold text-gray-800">{details.distance}</div>
              </div>
            </div>
          </div>

          {/* Note informative */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800 leading-relaxed">
              <strong>Note:</strong> Ces recommandations sont générées par des modèles d'intelligence artificielle 
              basés sur les données historiques et les performances académiques. Elles servent d'aide à la décision 
              et doivent être considérées en complément d'une évaluation humaine complète.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 rounded-b-lg border-t border-gray-200">
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-3 px-6 rounded-lg transition shadow-lg"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIRecommendationModal;
