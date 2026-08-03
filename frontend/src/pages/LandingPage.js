import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle, Award, Users, Zap } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const LandingPage = ({ isAuthenticated, userRole, onLogout }) => {
  // Zelij Pattern SVG
  const ZelijPattern = ({ className = "" }) => (
    <svg className={className} viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="zelij" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
          <rect width="40" height="40" fill="currentColor" opacity="0.05"/>
          <path d="M20,0 L40,20 L20,40 L0,20 Z" stroke="currentColor" strokeWidth="1" fill="none" opacity="0.3"/>
          <circle cx="20" cy="20" r="8" fill="none" stroke="currentColor" strokeWidth="1" opacity="0.3"/>
          <rect x="10" y="10" width="20" height="20" stroke="currentColor" strokeWidth="1" fill="none" opacity="0.2"/>
        </pattern>
      </defs>
      <rect width="200" height="200" fill="url(#zelij)"/>
    </svg>
  );

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-blue-50">
      <Navbar isAuthenticated={isAuthenticated} userRole={userRole} onLogout={onLogout} />

      {/* Hero Section - Moroccan Style */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 text-white py-24">
        {/* Zelij Pattern Background */}
        <div className="absolute inset-0 opacity-10">
          <ZelijPattern className="w-full h-full text-white" />
        </div>
        
        {/* Geometric Border Top */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block mb-4 px-4 py-2 bg-amber-500 bg-opacity-30 rounded-full border border-amber-300">
                <span className="text-amber-200 font-semibold text-sm">🎓 Excellence Académique depuis 1950</span>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight text-white drop-shadow-lg">
                Transformez Votre Avenir
              </h1>
              <p className="text-xl mb-8 text-blue-100 leading-relaxed">
                Accédez à une distribution intelligente des bourses alimentée par l'apprentissage automatique. Opportunités de parrainage à 100% pour les étudiants qualifiés du Maroc et du monde.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/student-register" className="flex items-center justify-center space-x-2 bg-gradient-to-r from-amber-400 to-amber-500 text-blue-900 hover:from-amber-300 hover:to-amber-400 px-8 py-3 rounded-lg font-bold transition transform hover:scale-105 shadow-lg">
                  <span>Postuler Maintenant</span>
                  <ArrowRight size={20} />
                </Link>
                <Link to="/details" className="px-8 py-3 border-2 border-amber-400 rounded-lg font-bold hover:bg-amber-400 hover:text-blue-900 transition">
                  En Savoir Plus
                </Link>
              </div>
            </div>
            <div className="relative hidden md:block">
              {/* Moroccan Geometric Design */}
              <div className="absolute inset-0 bg-gradient-to-br from-amber-500 to-red-500 opacity-20 rounded-3xl transform rotate-6 blur-xl"></div>
              <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-3xl shadow-2xl p-8 relative z-10 border-2 border-amber-200">
                <div className="text-center">
                  <div className="text-7xl mb-4">🎓</div>
                  <h3 className="text-3xl font-bold text-blue-900 mb-2">100% Sponsorship</h3>
                  <div className="h-1 w-16 bg-gradient-to-r from-amber-500 to-red-500 mx-auto mb-4 rounded"></div>
                  <p className="text-gray-700">Pour les étudiants qualifiés du monde entier</p>
                  <div className="mt-6 text-sm text-gray-600">
                    <p className="font-semibold mb-2">Conditions Minimales:</p>
                    <p>✓ Note générale ≥ 12/20 (Bac)</p>
                    <p>✓ Besoin financier démontré</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* School Heritage Section - Moroccan Heritage */}
      <section className="py-20 md:py-28 relative">
        {/* Zelij Pattern Background */}
        <div className="absolute inset-0 opacity-5">
          <ZelijPattern className="w-full h-full text-blue-900" />
        </div>

        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-blue-900 mb-4">À Propos de Notre Institution</h2>
            <div className="h-1 w-24 bg-gradient-to-r from-amber-500 to-red-500 mx-auto rounded mb-6"></div>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto font-medium">
              Leader dans l'excellence éducative depuis 1950 - Un pont entre tradition et modernité
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Heritage Card */}
            <div className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-t-4 border-blue-600">
              <div className="h-2 bg-gradient-to-r from-blue-600 to-blue-400"></div>
              <div className="p-8">
                <div className="text-5xl mb-4">🏛️</div>
                <h3 className="text-2xl font-bold text-blue-900 mb-4">Notre Héritage</h3>
                <div className="h-0.5 w-12 bg-amber-500 mb-4 rounded"></div>
                <p className="text-gray-700 leading-relaxed">
                  Établie en 1950, notre institution s'inspire de l'excellence marocaine et de l'innovation. Avec plus de 70 ans d'expérience, nous avons formé les leaders et innovateurs de demain, ancrés dans les valeurs de la société marocaine.
                </p>
              </div>
            </div>

            {/* Mission Card */}
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-t-4 border-amber-600">
              <div className="h-2 bg-gradient-to-r from-amber-600 to-orange-500"></div>
              <div className="p-8">
                <div className="text-5xl mb-4">🎯</div>
                <h3 className="text-2xl font-bold text-blue-900 mb-4">Notre Mission</h3>
                <div className="h-0.5 w-12 bg-blue-600 mb-4 rounded"></div>
                <p className="text-gray-700 leading-relaxed">
                  Fournir une éducation de classe mondiale qui responsabilise les étudiants pour atteindre leur plein potentiel. Nous croyons que l'excellence éducative doit être accessible à tous, indépendamment de leur situation financière.
                </p>
              </div>
            </div>

            {/* Vision Card */}
            <div className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-t-4 border-red-600">
              <div className="h-2 bg-gradient-to-r from-red-600 to-red-400"></div>
              <div className="p-8">
                <div className="text-5xl mb-4">🌟</div>
                <h3 className="text-2xl font-bold text-blue-900 mb-4">Notre Vision</h3>
                <div className="h-0.5 w-12 bg-amber-500 mb-4 rounded"></div>
                <p className="text-gray-700 leading-relaxed">
                  Devenir une institution mondialement reconnue pour l'excellence académique et la recherche. Former des leaders éthiques et responsables qui contribuent au progrès du Maroc et du monde.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* 100% Sponsorship Section - Moroccan Style */}
      <section className="py-20 md:py-28 bg-gradient-to-br from-blue-50 via-amber-50 to-orange-50 relative">
        {/* Top Border */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-amber-500 to-red-600"></div>

        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-blue-900 mb-4">
              Opportunités de Parrainage à 100%
            </h2>
            <div className="h-1 w-24 bg-gradient-to-r from-amber-500 to-red-500 mx-auto rounded mb-6"></div>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto font-medium">
              Soutien complet pour les étudiants méritants
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            {/* Complete Coverage Card */}
            <div className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-l-4 border-blue-600">
              <div className="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-6 flex items-center space-x-4">
                <Award className="flex-shrink-0" size={32} />
                <h3 className="text-2xl font-bold">Couverture Complète</h3>
              </div>
              <div className="p-8">
                <ul className="space-y-4">
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Frais de scolarité complets pour tous les programmes</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Logement et restauration fournis</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Livres et matériel pédagogique</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Allocation mensuelle pour subsistance</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Assurance santé complète</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Additional Benefits Card */}
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden border-l-4 border-amber-600">
              <div className="bg-gradient-to-r from-amber-600 to-orange-500 text-white p-6 flex items-center space-x-4">
                <Zap className="flex-shrink-0" size={32} />
                <h3 className="text-2xl font-bold">Avantages Supplémentaires</h3>
              </div>
              <div className="p-8">
                <ul className="space-y-4">
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Opportunités de stage en entreprise</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Mentorat et conseil en carrière</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Accès aux installations modernes</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Programmes d'échange international</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <div className="flex-shrink-0 h-6 w-6 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mt-0.5">
                      <CheckCircle className="text-white" size={16} />
                    </div>
                    <span className="text-gray-700 font-medium">Soutien académique personnalisé</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Moroccan Eligibility Section */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden border-t-4 border-red-600">
            <div className="bg-gradient-to-r from-red-600 to-red-500 text-white p-8 flex items-center space-x-4">
              <Users className="flex-shrink-0" size={32} />
              <h3 className="text-2xl font-bold">Critères d'Admissibilité</h3>
            </div>
            <div className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="border-l-4 border-blue-600 pl-6">
                  <h4 className="font-bold text-blue-900 mb-3 text-lg">📚 Excellence Académique</h4>
                  <p className="text-gray-700 leading-relaxed">
                    Note générale minimale de <span className="font-semibold">12/20</span> au Baccalauréat. Excellente performance en mathématiques et français. Pour Bac+2 et plus: minimum <span className="font-semibold">11/20</span>.
                  </p>
                </div>
                <div className="border-l-4 border-amber-600 pl-6">
                  <h4 className="font-bold text-blue-900 mb-3 text-lg">💰 Besoins Financiers</h4>
                  <p className="text-gray-700 leading-relaxed">
                    Revenus familiaux limités avec documents justificatifs. Priorité aux familles de classe moyenne et modeste. Analyse complète de la situation économique requise.
                  </p>
                </div>
                <div className="border-l-4 border-red-600 pl-6">
                  <h4 className="font-bold text-blue-900 mb-3 text-lg">⭐ Caractère et Engagement</h4>
                  <p className="text-gray-700 leading-relaxed">
                    Lettres de recommandation solides, engagement communautaire et leadership. Démonstration claire d'engagement envers le succès académique et professionnel.
                  </p>
                </div>
              </div>
              
              <div className="mt-8 p-6 bg-blue-50 rounded-lg border border-blue-200">
                <h4 className="font-bold text-blue-900 mb-4 flex items-center space-x-2">
                  <span className="text-lg">🇲🇦</span>
                  <span>Conditions Spéciales pour Étudiants Marocains</span>
                </h4>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-500 font-bold">✓</span>
                    <span>Citoyenneté marocaine ou résidence depuis 5 ans minimum</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-500 font-bold">✓</span>
                    <span>Reconnaissance de diplôme Baccalauréat marocain ou équivalent</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-500 font-bold">✓</span>
                    <span>Priorité accordée aux candidats des régions en développement</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* Call to Action - Moroccan Style */}
      <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 text-white py-20 md:py-24 overflow-hidden">
        {/* Zelij Pattern Background */}
        <div className="absolute inset-0 opacity-10">
          <ZelijPattern className="w-full h-full text-white" />
        </div>

        {/* Geometric Border */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>

        <div className="container mx-auto px-4 relative z-10 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 drop-shadow-lg">Prêt à Transformer Votre Avenir ?</h2>
          <div className="h-1 w-24 bg-gradient-to-r from-amber-400 to-red-400 mx-auto rounded mb-8"></div>
          <p className="text-xl mb-12 text-blue-100 max-w-2xl mx-auto leading-relaxed">
            Rejoignez des milliers de boursiers qui ont transformé leur vie par l'excellence éducative. Votre excellence académique et votre engagement méritent d'être soutenus.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/student-register" className="px-8 py-3 bg-gradient-to-r from-amber-400 to-amber-500 text-blue-900 font-bold rounded-lg hover:from-amber-300 hover:to-amber-400 transition transform hover:scale-105 shadow-lg">
              Commencer Votre Candidature
            </Link>
            <Link to="/details" className="px-8 py-3 border-2 border-amber-400 rounded-lg font-bold hover:bg-amber-400 hover:text-blue-900 transition">
              En Savoir Plus sur les Programmes
            </Link>
          </div>

          <div className="mt-12 pt-8 border-t border-blue-400 border-opacity-30">
            <p className="text-blue-100 text-sm">
              📞 Contactez notre équipe d'admission pour plus d'informations | 📧 admission@institution.edu
            </p>
          </div>
        </div>
      </section>

      {/* Presentation Section */}
      <section className="py-20 bg-gradient-to-br from-purple-900 to-blue-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              🎓 Présentation du Projet
            </h2>
            <p className="text-xl text-purple-200 max-w-2xl mx-auto">
              Découvrez notre système intelligent d'admission basé sur le Machine Learning
            </p>
          </div>
          <div className="max-w-2xl mx-auto">
            <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-8 hover:bg-white/15 transition">
              <div className="text-center mb-6">
                <div className="text-5xl mb-4">🤖</div>
                <h3 className="text-2xl font-bold text-white mb-2">
                  Système Intelligent d'Admission et d'Attribution de Bourses
                </h3>
                <p className="text-purple-200 mb-6">
                  Une présentation interactive couvrant les 3 modèles ML, l'architecture, et les résultats
                </p>
              </div>
              <Link
                to="/presentation-landing"
                className="inline-block w-full text-center px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded-lg transition transform hover:scale-105 shadow-lg"
              >
                Lancer la Présentation Interactive →
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
