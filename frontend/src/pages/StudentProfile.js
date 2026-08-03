import React, { useState, useEffect } from 'react';
import { User, FileText, Download, Edit2, LogOut, TrendingUp, CheckCircle, XCircle, Clock } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import studentService from '../services/studentService';
import { exportChartAsPDF } from '../utils/exportUtils';

const StudentProfile = ({ onLogout, user }) => {
  const [studentData, setStudentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState(null);
  const [saveLoading, setSaveLoading] = useState(false);
  const [predictions, setPredictions] = useState({
    capaciteFinanciere: 0,
    capaciteFinanciereNiveau: 'Chargement...',
    typeBourse: 'Chargement...',
    pourcentageBourse: 0,
    montantBourse: 0,
    messageBourse: '',
    probabiliteInscription: 0,
    niveauInscription: 'Chargement...',
    decisionGlobale: 'Chargement...',
    justification: ''
  });

  useEffect(() => {
    loadStudentData();
  }, []);

  useEffect(() => {
    if (studentData?.idEtudiant) {
      fetchPredictions(studentData.idEtudiant);
    }
  }, [studentData?.idEtudiant]);

  const fetchPredictions = async (studentId) => {
    if (!studentId) {
      console.error('Student ID is undefined');
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/predictions/etudiant/${studentId}/recommandations`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      if (response.ok) {
        const data = await response.json();
        setPredictions({
          capaciteFinanciere: data.capaciteFinanciere?.score || 0,
          capaciteFinanciereNiveau: data.capaciteFinanciere?.niveau || 'N/A',
          typeBourse: data.recommandationBourse?.type || 'N/A',
          pourcentageBourse: calculatePercentage(data.recommandationBourse?.type || 'Aucune'),
          montantBourse: data.recommandationBourse?.montant || 0,
          messageBourse: data.recommandationBourse?.message || '',
          probabiliteInscription: data.probabiliteInscription?.confiance || 0,
          niveauInscription: data.probabiliteInscription?.niveau || 'N/A',
          decisionGlobale: data.recommandationGlobale?.decision || 'N/A',
          justification: data.recommandationGlobale?.justification || ''
        });
      } else if (response.status === 404) {
        console.error('Student not found or predictions not available');
      }
    } catch (error) {
      console.error('Erreur lors du chargement des prédictions:', error);
    }
  };

  const calculatePercentage = (typeBourse) => {
    const percentages = {
      'Aucune': 0,
      'Partielle': 25,
      'Complète': 100
    };
    return percentages[typeBourse] || 0;
  };

  const loadStudentData = () => {
    try {
      const storedData = localStorage.getItem('studentData');
      if (storedData) {
        const data = JSON.parse(storedData);
        setStudentData(data);
        setEditData(data);
        
        // Fetch fresh data from backend to ensure we have complete information
        if (data.idEtudiant) {
          fetch(`http://localhost:8000/api/v1/etudiants/${data.idEtudiant}`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          })
            .then(response => response.json())
            .then(freshData => {
              // Remove MongoDB _id field if present
              if (freshData._id) {
                delete freshData._id;
              }
              setStudentData(freshData);
              setEditData(freshData);
              localStorage.setItem('studentData', JSON.stringify(freshData));
            })
            .catch(error => console.error('Erreur lors de la récupération des données fraîches:', error));
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async () => {
    if (isEditing) {
      // Sauvegarder les modifications
      setSaveLoading(true);
      try {
        const updated = await studentService.updateStudent(studentData.idEtudiant, editData);
        setStudentData(updated);
        localStorage.setItem('studentData', JSON.stringify(updated));
        setIsEditing(false);
      } catch (error) {
        console.error('Erreur lors de la mise à jour:', error);
        alert('Erreur lors de la sauvegarde des modifications');
      } finally {
        setSaveLoading(false);
      }
    } else {
      setIsEditing(true);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const downloadCertificate = () => {
    if (studentData?.statut !== 'Approuvé') {
      alert('Vous pouvez télécharger le certificat uniquement après approbation');
      return;
    }
    
    // Générer un PDF simple avec les données de l'étudiant
    const element = document.getElementById('profile-content');
    if (element) {
      exportChartAsPDF(element, `certificat_${studentData.prenom}_${studentData.nom}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar isAuthenticated={true} userRole="student" onLogout={onLogout} />
        <div className="flex-1 flex items-center justify-center">
          <p className="text-gray-600">Chargement des données...</p>
        </div>
        <Footer />
      </div>
    );
  }

  if (!studentData) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <Navbar isAuthenticated={true} userRole="student" onLogout={onLogout} />
        <div className="flex-1 flex items-center justify-center">
          <p className="text-red-600">Erreur: Données étudiant non trouvées</p>
        </div>
        <Footer />
      </div>
    );
  }

  const isApproved = studentData.statut === 'Approuvé';
  const isPending = studentData.statut === 'En attente';
  const isRejected = studentData.statut === 'Rejeté';

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar isAuthenticated={true} userRole="student" onLogout={onLogout} />

      <div className="flex-1">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Profil Étudiant</h1>
            <p className="text-gray-600">Gérez votre candidature et consultez les prédictions de bourses</p>
          </div>

          {/* Status Alert */}
          {isPending && (
            <div className="mb-6 p-4 bg-yellow-50 border-l-4 border-yellow-500 flex items-start gap-4 rounded">
              <Clock className="text-yellow-600 flex-shrink-0 mt-0.5" size={24} />
              <div>
                <h3 className="font-bold text-yellow-800">Demande en attente d'approbation</h3>
                <p className="text-yellow-700 text-sm mt-1">
                  Votre candidature est actuellement en cours de traitement par l'administration. 
                  Veuillez patienter. Une notification vous sera envoyée dès qu'une décision sera prise.
                </p>
              </div>
            </div>
          )}

          {isApproved && (
            <div className="mb-6 p-4 bg-green-50 border-l-4 border-green-600 flex items-start gap-4 rounded">
              <CheckCircle className="text-green-600 flex-shrink-0 mt-0.5" size={24} />
              <div>
                <h3 className="font-bold text-green-800">Candidature approuvée!</h3>
                <p className="text-green-700 text-sm mt-1">
                  Félicitations! Votre candidature a été approuvée. Vous pouvez maintenant télécharger votre certificat d'admission.
                </p>
              </div>
            </div>
          )}

          {isRejected && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-600 flex items-start gap-4 rounded">
              <XCircle className="text-red-600 flex-shrink-0 mt-0.5" size={24} />
              <div>
                <h3 className="font-bold text-red-800">Candidature rejetée</h3>
                <p className="text-red-700 text-sm mt-1">
                  Nous regrettons de vous informer que votre candidature a été rejetée. 
                  Pour plus de détails, veuillez contacter l'administration.
                </p>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2" id="profile-content">
              {/* Personal Information */}
              <div className="card mb-8">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-gray-900 flex items-center space-x-3">
                    <User className="text-red-600" size={28} />
                    <span>Informations Personnelles</span>
                  </h2>
                  <button
                    onClick={handleEdit}
                    disabled={saveLoading}
                    className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Edit2 size={18} />
                    <span>{isEditing ? (saveLoading ? 'Enregistrement...' : 'Enregistrer') : 'Modifier'}</span>
                  </button>
                </div>

                {isEditing ? (
                  <div className="space-y-6">

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="form-label">Prénom</label>
                        <input
                          type="text"
                          name="prenom"
                          value={editData.prenom}
                          onChange={handleInputChange}
                          className="form-input"
                        />
                      </div>
                      <div>
                        <label className="form-label">Nom de Famille</label>
                        <input
                          type="text"
                          name="nom"
                          value={editData.nom}
                          onChange={handleInputChange}
                          className="form-input"
                        />
                      </div>
                      <div>
                        <label className="form-label">Email</label>
                        <input
                          type="email"
                          name="email"
                          value={editData.email}
                          onChange={handleInputChange}
                          className="form-input"
                        />
                      </div>
                      <div>
                        <label className="form-label">Téléphone</label>
                        <input
                          type="tel"
                          name="phone"
                          value={editData.phone}
                          onChange={handleInputChange}
                          className="form-input"
                        />
                      </div>
                      <div className="md:col-span-2">
                        <label className="form-label">Adresse</label>
                        <input
                          type="text"
                          name="address"
                          value={editData.address}
                          onChange={handleInputChange}
                          className="form-input"
                        />
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-gray-600 text-sm">Prénom</p>
                        <p className="font-semibold text-gray-900">{studentData.prenom}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 text-sm">Nom de Famille</p>
                        <p className="font-semibold text-gray-900">{studentData.nom}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 text-sm">Email</p>
                        <p className="font-semibold text-gray-900">{studentData.email}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 text-sm">Téléphone</p>
                        <p className="font-semibold text-gray-900">{studentData.phone}</p>
                      </div>
                      <div className="md:col-span-2">
                        <p className="text-gray-600 text-sm">Adresse</p>
                        <p className="font-semibold text-gray-900">{studentData.address}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Academic & Financial Information */}
              <div className="card">
                <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-3">
                  <FileText className="text-red-600" size={28} />
                  <span>Données Académiques et Financières</span>
                </h2>

                {/* Education Level Display */}
                {studentData.niveau_etude && (
                  <div className="mb-6 p-4 bg-purple-50 border-l-4 border-purple-600 rounded">
                    <p className="text-sm text-gray-600 font-semibold">Niveau d'Études</p>
                    <p className="text-lg font-bold text-purple-700">{studentData.niveau_etude}</p>
                  </div>
                )}

                {/* Baccalauréat Information */}
                {studentData.donnees_baccalaureat && (
                  <div className="mb-6 p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
                    <h3 className="text-lg font-bold text-blue-900 mb-4">Données du Baccalauréat</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-white p-4 rounded-lg">
                        <p className="text-gray-600 text-sm font-semibold mb-1">Notes Régionales</p>
                        <p className="text-3xl font-bold text-blue-600">{studentData.donnees_baccalaureat.notes_regionales}</p>
                        <p className="text-xs text-gray-600 mt-1">Sur 20</p>
                      </div>
                      <div className="bg-white p-4 rounded-lg">
                        <p className="text-gray-600 text-sm font-semibold mb-1">Note Générale</p>
                        <p className="text-3xl font-bold text-blue-600">{studentData.donnees_baccalaureat.note_generale}</p>
                        <p className="text-xs text-gray-600 mt-1">Sur 20</p>
                      </div>
                      <div className="bg-white p-4 rounded-lg">
                        <p className="text-gray-600 text-sm font-semibold mb-1">Option</p>
                        <p className="text-2xl font-bold text-blue-600">{studentData.donnees_baccalaureat.option}</p>
                        <p className="text-xs text-gray-600 mt-1">Filière</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Diplôme Information (for Bac+2 and above) */}
                {studentData.donnees_diplome && (
                  <div className="mb-6 p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
                    <h3 className="text-lg font-bold text-green-900 mb-4">Données du Diplôme</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-white p-4 rounded-lg">
                        <p className="text-gray-600 text-sm font-semibold mb-1">Notes du Diplôme</p>
                        <p className="text-3xl font-bold text-green-600">{studentData.donnees_diplome.notes_diplome}</p>
                        <p className="text-xs text-gray-600 mt-1">Sur 20</p>
                      </div>
                      <div className="bg-white p-4 rounded-lg">
                        <p className="text-gray-600 text-sm font-semibold mb-1">Spécialité</p>
                        <p className="text-2xl font-bold text-green-600">{studentData.donnees_diplome.option}</p>
                        <p className="text-xs text-gray-600 mt-1">Domaine</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Financial & Context Information */}
                <div className="card">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Informations Financières et Contextuelles</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-gray-600 text-sm">Revenu Familial Annuel</p>
                      <p className="font-semibold text-gray-900 text-lg">${studentData.donnees_financieres?.revenu?.toLocaleString() || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Nombre de Dépendants</p>
                      <p className="font-semibold text-gray-900 text-lg">{studentData.donnees_financieres?.dependants || 'N/A'} membres</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Distance de l'Université</p>
                      <p className="font-semibold text-gray-900 text-lg">{studentData.donnees_contextuelles?.distance || 'N/A'} km</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Année d'Inscription</p>
                      <p className="font-semibold text-gray-900 text-lg">{studentData.annee || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-gray-600 text-sm">Type de Parrainage Demandé</p>
                      <p className="font-semibold text-gray-900 text-lg">{studentData.type_sponsorship || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar - Predictions */}
            <div>
              {/* Financial Capacity Score */}
              <div className="card mb-6 bg-gradient-to-br from-red-600 to-red-800 text-white">
                <h3 className="text-lg font-bold mb-4 flex items-center space-x-2">
                  <TrendingUp size={24} />
                  <span>Capacité Financière</span>
                </h3>
                <div className="text-center">
                  <div className="text-5xl font-bold mb-2">{predictions.capaciteFinanciere}</div>
                  <div className="w-full bg-red-400 rounded-full h-2 mb-4">
                    <div
                      className="bg-white h-2 rounded-full"
                      style={{ width: `${predictions.capaciteFinanciere}%` }}
                    ></div>
                  </div>
                  <p className="text-red-100">Votre score de capacité financière</p>
                </div>
              </div>

              {/* Scholarship Recommendation */}
              <div className="card mb-6 bg-gradient-to-br from-red-600 to-red-800 text-white">
                <h3 className="font-bold mb-4">Attribution de Bourse</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-red-100 text-sm mb-1">Type</p>
                    <p className="text-xl font-bold">{predictions.typeBourse}</p>
                  </div>
                  <div>
                    <p className="text-red-100 text-sm mb-1">Couverture</p>
                    <p className="text-3xl font-bold">{predictions.pourcentageBourse}%</p>
                  </div>
                  <div className="bg-red-500 bg-opacity-30 rounded-lg p-4 mt-4">
                    <p className="text-sm text-red-100">
                      Votre candidature est compétitive pour un parrainage complet. Vérification des documents requise.
                    </p>
                  </div>
                </div>
              </div>

              {/* Enrollment Probability */}
              <div className="card mb-6 bg-gradient-to-br from-red-600 to-red-800 text-white">
                <h3 className="font-bold mb-4">Probabilité d'Inscription</h3>
                <div className="text-center">
                  <div className="text-4xl font-bold mb-2">{predictions.probabiliteInscription}%</div>
                  <p className="text-red-100">Probabilité prédite d'inscription</p>
                </div>
              </div>

              {/* Actions */}
              <div className="space-y-3">
                <button
                  onClick={downloadCertificate}
                  disabled={!isApproved}
                  title={!isApproved ? 'Disponible après approbation de votre candidature' : 'Télécharger votre certificat d\'admission'}
                  className={`w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-semibold transition ${
                    isApproved
                      ? 'bg-red-600 hover:bg-red-700 text-white cursor-pointer'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-60'
                  }`}
                >
                  <Download size={20} />
                  <span>{isApproved ? 'Télécharger le Certificat' : 'En attente d\'approbation'}</span>
                </button>
                <button
                  onClick={onLogout}
                  className="w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-semibold bg-gray-600 hover:bg-gray-700 text-white transition"
                >
                  <LogOut size={20} />
                  <span>Déconnexion</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default StudentProfile;
