import React from 'react';
import { AlertCircle, Lock, FileText, Eye, Shield, Server } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Confidentiality = ({ isAuthenticated, userRole, onLogout }) => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-blue-50">
      <Navbar isAuthenticated={isAuthenticated} userRole={userRole} onLogout={onLogout} />

      {/* Hero - Moroccan Style */}
      <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 text-white py-16 overflow-hidden">
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="flex items-start space-x-4 mb-4">
            <Shield size={48} className="flex-shrink-0 text-amber-300" />
            <div>
              <h1 className="text-5xl font-bold mb-4">🔒 Confidentialité et Sécurité des Données</h1>
              <div className="h-1 w-16 bg-gradient-to-r from-amber-400 to-red-400 mb-4 rounded"></div>
              <p className="text-xl text-blue-100">Comment nous protégeons vos informations personnelles et académiques</p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16">
        <div className="container mx-auto px-4 max-w-4xl">
          
          {/* Warning Box - Moroccan Style */}
          <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-l-4 border-amber-600 rounded-xl p-8 mb-12 shadow-lg">
            <h2 className="text-2xl font-bold text-amber-900 mb-6 flex items-center space-x-3">
              <AlertCircle className="text-amber-600" size={32} />
              <span>⚠️ Important: Intégrité et Vérification des Informations</span>
            </h2>
            <div className="text-amber-900 space-y-4">
              <p className="font-semibold text-lg">En soumettant une candidature, vous reconnaissez et acceptez que:</p>
              <ul className="space-y-3 ml-6">
                <li className="flex items-start space-x-3">
                  <span className="text-amber-600 font-bold mt-0.5">✓</span>
                  <span>Toutes les informations fournies doivent être <strong>complètement exactes et véridiques</strong></span>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-amber-600 font-bold mt-0.5">✓</span>
                  <span>Toute information fausse, trompeuse ou fabriquée entraînera une <strong>disqualification immédiate</strong></span>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-amber-600 font-bold mt-0.5">✓</span>
                  <span>La fourniture de faux documents peut entraîner des <strong>poursuites judiciaires</strong></span>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-amber-600 font-bold mt-0.5">✓</span>
                  <span>L'institution se réserve le droit de mener une <strong>vérification complète des antécédents</strong></span>
                </li>
                <li className="flex items-start space-x-3">
                  <span className="text-amber-600 font-bold mt-0.5">✓</span>
                  <span>Les candidats acceptent que la vérification puisse inclure le contact d'institutions éducatives et d'employeurs</span>
                </li>
              </ul>
              <div className="mt-6 p-4 bg-white rounded-lg border border-amber-200">
                <p className="font-semibold text-amber-900 mb-3">📞 Après acceptation, l'administration vous contactera pour:</p>
                <ul className="space-y-2 ml-6">
                  <li className="flex items-start space-x-2">
                    <span>•</span>
                    <span>Programmer une réunion en personne ou un entretien</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span>•</span>
                    <span>Demander les documents originaux (diplômes, relevés, cartes d'identité)</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span>•</span>
                    <span>Vérifier votre adresse et informations de contact</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span>•</span>
                    <span>Évaluation finale de l'admissibilité</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span>•</span>
                    <span>Discuter des termes et conditions de la bourse</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Data Protection - Moroccan Cards */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-blue-900 mb-6 flex items-center space-x-3">
              <Lock className="text-blue-600" size={32} />
              <span>🔐 Protection et Sécurité des Données</span>
            </h2>
            <div className="h-1 w-16 bg-gradient-to-r from-amber-500 to-red-500 mb-8 rounded"></div>
            
            <div className="space-y-6">
              {/* Card 1 */}
              <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden border-l-4 border-blue-600 p-6">
                <h3 className="text-xl font-bold text-blue-900 mb-3 flex items-center space-x-2">
                  <span>📋</span>
                  <span>1. Informations que nous collectons</span>
                </h3>
                <p className="text-gray-700 mb-4">Nous collectons uniquement les informations essentielles:</p>
                <ul className="space-y-2 ml-6 text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600">•</span>
                    <span><strong>Identification:</strong> nom, date de naissance, CNI/passeport</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600">•</span>
                    <span><strong>Contact:</strong> email, téléphone, adresse</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600">•</span>
                    <span><strong>Académique:</strong> notes, diplômes, relevés</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-600">•</span>
                    <span><strong>Financier:</strong> revenus, déclarations fiscales</span>
                  </li>
                </ul>
              </div>

              {/* Card 2 */}
              <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden border-l-4 border-amber-600 p-6">
                <h3 className="text-xl font-bold text-blue-900 mb-3 flex items-center space-x-2">
                  <span>🔄</span>
                  <span>2. Utilisation de Vos Informations</span>
                </h3>
                <p className="text-gray-700 mb-4">Vos données sont utilisées exclusivement pour:</p>
                <ul className="space-y-2 ml-6 text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-600">•</span>
                    <span><strong>Traitement:</strong> Examen de votre admissibilité</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-600">•</span>
                    <span><strong>IA/ML:</strong> Modèles pour évaluer potentiel et besoin</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-600">•</span>
                    <span><strong>Vérification:</strong> Confirmation des informations</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-amber-600">•</span>
                    <span><strong>Communication:</strong> Notification des décisions</span>
                  </li>
                </ul>
              </div>

              {/* Card 3 */}
              <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden border-l-4 border-green-600 p-6">
                <h3 className="text-xl font-bold text-blue-900 mb-3 flex items-center space-x-2">
                  <span>🛡️</span>
                  <span>3. Mesures de Sécurité</span>
                </h3>
                <p className="text-gray-700 mb-4">Nous utilisons des standards de sécurité industrie:</p>
                <ul className="space-y-2 ml-6 text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600">•</span>
                    <span><strong>Chiffrement:</strong> HTTPS pour toutes les transmissions</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600">•</span>
                    <span><strong>Accès:</strong> Contrôle d'accès basé sur les rôles</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600">•</span>
                    <span><strong>Base de données:</strong> Authentication sécurisée</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600">•</span>
                    <span><strong>Audits:</strong> Tests réguliers de sécurité</span>
                  </li>
                </ul>
              </div>

              {/* Card 4 */}
              <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden border-l-4 border-red-600 p-6">
                <h3 className="text-xl font-bold text-blue-900 mb-3 flex items-center space-x-2">
                  <span>📅</span>
                  <span>4. Rétention des Données</span>
                </h3>
                <p className="text-gray-700 mb-4">Vos données sont conservées selon la période:</p>
                <ul className="space-y-2 ml-6 text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-red-600 font-bold">→</span>
                    <span><strong>7 ans:</strong> Après graduation (boursiers)</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-red-600 font-bold">→</span>
                    <span><strong>3 ans:</strong> Après candidature (non-retenus)</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-red-600 font-bold">→</span>
                    <span><strong>Indéfini:</strong> Données anonymisées pour recherche</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Compliance - Moroccan Style */}
          <div className="bg-gradient-to-br from-blue-50 to-amber-50 rounded-xl p-8 border border-blue-200">
            <h2 className="text-3xl font-bold text-blue-900 mb-6 flex items-center space-x-3">
              <Shield className="text-blue-600" size={32} />
              <span>✅ Conformité aux Normes Internationales</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start space-x-4">
                <div className="text-2xl">🇪🇺</div>
                <div>
                  <h4 className="font-bold text-blue-900 mb-2">RGPD</h4>
                  <p className="text-sm text-gray-700">Protection des données pour les utilisateurs de l'Union Européenne</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="text-2xl">🇺🇸</div>
                <div>
                  <h4 className="font-bold text-blue-900 mb-2">CCPA</h4>
                  <p className="text-sm text-gray-700">Loi californienne sur la vie privée des consommateurs</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="text-2xl">🇲🇦</div>
                <div>
                  <h4 className="font-bold text-blue-900 mb-2">Lois Marocaines</h4>
                  <p className="text-sm text-gray-700">Conformité avec la législation marocaine sur la protection des données</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="text-2xl">🎓</div>
                <div>
                  <h4 className="font-bold text-blue-900 mb-2">FERPA</h4>
                  <p className="text-sm text-gray-700">Protection des dossiers scolaires des étudiants</p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact & Rights */}
          <div className="mt-12 bg-white rounded-xl shadow-md overflow-hidden border-l-4 border-blue-600 p-8">
            <h2 className="text-3xl font-bold text-blue-900 mb-6 flex items-center space-x-3">
              <Eye className="text-blue-600" size={32} />
              <span>👤 Vos Droits et Contact</span>
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-bold text-blue-900 mb-4">Vous avez le droit de:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-center space-x-2">
                    <span className="text-blue-600 font-bold">✓</span>
                    <span><strong>Accès:</strong> Demander vos données</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <span className="text-blue-600 font-bold">✓</span>
                    <span><strong>Correction:</strong> Rectifier les erreurs</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <span className="text-blue-600 font-bold">✓</span>
                    <span><strong>Suppression:</strong> Effacer vos données</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <span className="text-blue-600 font-bold">✓</span>
                    <span><strong>Opposition:</strong> Refuser le traitement</span>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="font-bold text-blue-900 mb-4">📧 Nous Contacter:</h3>
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200 space-y-2">
                  <p className="text-sm text-gray-700">
                    <strong>DPO (Responsable Protection Données):</strong>
                    <br/><span className="text-blue-600">privacy@smartenrollment.edu</span>
                  </p>
                  <p className="text-sm text-gray-700">
                    <strong>Support Administratif:</strong>
                    <br/><span className="text-blue-600">admin@smartenrollment.edu</span>
                  </p>
                  <p className="text-sm text-gray-700">
                    <strong>Délai de Réponse:</strong>
                    <br/>Maximum 30 jours ouvrables
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Updated Note */}
          <div className="mt-12 text-center text-sm text-gray-600 p-4 bg-gray-100 rounded-lg">
            <p>Dernière mise à jour: Janvier 2024</p>
            <p>Cette politique peut être modifiée. Nous vous notifierons des changements importants par email.</p>
          </div>

          {/* Contact Section */}
          <div className="bg-red-50 rounded-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-3">
              <Eye className="text-red-600" size={32} />
              <span>Préoccupations concernant la Protection des Données et la Vie Privée</span>
            </h2>
            <p className="text-gray-600 mb-4">
              Si vous avez des préoccupations concernant vos données ou la manière dont elles sont utilisées, veuillez nous contacter:
            </p>
            <div className="bg-white rounded-lg p-4 space-y-2">
              <p><strong>Responsable de la Protection des Données:</strong> dpo@smartenrollment.edu</p>
              <p><strong>Équipe de Confidentialité:</strong> privacy@smartenrollment.edu</p>
              <p><strong>Adresse du Bureau:</strong> Bâtiment Smart Enrollment, 123 Avenue Université</p>
              <p><strong>Téléphone:</strong> +1 (555) 123-4567</p>
            </div>
          </div>

          {/* Last Updated */}
          <div className="mt-12 text-center text-gray-600">
            <p>Dernière mise à jour: Janvier 2024</p>
            <p>Cette politique est sujette à changement. Nous notifierons les utilisateurs des changements importants.</p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Confidentiality;
