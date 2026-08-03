import React from 'react';
import { motion } from 'framer-motion';

const Slide2 = () => {
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
    <div className="w-full h-full bg-gradient-to-br from-slate-50 to-blue-50 p-0 overflow-hidden flex flex-col">
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
            <div className="p-3 bg-blue-600 rounded-xl">
              <span className="text-xl sm:text-2xl md:text-3xl">🤖</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
              Machine Learning
            </h1>
          </div>
          <div className="h-1 w-24 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mt-2 sm:mt-3" />
        </motion.div>

        {/* Section 1 */}
        <motion.div variants={itemVariants} className="mb-4 sm:mb-5">
          <h2 className="text-sm md:text-base md:text-xl font-bold text-gray-800 mb-4">
            Qu'est-ce que le Machine Learning ?
          </h2>
          <div className="bg-white rounded-xl p-3 sm:p-4 shadow-lg border-l-4 border-blue-600">
            <p className="text-gray-700 text-sm md:text-base leading-relaxed">
              Le Machine Learning est une branche de l'intelligence artificielle qui permet à une machine
              d'<span className="font-semibold text-blue-600">apprendre automatiquement à partir des données</span>,
              sans être explicitement programmée pour chaque règle.
            </p>
          </div>
        </motion.div>

        {/* Section 2 */}
        <motion.div variants={itemVariants} className="mb-4 sm:mb-5">
          <h2 className="text-sm md:text-base md:text-xl font-bold text-gray-800 mb-4">
            Principe Général
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
            {[
              { icon: '📚', title: 'Observer', desc: 'Données historiques' },
              { icon: '🧠', title: 'Apprendre', desc: 'Relations mathématiques' },
              { icon: '🎯', title: 'Prédire', desc: 'Nouvelles données' },
            ].map((step, idx) => (
              <motion.div
                key={idx}
                whileHover={{ y: -8 }}
                className="bg-white rounded-xl p-3 sm:p-4 shadow-lg text-center border-t-4 border-blue-600"
              >
                <div className="text-4xl mb-3">{step.icon}</div>
                <h3 className="font-bold text-gray-900 text-sm md:text-base mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Section 3 */}
        <motion.div variants={itemVariants}>
          <h2 className="text-sm md:text-base md:text-xl font-bold text-gray-800 mb-4">
            Pourquoi le Machine Learning ?
          </h2>
          <div className="space-y-4">
            {[
              '✓ Gestion de grandes quantités de données',
              '✓ Décisions plus objectives',
              '✓ Amélioration continue avec le temps',
            ].map((benefit, idx) => (
              <motion.div
                key={idx}
                whileHover={{ x: 10 }}
                className="flex items-center gap-4 bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border-l-4 border-blue-600"
              >
                <span className="text-sm md:text-base md:text-xl">💡</span>
                <span className="text-gray-800 text-sm md:text-base font-medium">{benefit}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </motion.div>
      </div>
    </div>
  );
};

export default Slide2;
