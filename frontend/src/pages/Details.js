import React, { useState } from 'react';
import { FileText, BookOpen, Users, TrendingUp, Award, Globe, ChevronDown } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Details = ({ isAuthenticated, userRole, onLogout }) => {
  const [activeTab, setActiveTab] = useState('programs');
  const [expandedFaq, setExpandedFaq] = useState(null);

  const programs = [
    {
      name: 'Licence en Ingénierie',
      duration: '4 ans',
      description: 'Programme d\'ingénierie complet couvrant les disciplines du génie civil, mécanique, électrique et informatique.',
      specializations: ['Génie Civil', 'Génie Mécanique', 'Génie Électrique', 'Génie Logiciel'],
      icon: '🏗️'
    },
    {
      name: 'Licence en Administration des Affaires',
      duration: '4 ans',
      description: 'Préparez-vous à des rôles de direction en affaires avec des cours en gestion, finance, marketing et entrepreneuriat.',
      specializations: ['Finance', 'Marketing', 'Gestion', 'Entrepreneuriat'],
      icon: '💼'
    },
    {
      name: 'Licence en Informatique',
      duration: '4 ans',
      description: 'Maîtrisez la programmation moderne, les algorithmes, l\'IA et l\'apprentissage automatique dans un cursus à la pointe.',
      specializations: ['Intelligence Artificielle', 'Science des Données', 'Cybersécurité', 'Développement Web'],
      icon: '💻'
    },
    {
      name: 'Licence en Études Libérales',
      duration: '4 ans',
      description: 'Explorez les sciences humaines, sociales et naturelles avec une flexibilité dans la sélection des cours.',
      specializations: ['Psychologie', 'Histoire', 'Littérature', 'Sciences Politiques'],
      icon: '📚'
    }
  ];

  const processSteps = [
    {
      number: '1',
      title: 'Soumettre une Candidature',
      description: 'Remplissez le formulaire de candidature en ligne avec vos informations personnelles, académiques et financières.',
      icon: '📝'
    },
    {
      number: '2',
      title: 'Évaluation par IA',
      description: 'Nos modèles ML analysent votre profil pour évaluer votre potentiel académique et votre besoin financier.'  ,
      icon: '🤖'
    },
    {
      number: '3',
      title: 'Vérification des Documents',
      description: 'Soumettez les documents justificatifs (relevés de notes, preuve de revenus, documents d\'identité, etc.)',
      icon: '📋'
    },
    {
      number: '4',
      title: 'Entretien',
      description: 'Participez à un entretien avec notre équipe des admissions pour discuter de vos objectifs et de votre admissibilité.',
      icon: '💬'
    },
    {
      number: '5',
      title: 'Décision',
      description: 'Recevez une notification concernant le statut de votre bourse et le niveau de bourse.',
      icon: '✅'
    },
    {
      number: '6',
      title: 'Inscription',
      description: 'Complétez le processus d\'inscription et commencez votre parcours académique avec nous.',
      icon: '🎓'
    }
  ];

  const faqs = [
    {
      question: 'Quelles sont les exigences académiques minimales ?',
      answer: 'Note générale minimale de 12/20 au Baccalauréat ou équivalent. Vous devez également démontrer de bonnes performances dans les matières fondamentales comme les mathématiques et les langues (français et arabe).'
    },
    {
      question: 'Comment le besoin financier est-il évalué ?',
      answer: 'Nous évaluons le besoin financier par une évaluation complète du revenu familial, des actifs, du nombre de personnes à charge et du coût de la vie régional. Nos modèles ML aident à identifier les candidats les plus méritants selon la méthodologie marocaine.'
    },
    {
      question: 'Puis-je travailler pendant mes études ?',
      answer: 'Oui, les bénéficiaires de bourses sont autorisés à travailler jusqu\'à 20 heures par semaine pendant l\'année académique. Nous offrons également des opportunités d\'emploi sur le campus avec salaire équitable.'
    },
    {
      question: 'Les bourses sont-elles renouvelables ?',
      answer: 'Oui, les bourses sont renouvelables annuellement, à condition de maintenir une note générale minimale de 11/20 et de montrer des progrès académiques satisfaisants.'
    },
    {
      question: 'Les étudiants internationaux peuvent-ils postuler ?',
      answer: 'Absolument ! Nous accueillons les étudiants des pays d\'Afrique du Nord et du Moyen-Orient. Tous les candidats éligibles, indépendamment de leur nationalité, peuvent postuler pour nos bourses.'
    },
    {
      question: 'Quelle est la date limite de candidature ?',
      answer: 'Les candidatures sont acceptées en continu. Cependant, une considération prioritaire est accordée aux candidatures soumises avant le 31 mars pour l\'inscription d\'automne.'
    }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-blue-50">
      <Navbar isAuthenticated={isAuthenticated} userRole={userRole} onLogout={onLogout} />

      {/* Hero Section - Moroccan Style */}
      <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 text-white py-16 overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
        <div className="container mx-auto px-4 relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">Détails des Programmes</h1>
          <div className="h-1 w-16 bg-gradient-to-r from-amber-400 to-red-400 mb-6 rounded"></div>
          <p className="text-xl text-blue-100 max-w-2xl">Informations complètes sur nos programmes d'excellence et le processus de candidature intelligent</p>
        </div>
      </section>

      {/* Tabs - Moroccan Style */}
      <section className="bg-white border-b-2 border-blue-200 sticky top-0 z-20 shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex overflow-x-auto space-x-1">
            <button
              onClick={() => setActiveTab('programs')}
              className={`py-4 px-6 font-bold border-b-4 transition whitespace-nowrap flex items-center space-x-2 ${
                activeTab === 'programs'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-blue-600'
              }`}
            >
              <BookOpen size={20} />
              <span>Programmes</span>
            </button>
            <button
              onClick={() => setActiveTab('process')}
              className={`py-4 px-6 font-bold border-b-4 transition whitespace-nowrap flex items-center space-x-2 ${
                activeTab === 'process'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-blue-600'
              }`}
            >
              <TrendingUp size={20} />
              <span>Processus</span>
            </button>
            <button
              onClick={() => setActiveTab('faq')}
              className={`py-4 px-6 font-bold border-b-4 transition whitespace-nowrap flex items-center space-x-2 ${
                activeTab === 'faq'
                  ? 'border-blue-600 text-blue-600 bg-blue-50'
                  : 'border-transparent text-gray-600 hover:text-blue-600'
              }`}
            >
              <FileText size={20} />
              <span>FAQ</span>
            </button>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          {/* Programs Tab */}
          {activeTab === 'programs' && (
            <div>
              <div className="mb-12">
                <h2 className="text-4xl font-bold text-blue-900 mb-4">🎓 Nos Programmes d'Excellence</h2>
                <div className="h-1 w-16 bg-gradient-to-r from-amber-500 to-red-500 rounded"></div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {programs.map((program, index) => (
                  <div key={index} className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-t-4 border-blue-600">
                    <div className="bg-gradient-to-r from-blue-50 to-amber-50 p-6 flex items-center space-x-4">
                      <span className="text-5xl">{program.icon}</span>
                      <div>
                        <h3 className="text-2xl font-bold text-blue-900">{program.name}</h3>
                        <p className="text-amber-600 font-semibold">⏱️ {program.duration}</p>
                      </div>
                    </div>
                    <div className="p-6">
                      <p className="text-gray-700 mb-6 leading-relaxed">{program.description}</p>
                      <div>
                        <h4 className="font-bold text-blue-900 mb-3 flex items-center space-x-2">
                          <span>📌 Spécialisations:</span>
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {program.specializations.map((spec, i) => (
                            <span key={i} className="bg-gradient-to-r from-blue-100 to-amber-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium border border-blue-200">
                              ✓ {spec}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Process Tab */}
          {activeTab === 'process' && (
            <div>
              <div className="mb-12">
                <h2 className="text-4xl font-bold text-blue-900 mb-4">🚀 Processus de Candidature</h2>
                <div className="h-1 w-16 bg-gradient-to-r from-amber-500 to-red-500 rounded"></div>
              </div>
              <div className="relative">
                {/* Vertical Timeline */}
                <div className="space-y-6">
                  {processSteps.map((step, index) => (
                    <div key={index} className="relative flex gap-6">
                      {/* Timeline Dot */}
                      <div className="flex flex-col items-center">
                        <div className="flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-br from-blue-600 to-blue-500 text-white font-bold text-lg flex-shrink-0 border-4 border-white shadow-lg">
                          {step.number}
                        </div>
                        {index < processSteps.length - 1 && (
                          <div className="w-1 bg-gradient-to-b from-blue-500 to-blue-300 h-16 mt-2"></div>
                        )}
                      </div>

                      {/* Content Card */}
                      <div className="flex-1 pt-2 pb-6">
                        <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition p-6 border-l-4 border-amber-500">
                          <div className="flex items-start space-x-3">
                            <span className="text-3xl">{step.icon}</span>
                            <div>
                              <h3 className="text-xl font-bold text-blue-900 mb-2">{step.title}</h3>
                              <p className="text-gray-700">{step.description}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* FAQ Tab */}
          {activeTab === 'faq' && (
            <div>
              <div className="mb-12">
                <h2 className="text-4xl font-bold text-blue-900 mb-4">❓ Questions Fréquemment Posées</h2>
                <div className="h-1 w-16 bg-gradient-to-r from-amber-500 to-red-500 rounded"></div>
              </div>
              <div className="space-y-4 max-w-4xl">
                {faqs.map((faq, index) => (
                  <div key={index} className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden border-l-4 border-blue-600">
                    <button
                      onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
                      className="w-full p-6 text-left flex items-center justify-between hover:bg-blue-50 transition"
                    >
                      <h3 className="text-lg font-bold text-blue-900 flex-1">{faq.question}</h3>
                      <ChevronDown
                        size={24}
                        className={`text-blue-600 flex-shrink-0 transition transform ${
                          expandedFaq === index ? 'rotate-180' : ''
                        }`}
                      />
                    </button>
                    {expandedFaq === index && (
                      <div className="px-6 pb-6 bg-blue-50 border-t border-blue-200">
                        <p className="text-gray-700 leading-relaxed">{faq.answer}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Statistics Section - Moroccan Styled */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-500 text-white py-16 relative overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-8 bg-white bg-opacity-10 rounded-xl backdrop-blur border border-white border-opacity-20">
              <Globe className="mx-auto mb-4" size={48} />
              <h3 className="text-3xl font-bold mb-2">🏫 Campus Moderne</h3>
              <p className="text-blue-100">Situé au cœur du Maroc avec des installations ultramodernes</p>
            </div>
            <div className="text-center p-8 bg-white bg-opacity-10 rounded-xl backdrop-blur border border-white border-opacity-20">
              <Users className="mx-auto mb-4" size={48} />
              <h3 className="text-3xl font-bold mb-2">👥 12 000+ Étudiants</h3>
              <p className="text-blue-100">Corps étudiant diversifié en provenance de 50+ pays</p>
            </div>
            <div className="text-center p-8 bg-white bg-opacity-10 rounded-xl backdrop-blur border border-white border-opacity-20">
              <Award className="mx-auto mb-4" size={48} />
              <h3 className="text-3xl font-bold mb-2">👨‍🎓 Faculté d'Experts</h3>
              <p className="text-blue-100">Titulaires de doctorats et professionnels reconnus</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Details;
