import React from 'react';
import { motion } from 'framer-motion';

const Slide8 = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 },
    },
  };

  const itemVariants = {
    hidden: { x: -50, opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: { duration: 0.6, type: 'spring' },
    },
  };

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-pink-50 p-0 overflow-hidden flex flex-col relative">
      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto relative z-10 px-4 sm:px-6 md:px-8 py-6 md:py-8">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto space-y-5 sm:space-y-6"
        >
          {/* Title */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center gap-3 sm:gap-4">
              <div className="p-2.5 sm:p-3 bg-pink-600 rounded-xl">
                <span className="text-lg sm:text-xl md:text-2xl">🔧</span>
              </div>
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900">
                Prétraitement des Données
              </h1>
            </div>
            <div className="h-1 w-20 bg-gradient-to-r from-pink-600 to-red-600 rounded-full mt-2 sm:mt-3" />
          </motion.div>

          {/* Étapes */}
          <motion.div variants={itemVariants}>
            <h2 className="text-base sm:text-lg md:text-xl font-bold text-gray-800 mb-3 sm:mb-4">
              🛠️ Étapes Réalisées
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
              {[
                { icon: '🧹', title: 'Nettoyage', desc: 'Suppression des données corrompues' },
                { icon: '⚠️', title: 'Gestion Valeurs Manquantes', desc: 'Imputation intelligente' },
                { icon: '📊', title: 'Normalisation', desc: 'Mise à l\'échelle des features' },
                { icon: '✂️', title: 'Séparation Train/Test', desc: '70% / 30%' },
              ].map((step, idx) => (
                <motion.div
                  key={idx}
                  whileHover={{ y: -5 }}
                  className="bg-white rounded-xl p-3 sm:p-4 shadow-lg border-t-4 border-pink-600"
                >
                  <div className="text-3xl sm:text-4xl mb-2 sm:mb-3">{step.icon}</div>
                  <h3 className="font-bold text-gray-900 text-sm md:text-base mb-1">{step.title}</h3>
                  <p className="text-gray-600 text-xs sm:text-sm">{step.desc}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Process Flow */}
          <motion.div variants={itemVariants}>
            <h2 className="text-base sm:text-lg md:text-xl font-bold text-gray-800 mb-3 sm:mb-4">
              📈 Processus Détaillé
            </h2>
            <div className="bg-white rounded-xl p-5 sm:p-6 md:p-8 shadow-lg">
              <div className="space-y-4 sm:space-y-5">
                {[
                  { step: 1, title: 'Nettoyage des données', details: 'Suppression des doublets, valeurs aberrantes, données incohérentes' },
                  { step: 2, title: 'Gestion des valeurs manquantes', details: 'Imputation par moyenne, médiane ou suppression intelligente' },
                  { step: 3, title: 'Normalisation/Scaling', details: 'Mise à l\'échelle pour que toutes les features aient le même poids' },
                  { step: 4, title: 'Encodage catégories', details: 'Conversion des variables catégoriques en numériques' },
                  { step: 5, title: 'Séparation Train/Test', details: '70% données d\'entraînement, 30% de test' },
                ].map((item, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ x: 5 }}
                    className="flex items-start gap-2 sm:gap-3 pb-4 sm:pb-5 border-b border-gray-200 last:border-0"
                  >
                    <div className="bg-gradient-to-br from-pink-600 to-red-600 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold flex-shrink-0 text-sm sm:text-base">
                      {item.step}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-900 text-sm md:text-base mb-1">{item.title}</h3>
                      <p className="text-gray-700 text-xs sm:text-sm">{item.details}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Pourquoi le prétraitement */}
          <motion.div variants={itemVariants}>
            <h2 className="text-base sm:text-lg md:text-xl font-bold text-gray-800 mb-3 sm:mb-4">
              ✅ Pourquoi le Prétraitement ?
            </h2>
            <div className="bg-gradient-to-r from-pink-500 to-red-500 rounded-xl p-5 sm:p-6 md:p-8 shadow-xl text-white">
              <p className="text-sm md:text-base font-semibold mb-3 sm:mb-4">Garantir:</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
                {[
                  { icon: '⚡', title: 'Stabilité', desc: 'Modèles plus stables et robustes' },
                  { icon: '🎯', title: 'Convergence', desc: 'Meilleure convergence durant l\'entraînement' },
                  { icon: '✅', title: 'Fiabilité', desc: 'Résultats plus fiables et prédictifs' },
                ].map((benefit, idx) => (
                  <div key={idx} className="text-center">
                    <div className="text-3xl sm:text-4xl mb-2 sm:mb-3">{benefit.icon}</div>
                    <h3 className="font-bold text-sm md:text-base mb-1">{benefit.title}</h3>
                    <p className="text-xs sm:text-sm opacity-90">{benefit.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Slide8;
