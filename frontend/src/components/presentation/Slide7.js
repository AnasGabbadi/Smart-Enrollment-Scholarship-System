import React from 'react';
import { motion } from 'framer-motion';

const Slide7 = () => {
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

  const features = [
    { name: 'GPA', description: 'Moyenne générale de l\'étudiant', icon: '📊' },
    { name: 'Note Examen', description: 'Résultat du test académique', icon: '✍️' },
    { name: 'Revenu Mensuel', description: 'Situation financière', icon: '💰' },
    { name: 'Dépendants', description: 'Charge familiale', icon: '👨‍👩‍👧‍👦' },
    { name: 'Distance', description: 'Éloignement géographique', icon: '📍' },
  ];

  return (
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-yellow-50 p-0 overflow-hidden flex flex-col">
      <div className="flex-1 overflow-y-auto">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto px-4 sm:px-6 md:px-8 py-8 md:py-10"
        >
        {/* Title */}
        <motion.div variants={itemVariants} className="mb-4 sm:mb-5">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-600 rounded-xl">
              <span className="text-xl sm:text-2xl md:text-3xl">📦</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
              Présentation du Dataset
            </h1>
          </div>
          <div className="h-1 w-24 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-full mt-2 sm:mt-3" />
        </motion.div>

        {/* Source */}
        <motion.div variants={itemVariants} className="mb-4 sm:mb-5">
          <h2 className="text-sm md:text-base md:text-xl font-bold text-gray-800 mb-4 sm:mb-5">
            📊 Source des Données
          </h2>
          <div className="bg-white rounded-xl p-8 shadow-lg border-l-4 border-yellow-600">
            <p className="text-gray-700 text-sm md:text-base mb-4 sm:mb-5">
              Données historiques d'étudiants marocains:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
              {[
                { icon: '✅', label: 'Admis / Non admis', count: '500K+' },
                { icon: '🎓', label: 'Boursiers / Non boursiers', count: 'records' },
                { icon: '📈', label: 'Données complètes', count: 'nettoyées' },
              ].map((item, idx) => (
                <div key={idx} className="text-center">
                  <div className="text-4xl mb-2">{item.icon}</div>
                  <p className="font-semibold text-gray-900">{item.label}</p>
                  <p className="text-yellow-600 text-sm">{item.count}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div variants={itemVariants} className="mb-4 sm:mb-5">
          <h2 className="text-sm md:text-base md:text-xl font-bold text-gray-800 mb-4 sm:mb-5">
            🎯 Features (Caractéristiques) Utilisées
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                whileHover={{ y: -8 }}
                className="bg-white rounded-xl p-3 sm:p-4 shadow-lg text-center border-t-4 border-yellow-600"
              >
                <div className="text-3xl mb-2">{feature.icon}</div>
                <h3 className="font-bold text-gray-900 text-sm mb-2">{feature.name}</h3>
                <p className="text-xs text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>

          {/* Table */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-yellow-600 to-orange-600 text-white">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-bold">Feature</th>
                    <th className="px-6 py-3 text-left text-sm font-bold">Description</th>
                    <th className="px-6 py-3 text-left text-sm font-bold">Type</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {[
                    { feature: 'GPA', desc: 'Moyenne générale', type: 'Numérique (0-20)' },
                    { feature: 'Note Examen', desc: 'Résultat du test', type: 'Numérique (0-20)' },
                    { feature: 'Revenu Mensuel', desc: 'Situation financière', type: 'Numérique (DH)' },
                    { feature: 'Dépendants', desc: 'Nombre de charges', type: 'Entier' },
                    { feature: 'Distance', desc: 'Éloignement en km', type: 'Numérique' },
                  ].map((row, idx) => (
                    <tr key={idx} className="hover:bg-yellow-50 transition">
                      <td className="px-6 py-4 font-semibold text-gray-900">{row.feature}</td>
                      <td className="px-6 py-4 text-gray-700">{row.desc}</td>
                      <td className="px-6 py-4 text-sm text-gray-600 bg-yellow-50">{row.type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </motion.div>

        {/* Key Point */}
        <motion.div variants={itemVariants}>
          <div className="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-xl p-8 shadow-xl text-white">
            <div className="flex items-start gap-4">
              <span className="text-2xl sm:text-3xl md:text-4xl">🎯</span>
              <div>
                <h3 className="text-xl font-bold mb-2">Ces données représentent le problème réel à résoudre</h3>
                <p className="text-sm md:text-base opacity-90">
                  Elles reflètent les critères objectifs et subjectifs utilisés dans les décisions d'admission et d'attribution de bourses.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
      </div>
    </div>
  );
};

export default Slide7;
